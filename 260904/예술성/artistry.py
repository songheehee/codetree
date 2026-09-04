# 동일한 숫자 상하좌우 인접 -> 동일한 그룹
# 초기 예술 점수 -> 회전
# 정중앙 기준으로 십자 모양 -> 반시계 90도
# 4개 정사각형 시계 90도

from collections import deque

def bfs(r, c):
    q = deque([(r, c)])
    color = matrix[r][c]
    group_matrix[r][c] = len(groups)
    count = 1

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if group_matrix[nr][nc] != -1 or matrix[nr][nc] != color: # 이미 방문했거나 다른 색이면
                continue

            group_matrix[nr][nc] = len(groups)
            q.append((nr, nc))
            count += 1

    return color, count

def side(): # 맞닿은 변의 수
    for k in range(len(groups)):
        count = [0] * len(groups)

        for i in range(N):
            for j in range(N):
                if group_matrix[i][j] == k:
                    for d in range(4):
                        nr = i + dr[d]
                        nc = j + dc[d]

                        if not (0 <= nr < N and 0 <= nc < N):
                            continue

                        if group_matrix[nr][nc] != k:
                            count[group_matrix[nr][nc]] += 1

        group_line.append(count)

def calc(a, b):
    # (그룹 a 칸의 수 + b 칸의 수) * 그룹 a 숫자 * 그룹 b 숫자 * 맞닿아 있는 변의 수
    global score

    score += (groups[a][1] + groups[b][1]) * groups[a][0] * groups[b][0] * group_line[a][b]

def rotate():
    new_matrix = [[0] * N for _ in range(N)]
    # 십자가 반시계
    hor = matrix[N//2][::-1]
    ver = [row[N//2] for row in matrix]

    new_matrix[N//2] = ver
    for i in range(N):
        new_matrix[i][N//2] = hor[i]

    # 정사각형들 90도
    for i in range(0, N//2):
        for j in range(0, N//2):
            new_matrix[i][j] = matrix[N//2-1-j][i]

    for i in range(N//2+1, N):
        for j in range(0, N//2):
            new_matrix[i][j] = matrix[N-1-j][i-(N//2+1)]

    for i in range(0, N//2):
        for j in range(N//2+1, N):
            new_matrix[i][j] = matrix[N-1-j][N//2+1+i]

    for i in range(N//2+1, N):
        for j in range(N//2+1, N):
            new_matrix[i][j] = matrix[N+N//2-j][i]

    return new_matrix

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N = int(input()) # 격자 크기. 홀수. 30
matrix = [list(map(int, input().split())) for _ in range(N)]
score = 0

for turn in range(4):
    groups = []  # 색깔, 칸수
    group_matrix = [[-1] * N for _ in range(N)]  # 각 그룹 인덱스
    group_line = []

    if turn > 0:
        # 1. 회전
        matrix = rotate()

    # 2. 그룹 파악
    for i in range(N):
        for j in range(N):
            if group_matrix[i][j] == -1:
                groups.append(bfs(i, j))

    # 3. 점수 계산
    side()
    for i in range(len(groups)):
        for j in range(i+1, len(groups)):
            calc(i, j)

print(score) # 초기 + 1회전 + 2회전 + 3회전 점수 합