# 1번말 한 방향
# 2번말 양방향 (반대)
# 3번말 위오
# 4번말 한쪽 제외
# 5번말 4방
# 각 말들은 한 가지 방향 선택 가능 -> 이동할 수 있는 격자 범위 다름
# 갈 수 없는 격자 크기 최소화 -> 최대한 많이 가기

# 본인 말은 뛰어넘어서 갈 수 있음 but 상대 말은 뛰어넘을 수 없음
# 갈 수 없는 격자 상대편 말 계산하지 않음. 빈 곳만 계산

def go(r, c, d):
    htype = matrix[r][c] # 말 종류

    if htype == 1:
        drange = [d]
    elif htype == 2: # 반대
        drange = [d, (d+2)%4]
    elif htype == 3: # 자기 오른쪽
        drange = [d, (d+1)%4]
    elif htype == 4: # 해당 방향 빼고 다
        drange = [di for di in range(4) if di != d]
    elif htype == 5: # 네 방향 다
        drange = range(4)

    for cd in drange:
        cr, cc = r, c

        while True:
            nr = cr + dr[cd]
            nc = cc + dc[cd]

            if not (0 <= nr < N and 0 <= nc < M and matrix[nr][nc] != 6):  # 벽, 상대편
                break

            if matrix[nr][nc] == 0:
                matrix[nr][nc] = -1

            cr, cc = nr, nc


def dfs(idx):
    global min_area, matrix

    if idx == len(horses):
        area = sum(row.count(0) for row in matrix)
        min_area = min(min_area, area)
        return

    for d in range(4):
        roll_matrix = [row[:] for row in matrix]
        go(*horses[idx], d)
        dfs(idx+1)
        matrix = roll_matrix


dr = [-1, 0, 1, 0] # 위오아왼
dc = [0, 1, 0, -1]

N, M = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(N)]
# 0 = 빈칸, 1~5 = 내 말, 6 = 상대편. 갈 수 있는 위치 -1로 표시
horses = [] # 말들 위치

for i in range(N):
    for j in range(M):
        if 1 <= matrix[i][j] <= 4:
            horses.append((i, j))

        if matrix[i][j] == 5: # 4방은 갈 수 있는 곳 다 표시해놓기
            go(i, j, 0)

min_area = sum(row.count(0) for row in matrix)
dfs(0)

print(min_area) # 갈 수 없는 체스판 영역의 최솟값