# 모든 위치에 포탑 존재
# 공격력 0 이하 되면 부서짐. 최초 0도 있을 수 있음
# 부서지지 않은 포탑이 1개 되면 끝

# 1. 공격자 선정 - 0보다 큰 가장 약한 포탑. N+M만큼 공격력 증가
# 1-1. 공격력 낮은 거 여러개면 가장 최근에 공격한 포탑. 모든 포탑은 0초에 공격한 경험 있음
# 1-2. 그것도 여러개면 행+열 합 가장 큰 포탑
# 1-3. 그것도 여러개면 열 값이 가장 큰 애
# 2. 공격자 공격 - 자신 제외 가장 강한 포탑 공격
# 2-1. 공격한지 가장 오래된 포탑
# 2-2. 행+열 가장 작은 포탑
# 2-3. 열 값 가장 작은 애
# 2-4. 레이저 공격 - 0 지날 수 없음. 가장 자리면 이어져서 다른 쪽으로. 최단 경로로 공격. 우하좌상 우선
#       경로에 있는 애들도 공격 받음. 절반 만큼만
# 2-5. 포탄 공격 - 최단 경로 없으면. 주위 8방 애들도 피해 입는데 절반만. 공격자 제외
# 3. 포탑 부서짐
# 4. 포탑 정비 - 안 부서지고 공격과 무관했던 포탑은 +1. 공격자도 아니고 피해 입지도 않은 애들

from collections import deque

def find():
    min_val, minr, minc = 5001, -1, -1 # 제일 약한 애
    max_val, maxr, maxc = 0, -1, -1 # 제일 강한 애

    for i in range(N):
        for j in range(M):
            val = matrix[i][j]
            if val == 0:
                continue

            if (-val, last[i][j], i+j, j) > (-min_val, last[minr][minc], minr+minc, minc):
                min_val = val
                minr, minc = i, j
                
            if (-val, last[i][j], i+j, j) < (-max_val, last[maxr][maxc], maxr+maxc, maxc):
                max_val = val
                maxr, maxc = i, j

    matrix[minr][minc] += N+M
    last[minr][minc] = time

    return minr, minc, maxr, maxc

def razor():
    visited = [[0] * M for _ in range(N)]
    q = deque([(ar, ac, [])])
    visited[ar][ac] = 1

    while q:
        cr, cc, points = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < M):
                nr = (nr+N) % N
                nc = (nc+M) % M

            if matrix[nr][nc] == 0 or visited[nr][nc]:
                continue

            if nr == sr and nc == sc:
                return points

            visited[nr][nc] = 1
            q.append((nr, nc, points+[(nr, nc)]))

    return bomb() # 못 감

def bomb():
    points = []

    for d in range(8):
        nr = sr + pdr[d]
        nc = sc + pdc[d]

        if not (0 <= nr < N and 0 <= nc < M):
            nr = (nr + N) % N
            nc = (nc + M) % M

        if matrix[nr][nc] == 0 or (nr == ar and nc == ac): # 자기 자신 제외
            continue

        points.append((nr, nc))

    return points


dr = [0, 1, 0, -1] # 우하좌상
dc = [1, 0, -1, 0]

pdr = [-1, -1, -1, 0, 0, 1, 1, 1]
pdc = [-1, 0, 1, -1, 1, -1, 0, 1]

N, M, K = map(int, input().split()) # 10, 10, 1000
matrix = [list(map(int, input().split())) for _ in range(N)]
last = [[0] * M for _ in range(N)] # 마지막으로 언제 공격했는지. 최근이 더 큼

for time in range(1, K+1):
    if sum(row.count(0) for row in matrix) == (N*M) - 1: # 남은 포탑 1개
        break

    # 1. 공격자 선정
    ar, ac, sr, sc = find()

    # 2. 레이저 -> 안되면 포탄
    points = razor()

    power = matrix[ar][ac]
    matrix[sr][sc] -= power
    matrix[sr][sc] = max(matrix[sr][sc], 0)

    power //= 2
    for r, c in points: # 반만 공격
        matrix[r][c] -= power
        matrix[r][c] = max(matrix[r][c], 0)

    # 3. 공격 무관한 애들 +1
    for i in range(N):
        for j in range(M):
            if matrix[i][j] == 0:
                continue

            if (i == ar and j == ac) or (i == sr and j == sc) or (i, j) in points:
                continue

            matrix[i][j] += 1

print(max(max(row) for row in matrix)) # 남은 애들 중 가장 강한 포탑의 공격력