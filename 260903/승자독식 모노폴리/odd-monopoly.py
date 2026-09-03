# 1. 플레이어들 한칸씩 이동. 해당 칸 독점 계약. 그 전칸도
# 2. 독점 계약은 k 턴 만큼만 유효
# 3. 방향별로 이동 우선 순위. 인접한 상하좌우 4칸 중 빈칸 -> 없으면 본인 땅으로 이동. 직전 이동한 방향
# 4. 한칸에 여러명이 있으면 가장 작은 번호만 살아남음
# 0부터 하고 싶었으나 1번이 0이 돼서 안됨
# 죽은 걸 어떻게 표현할까 매트릭스 순회하기 싫은데 현재 방향 -1 처리할까. player 만들었으니까 0 처리하자
# 1000번 다시 for문 돌리는게 나을까 monopoly도 새롭게 생성해주는게 나을까
# 먼저 턴 빼주는거 안됨
# 매트릭스 조건도 넣어줘야되나 고민했는데 어차피 독점계약 될듯
# out of range인 경우에는 어떻게 하지?

def in_range(r, c):
    return 0 <= r < N and 0 <= c < N

def move():
    global matrix
    new_matrix = [[0] * N for _ in range(N)] # 위치 저장. 한번에 이동해야함

    for i in range(1, P+1): # 1번부터
        if not player[i]: # 이미 죽은 애
            continue

        r, c = player[i]

        # 현재 방향 기준으로 우선순위
        # 우선순위 중 독점계약 맺지 않은 칸 -> 없으면 자기 땅
        mr, mc, md = -1, -1, -1
        
        for d in fav[i][curd[i]]:
            nr = r + dr[d]
            nc = c + dc[d]

            if not in_range(nr, nc):
                continue

            # 빈칸이고 독점계약 없으면 이동
            if monopoly[nr][nc] == 0:
                if new_matrix[nr][nc]:  # 사람 있으면 무조건 나보다 앞 번호
                    player[i] = 0  # 죽음
                else:
                    new_matrix[nr][nc] = i
                    player[i] = (nr, nc)
                    curd[i] = d  # 방향 바꿔주기
                break

            elif (mr, mc) == (-1, -1) and monopoly[nr][nc][0] == i:
                mr, mc, md = nr, nc, d

        else: # 다 돌았는데도 못 찾음 -> 자기 땅으로
            new_matrix[mr][mc] = i
            player[i] = (mr, mc)
            curd[i] = md  # 방향 바꿔주기

    matrix = new_matrix

def minus_turn():
    # 턴 빼주기
    for i in range(N):
        for j in range(N):
            if monopoly[i][j] == 0:
                continue

            p, y = monopoly[i][j]
            y -= 1

            if y == 0:
                monopoly[i][j] = 0
            else:
                monopoly[i][j] = (p, y)

def monopolize(): # 독점계약
    for i in range(1, P + 1):
        if not player[i]:
            continue

        r, c = player[i]
        monopoly[r][c] = (i, K)


dr = [-1, 1, 0, 0] # 위아왼오
dc = [0, 0, -1, 1]

N, P, K = map(int, input().split()) # 격자 크기, 플레이어 수, 턴 수. 20, 400, 1000
matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 빈칸, P = 플레이어 번호
curd = [-1] + list(map(lambda x: int(x)-1, input().split())) # 플레이어들 현재 방향
fav = [-1] + [[list(map(lambda x: int(x)-1, input().split())) for _ in range(4)] for _ in range(P)] # 플레이어들 방향에 따른 이동 우선순위. 위아왼오

monopoly = [[0] * N for _ in range(N)] # 독점계약 누구건지, 남은 턴 수
player = [0] * (P+1) # 플레이어 현재 위치. 1번부터
turn = 0

for i in range(N):
    for j in range(N):
        if matrix[i][j]:
            p = matrix[i][j]
            monopoly[i][j] = (p, K) # 해당 땅 독점
            player[p] = (i, j)

while True:
    turn += 1

    if turn >= 1000:
        turn = -1
        break

    # 1. 방향 정하기 -> 이동
    move()

    # 1번만 남을 때까지. 첫번째 턴에서 무조건 이동
    if player.count(0) == P:
        break

    # 2. 턴 빼주기
    minus_turn()

    # 3. 독점계약. 빼준 뒤에 K 해야함
    monopolize()

print(turn) # 1번 플레이어만 살아남기까지 걸린 턴의 수