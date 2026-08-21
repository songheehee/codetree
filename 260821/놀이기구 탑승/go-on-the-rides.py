## 놀이기구 순서대로 탑승. 모든 칸 비어져있음
# 학생 별로 좋아하는 학생 4명 (자기 자신 아님)
# 우선순위 높은 칸 탑승. 항상 비어있는 칸에만 탑승
# 1. 격자를 벗어나지 않는 4방향으로 인접한 칸 중 앉아있는 좋아하는 친구 수가 가장 많은 곳
# 2. 만약 1번 여러 곳이면 비어있는 칸의 수가 가장 많은 곳
# 3. 2번도 동일 -> 행 번호 가장 작은 곳
# 4. 3번도 동일 -> 열 번호 가장 작은 곳
# 각 학생마다 인접한 곳에 앉아있는 좋아하는 친구 수 합산 -> 점수
# 학생 수는 1~n*n인가

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

n = int(input()) # 3~20. 격자 크기
matrix = [[0] * n for _ in range(n)] # 격자에 1~n*n 저장
friends = [set() for _ in range(n*n+1)] # 1부터

for _ in range(n*n):
    num, *f = map(int, input().split())
    friends[num] = set(f)

    maxf = 0 # 좋아하는 친구 수
    maxe = 0 # 비어있는 칸 수
    minr, minc = n, n

    # 격자마다 돌면서 좋아하는 친구 수, 비어있는 칸 수 탐색
    for i in range(n):
        for j in range(n):
            if matrix[i][j]: # 이미 차있음
                continue

            fcount = 0
            ecount = 0

            for d in range(4):
                nr = i + dr[d]
                nc = j + dc[d]

                if not (0 <= nr < n and 0 <= nc < n):
                    continue

                if matrix[nr][nc] == 0:
                    ecount += 1
                else: # 사람 있음
                    if matrix[nr][nc] in friends[num]:
                        fcount += 1

            # 1. 격자를 벗어나지 않는 4방향으로 인접한 칸 중 앉아있는 좋아하는 친구 수가 가장 많은 곳
            # 2. 만약 1번 여러 곳이면 비어있는 칸의 수가 가장 많은 곳
            # 3. 2번도 동일 -> 행 번호 가장 작은 곳
            # 4. 3번도 동일 -> 열 번호 가장 작은 곳
            if fcount > maxf:
                maxf = fcount
                maxe = ecount
                minr, minc = i, j

            elif fcount == maxf:
                if ecount > maxe:
                    maxe = ecount
                    minr, minc = i, j

                elif ecount == maxe:
                    if i < minr:
                        minr, minc = i, j
                    elif i == minr:
                        minc = min(minc, j)

    matrix[minr][minc] = num

# 각 학생마다 좋아하는 친구 수 합산
score = [0, 1, 10, 100, 1000]
total = 0

for i in range(n):
    for j in range(n):
        num = matrix[i][j]
        fcount = 0

        for d in range(4):
            nr = i + dr[d]
            nc = j + dc[d]

            if not (0 <= nr < n and 0 <= nc < n):
                continue

            if matrix[nr][nc] in friends[num]:
                fcount += 1

        total += score[fcount]

print(total)