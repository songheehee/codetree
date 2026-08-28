# 제초제 k 범위만큼 대각선으로 퍼짐. 벽이 있는 경우 전파되지 않음
# 1. 인접한 네칸 중 나무가 있는 칸의 수만큼 나무 성장. 동시에 성장
# 2. 벽, 다른나무, 제초제 없는 칸에 번식. 나무 // 번식 가능한 칸. 동시에 번식
# 3. 나무가 가장 많이 박멸되는 칸에 제초제, 대각선 4방향으로 k만큼 전파 until 벽 or 노나무 칸. c년까지 제초제
# 이미 제초제 있는 칸이면 다시 c년
# 박멸시키는 나무의 수가 동일하면 행, 열 작은 순서대로

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

def grow():
    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0: # 나무 있는 경우에만
                count = 0 # 주변 나무 개수

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if matrix[nr][nc] > 0:
                        count += 1

                matrix[i][j] += count

def produce():
    trees = [[0] * N for _ in range(N)] # 한번에 번식

    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0: # 나무 있으면
                count = 0 # 번식 가능한 칸 개수
                loc = [] # 번식 나무 위치 저장

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if matrix[nr][nc] == 0 and medic[nr][nc] == 0: # 제초제도 없어야함
                        count += 1
                        loc.append((nr, nc))

                if count: # 번식 가능하면
                    for r, c in loc:
                        trees[r][c] += matrix[i][j] // count

    # 번식 진행
    for i in range(N):
        for j in range(N):
            if trees[i][j]: # 조건 없어도 될거 같긴 한데
                matrix[i][j] += trees[i][j]


# 대각선
ddr = [-1, -1, 1, 1]
ddc = [-1, 1, -1, 1]

def spread():
    # 가장 많이 박멸되는 칸 찾기
    dead = [[0] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0: # 나무 있는 칸만 탐색
                dead[i][j] = matrix[i][j] # 본인 포함

                for d in range(4): # 대각선
                    for k in range(1, K+1): # k번 만큼
                        nr = i + (ddr[d] * k)
                        nc = j + (ddc[d] * k)

                        if not (0 <= nr < N and 0 <= nc < N):
                            break

                        if matrix[nr][nc] == -1 or matrix[nr][nc] == 0: # 벽이거나 나무 없음
                            break

                        dead[i][j] += matrix[nr][nc]

    # 박멸시키는 나무의 수가 동일하면 행, 열 작은 순서대로
    max_dead = 0
    max_r, max_c = 0, 0 # 개수 동일하면 행, 열 작은 순이라 0,0임

    # 제초제 줄어들기도 같이
    for i in range(N):
        for j in range(N):
            if dead[i][j] > max_dead:
                max_dead = dead[i][j]
                max_r, max_c = i, j

            if medic[i][j]: # 제초제 있으면
                medic[i][j] -= 1

    # 제초제 뿌리기. 자기 자신도
    # 만약 나무가 없는 곳에 제초제 뿌려야 한다면
    global ans
    
    if max_dead == 0:
        medic[max_r][max_c] = C
    else:
        medic[max_r][max_c] = C
        ans += matrix[max_r][max_c]
        matrix[max_r][max_c] = 0
    
        for d in range(4): # 대각선
            for k in range(1, K+1):
                nr = max_r + (ddr[d] * k)
                nc = max_c + (ddc[d] * k)
    
                if not (0 <= nr < N and 0 <= nc < N):
                    break
    
                if matrix[nr][nc] == -1 or matrix[nr][nc] == 0:  # 벽이거나 나무 없음
                    medic[nr][nc] = C
                    break
    
                medic[nr][nc] = C
                ans += matrix[nr][nc]
                matrix[nr][nc] = 0


N, M, K, C = map(int, input().split()) # 격자 크기, 년수, 제초제 확산 범위, 제초제 남아있는 년수
matrix = [list(map(int, input().split())) for _ in range(N)]
medic = [[0] * N for _ in range(N)] # 제초제 년수 저장
# -1 = 벽, 0 = 빈칸, 양수는 나무
ans = 0 # 박멸한 나무 수

for _ in range(M):
    # 1. 성장
    grow()

    # 2. 번식
    produce()

    # 3. 제초제
    spread()

print(ans) # M년 동안 박멸한 나무 그루 수
