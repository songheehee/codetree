# 좌하단이 0,0임. 좌표 선임

# 1. 미생물 투입
# 직사각형 영역에 미생물 투입
# 새로 들어온 애가 원래 있던 애 잡아먹음
# 영역 둘로 나눠지면 나눠진 애들 다 사라짐

# 2. 미생물 이동
# 새로운 용기로 이동
# 가장 큰 영역 차지한 미생물. 같을 경우 더 먼저 투입된 애
# 형태 유지하면서 범위 넘지 않으면서 영역 안 겹치게
# 최대한 열작, 행작
# 어디에도 둘 수 없으면 사라짐

# 3. 실험 결과
# 인접한 무리 쌍 확인. A * B 만큼 점수
# 모든 쌍의 성과 더하기

from collections import deque

def nearby(r, c):
    q = deque([(r, c)])
    visited[r][c] = idx
    nums = set() # 인접한 다른 무리

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or matrix[nr][nc] == 0:
                continue

            if matrix[nr][nc] == idx:
                q.append((nr, nc))
                visited[nr][nc] = idx
            else: # visited 처리 해서 다시 계산 안함
                nums.add(matrix[nr][nc])

    score = 0
    area = len(groups[idx][1]) # 나의 영역 넓이

    for num in nums:
        score += area * len(groups[num][1])

    return score


def draw():
    for j in range(N):
        for i in range(N):
            for r, c in points: # 상대 좌표
                nr = i + r
                nc = j + c

                if not (0 <= nr < N and 0 <= nc < N and new_matrix[nr][nc] == 0):
                    break

            else: # 다 돌 수 있으면 그려주기
                for r, c in points:
                    nr, nc = i+r, j+c
                    new_matrix[nr][nc] = idx
                return 1

    return 0


def bfs(r, c):
    q = deque([(r, c)])
    visited[r][c] = idx
    points = [(0, 0)] # 상대 좌표. 현재 위치 포함

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or matrix[nr][nc] != idx:
                continue

            q.append((nr, nc))
            visited[nr][nc] = idx
            points.append((nr-r, nc-c)) # 첫 좌표 기준

    return points


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N, Q = map(int, input().split()) # 격자, 실험 횟수
matrix = [[0] * N for _ in range(N)]

for num in range(1, Q+1):
    # 1. 미생물 투입 - 매트릭스에 그려주기
    c1, r1, c2, r2 = map(int, input().split())

    for i in range(r1, r2):
        for j in range(c1, c2):
            matrix[i][j] = num

    # 2. 배양 용기 이동. 둘로 나눠졌는지 확인
    groups = [None] * (num+1) # 크기, 투입 번호. 1번부터
    visited = [[0] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if matrix[i][j] and not visited[i][j]:
                idx = matrix[i][j]
                if groups[idx] is not None: # 이미 찾은 애 -> 둘로 나뉨
                    groups[idx] = 0
                else:
                    points = bfs(i, j)
                    groups[idx] = (idx, points)

    bacteria = [x for x in groups if x] # 있는 애들만
    bacteria.sort(key=lambda x: (-len(x[1]), x[0])) # 크기는 크고 번호는 작음

    # 이동시키고 그려주기. 열작, 행작
    new_matrix = [[0] * N for _ in range(N)]
    count = 0 # 그려진 미생물 개수

    for idx, points in bacteria:
        count += draw()

    matrix = new_matrix

    # 3. 실험 점수
    score = 0

    if count > 1: # 군집 개수가 두개 이상이어야함
        visited = [[0] * N for _ in range(N)]

        for i in range(N):
            for j in range(N):
                if matrix[i][j] and not visited[i][j]:
                    idx = matrix[i][j]
                    score += nearby(i, j)

    print(score) # 모든 쌍의 성과