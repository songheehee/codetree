# 좌상단 1,1
# 동,서,남 벽으로 막혀있음. 북으로만 숲에 들어올 수 있음
# K명 정령 십자 모양 골렘 타고 숲 탐색. 5칸 차지. 골렘에서 내릴 때는 끄트머리 네칸 중 하나로만 가능
# i번째로 숲을 탐색하는 골렘은 골렘의 중앙이 c열이 되도록 하는 위치에서 내려옴. 초기 골렘 출구 d

# 더 이상 움직이지 못할 때까지 반복. 숲 바깥도 동일
# 1. 아래로 한칸 (밑이 비어있을 때만)
# 2. 아래 불가능하면 서쪽으로 회전하면서 내려감. 서쪽으로 갔다가 내려감. 출구는 반시계 회전
# 3. 불가능하면 동쪽으로 회전하면서 내려감. 오 -> 시계 회전 -> 아래
# 4. 가장 남쪽에 도달해서 이동할 수 없으면 정령은 골렘 안에서 상하좌우 이동 가능
#    출구가 다른 골렘과 인접하다면 다른 골렘으로 이동도 가능
#    갈 수 있는 모든 칸 중 가장 남쪽으로 가고 이동 종료 -> 최종 위치
# 최종 위치 행 번호의 합 (1부터 시작이라 +1 해줘야함!!!)
# 골렘의 몸 일부가 숲을 벗어난 상태면 숲 리셋. 다음 골렘부터 다시 시작
# 벗어난 애 포함 안 시키고 새로 시작한 애는 누적 맞겠지?
# 출구 -> 출구 갈 수 있나? -> 정령 어떤 방향에서든 탈 수 있음

from collections import deque

def down(r, c):
    nr = r+1 # 중심

    for i in range(1, 4): # 골렘 하좌우
        gr = nr + dr[i]
        gc = c + dc[i]

        if gr < 0: # 아직 숲 밖에 있는 애
            continue

        if not (0 <= gc < C) or matrix[gr][gc]: # 왼, 오로는 나가면 안됨 or 다른 골렘 있음
            return False, r, c

    return True, nr, c # 골렘 안 마주침


def side(nc, nd): # 왼쪽 이동, 반시계
    for i in range(4):  # 골렘
        gr = r + dr[i]
        gc = nc + dc[i]

        if gr < 0: # 위에 있는 골렘 패스
            continue

        if not (0 <= gc < C) or matrix[gr][gc]: # 이동 불가
            return False, r, c, d

    # 왼쪽 갔으면 아래도
    possible, nr, nc = down(r, nc)

    if not possible: # 아래로 못가
        return False, r, c, d

    # 아래로 이동 성공
    return True, nr, nc, nd


def draw(): # 맵에 표시
    matrix[r][c] = num # 가운데

    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]

        matrix[nr][nc] = num if i != d else -num # 끄트머리, 출구


def move(): # 정령 이동
    visited = [[0] * C for _ in range(R)]
    q = deque([(r, c, matrix[r][c])]) # 골렘 번호
    visited[r][c] = 1
    maxr = r

    while q:
        cr, cc, num = q.popleft()

        if maxr == R-1: # 마지막 행이면 검사할 필요 없음
            return maxr + 1

        for i in range(4):
            nr = cr + dr[i]
            nc = cc + dc[i]

            if not (0 <= nr < R and 0 <= nc < C):
                continue

            if visited[nr][nc] or not matrix[nr][nc]:
                continue

            if (num > 0 and abs(matrix[nr][nc]) == num) or num < 0: # 같은 골렘 내 or 출구
                q.append((nr, nc, matrix[nr][nc]))
                visited[nr][nc] = 1
                maxr = max(maxr, nr)

    return maxr + 1

dr = [-1, 0, 1, 0] # 북동남서. 위오아왼
dc = [0, 1, 0, -1]

R, C, K = map(int, input().split()) # 숲 크기, 정령 수. 70, 1000
matrix = [[0] * C for _ in range(R)] # 골렘 표시, 출구도 표시 (마이너스)
total = 0

for num in range(1, K+1):
    c, d = map(int, input().split()) # 골렘 열, 출구 방향
    r, c = -2, c-1

    # 1. 골렘 내려온다 -> 최종 위치 저장, 맵에 반영
    while True:
        possible, r, c = down(r, c)

        # 못 가면 왼쪽
        if not possible:
            possible, r, c, d = side(c-1, (d-1+4) % 4)

        # 왼쪽 이동 불가 -> 오른쪽
        if not possible:
            possible, r, c, d = side(c+1, (d+1) % 4)

        # 그래도 못 가거나 바닥까지 갔으면 끝
        if not possible or r == R-2:
            break

    # 만약 내려왔는데도 격자 밖이다 -> 새 맵. 다시 시작
    if r <= 0:
        matrix = [[0] * C for _ in range(R)]
        continue

    # 맵에 반영
    draw()

    # 2. 정령 이동. 가장 밑으로
    total += move()

print(total) # 행의 총합. 1부터