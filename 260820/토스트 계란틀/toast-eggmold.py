# 계란틀은 정사각형. 각각의 계란틀에 담긴 계란의 양
# 계란틀을 이루는 4개의 선은 분리 가능
# bfs로 풀어야할듯?
# 4방 탐색하면서 차이나는 애들 다 더하기
# while 해도 되나? 2000 * 50 * 50

# 1. 계란의 양이 너무 차이나지 않게 하나의 선을 맞대고 있는 두 계란의 차이가 L 이상 R 이하라면 해당 선 분리
# 2. 모든 계란틀에 대해 검사, 모두 선 분리
# 3. 선 분리 후에 계란 하나로 합치고 이후에 다시 분리..?
# 4. 합쳐진 계란의 총 합 / 합쳐진 계란틀의 총 개수. 소수점 버리기
from collections import deque

def bfs(r, c):
    global no_move

    q = deque([(r, c)])
    visited[r][c] = 1
    total = matrix[r][c]
    eggs = [(r, c)] # 해당 칸들

    while q:
        cr, cc = q.popleft()

        for i in range(4):
            nr = cr + dr[i]
            nc = cc + dc[i]

            if not (0 <= nr < n and 0 <= nc < n and not visited[nr][nc]):
                continue

            # 차이 비교
            diff = abs(matrix[nr][nc] - matrix[cr][cc])
            if L <= diff <= R:
                q.append((nr, nc))
                visited[nr][nc] = 1

                total += matrix[nr][nc]
                eggs.append((nr, nc))

    # 하나로 합치고 분리
    if len(eggs) > 1:
        amount = total // len(eggs)

        for er, ec in eggs:
            matrix[er][ec] = amount
    else:
        no_move += 1


dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

n, L, R = map(int, input().split()) # 칸 크기, 이동 범위 최솟값, 최댓값. 50, 100, 100
matrix = [list(map(int, input().split())) for _ in range(n)] # 계란 개수. 0~100
move = 0 # 계란 몇번 이동하는지

while True:
    no_move = 0  # 계란 이동 필요없는 개수
    visited = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                bfs(i, j)

    if no_move == n*n:
        break

    move += 1

print(move) # 계란 이동 몇번 하는지. 2000번 이하임