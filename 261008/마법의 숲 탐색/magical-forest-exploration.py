# 51분

# 좌상단 1,1
# 북쪽을 통해서만 숲에 들어옴
# F명의 정령들 골렘 타고 탐색. 골렘은 십자 모양
# 중앙 제외 4칸 중 한칸은 출구. 어디든 탑승할 수 있지만 출구는 한칸으로만
# 북쪽 바깥에서 c열에서 시작. 초기 출구 주어짐
# 1. 남쪽으로 한칸
# 2. 남쪽으로 못 내려가면 왼 -> 아
# 3. 그래도 못 가면 오 -> 아. 둘 다 가야됨
# 4. 가장 남쪽에 도착하면 정령 이동
# 골렘 안에서 상하좌우. 출구가 다른 골렘과 인접하면 다른 골렘으로 이동
# 갈 수 있는 가장 남쪽으로 가기 (+1 해주기)
# 최종 행 번호의 합
# 최대한 남쪽으로 갔지만 숲을 벗어난 상태라면 다 지우고 새롭게 시작 (답 포함 안함)
# 골렘 팔 처음부터 밖인 경우는 없겠지...

from collections import deque

def fairy(r, c):
    visited = [[0] * C for _ in range(R)]
    q = deque([(r, c)])
    visited[r][c] = 1
    maxr = r # 최소 여기서 시작

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]
            num = matrix[cr][cc]

            if not (3 <= nr < R and 0 <= nc < C):
                continue

            if matrix[nr][nc] == 0 or visited[nr][nc]: # 빈곳
                continue

            if num < 0 or abs(matrix[nr][nc]) == num: # 같은 숫자거나 출구
                q.append((nr, nc))
                visited[nr][nc] = 1
                maxr = max(maxr, nr)

                if maxr == R-1: # 끝까지 도착
                    return maxr-2

    return maxr-2


def down(r, c):
    # 중앙 한칸 내려가기
    sr = r+1

    for d in range(1, 4): # 오아왼만
        nr = sr + dr[d]
        nc = c + dc[d]

        if not (0 <= nr < R and 0 <= nc < C and matrix[nr][nc] == 0): # 격자 밖 나갈 수 있나?
            return False, r, c # 원래 위치

    return True, sr, c


def side(r, c, sc):
    for d in range(4):
        nr = r + dr[d]
        nc = sc + dc[d]

        if not (0 <= nr < R and 0 <= nc < C and matrix[nr][nc] == 0): # 격자 밖 나갈 수 있나?
            return False, r, c # 원래 위치

    res, fr, fc = down(r, sc) # 내려가는 거까지 확인
    if res: # 내려가는 거 성공
        return True, fr, fc

    return False, r, c


dr = [-1, 0, 1, 0] # 위오아왼
dc = [0, 1, 0, -1]

R, C, F = map(int, input().split()) # 숲, 정령 수. 70, 70, 1000
R += 3
matrix = [[0] * C for _ in range(R)] # 0, 1은 밖
total = 0 # 행 총합

for num in range(1, F+1):
    c, d = map(int, input().split())
    c -= 1
    r = 1

    # 1. 내려갈 수 있을 때까지 내려가기
    while True:
        move, r, c = down(r, c)

        if not move: # 아래로 못 내려감 -> 왼쪽
            move, r, c = side(r, c, c-1)

            if move: # 왼쪽으로 회전
                d = (d-1) % 4
        if not move: # 왼쪽 못 갔음 -> 오른쪽
            move, r, c = side(r, c, c+1)

            if move: # 오른쪽 회전
                d = (d+1) % 4

        if r == R-2 or not move: # 끝까지 왔거나 더 이상 못 움직임
            break

    # 격자 밖이면 새 격자
    if r <= 3:
        matrix = [[0] * C for _ in range(R)]
        continue

    # 최종 위치 그려주기
    matrix[r][c] = num

    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]

        matrix[nr][nc] = num if i != d else -num # 탈출구 마이너스 표시

    # 2. 정령 이동
    if r == R-2: # 끝에 도착
        total += R-3
    else:
        total += fairy(r, c)

print(total)