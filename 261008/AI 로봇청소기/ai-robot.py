# 좌상단 1,1
# 1) 먼지 있거나 (1-100) 2) 먼지 없거나 (0) 3) 물건 있거나 (-1)
# 로봇 청소기 초기 위치 먼지 없음

# 1. 청소기 이동 - 순서대로
# 이동 거리 가장 가까운 먼지 있는 곳으로 이동
# 물건 있거나 청소기 있으면 이동 불가
# 가까운 격자 여러개면 행작, 열작
# 현재 위치에 먼지 있으면 이동 X

# 2. 청소 - 순서대로
# 바라보는 방향 기준 3방향 청소
# 바라보는 방향 4개 중 제일 먼지량 큰 방향으로 청소
# 청소할 수 있는 최대 먼지량 20
# 합이 같을 경우 오아왼위 우선순위

# 3. 먼지 축적
# 먼지 있는 곳 (0 보다 큰) +5

# 4. 먼지 확산 - 동시에
# 먼지 0 인 곳 주변 4방향 먼지량 합 // 10

# 전체 공간의 총 먼지량 (물건 제외)
# 먼지 있는 곳 없으면 0 출력 후 종료

from collections import deque

def clean(r, c): # 현재 위치에서 최대 먼지량
    max_dust, max_d = 0, 0

    for d in range(4): # 바라보는 방향
        dust = 0 # 해당 방향 먼지량

        for fd in range(4): # 해당 방향의 반대 제외
            if fd == (d+2) % 4:
                continue

            nr = r + dr[fd]
            nc = c + dc[fd]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if matrix[nr][nc] > 0:
                dust += min(matrix[nr][nc], 20) # 최대 20개

        if max_dust < dust:
            max_dust, max_d = dust, d

    max_dust += matrix[r][c] # 자기 위치

    if max_dust: # 청소할 먼지 있으면
        matrix[r][c] -= min(matrix[r][c], 20) # 현재 위치도

        for d in range(4):
            if d == (max_d+2) % 4:
                continue

            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] > 0):
                continue

            matrix[nr][nc] -= min(matrix[nr][nc], 20)


def move(r, c):
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

                if matrix[nr][nc] == -1 or clean_grid[nr][nc]:  # 물건, 청소기 위치 못 감
                    continue

                if matrix[nr][nc]: # 먼지 있으면
                    if (minr, minc) > (nr, nc):
                        minr, minc = nr, nc
                else:
                    q.append((nr, nc))
                    visited[nr][nc] = visited[cr][cc] + 1

        if minr < N: # 최단 찾음
            return minr, minc

    return r, c # 이동 불가


def spread():
    new_matrix = [row[:] for row in matrix]

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 0: # 먼지 없는 곳만
                total = 0

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] > 0):
                        continue

                    total += matrix[nr][nc]

                new_matrix[i][j] = total // 10

    return new_matrix


dr = [0, 1, 0, -1] # 오아왼위
dc = [1, 0, -1, 0]

N, C, R = map(int, input().split()) # 격자, 청소기 개수, 테스트 횟수. 30, 50, 50
matrix = [list(map(int, input().split())) for _ in range(N)] # 물건, 먼지
cleaner = [None] # 1번부터
clean_grid = [[0] * N for _ in range(N)] # 청소기 번호

for i in range(1, C+1):
    r, c = map(lambda x: int(x) - 1, input().split())
    cleaner.append((r, c))
    clean_grid[r][c] = i

for _ in range(R):
    # 1. 청소기 이동. 행작, 열작
    for i in range(1, C+1):
        r, c = cleaner[i]

        if matrix[r][c] == 0: # 현재 위치에 먼지 없으면 이동
            clean_grid[r][c] = 0  # 전 위치 비워주기
            nr, nc = move(r, c)
            clean_grid[nr][nc] = i
            cleaner[i] = (nr, nc)

    # 2. 청소
    for r, c in cleaner[1:]:
        clean(r, c)

    # 먼지 없으면 끝
    total = sum(val for row in matrix for val in row if val > 0)
    if total == 0:
        print(0)
        break

    # 3. 먼지 축적
    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0: # 먼지 있는 곳만
                matrix[i][j] += 5

    # 4. 먼지 확산
    matrix = spread()

    print(sum(val for row in matrix for val in row if val > 0)) # 먼지량 총합