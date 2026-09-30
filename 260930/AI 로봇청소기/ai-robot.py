# 좌상단 1,1
# 1. 먼지가 있거나, 2. 먼지가 없거나, 3. 물건 있거나
# 먼지는 1~100
# 초기 청소기 위치에는 먼지 없음

# 1. 청소기 이동 (여러개) - 순서대로
# 이동 거리가 가장 가까운 먼지 있는 곳
# 물건이 있거나 청소기가 있는 격자로는 못감
# 행작, 열작

# 2. 청소 - 순서대로
# 바라보는 방향 기준, ㅗ 모양
# 청소할 수 있는 먼지량이 가장 큰 방향으로
# 격자 당 청소할 수 있는 최대 먼지량은 20
# 방향 여러개면 오,아,왼,위 우선순위

# 3. 먼지 축적
# 먼지 있는 곳 +5

# 4. 먼지 확산 - 동시에
# 깨끗한 격자에 주변 4방 합 // 10

# 오염된 곳이 없으면 어디로 가지...

from collections import deque

def spread():
    new_matrix = [row[:] for row in matrix] # 동시 확산

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 0: # 먼지 없는 곳
                dust = 0

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if matrix[nr][nc] > 0: # 먼지 있는 곳만
                        dust += matrix[nr][nc]

                new_matrix[i][j] = dust // 10

    return new_matrix


def cleaning():
    for r, c in clean:
        max_dust, maxd = 0, 0 # 먼지량 가장 큰 방향
        matrix[r][c] -= min(matrix[r][c], 20) # 본인 위치 먼지 제거

        for d in range(4):
            dust = 0

            for fd in front[d]: # 3방향
                nr = r + dr[fd]
                nc = c + dc[fd]

                if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] > 0):
                    continue

                dust += min(matrix[nr][nc], 20)

            if dust > max_dust:
                max_dust, maxd = dust, d

        # 가장 큰 방향 정해졌으면 먼지 없애주기
        if max_dust:
            for fd in front[maxd]:
                nr = r + dr[fd]
                nc = c + dc[fd]

                if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] > 0):
                    continue

                matrix[nr][nc] -= min(matrix[nr][nc], 20)


def move(r, c, idx):
    visited = [[0] * N for _ in range(N)]
    q = deque([(r, c)])
    visited[r][c] = 1
    minr, minc = N, N

    while q:
        for _ in range(len(q)):
            cr, cc = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                    continue

                if matrix[nr][nc] == -1 or (nr, nc) in clean: # 물건 있거나, 청소기 있거나
                    continue

                if matrix[nr][nc]:
                    if (minr, minc) > (nr, nc): # 먼지 있으면
                        minr, minc = nr, nc
                else:
                    q.append((nr, nc))
                    visited[nr][nc] = visited[cr][cc] + 1

        if minr < N: # 먼지 있는 곳 찾음
            clean[idx] = minr, minc  # 새 위치
            break


dr = [0, 1, 0, -1] # 오아왼위
dc = [1, 0, -1, 0]

front = [[0, 1, 3], # 오 -> 왼만 제외
         [0, 1, 2], # 아 -> 위 제외
         [1, 2, 3], # 왼
         [0, 2, 3]] # 위

N, K, L = map(int, input().split()) # 격자, 청소기 개수, 테스트 횟수. 30, 50, 50
matrix = [list(map(int, input().split())) for _ in range(N)] # -1=물건
clean = []

for _ in range(K):
    r, c = map(lambda x: int(x)-1, input().split())
    clean.append((r, c))

for _ in range(L):
    # 먼지 없으면 0 프린트 후 종료
    total = sum(val for row in matrix for val in row if val > 0)
    if total == 0:
        print(0)
        break

    # 1. 청소기 이동
    for idx, (r, c) in enumerate(clean):
        if matrix[r][c] == 0: # 지금 위치에 먼지가 없으면
            move(r, c, idx)

    # 2. 청소
    cleaning()

    # 3. 먼지 축적
    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0:
                matrix[i][j] += 5

    # 4. 먼지 확산
    matrix = spread()

    print(sum(val for row in matrix for val in row if val > 0)) # 총 먼지량 출력