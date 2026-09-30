'''
소요시간 : 1시간 33분 30초
수행 시간 : 145ms / 메모리 : 21MB
시도 : 3번

이해 및 구상 (13분) - 구현 및 디버깅 (50분) - 디버깅 (30분 30초)

[구상]
    - 구상은 쉬웠다. 하라는 대로 하면 될듯?
    - 물건 있는 거 유의!! matrix[i][j] 로 검사하면 안되고 0보다 큰 걸로 검사해야된다
    - 이동할 때 가장 가까운 곳 중 행작, 열작 -> 단계 bfs로 하자
    - 이동, 청소 모두 순서대로. 확산만 동시에

[구현]
    - 현재 청소기 위치에 먼지가 남아있을 수 있음 -> 그럼 움직이지 않음
    - 먼지가 없으면 청소기 위치 어떻게 찾지? -> 어차피 끝
    - 먼지 청소할 때 최대가 20. 자기 위치는 무조건 청소함
    - 청소할 때 4방 다 먼지 없을 수도 -> 그럼 청소하지 않음
    - 먼지 축적은 먼지 있는 곳만, 먼지 확산은 먼지 없는 곳만 -> 새로운 매트릭스 덮어씌워주기
    - 4방 탐색할 때 인덱스 유의! 물건 있는 곳 유의!

[실수]
    - 청소기 장애물에 가로막혀서 못 움직일 수도 있다!
    - 먼지가 없을 수도 있음...
    - 3방향 볼 때 자기 반대편만 안 보면 됨 -> 오타 났었음
'''
# 좌상단 1,1
# 1. 먼지가 있거나, 2. 먼지가 없거나, 3. 물건 있거나
# 먼지는 1~100
# 초기 청소기 위치에는 먼지 없음

# 1. 청소기 이동 (여러개) - 순서대로
# 이동 거리가 가장 가까운 먼지 있는 곳
# 물건이 있거나 청소기가 있는 격자로는 못감
# 행작, 열작

# 2. 청소 - 순서대로
# 바라보는 방향 기준, ㅗ 모양
# 청소할 수 있는 먼지량이 가장 큰 방향으로
# 격자 당 청소할 수 있는 최대 먼지량은 20
# 방향 여러개면 오,아,왼,위 우선순위

# 3. 먼지 축적
# 먼지 있는 곳 +5

# 4. 먼지 확산 - 동시에
# 깨끗한 격자에 주변 4방 합 // 10

# 오염된 곳이 없으면 어디로 가지...

from collections import deque

def spread():
    new_matrix = [row[:] for row in matrix] # 동시 확산

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 0: # 먼지 없는 곳
                dust = 0

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] > 0): # 먼지 있는 곳만
                        continue

                    dust += matrix[nr][nc]

                new_matrix[i][j] = dust // 10

    return new_matrix


def cleaning():
    for r, c in clean:
        matrix[r][c] -= min(matrix[r][c], 20) # 본인 위치 먼지 제거
        dir_dust = [0] * 4 # 방향 별 먼지. 오아왼위 순

        for d in range(4):
            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] > 0):
                continue

            dir_dust[d] = min(matrix[nr][nc], 20)

        # 주변에 먼지가 하나라도 있어야 청소
        if sum(dir_dust):
            max_dust, maxd = 0, 0 # 먼지량 가장 큰 방향

            for d in range(4):
                total = sum(dir_dust[idx] for idx in range(4) if idx != (d+2)%4) # 자기 반대편 제외 먼지 합
                
                if total > max_dust:
                    max_dust, maxd = total, d

            for d in range(4):
                if d == (maxd+2) % 4 or dir_dust[d] == 0: # 반대편 제외, 먼지 없는 곳 제외
                    continue

                nr = r + dr[d]
                nc = c + dc[d]

                matrix[nr][nc] -= min(matrix[nr][nc], 20)


def move(r, c, idx):
    visited = [[0] * N for _ in range(N)]
    q = deque([(r, c)])
    visited[r][c] = 1
    minr, minc = N, N

    while q:
        for _ in range(len(q)):
            cr, cc = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                    continue

                if matrix[nr][nc] == -1 or (nr, nc) in clean: # 물건 있거나, 청소기 있거나
                    continue

                if matrix[nr][nc]: # 먼지 있으면
                    if (minr, minc) > (nr, nc):
                        minr, minc = nr, nc
                else: # 먼지 없는 곳이면 이동 가능
                    q.append((nr, nc))
                    visited[nr][nc] = visited[cr][cc] + 1

        if minr < N: # 먼지 있는 곳 찾음
            clean[idx] = minr, minc  # 새 위치
            break


dr = [0, 1, 0, -1] # 오아왼위
dc = [1, 0, -1, 0]

front = [[0, 1, 3], # 오 -> 왼만 제외
         [0, 1, 2], # 아 -> 위 제외
         [1, 2, 3], # 왼
         [0, 2, 3]] # 위

N, K, L = map(int, input().split()) # 격자, 청소기 개수, 테스트 횟수. 30, 50, 50
matrix = [list(map(int, input().split())) for _ in range(N)] # -1 = 물건
clean = []

for _ in range(K):
    r, c = map(lambda x: int(x)-1, input().split())
    clean.append((r, c))

for _ in range(L):
    # 먼지 없으면 0 프린트 후 종료
    total = sum(val for row in matrix for val in row if val > 0)
    if total == 0:
        print(0)
        break

    # 1. 청소기 이동
    for idx, (r, c) in enumerate(clean):
        if matrix[r][c] == 0: # 지금 위치에 먼지가 없으면
            move(r, c, idx)

    # 2. 청소
    cleaning()

    # 3. 먼지 축적
    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0:
                matrix[i][j] += 5

    # 4. 먼지 확산
    matrix = spread()

    print(sum(val for row in matrix for val in row if val > 0)) # 총 먼지량 출력