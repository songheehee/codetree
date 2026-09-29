# P명의 플레이어
# 플레이어 한칸 이동 -> 독점 계약. 초기 땅도 독점 계약
# 독점 계약은 k 턴만큼만 유효
# 각 플레이어 방향별로 이동 우선순위. 인접 상하좌우 중 독점 없는 칸으로. 없으면 본인 땅으로
# 한칸에 여러명이면 가장 작은 번호 플레이어만 삶
# 첫번째 턴에 이동하지 못하는 경우 없음

def move():
    new_monopoly = [row[:] for row in monopoly]

    for idx in range(1, P+1):
        if player[idx] is None: # 사라진 플레이어
            continue

        r, c, cd = player[idx]
        mr, mc, md = -1, -1, -1 # 자기 땅
        matrix[r][c] = 0 # 이전 위치 삭제

        for d in fav[idx][cd]:
            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if monopoly[nr][nc] == 0: # 독점 계약 안된 땅
                if matrix[nr][nc]: # 다른 애 있으면 나보다 번호 작은 애임
                    player[idx] = None
                else:
                    player[idx] = (nr, nc, d)
                    matrix[nr][nc] = idx
                    new_monopoly[nr][nc] = (idx, K+1)
                break

            if monopoly[nr][nc][0] == idx and mr == -1: # 내 땅
                mr, mc, md = nr, nc, d

        else: # 다 돌았는데 없으면 자기 땅으로 가야함
            player[idx] = (mr, mc, md)
            matrix[mr][mc] = idx
            new_monopoly[mr][mc] = (idx, K+1)

    return new_monopoly


dr = [-1, 1, 0, 0] # 위아왼오
dc = [0, 0, -1, 1]

N, P, K = map(int, input().split()) # 격자, 플레이어, 독점 턴수. 20, 400, 1000
matrix = [list(map(int, input().split())) for _ in range(N)] # 현재 위치만 기록
monopoly = [[0] * N for _ in range(N)] # 독점 계약 (주인, 남은 턴)
player = [None] + list(map(lambda x: int(x)-1, input().split())) # 1번부터. 위치, 방향
fav = [None] + [[list(map(lambda x: int(x)-1, input().split())) for _ in range(4)] for _ in range(P)]

for i in range(N):
    for j in range(N):
        idx = matrix[i][j]
        if idx:
            monopoly[i][j] = (idx, K)
            player[idx] = (i, j, player[idx])

turn = 0
while True:
    turn += 1

    if turn >= 1000:
        turn = -1
        break

    # 1. 이동
    monopoly = move()

    # 1번만 남으면 끝
    if player.count(None) == P:
        break

    # 2. 독점 계약 -1
    for i in range(N):
        for j in range(N):
            if monopoly[i][j]:
                idx, left = monopoly[i][j]
                left -= 1

                if left:
                    monopoly[i][j] = (idx, left)
                else:
                    monopoly[i][j] = 0

print(turn) # 1번 플레이어만 남기까지 걸린 턴 수. 1000 이상이거나 불가능하면 -1