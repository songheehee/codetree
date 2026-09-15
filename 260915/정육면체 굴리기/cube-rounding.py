# 칸에 쓰인 수가 0이면 주사위 바닥면에 쓰여있는 수가 칸에 복사
# 칸에 쓰인 수가 0이 아니면 칸에 쓰인 수가 정육면체 바닥으로 복사. 해당 칸은 0
# 정육면체 밖으로 이동 불가

from collections import deque

dr = [0, 0, -1, 1] # 동서북남
dc = [1, -1, 0, 0]

N, M, sr, sc, K = map(int, input().split()) # 세로, 가로, 정육면체 초기 위치, 굴리기 횟수. 20, 1000
matrix = [list(map(int, input().split())) for _ in range(N)]
rolls = list(map(lambda x: int(x)-1, input().split()))
dice = [0, deque([0, 0, 0, 0]), 0] # 0=밑, 2=위

for d in rolls:
    # 바깥으로 나가면 굴리지 않음
    nr = sr + dr[d]
    nc = sc + dc[d]

    if not (0 <= nr < N and 0 <= nc < M):
        continue

    sr, sc = nr, nc  # 위치 이동

    # 주사위 돌려주기
    if d == 3: # 남
        dice[1].rotate(-1)
    elif d == 2: # 북
        dice[1].rotate(1)
    elif d == 1: # 서
        dice[0], dice[2], dice[1][0], dice[1][2] = dice[1][2], dice[1][0], dice[0], dice[2]
    else: # 동
        dice[0], dice[2], dice[1][0], dice[1][2] = dice[1][0], dice[1][2], dice[2], dice[0]

    if matrix[nr][nc]: # 칸에 숫자 있음 -> 정육면체 바닥으로. 해당 칸 0
        dice[1][0] = matrix[nr][nc]
        matrix[nr][nc] = 0

    else: # 주사위 바닥 칸에 복사
        matrix[nr][nc] = dice[1][0]

    print(dice[1][2]) # 상단 면 숫자 출력