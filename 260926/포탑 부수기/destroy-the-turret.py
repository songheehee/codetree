# 포탑 개수는 N*M 개
# 공격력이 0 이하 되면 포탑 부서짐. 최초에 공격력 0인 포탑 존재 가능
# 부서지지 않은 포탑이 1개면 즉시 중지
# 최초에 부서지지 않은 포탑은 최소 2개 이상임

# 1. 공격자 선정
# 부서지지 않은 포탑 중 가장 약한 포탑. N+M 만큼 공격력 증가
# - 공격력 가장 낮은 포탑
# - 여러개면 가장 최근 공격한 포탑
# - 여러개면 행+열 합이 가장 큰 포탑
# - 여러개면 열 값이 가장 큰 포탑

# 2. 공격자 공격
# 자신을 제외한 가장 강한 포탑 공격
# - 공격력 가장 높은 포탑
# - 여러개면 공격한지 가장 오래된 포탑
# - 여러개면 행+열 가장 작은 포탑
# - 여러개면 열 가장 작은 포탑

# 3-1. 레이저 공격
# 상하좌우. 부서진 포탑이 있는 곳은 못감
# 가장자리 -> 반대편으로 나옴
# 최단 경로로 공격. 최단 경로 없으면 -> 포탑
# 우하좌상 우선순위
# 공격 대상은 공격자의 공격력 만큼의 피해
# 경로에 있는 포탑은 공격력 절반 만큼

# 3-2. 포탄 공격 (레이저 불가)
# 공격 대상 공격력 만큼의 피해
# 주위 8방 공격력 절반 만큼 피해
# 공격자는 영향 받지 않음
# 가장자리 -> 반대편도 받음

# 4. 포탑 정비
# 안 부서진 애들 중 공격과 무관한 포탑 공격력 +1
# 공격자도 아니고, 공격에 피해입지도 않은 애들

from collections import deque

def bomb(): # 포탄 공격
    path = []

    for d in range(8):
        nr = sr + dr[d]
        nc = sc + dc[d]

        if not (0 <= nr < N and 0 <= nc < M):
            nr = (nr + N) % N
            nc = (nc + M) % M

        if not matrix[nr][nc] or (nr == wr and nc == wc): # 부서진 포탑, 공격자 제외
            continue

        path.append((nr, nc))

    return path


def laser():
    visited = [[0] * M for _ in range(N)]
    q = deque([(wr, wc, [])])
    visited[wr][wc] = 1

    while q:
        cr, cc, path = q.popleft()

        for d in [4,6,3,1]: # 우하좌상
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < M): # 반대쪽으로 나오기
                nr = (nr+N) % N
                nc = (nc+M) % M

            if not matrix[nr][nc] or visited[nr][nc]: # 부서진 포탑
                continue

            if nr == sr and nc == sc: # 공격 위치 도착
                return path

            q.append((nr, nc, path+[(nr, nc)]))
            visited[nr][nc] = visited[cr][cc] + 1

    return bomb() # 불가능하면 포탄 공격


def find(): # 약한 포탑, 강한 포탑
    min_power, max_last, maxr, maxc = 5000, 0, 0, 0
    max_power, min_last, minr, minc = 0, K, N, M

    for i in range(N):
        for j in range(M):
            if not matrix[i][j]: # 부서진 포탑
                continue

            if (-matrix[i][j], last[i][j], i+j, j) > (-min_power, max_last, maxr+maxc, maxc):
                min_power, max_last, maxr, maxc = matrix[i][j], last[i][j], i, j

            if (-matrix[i][j], last[i][j], i+j, j) < (-max_power, min_last, minr+minc, minc):
                max_power, min_last, minr, minc = matrix[i][j], last[i][j], i, j

    return maxr, maxc, minr, minc

dr = [-1, -1, -1, 0, 0, 1, 1, 1] # 우하좌상 4,6,3,1
dc = [-1, 0, 1, -1, 1, -1, 0, 1]

N, M, K = map(int, input().split()) # 격자, 라운드. 10, 10, 1000
matrix = [list(map(int, input().split())) for _ in range(N)]
last = [[0] * M for _ in range(N)] # 마지막 공격. 큰게 최근

for turn in range(1, K+1):
    # 1. 공격자 선정
    wr, wc, sr, sc = find()
    matrix[wr][wc] += N+M
    last[wr][wc] = turn

    # 2. 레이저/포탄 공격
    path = laser() # 공격자, 피공격자 제외

    dam = matrix[wr][wc]
    matrix[sr][sc] = max(matrix[sr][sc]-dam, 0) # 0보다 작아지지 않게

    dam //= 2 # 경로는 반만 피해
    for r, c in path:
        matrix[r][c] = max(matrix[r][c]-dam, 0)

    # 부서지지 않은 포탑 1개면 즉시 중지
    if sum(row.count(0) for row in matrix) == N*M-1:
        break

    # 3. 포탑 정비
    # 공격과 무관한 애들 +1
    path.append((sr, sc))
    path.append((wr, wc))

    for i in range(N):
        for j in range(M):
            if matrix[i][j] and (i, j) not in path:
                matrix[i][j] += 1

print(max(map(max, matrix))) # 남아있는 포탑 중 가장 강한 포탑의 공격력