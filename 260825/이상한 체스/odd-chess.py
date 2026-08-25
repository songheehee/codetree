# 1시간 51분
# 말들의 방향을 적절히 설정하여 갈 수 없는 격자의 크기 최소화
# 본인 말은 뛰어넘어서 지나갈 수 있음
# 상대편 말은 못 지나감. 대신 상대편 말이 있는 격자는 계산하지 않음

# 1 = 위, 2 = 오왼, 3 = 위오, 4 = 위오왼, 5 = 위오왼아, 6 = 상대편
def bfs(h, r, c, d):
    if h == 4:
        for i in range(3):
            cr, cc = r, c
            while True:  # 벽, 6 만나기 전까지
                nr = cr + dr[(d+i)%4]
                nc = cc + dc[(d+i)%4]

                if not (0 <= nr < n and 0 <= nc < m and matrix[nr][nc] != 6):
                    break

                if not visited[nr][nc]:
                    visited[nr][nc] = h
                cr, cc = nr, nc
        return

    if h == 3:
        for i in range(2):
            cr, cc = r, c
            while True:  # 벽, 6 만나기 전까지
                nr = cr + dr[(d + i) % 4]
                nc = cc + dc[(d + i) % 4]

                if not (0 <= nr < n and 0 <= nc < m and matrix[nr][nc] != 6):
                    break

                if not visited[nr][nc]:
                    visited[nr][nc] = h
                cr, cc = nr, nc
        return

    if h == 2:
        for i in [0, 2]:
            cr, cc = r, c
            while True:  # 벽, 6 만나기 전까지
                nr = cr + dr[(d + i) % 4]
                nc = cc + dc[(d + i) % 4]

                if not (0 <= nr < n and 0 <= nc < m and matrix[nr][nc] != 6):
                    break

                if not visited[nr][nc]:
                    visited[nr][nc] = h
                cr, cc = nr, nc
        return

    if h == 1:
        cr, cc = r, c
        while True:  # 벽, 6 만나기 전까지
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < n and 0 <= nc < m and matrix[nr][nc] != 6):
                break

            if not visited[nr][nc]:
                visited[nr][nc] = h
            cr, cc = nr, nc
        return


def dfs():
    global visited, min_count
    
    if not horses:
        min_count = min(min_count, sum(row.count(0) for row in visited))
        return

    h, r, c = horses.pop(0)
    
    srange = 4
    if h == 2:
        srange = 2
    
    for d in range(srange): # 시작점
        visited_roll = [row[:] for row in visited]  # 롤백시켜주기 위함
        bfs(h, r, c, d) # 이동할 수 있는 0 개수
        dfs()
        visited = visited_roll

    horses.append((h, r, c))

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

n, m = map(int, input().split()) # 세로 가로
matrix = [list(map(int, input().split())) for _ in range(n)]

# 큰 말부터 하면서 거꾸로. 큐에다 넣고?
# 매트릭스에 표시할까 visited 만들까
# 백트래킹 해야될거 같은데
horses = []
visited = [[0] * m for _ in range(n)]
min_count = n * m # 남은 곳 개수

for i in range(n):
    for j in range(m):
        if 0 < matrix[i][j] < 6:
            horses.append((matrix[i][j], i, j))
            visited[i][j] = matrix[i][j]
            
        elif matrix[i][j] == 6:
            visited[i][j] = 6

horses.sort(reverse=True)

# 5는 다 표시
for h, r, c in horses:
    if h == 5:
        horses.pop(0)

        for i in range(4):
            cr, cc = r, c
            while True:  # 벽, 6 만나기 전까지
                nr = cr + dr[i]
                nc = cc + dc[i]

                if not (0 <= nr < n and 0 <= nc < m and matrix[nr][nc] != 6):
                    break

                if matrix[nr][nc] == 0:
                    visited[nr][nc] = h # 임시 표시
                cr, cc = nr, nc
    else:
        break

dfs()

print(min_count)