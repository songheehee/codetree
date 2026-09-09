# 0 = 빈칸, 1 = 사무실, 2 = 에어컨 (왼), 3 = 에어컨 (위), 4 = 에어컨 (오), 5 = 에어컨 (아래)
# 1. 공기 시원하게 함 but 벽 있으면 ㄴㄴ. 위 45도는 위->오, 아래 45도는 아래->오. 에어컨 있는 곳도 전파 가능
# 2. 시원한 공기들 섞임. 인접한 칸 차이 // 4. 벽 사이에 두고는 일어나지 않음
# 3. 바깥쪽 칸 -1. 0이면 0
# 모든 사무실이 k 이상일 때까지
# 벽 != 외벽, 에어컨 바로 앞 격자 안 나감, 사무실이랑 에어컨 최소 하나씩
# 모든 칸에 대해서 대각선 위, 앞, 대각선 아래
from collections import deque

def blow():
    for (r, c), d in air.items():
        visited = [[0] * N for _ in range(N)]
        q = deque([(r, c)])
        visited[r][c] = 6

        while q:
            nq = deque([])

            for cr, cc in q:
                if visited[cr][cc] == 1:
                    break

                if visited[cr][cc] == 6: # 맨 처음은 앞만 검사
                    nr = cr + dr[d]
                    nc = cc + dc[d]

                    # 에어컨 바로 옆/앞 벽 없음
                    visited[nr][nc] = visited[cr][cc] - 1
                    cold[nr][nc] += visited[nr][nc]
                    nq.append((nr, nc))
                    break

                for lst in wind[d]:
                    # 벽 검사 후 둘 다 이동
                    ccr, ccc = cr, cc
                    for ndr, ndc, nw in lst:
                        nr = ccr + ndr
                        nc = ccc + ndc

                        if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                            break

                        if nw in (0, 1): # 왼위 체크
                            if (ccr, ccc) in wall and nw in wall[(ccr, ccc)]: # 움직인 걸로 체크해야지...
                                break
                        else: # 오아 체크. 다음칸
                            if (nr, nc) in wall and nw-2 in wall[(nr, nc)]:
                                break

                        ccr, ccc = nr, nc

                    else: # 다 갔음
                        visited[nr][nc] = visited[cr][cc] - 1
                        cold[nr][nc] += visited[nr][nc]
                        nq.append((nr, nc))

            q = nq

def mix():
    new_cold = [[0] * N for _ in range(N)] # 동시에

    for i in range(N):
        for j in range(N):
            for d in range(4):
                nr = i + dr[d]
                nc = j + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if d in (0, 1):  # 왼위 체크
                    if (i, j) in wall and d in wall[(i, j)]:
                        continue
                else:  # 오아 체크. 다음칸
                    if (nr, nc) in wall and d-2 in wall[(nr, nc)]:
                        continue

                diff = abs(cold[i][j] - cold[nr][nc]) // 4
                if cold[i][j] > cold[nr][nc]:
                    new_cold[i][j] -= diff
                    new_cold[nr][nc] += diff
                else:
                    new_cold[nr][nc] -= diff
                    new_cold[i][j] += diff

    for i in range(N):
        for j in range(N):
            cold[i][j] += new_cold[i][j] // 2
            cold[i][j] = max(cold[i][j], 0) # 0 보다 작아지지 않음


dr = [0, -1, 0, 1] # 왼위오아
dc = [-1, 0, 1, 0]
# 에어컨 시원함 퍼지는 정도
wind = [[[(-1, 0, 1), (0, -1, 0)], [(0, -1, 0)], [(1, 0, 3), (0, -1, 0)]],
        [[(0, -1, 0), (-1, 0, 1)], [(-1, 0, 1)], [(0, 1, 2), (-1, 0, 1)]],
        [[(-1, 0, 1), (0, 1, 2)], [(0, 1, 2)], [(1, 0, 3), (0, 1, 2)]],
        [[(0, -1, 0), (1, 0, 3)], [(1, 0, 3)], [(0, 1, 2), (1, 0, 3)]]]

N, W, K = map(int, input().split()) # 격자 크기, 벽 개수, 시원함 정도. 20, 400, 1000
matrix = [list(map(int, input().split())) for _ in range(N)]
cold = [[0] * N for _ in range(N)]
wall = dict() # 좌표 : 방향(위/왼). 여러개 가능
air = dict() # 에어컨 위치. 한칸에 하나. 좌표 : 방향
office = [] # 사무실 위치
time = 0

for i in range(N):
    for j in range(N):
        if matrix[i][j] > 1:
            air[(i, j)] = matrix[i][j] - 2
        elif matrix[i][j] == 1:
            office.append((i, j))

for _ in range(W):
    x, y, s = map(lambda x: int(x)-1, input().split())
    s = -s # 좌표에 맞춤. 1 = 위, 0 = 왼

    if (x, y) in wall:
        wall[(x, y)].add(s)
    else:
        wall[(x, y)] = {s}

while True:
    if time > 100: # 100분까지도 도나?
        time = -1
        break

    # k 이상 되면 끝. 시작하자마자 이미 사무실 k일 수 있음
    for r, c in office:
        if cold[r][c] < K:
            break
    else:
        break

    # 1. 공기 시원하게 함
    blow()

    # 2. 공기 섞임
    mix()

    # 3. 외벽 -1
    for i in range(N):
        for j in range(N):
            if (i in (0, N-1) or j in (0, N-1)) and cold[i][j] > 0:
                cold[i][j] -= 1

    time += 1

print(time) # k 이상 되는 최초의 시간. 100분 넘으면 -1