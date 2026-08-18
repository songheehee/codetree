# 불은 상하좌우로 '모두' 번짐. 방화벽 뚫을 수는 없음
# 방화벽 추가로 3개 설치 가능. 불 있는 위치에는 불가
# 불이 퍼지지 않는 영역이 최대일 때 크기
from collections import deque

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

def bfs():
    new_matrix = [row[:] for row in matrix] # 원본꺼 안 건드리기

    for r, c in select:
        new_matrix[r][c] = 1 # 방화벽

    q = deque()
    q.extend(fire)

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < n and 0 <= nc < m):
                continue

            if new_matrix[nr][nc] == 0:
                new_matrix[nr][nc] = 2 # 불
                q.append((nr, nc))

    # 불이 퍼지지 않은 영역 카운트
    count = 0

    for i in range(n):
        for j in range(m):
            if new_matrix[i][j] == 0:
                count += 1

    return count


def dfs(): # 방화벽 설치할 곳 3개 고르기
    global max_area

    if len(select) == 3:
        # 방화벽 설치 후 불 퍼트리기
        area = bfs()
        max_area = max(max_area, area)
        return

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 0 and not visited[i][j]: # 빈칸일때만 방화벽 가능
                visited[i][j] = 1
                select.append((i, j))
                dfs()
                select.pop()
                visited[i][j] = 0


n, m = map(int, input().split()) # 3~8
matrix = [list(map(int, input().split())) for _ in range(n)]
# 2 = 불, 1 = 방화벽, 0 = 빈칸
fire = []

for i in range(n):
    for j in range(m):
        if matrix[i][j] == 2:
            fire.append((i, j))

visited = [[0] * m for _ in range(n)]
select = []
max_area = 0

dfs()

print(max_area)