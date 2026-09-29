# P명의 참가자
# 좌상단 1,1
# 미로 : 빈칸, 벽 (1~9), 출구
# 벽 회전할 때 내구도 1씩 깎임. 0 되면 빈칸
# 출구 도착하면 즉시 탈출

# 1. 참가자 이동
# 참가자 한칸씩 움직임. 동시에
# 최단거리 = 맨해튼
# 상하좌우로, 벽 없는 곳으로만
# 움직인 칸은 출구랑 최단 거리 더 가까워야함
# 움직일 수 있는 칸이 여러개면 상하 우선
# 움직일 수 없으면 움직이지 않음
# 한칸에 여러명 가능

# 2. 미로 회전
# 한명 이상의 참가자와 출구 포함해서 가장 작은 정사각형
# 좌상단 r 좌표 작은거 우선, c 작은거 우선
# 90도 회전. 벽 -1

# K초 전에 참가자 모두 탈출하면 게임 종료
# 모든 참가자의 이동 거리 합, 마지막 출구 좌표
# 처음 참가자 좌표는 무조건 빈칸
# 처음 출구 좌표는 참가자 좌표와 중복되지 않음

def spin():
    global er, ec
    # 가장 작은 정사각형 찾기
    size, r, c = find_square()

    # 회전
    sq = [row[c:c+size] for row in matrix[r:r+size]]
    sq = list(map(list, zip(*sq[::-1])))

    for i in range(r, r+size):
        for j in range(c, c+size):
            matrix[i][j] = sq[i-r][j-c]

    # 출구, 사람 좌표
    er, ec = er-r, ec-c
    er, ec = ec, size-1-er
    er, ec = er+r, ec+c

    for idx in range(P):
        if player[idx] is None:
            continue

        pr, pc = player[idx]
        if r <= pr < r+size and c <= pc < c+size:
            pr, pc = pr - r, pc - c
            pr, pc = pc, size-1-pr
            pr, pc = pr + r, pc + c
            player[idx] = (pr, pc)

    # 내구도 -1
    for i in range(r, r+size):
        for j in range(c, c+size):
            if matrix[i][j]:
                matrix[i][j] -= 1


def find_square():
    # 시작점 잡고 사각형 크기 다 돌기
    for size in range(2, N+1):
        for i in range(N+1-size):
            for j in range(N+1-size):
                if i <= er < i+size and j <= ec < j+size: # 출구 있음
                    for idx in range(P):
                        if player[idx] is None:
                            continue

                        r, c = player[idx]
                        if i <= r < i+size and j <= c < j+size:
                            return size, i, j


def move():
    total = 0

    for idx in range(P):
        if player[idx] is None:
            continue

        r, c = player[idx]
        min_dist = abs(er-r) + abs(ec-c)
        minr, minc = r, c

        for d in range(4):
            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] == 0): # 벽 없는 곳으로
                continue

            dist = abs(er-nr) + abs(ec-nc)
            if dist >= min_dist: # 더 가까워지지 않음
                continue

            min_dist = dist
            minr, minc = nr, nc

        # 이동하지 않음
        if minr == r and minc == c:
            continue

        total += 1

        if minr == er and minc == ec: # 출구 도착
            player[idx] = None
        else:
            player[idx] = (minr, minc)

    return total # 이동한 거리


dr = [-1, 1, 0, 0] # 상하 우선
dc = [0, 0, -1, 1]



N, P, K = map(int, input().split()) # 10, 10, 100
matrix = [list(map(int, input().split())) for _ in range(N)] # 빈칸, 벽
player = [] # 플레이어 위치
total = 0 # 플레이어들 이동한 거리

for _ in range(P):
    r, c = map(lambda x: int(x)-1, input().split())
    player.append((r, c))

er, ec = map(lambda x: int(x)-1, input().split())

for _ in range(K):
    # 1. 참가자 이동
    total += move()

    # 참가자 나갔으면 종료
    if player.count(None) == P:
        break

    # 2. 미로 회전
    spin()

print(total)
print(er+1, ec+1)