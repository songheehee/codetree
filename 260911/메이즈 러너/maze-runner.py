# 1,1 시작. 미로 칸은 세가지 중 하나
# 1. 빈칸 (이동 가능) = 0
# 2. 벽 (이동 불가, 1~9 내구도, 회전 시 내구도 깎임). 0 되면 빈칸
# 3. 출구 (즉시 탈출) - 한개임 = -1
# 참가자 좌표 != 출구 좌표

# 1초마다 한칸씩 이동. 동시에 이동
# 상하좌우로 벽 없는 곳까지
# 움직인 칸은 현재보다 출구까지의 최단 거리가 가까워야됨
# 움직일 수 있는 칸이 여러개이면 상하로 움직이는 게 우선
# 움직일 수 없으면 이동하지 않음
# 한칸에 여러명 가능
# 여러개 중에 최단거리 아니겠지?
# 플레이어 0 처리 해줄까 pop 할까

# 미로 회전
# 한명 이상의 참가자와 출구 포함한 가장 작은 정사각형
# 여러개면 행작, 열작 우선
# 시계방향으로 90도 회전, 벽 내구도 깎임

from collections import deque

def move():
    count = 0 # 움직인 횟수

    for i in range(P): # 거꾸로. pop 해줘야하니까
        if not player[i]:
            continue

        r, c = player[i]
        min_dist = abs(er-r) + abs(ec-c) # 현재보다 가까워야함

        for d in range(4):
            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N): # 벽이면 안됨
                continue

            dist = abs(er-nr) + abs(ec-nc)
            if matrix[nr][nc] > 0 or dist >= min_dist: # 벽이거나 현재보다 최단 거리 멈
                continue

            # 이동
            if matrix[nr][nc] == -1: # 바로 탈출
                player[i] = 0
                player_grid[r][c].remove(i)
            else:
                player[i] = nr, nc
                player_grid[r][c].remove(i)
                player_grid[nr][nc].append(i)

            count += 1
            break

    return count


def square():
    # 1. 출구에서부터 제일 가까운 참가자 찾기. 꼭 bfs가 더 빠르다고 제일 가까운 건 아님...
    visited = [[0] * N for _ in range(N)]
    q = deque([(er, ec)]) # 출구
    visited[er][ec] = 1
    minr, minc = N, N
    size = N*N # 최대로 주자

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                continue


            if (nr, nc) in player:
                cur_size = max(abs(nr - er), abs(nc - ec))

                if size > cur_size:
                    minr, minc, size = nr, nc, cur_size
                elif size == cur_size: # 좌상단 찾아주기
                    nsr, nsc = find_start(nr, nc, cur_size)
                    csr, csc = find_start(minr, minc, size)

                    if (csr, csc) > (nsr, nsc):
                        minr, minc = nr, nc

            visited[nr][nc] = visited[cr][cc] + 1
            q.append((nr, nc))

    return minr, minc, size


def find_start(r, c, size): # 정사각형 좌상단 찾기
    sr, sc = 0, 0

    if abs(r - er) == size:
        sr = min(r, er)
        sc = max(max(c, ec) - size, 0)

    elif abs(c - ec) == size:
        sr = max(max(r, er) - size, 0)
        sc = min(c, ec)

    return sr, sc

def spin():
    global er, ec
    # 네개의 좌표 찾기. 행작 열작 우선
    # 꼭 꼭지점이 아닐 수 있음
    # 무조건 행/열 하나는 뺐을 때 size여야함
    sr, sc = find_start(minr, minc, size)

    lr, lc = sr + size, sc + size

    sq = [row[sc:lc+1] for row in matrix[sr:lr+1]]
    sq = list(map(list, zip(*sq[::-1])))

    rp, cp = 0, 0 # 정사각형 포인터

    for i in range(sr, lr+1):
        for j in range(sc, lc+1):
            if sq[rp][cp] > 0:
                sq[rp][cp] -= 1

            matrix[i][j] = sq[rp][cp]
            cp += 1

        rp += 1
        cp = 0

    # 플레이어, 출구 좌표 갱신
    for p in range(P):
        if not player[p]:
            continue

        pr, pc = player[p]

        if sr <= pr <= lr and sc <= pc <= lc:
            for i in range(sr, lr+1):
                if (pr, pc) == (i, sc):
                    pr, pc = sr, lc-abs(i-sr)
                    break
                elif (pr, pc) == (i, lc):
                    pr, pc = lr, lc-abs(i-sr)
                    break
            else:
                for j in range(sc+1, lc):
                    if (pr, pc) == (sr, j):
                        pr, pc = lr-abs(lc-j), lc
                        break
                    elif (pr, pc) == (lr, j):
                        pr, pc = lr-abs(lc-j), sc
                        break

            player[p] = pr, pc

    sq = [row[sc:lc + 1] for row in player_grid[sr:lr + 1]]
    sq = list(map(list, zip(*sq[::-1])))

    rp, cp = 0, 0  # 정사각형 포인터

    for i in range(sr, lr + 1):
        for j in range(sc, lc + 1):
            player_grid[i][j] = sq[rp][cp]
            cp += 1

        rp += 1
        cp = 0

    # 출구 그냥 for문 돌리자
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == -1:
                er, ec = i, j
                return


dr = [-1, 1, 0, 0] # 상하좌우
dc = [0, 0, -1, 1]

N, P, K = map(int, input().split()) # 10, 10, 100
matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 빈칸, 1~9 = 벽, -1 = 출구
player = [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(P)] # 좌표 저장
er, ec = map(lambda x: int(x)-1, input().split())
matrix[er][ec] = -1 # 출구 표시
total = 0 # 이동 거리 합. 움직일 때마다
player_grid = [[[] for _ in range(N)] for _ in range(N)]

for i, (r, c) in enumerate(player):
    player_grid[r][c].append(i)

for _ in range(K): # K초 동안 반복. 그 전에 탈출하면 게임 끝
    # 1. 참가자 이동
    total += move()

    if player.count(0) == P:
        break

    # 2. 가장 작은 정사각형 찾기
    minr, minc, size = square()

    # 3. 회전
    spin()

print(total) # 이동 거리 합
print(er+1, ec+1) # 좌표값 하나 더해주기