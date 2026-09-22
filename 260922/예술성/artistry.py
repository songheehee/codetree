# 색깔 1~10. 동일한 색깔 상하좌우 인접해있으면 한 그룹
# 예술 점수 = 모든 그룹 쌍의 조화로움의 합
# (a에 속한 칸의 수 + b 칸의 수) * a 숫자 * b 숫자 * 맞닿은 변의 수
# 예술 점수 구하기 -> 회전
# 십자 모양은 반시계 90도
# 정사각형은 시계 90도

from collections import deque

def rotate():
    new_matrix = [row[:] for row in matrix]
    # 십자가 회전
    for i in range(N):
        new_matrix[N//2][i] = matrix[i][N//2]

    for j in range(N):
        new_matrix[N-1-j][N//2] = matrix[N//2][j]

    # 정사각형 회전
    for sr, er, sc, ec in [(0, N//2, 0, N//2), (0, N//2, N//2+1, N), (N//2+1, N, 0, N//2), (N//2+1, N, N//2+1, N)]:
        sq = [row[sc:ec] for row in matrix[sr:er]]
        sq = list(map(list, zip(*sq[::-1])))

        for i in range(sr, er):
            for j in range(sc, ec):
                new_matrix[i][j] = sq[i-sr][j-sc]

    return new_matrix


def nearby(): # 그룹 근처 다른 그룹 맞닿은 변 수
    for idx in range(1, len(group)): # 그룹 인덱스
        near_group = dict()
        points = group[idx][2]

        for r, c in points: # 주변 4방 탐색
            for d in range(4):
                nr = r + dr[d]
                nc = c + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                nxt = group_matrix[nr][nc]
                if nxt <= group_matrix[r][c]: # 같거나 나보다 작은 애. 작은 애 앞에서 처리했음
                    continue

                if nxt in near_group:
                    near_group[nxt] += 1
                else:
                    near_group[nxt] = 1

        group[idx][2] = near_group # 어차피 좌표 안 쓰니까 덮어쓰기


def bfs(r, c, idx):
    q = deque([(r, c)])
    group_matrix[r][c] = idx
    color = matrix[r][c]
    count = 1
    points = [(r, c)] # 해당 그룹 좌표들

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if group_matrix[nr][nc] or matrix[nr][nc] != color: # 이미 체크됨 or 다른 색
                continue

            group_matrix[nr][nc] = idx
            q.append((nr, nc))
            count += 1
            points.append((nr, nc))

    return count, points


def make_group(): # 그룹 칸수 구하고 group_matrix 구해주기
    idx = 1

    for i in range(N):
        for j in range(N):
            if not group_matrix[i][j]:
                count, points = bfs(i, j, idx)
                group.append([count, matrix[i][j], points])

                idx += 1


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N = int(input()) # 홀수. 29
matrix = [list(map(int, input().split())) for _ in range(N)]
score = 0

for i in range(4):
    # 1. 그룹 나눠주기
    group = [None]  # 칸 수, 숫자, {맞닿은 그룹 : 변 수}. 1번부터
    group_matrix = [[0] * N for _ in range(N)]
    make_group()
    nearby()

    # 2. 예술 점수 구하기
    for count, num, nears in group[1:]:
        if not nears:
            continue

        for idx, v in nears.items(): # 인접한 그룹. 그룹 인덱스, 변 수
            gcount, gnum, _ = group[idx]
            score += (count + gcount) * num * gnum * v

    if i == 3: # 3회전 이후에는 회전 안함
        break

    # 3. 회전
    matrix = rotate()

print(score) # 초기 + 1회전 + 2회전 + 3회전 이후