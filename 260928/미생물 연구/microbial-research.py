# 좌측 하단이 0,0
# 총 Q번의 실험을 진행하며 실험 결과 기록

# 1. 미생물 투입
# 좌측 하단 좌표랑 우측 상단 좌표 직사각형 영역에 미생물 투입
# 만약 영역 내에 미생물이 존재하면 새로 투입된 애들이 잡아먹음 -> 새로 투입된 애들만 남음
# A가 새로 투입된 미생물 B에게 잡아먹혀서 영역이 나눠지면 A는 모두 사라짐

# 2. 배양 용기 이동
# 기존 배양 용기에 한 마리도 안 남을 때까지
# 기존 용기에서 가장 넓은 영역인 미생물 선택
# 여러 개일 경우 가장 먼저 투입된 미생물 선택
# 형태 유지하면서 범위 벗어나지 않고 다른 미생물과 겹치지 않도록. 최대한 c 작, r 큼
# 어떤 곳에도 둘 수 없으면 옮겨지지 않고 사라짐

# 3. 실험 결과 기록
# 인접한 무리 쌍 확인. 한번만 확인
# A 영역 넓이 * B 영역 넓이

# 좌표 변환 해줄까 말까

from collections import deque

def nearby(r, c, idx):
    q = deque([(r, c)])
    visited[r][c] = idx
    count = 1
    near_set = set()

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                continue

            if matrix[nr][nc] == idx:
                q.append((nr, nc))
                visited[nr][nc] = idx
                count += 1
            elif matrix[nr][nc]:
                near_set.add(matrix[nr][nc])

    group_draw[idx] = count, list(near_set)


def find_group(r, c):
    q = deque([(r, c)])
    visited[r][c] = idx
    count = 1
    maxr, maxc = r, c # 끝지점 찾아주기
    minr, minc = r, c # 제일 작은 시작점

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
            count += 1

            maxr, maxc = max(maxr, nr), max(maxc, nc)
            minr, minc = min(minr, nr), min(minc, nc)

    return count, idx, maxc-minc+1, maxr-minr+1, minr, minc


def draw(r, c, h, w, sr, sc, idx): # 새 매트릭스에 그려주기
    global new_matrix
    temp = [row[:] for row in new_matrix]

    for i in range(sr, sr+h):
        for j in range(sc, sc+w):
            if i >= N or j >= N:
                return False

            if matrix[r+(i-sr)][c+(j-sc)] == idx: # 그릴게 있으면
                if new_matrix[i][j]: # 이미 차지했음
                    return False

                temp[i][j] = matrix[r+(i-sr)][c+(j-sc)]

    new_matrix = temp
    return True

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N, Q = map(int, input().split()) # 격자 크기, 실험 진행. 15, 50
matrix = [[0] * N for _ in range(N)]

for num in range(1, Q+1):
    x1, y1, x2, y2 = map(int, input().split()) # 좌측 하단, 우측 상단

    # 1. 미생물 투입
    for i in range(y1, y2):
        for j in range(x1, x2):
            matrix[i][j] = num

    # 2. 그룹 찾기
    # 제일 큰 애, 제일 오래된 애 순으로
    visited = [[0] * N for _ in range(N)]
    groups = [0] * (num+1) # 1번부터. 개수, 투입 번호, width, height

    for i in range(N):
        for j in range(N):
            idx = matrix[i][j]
            if idx and not visited[i][j] and groups[idx] is not None:
                if groups[idx]: # 그룹 두개로 나눠짐
                    groups[idx] = None
                else:
                    groups[idx] = find_group(i, j)

    groups = [group for group in groups if group] # 남은 애들만
    groups.sort(key=lambda x: (-x[0], x[1]))

    # 3. 배양 용기 이동
    # 빈 곳 중에 c 작, r 작
    new_matrix = [[0] * N for _ in range(N)]
    group_draw = [False] * (num+1) # 그려진 그룹

    for _, idx, w, h, r, c in groups:
        for j in range(N):
            for i in range(N):
                group_draw[idx] = draw(r, c, h, w, i, j, idx)

                if group_draw[idx]:
                    break
            if group_draw[idx]:
                break

    matrix = new_matrix

    # 4. 실험 결과
    # 인접한 무리 쌍
    if sum(group_draw) > 1: # 그려진 애가 두개 이상
        visited = [[0] * N for _ in range(N)]
        score = 0

        for i in range(N):
            for j in range(N):
                if matrix[i][j] and not visited[i][j]:
                    nearby(i, j, matrix[i][j])

        for i in range(1, len(group_draw)):
            if group_draw[i]:
                count, lst = group_draw[i]

                for ni in lst:
                    score += count * group_draw[ni][0]

        print(score)

    else:
        print(0)