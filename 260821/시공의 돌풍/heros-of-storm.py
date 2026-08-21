from collections import deque

def spread(r, c): # 먼지 확산
    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]

        if not (0 <= nr < n and 0 <= nc < m):
            continue

        if matrix[nr][nc] == -1: # 돌풍
            continue

        ash[nr][nc] += matrix[r][c] // 5
        ash[r][c] -= matrix[r][c] // 5 # 확산된 만큼 빼주기. matrix 빼주는게 낫나?

def clean(r, c, idx):
    q = deque([(r, c, 0)]) # 돌풍 0 처리
    d = 0 # 시작은 오른쪽

    while q:
        cr, cc, val = q.popleft()

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

        if matrix[nr][nc] == -1: # 돌풍 만나면 끝. 범위 체크한 후에 해야됨
            return

        q.append((nr, nc, matrix[nr][nc]))
        # 여기서 바로 바꿔주기
        matrix[nr][nc] = val


dr = [0, -1, 0, 1] # 오위왼아
dc = [1, 0, -1, 0]

n, m, t = map(int, input().split()) # 6~50, 1~1000
matrix = [list(map(int, input().split())) for _ in range(n)] # 먼지 양
# 돌풍 -1. 항상 맨 왼쪽. 맨윗행과 맨아랫행과 적어도 두칸 이상 차이남
wind = []

# 돌풍은 무조건 0열에 있어서 이중 for문 안 돌려도 됨...omg
for i in range(n):
    if matrix[i][0] == -1:
        wind.append((i, 0))

for _ in range(t):
    ash = [[0] * m for _ in range(n)] # 한번에 처리

    for i in range(n):
        for j in range(m):
            if matrix[i][j] != -1 and matrix[i][j] >= 5: # 5 이상이어야 확산 가능
                spread(i, j)

    for i in range(n):
        for j in range(m):
            matrix[i][j] += ash[i][j]

    # 돌풍 청소
    for idx, (wr, wc) in enumerate(wind):
        clean(wr, wc, idx)


print(sum(map(sum, matrix)) + 2) # t초 뒤에 남아있는 먼지 양. 돌풍 더해주기