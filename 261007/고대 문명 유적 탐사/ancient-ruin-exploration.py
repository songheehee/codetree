# 5*5 격자
# 유물 종류 7개 1~7

#1. 탐사 진행
# 3*3 격자 선택해서 회전
# 90도, 180도, 270도 중 하나
# 획득 가치 최대화
# 같을 경우 회전 각도 가장 작을 때
# 열작, 행작 순

# 2. 유물 획득
# 3개 이상 연결된 경우 유물 사라짐
# 벽에서 새 숫자 -> 열작, 행큰 순
# 세개 이상 있으면 또 획득

# 유물 없으면 즉시 종료. 출력하지 않음

from collections import deque

def bfs(r, c, matrix):
    q = deque([(r, c)])
    visited[r][c] = 1
    num = matrix[r][c]
    count = 1 # 개수
    points = [(r, c)]

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or matrix[nr][nc] != num: # 같은 유물만
                continue

            q.append((nr, nc))
            visited[nr][nc] = 1
            count += 1
            points.append((nr, nc))

    if count >= 3: # 유물 3개 이상이어야함
        return count, points

    return 0, [] # 유물 안됨


def search(matrix):
    global visited
    visited = [[0] * N for _ in range(N)]
    total_count, total_points = 0, []

    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                count, points = bfs(i, j, matrix)
                total_count += count
                total_points.extend(points)

    return total_count, total_points


def spin(r, c): # 3*3 돌리기
    global max_count, min_degree, minc, minr, remove_points, max_matrix

    new_matrix = [row[:] for row in matrix]
    sq = [row[c:c+3] for row in matrix[r:r+3]] # 3*3 떼어냄. 얘 돌릴거임

    for degree in (90, 180, 270):
        sq = list(map(list, zip(*sq[::-1])))

        for i in range(r, r+3):
            for j in range(c, c+3):
                new_matrix[i][j] = sq[i-r][j-c]

        count, points = search(new_matrix)

        if (-max_count, min_degree, minc, minr) > (-count, degree, c, r):
            max_count, min_degree, minc, minr = count, degree, c, r
            remove_points = points
            max_matrix = [row[:] for row in new_matrix]


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N = 5
R, C = map(int, input().split()) # 반복 횟수, 유물 개수
matrix = [list(map(int, input().split())) for _ in range(N)]
wall = deque(map(int, input().split()))
ans = [] # 각 탐사마다 얻은 유물

for _ in range(R):
    # 1. 탐사 진행
    max_count, min_degree = 0, 360
    minc, minr = N, N
    max_matrix, remove_points = [], []

    for i in range(N-2):
        for j in range(N-2): # 시작점
            spin(i, j)

    # 유물 없으면 끝
    if not max_count:
        break

    matrix = max_matrix # 회전한 매트릭스

    # 2. 유물 획득
    while True:
        remove_points.sort(key=lambda x: (x[1], -x[0]))
        for r, c in remove_points:
            matrix[r][c] = wall.popleft()

        count, points = search(matrix)

        if count == 0: # 더 이상 없으면
            break

        max_count += count
        remove_points = points

    ans.append(max_count)

print(*ans)