# 돌풍은 항상 1번 열. 크기 두칸 세로로
# 1. 먼지 인접한 4방향으로 확산
#   - 돌풍이 있거나 범위 벗어나면 확산 ㄴㄴ
#   - 확산 양은 원래 먼지 / 5. 소숫점 버림
#   - 원래 먼지는 확산된 먼지만큼 줄어듬 << 헷갈림. 원래 먼지 / 5 * 확산만큼 빠짐
#   - 확산된 먼지는 방에 있는 모든 먼지가 확산 끝낸 다음 해당 칸에 더해짐
# 2. 돌풍 청소 시작
#   - 반 나눠서 윗칸에서는 반시계 방향으로 바람. 아랫칸에서는 시계 방향으로 바람
#   - 먼지가 바람 방향대로 한칸 이동
#   - 돌풍으로 들어간 먼지는 사라짐
# visited가 필요할까? 어차피 한칸씩 돌아야되는데. 근데 더 효율적일거 같기도 하고 @.@
from collections import deque

def spread(r, c): # bfs. 먼지 확산
    q = deque([(r, c)])
    visited[r][c] = 1

    while q:
        cr, cc = q.popleft()

        for i in range(4):
            nr = cr + dr[i]
            nc = cc + dc[i]

            if not (0 <= nr < n and 0 <= nc < m):
                continue

            if matrix[nr][nc] == -1: # 돌풍
                continue

            ash[nr][nc] += matrix[cr][cc] // 5
            ash[cr][cc] -= matrix[cr][cc] // 5 # 확산된 만큼 빼주기. 미리 matrix에서 빼줄까 얘도 나중에 한번에 해줄까. while 끝나고?

            if not visited[nr][nc]:
                q.append((nr, nc))
                visited[nr][nc] = 1


def clean(r, c, idx):
    q = deque([(r, c)])
    d = 0 # 시작은 오른쪽

    while q:
        cr, cc = q.popleft()

        if idx == 0:
            nr = cr + dr[d]
        else:
            nr = cr - dr[d]
        nc = cc + dc[d]

        if not (0 <= nr < n and 0 <= nc < m): # 벽 부딪히면
            d += 1 # 어차피 네방향 돌고 끝

            if idx == 0:
                nr = cr + dr[d]
            else:
                nr = cr - dr[d]
            nc = cc + dc[d]

        if matrix[nr][nc] == -1: # 돌풍 만나면 끝
            break

        change[nr][nc] = matrix[cr][cc] if matrix[cr][cc] != -1 else 0
        q.append((nr, nc))


dr = [0, -1, 0, 1] # 오위왼아
dc = [1, 0, -1, 0]

n, m, t = map(int, input().split()) # 6~50, 1~1000
matrix = [list(map(int, input().split())) for _ in range(n)] # 먼지 양
# 돌풍 -1. 항상 맨 왼쪽. 맨윗행과 맨아랫행과 적어도 두칸 이상 차이남
time = 0
wind = []

for i in range(n):
    for j in range(m):
        if matrix[i][j] == -1:
            wind.append((i, j))

while time < t:
    time += 1
    ash = [[0] * m for _ in range(n)] # 한번에 처리
    visited = [[0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if matrix[i][j] != -1 and not visited[i][j]:
                spread(i, j)

    for i in range(n):
        for j in range(m):
            if matrix[i][j] != -1:
                matrix[i][j] += ash[i][j]

    # 돌풍 청소
    change = [[-1] * m for _ in range(n)]  # 바꿀거 기록

    for idx, (wr, wc) in enumerate(wind):
        clean(wr, wc, idx)

    # 바꿔주기
    for i in range(n):
        for j in range(m):
            if change[i][j] != -1:
                matrix[i][j] = change[i][j]


print(sum(map(sum, matrix)) + 2) # t초 뒤에 남아있는 먼지 양. 돌풍 더해주기