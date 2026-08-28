# 주사위는 0,0에서 시작 -> 오른쪽
# 주사위가 놓인 칸에 적혀있는 숫자와 상하좌우로 인접하며 같은 숫자가 적힌 모든 칸의 합만큼 점수
# 주사위의 아랫면이 보드의 해당 칸에 있는 숫자보다 크면 90도 시계방향 회전
# 아랫면이 더 작으면 90도 반시계
# 같으면 계속 같은 방향
# 격자판 벗어나게 되면 방향 반대 + 한칸

from collections import deque

def rotate_dice(idx):
    if idx == 0: # 오
        dice[0], dice[1][0], dice[2], dice[1][2] = dice[1][2], dice[0], dice[1][0], dice[2]
    elif idx == 1: # 아
        dice[1].rotate(1)
    elif idx == 2: # 왼
        dice[0], dice[1][0], dice[2], dice[1][2] = dice[1][0], dice[2], dice[1][2], dice[0]
    else: # 위
        dice[1].rotate(-1)

def calc(num): # 점수 계산
    # 같은 숫자 몇개인지
    count = 1 # 본인 포함
    visited = [[0] * N for _ in range(N)]
    q = deque([(sr, sc)])
    visited[sr][sc] = 1

    while q:
        cr, cc = q.popleft()

        for i in range(4):
            nr = cr + dr[i]
            nc = cc + dc[i]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if not visited[nr][nc] and matrix[nr][nc] == num:
                count += 1
                q.append((nr, nc))
                visited[nr][nc] = 1

    return count

dr = [0, 1, 0, -1] # 오아왼위
dc = [1, 0, -1, 0]

N, M = map(int, input().split()) # 격자 크기, M번 진행 (1000)
matrix = [list(map(int, input().split())) for _ in range(N)]
dice = [4, deque([1, 2, 6, 5]), 3] # deque 0번이 윗면, 2번 아랫면
didx = 0 # 처음 오른쪽 시작
sr, sc = 0, 0 # 주사위 시작 위치
score = 0

for _ in range(M):
    # 1. 이동
    # 주사위 위치 이동해주고 주사위 돌려주기
    nr = sr + dr[didx]
    nc = sc + dc[didx]

    # 격자판 벗어나면 반사+1
    if not (0 <= nr < N and 0 <= nc < N):
        didx = (didx+2) % 4
        nr = sr + dr[didx]
        nc = sc + dc[didx]

    sr, sc = nr, nc
    rotate_dice(didx)

    # 2. 점수
    num = matrix[sr][sc] # 바닥 숫자
    score += num * calc(num) # 최소 1개

    # 3. 회전
    if dice[1][2] > num: # 90도 시계방향
        didx = (didx + 1) % 4
    elif dice[1][2] < num: # 반시계
        didx = (didx - 1) % 4

print(score) # 주사위 M번 굴렸을 때 얻게 되는 점수 총합