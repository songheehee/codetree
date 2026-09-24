# 3명 이상 한팀
# 이동 선을 따라서만 이동. 끝 이어져있음. 겹치지 않음
# 이동선 반드시 2개의 인접한 칸만 존재
# 하나의 이동선에는 하나의 팀

# 1. 머리사람 따라 한칸 이동
# 2. 라운드마다 공 던져짐. 오 -> 위 -> 왼 (밑에서) -> 아 (왼쪽에서)
# 3. 공 던져지는 선에 사람 있으면 점수 얻게 됨. 머리사람부터 K번째면 k 제곱만큼 점수. 머리사람 = 1번
#   공 맞으면 방향 전환

from collections import deque

def change():
    # 맞은 애 찾고 몇번째인지 찾아서 점수 더해주기, 방향 바꿔주기
    for team in teams:
        if (pr, pc) in team:
            team.reverse()
            order = team.index((pr, pc)) + 1

            return order ** 2


def ball():
    bd = (turn // N) % 4 # 오위왼아
    start = turn % N # 시작 지점

    if bd == 0: # 오
        br, bc = start, -1
    elif bd == 1: # 위
        br, bc = N, start
    elif bd == 2: # 왼
        br, bc = N-1-start, N
    else: # 아
        br, bc = -1, N-1-start

    while True:
        nr = br + dr[bd]
        nc = bc + dc[bd]

        if not (0 <= nr < N and 0 <= nc < N): # 벽까지 가면 끝
            return -1, -1 # 아무도 안 맞음

        if matrix[nr][nc] in (1, 2, 3): # 사람 맞으면
            return nr, nc

        br, bc = nr, nc


def move():
    for team in teams: # 0이 꼬리. 끝이 머리
        tr, tc = team.pop(0)
        matrix[tr][tc] = 4

        tr, tc = team[0] # 새로운 꼬리
        matrix[tr][tc] = 3

        hr, hc = team[-1] # 머리
        matrix[hr][hc] = 2

        # 새로운 머리 찾기
        for d in range(4):
            nr = hr + dr[d]
            nc = hc + dc[d]

            if 0 <= nr < N and 0 <= nc < N and matrix[nr][nc] == 4:
                team.append((nr, nc))
                matrix[nr][nc] = 1


def find_team():
    visited = [[0] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 3:
                q = deque([(i, j)])
                visited[i][j] = 1
                team = [(i, j)]

                while q:
                    cr, cc = q.popleft()

                    if matrix[cr][cc] == 1: # 머리 사람
                        teams.append(team)
                        break

                    for d in range(4):
                        nr = cr + dr[d]
                        nc = cc + dc[d]

                        if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                            continue

                        if matrix[nr][nc] == 2 or (matrix[cr][cc] == 2 and matrix[nr][nc] == 1): # 앞사람 찾음
                            q.append((nr, nc))
                            visited[nr][nc] = 1
                            team.append((nr, nc))
                            break


dr = [0, -1, 0, 1] # 오위왼아
dc = [1, 0, -1, 0]

N, T, R = map(int, input().split()) # 격자 크기, 팀 개수, 라운드 수. 20, 5, 1000
matrix = [list(map(int, input().split())) for _ in range(N)]
# 0 = 빈칸, 1 = 머리사람, 2 = 나머지, 3 = 꼬리사람, 4 = 이동선
teams = [] # 꼬리가 0. 머리가 맨 끝
score = 0

# 팀 구하기
find_team()

for turn in range(R):
    # 1. 한칸 이동
    move()

    # 2. 볼 던짐
    pr, pc = ball()

    # 3. 맞으면 점수, 방향 전환
    if pr != -1:
        score += change()

print(score) # 각 팀이 획득한 점수의 총합