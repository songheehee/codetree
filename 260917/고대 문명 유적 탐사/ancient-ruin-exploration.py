# 유적지 5*5
# 유물 종류 1~7

# 1. 탐사진행
# 3*3 격자 회전
# 시계 방향으로 90, 180, 270. 무조건 회전 진행해야됨
# 1-1. 유물 1차 획득 가치 최대화
# 1-2. 회전 각도가 가장 적은 방법
# 1-3. 회전 중심 좌표 열작, 행작

# 2. 유물 획득
# 상하좌우로 인접한 같은 종류는 연결되어있음. 3개 이상 연결된 경우 사라지고 유물됨. 가치 = 모인 개수
# 사라진 자리에 벽면 숫자(???) 새로운 조각 생김. 쓴 이후에 다시 사용 불가. 충분히 많은 숫자
# 열작, 행큰
# 새로운 유물 생겨나지 않을 때까지 반복

# 유물 획득할 수 없다면 즉시 종료. 아무것도 출력하지 않음
# 초기에 유물 발견되지 않음. 첫번째 이후로는 항상 유물 발견

from collections import deque

def spin():
    # 각 좌표마다 회전시켜보고 유물 1차 획득 최대인 곳 찾기
    max_gold, min_angle, minc, minr = 0, 360, 5, 5
    max_matrix = []
    max_points = [] # 유물 좌표들

    for i in range(3):
        for j in range(3):
            new_matrix = [row[:] for row in matrix]
            sq = [row[j:j+3] for row in matrix[i:i+3]] # 3*3

            for angle in (90, 180, 270):
                sq = list(map(list, zip(*sq[::-1])))

                for sr in range(i, i+3):
                    for sc in range(j, j+3):
                        new_matrix[sr][sc] = sq[sr-i][sc-j]

                gold, points = check_gold(new_matrix)

                if (-max_gold, min_angle, minc, minr) > (-gold, angle, j, i):
                    max_gold, min_angle, minc, minr = gold, angle, j, i
                    max_matrix = [row[:] for row in new_matrix]
                    max_points = points[:]

    return max_matrix, max_gold, max_points

def check_gold(new_matrix):
    global visited
    visited = [[0] * 5 for _ in range(5)]
    gold = 0 # 유물 개수
    points = []

    for i in range(5):
        for j in range(5):
            if not visited[i][j]:
                g, point = bfs(i, j, new_matrix)
                gold += g
                points.extend(point)

    return gold, points

def bfs(r, c, new_matrix):
    q = deque([(r, c)])
    visited[r][c] = 1
    count = 1 # 자기 자신 포함
    num = new_matrix[r][c] # 유물 종류
    point = [(r, c)]

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < 5 and 0 <= nc < 5):
                continue

            if visited[nr][nc] or new_matrix[nr][nc] != num:
                continue

            count += 1
            visited[nr][nc] = 1
            q.append((nr, nc))
            point.append((nr, nc))

    return count if count >= 3 else 0, point if count >= 3 else []

def get_gold(points):
    global cur_gold

    points.sort(key=lambda x: (x[1], -x[0])) # 열작, 행큰

    for r, c in points:
        matrix[r][c] = nums.popleft() # 새 숫자 채워넣기

    gold, new_points = check_gold(matrix)

    if not gold:
        return

    cur_gold += gold
    get_gold(new_points)

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

K, N = map(int, input().split()) # 반복 횟수, 벽면 숫자 개수. 10, 300
matrix = [list(map(int, input().split())) for _ in range(5)] # 5*5
nums = deque(map(int, input().split()))
total = [] # 각 턴마다 획득한 유물 가치의 총합

for _ in range(K):
    # 1. 회전
    matrix, cur_gold, cur_points = spin()

    # 유물 획득 못하면 즉시 종료
    if not cur_gold:
        break

    # 2. 유물 획득
    get_gold(cur_points)

    total.append(cur_gold) # 이번 턴에 얻은 유물

print(*total) # 각 턴마다 획득한 유물의 가치 총합