'''
소요시간 : 1시간 30초
수행 시간 : 280ms / 23MB
시도 : 3번

이해 및 구상 (9분) - 구현 및 디버깅 (40분) - 디버깅2 (11분 30초)

[구상]
    - 얘도 문제가 그냥 하라는 대로 하면 될 거 같아서 이해는 쉬웠다
    - 성장 -> 번식 -> 제초제 순으로 했당
    - 제초제가 1년마다 줄어들어야되는데 언제 줄어들어야 되는지 헷갈렸는데 문제에서 제초제 위치 선정하고 사라지길래 그대로 함

[구현]
    - 구현은 순서대로 잘 했던 거 같다. 매트릭스를 많이 만들어야돼서 이렇게 계속 만들어도 되나? 했는데 20이라 머...그냥 킵고잉함
    - 2번 할때 제초제 없는 칸에 번식 << 중요하게 봄. 제초제 까먹을 거 같아서
    - 나무 있는 칸도 꼭꼭 체크했다!
    - 전파되는 도중 벽이 있거나 나무가 아예 없는 칸이 있는 경우, 그 칸 까지는 제초제가 뿌려지며 -> 제초제는 뿌려진다길래 똑~같이 해줌
    - 제초제 년도도 더해지는게 아니라 다시 C년만!
    - 처음에 가장 많이 박멸되는 칸 찾을 때 max(max)로 했는데 이상하게 나와서 (왜지? 이유는 모르겠음) 그냥 for문 돌려줌. 항상 의심하자
    - 그리고 어차피 for문 도는 김에 그때 제초제 년수 줄어드는 것도 같이 해줌. 같이 해줘도 되는건지는 모르겠으나 일단 함...
    - 나무 성장도 동시에 한다고 했는데 어차피 다른 나무에 영향 안 가서 바로 해줌

[실수]
    - 처음에 틀려서 maxr, maxc를 -1, -1에서 0, 0으로 해줬는데 그냥 애초에 박멸할 나무가 없을 때로 했어야 했음
    - 박멸할 나무가 없어도 제초제는 뿌려야되지 않나? 라고 생각했는데 좀 더 생각할걸 ^^
    - 박멸할 나무가 없을 때를 생각하지 못함

[리팩토링]
    - 나무가 없으면 어차피 답에 영향이 안 가서 제초제 뿌리거나 말거나 그냥 끝내면 됨! 생각하지 못함...하...바보
    - 코드가 거의 비슷해서 grow, produce 따로따로 말고 한꺼번에 해줬어도 됐을듯 그럼 이중 for문 덜 돌 수 있음
'''
# 제초제 k 범위만큼 대각선으로 퍼짐. 벽이 있는 경우 전파되지 않음
# 1. 인접한 네칸 중 나무가 있는 칸의 수만큼 나무 성장. 동시에 성장
# 2. 벽, 다른나무, 제초제 없는 칸에 번식. 나무 // 번식 가능한 칸. 동시에 번식
# 3. 나무가 가장 많이 박멸되는 칸에 제초제, 대각선 4방향으로 k만큼 전파 until 벽 or 노나무 칸. c년까지 제초제
# 이미 제초제 있는 칸이면 다시 c년
# 박멸시키는 나무의 수가 동일하면 행, 열 작은 순서대로

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

def grow():
    trees = [[0] * N for _ in range(N)] # 한번에 번식

    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0: # 나무 있는 경우에만
                tree_count = 0 # 주변 나무 개수
                empty_count = 0 # 번식 가능한 칸 개수
                loc = [] # 번식 나무 위치 저장

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if matrix[nr][nc] > 0:
                        tree_count += 1

                    if matrix[nr][nc] == 0 and medic[nr][nc] == 0: # 제초제도 없어야함
                        empty_count += 1
                        loc.append((nr, nc))

                matrix[i][j] += tree_count

                if empty_count: # 번식 가능하면
                    for r, c in loc:
                        trees[r][c] += matrix[i][j] // empty_count

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
    # 1. 성장, 2. 번식
    grow()

    # 3. 제초제
    spread()

print(ans) # M년 동안 박멸한 나무 그루 수
