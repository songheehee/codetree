import sys
sys.stdin = open("input.txt", "r")

# 0 = 빈공간, 1 = 사무실, 2 = 에어컨 왼, 3 = 에어컨 위, 4 = 에 오, 5 = 에 아
# 1. 에어컨 바람 퍼짐. 5부터
# 2. 공기 섞임. 시원함이 높은 곳에서 낮은 곳으로 시원함 차이 // 4. 동시에. 벽은 통과 안함
# 3. 외벽 시원함 -1. 0 은 감소하지 않음
# 모든 사무실 k 이상 되는 최소 시간. 100 분 넘으면 -1
# 벽 에어컨 바로 옆/앞에 없음. 벽 != 외벽
# 에어컨 바로 앞 격자 나가지 않음
# 사무실, 에어컨 최소 하나 이상

from collections import deque

def mix():
    new_cold = [row[:] for row in cold] # 동시에 전파, 벽 확인

    for i in range(N):
        for j in range(N):
            if cold[i][j]:
                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N and cold[i][j] > cold[nr][nc]): # 나보다 작은 애만
                        continue

                    if (i, j) in wall and d in wall[(i, j)]: # 벽 있으면
                        continue

                    diff = (cold[i][j] - cold[nr][nc]) // 4
                    new_cold[nr][nc] += diff
                    new_cold[i][j] -= diff

    return new_cold


def wind(ar, ac, ad):
    visited = [[0] * N for _ in range(N)]
    q = deque()

    # 바로 앞 무조건 갈 수 있음
    nr = ar + dr[ad]
    nc = ac + dc[ad]
    q.append((nr, nc))
    visited[nr][nc] = 5
    cold[nr][nc] += 5

    while q:
        for _ in range(len(q)):
            cr, cc = q.popleft()

            for d in [(ad - 1 + 4) % 4, None, (ad + 1) % 4]:  # ad 기준 양옆 -> ad
                sr, sc = cr, cc

                if d is not None:
                    nr = sr + dr[d]
                    nc = sc + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if visited[nr][nc] or ((sr, sc) in wall and d in wall[(sr, sc)]): # 벽 있으면 전파 x
                        continue

                    sr, sc = nr, nc

                # 여기까지 왔으면 직진
                nr = sr + dr[ad]
                nc = sc + dc[ad]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if visited[nr][nc] or ((sr, sc) in wall and ad in wall[(sr, sc)]): # 벽 있으면 전파 x
                    continue

                q.append((nr, nc))
                visited[nr][nc] = visited[cr][cc] - 1
                cold[nr][nc] += visited[nr][nc]

        if visited[cr][cc] == 1:
            break


dr = [0, -1, 0, 1] # 왼위오아
dc = [-1, 0, 1, 0]

# 왼 = 위->왼, 왼, 아->왼
# 위 = 왼->위, 위, 오->위
# 오 = 위->오, 오, 아->오
# 아 = 왼->아, 아, 오->아

N, W, K = map(int, input().split()) # 격자, 벽 개수, 사무실 시원함 정도
matrix = [list(map(int, input().split())) for _ in range(N)] # 사무실, 에어컨
wall = dict() # 해당 위치 위/왼 벽
air = [] # 에어컨 위치, 방향
office = [] # 사무실 위치. K 이상인지 확인 위함
cold = [[0] * N for _ in range(N)] # 시원함

for i in range(N):
    for j in range(N):
        if matrix[i][j] == 1:
            office.append((i, j))
        elif matrix[i][j]: # 에어컨
            air.append((i, j, matrix[i][j]-2))

for _ in range(W): # 벽 설치
    x, y, s = map(lambda x: int(x)-1, input().split()) # -1=위, 0=왼
    s = -s

    if (x, y) in wall:
        wall[(x, y)].append(s)
    else:
        wall[(x, y)] = [s]

    if s == 0: # 해당 위치 왼쪽에는 오른쪽 벽임
        y -= 1
    else:
        x -= 1 # 위쪽은 아래

    if 0 <= x < N and 0 <= y < N:
        s += 2

        if (x, y) in wall:
            wall[(x, y)].append(s)
        else:
            wall[(x, y)] = [s]

ans = -1

for time in range(1, 101):
    # 1. 에어컨 바람 퍼짐
    for ar, ac, ad in air:
        wind(ar, ac, ad)

    # 2. 공기 섞임. 높은 곳 -> 낮은 곳
    cold = mix()

    # 3. 외벽 -1
    for i in range(N):
        if i in (0, N-1):
            jrange = range(N)
        else:
            jrange = (0, N-1)

        for j in jrange:
            if cold[i][j]:
                cold[i][j] -= 1

    # 마지막에 체크하는 거 맞나?
    for r, c in office:
        if cold[r][c] < K:
            break
    else:  # 다 K 넘음
        ans = time
        break

print(ans) # 사무실 시원해지는 시간. 100 넘으면 -1