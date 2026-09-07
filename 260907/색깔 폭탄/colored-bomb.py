# -1 = 검정 돌, 0 = 빨강 폭탄, 1 <= 다른 색 폭탄
# 1. 크기가 가장 큰 폭탄 묶음 찾기. 2개 이상 같은 색 or 빨강 포함해서 2개의 색. 빨간색만 있는 건 안됨
# 1-1) 빨간색이 가장 적게 포함된 것
# 1-2) 행이 가장 큰 > 열이 가장 작은 애 (기준점은 빨강이 아니면서 행/열이 가장 큰 애)
# 2. 선택된 폭탄 묶음 전부 제거. 중력 작용해서 떨어짐 but 돌 위는 안 떨어짐
# 3. 반시계 방향으로 90도
# 4. 중력 작용. 돌 안 떨어짐
# 점수 = 폭탄 묶음 개수 제곱

from collections import deque

def bfs(sr, sc):
    global max_count, min_red, max_r, min_c, delete_bombs

    q = deque([(sr, sc)])
    visited[sr][sc] = 1
    color = matrix[sr][sc]

    count = 1  # 폭탄 개수. 자기 자신 포함
    red = 0  # 빨간색 개수
    br, bc = sr, sc
    bombs = [(sr, sc)]

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                continue

            if matrix[nr][nc] not in (color, 0):
                continue

            count += 1
            visited[nr][nc] = 1
            q.append((nr, nc))
            bombs.append((nr, nc))

            if matrix[nr][nc] == 0:
                red += 1
            else:
                if (br, -bc) < (nr, -nc):
                    br, bc = nr, nc

    if (count, -red, br, -bc) > (max_count, -min_red, max_r, -min_c):
        max_count, min_red, max_r, min_c = count, red, br, bc
        delete_bombs = bombs

    # 빨간색 다시 갈 수 있게 원복
    for r, c in red_bomb:
        visited[r][c] = 0

def gravity():
    new_matrix = list(zip(*matrix[::-1]))

    for i in range(N):
        new_row = []

        for j in range(N):
            if new_matrix[i][j] == -1:
                new_row.extend([-2] * (N - len(new_row) - len(new_matrix[i][j:])))
                new_row.append(-1) # 돌
                continue

            if new_matrix[i][j] == -2:
                continue

            new_row.append(new_matrix[i][j])

        if new_row:
            new_row.extend([-2] * (N - len(new_row)))
            new_matrix[i] = new_row

    return list(map(list, zip(*new_matrix)))[::-1]


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N, B = map(int, input().split()) # 격자 크기, 폭탄 종류. 20, 5
matrix = [list(map(int, input().split())) for _ in range(N)]
score = 0

while True:
    # 1. 폭탄 묶음 찾기
    visited = [[0] * N for _ in range(N)]
    max_count, min_red, max_r, min_c = 0, N*N, 0, N
    delete_bombs = []
    red_bomb = [] # 빨간색 좌표 저장

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 0:
                red_bomb.append((i, j))

    for i in range(N):
        for j in range(N):
            if matrix[i][j] not in (0, -1, -2) and not visited[i][j]: # 빨강, 돌은 계산 X
                bfs(i, j)

    if max_count <= 1:
        break

    score += max_count ** 2

    # 2. 삭제
    for r, c in delete_bombs:
        matrix[r][c] = -2 # 터진 폭탄

    # 3. 중력
    matrix = gravity()

    # 4. 반시계 회전 -> 중력
    matrix = list(map(list, zip(*matrix)))[::-1]
    matrix = gravity()

print(score)