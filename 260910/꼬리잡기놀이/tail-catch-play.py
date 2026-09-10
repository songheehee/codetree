# 3명 이상 한팀. 이동 선 따라 이동. 끝 이어져있음, 이동 선 겹치지 않음
# 1. 머리 사람 따라서 한칸 이동
# 2. 공이 정해진 선을 따라 던져짐. 오, 위, 왼(밑부터), 아(왼부터)
# 3. 공 선에 사람 있으면 최초에 만나는 사람이 점수 얻음. 팀 내 k번째면 k**2 -> 방향 반대
# 아 그냥 1차원으로 하고 머리만 4 찾아줄걸
# 인접한 칸 두개만 존재
# 3명 이상이니까 꼬리-머리 경우 없음

def change():
    # 몇번째인지 찾고 방향 반대로. 팀 꼬리부터
    for i in range(len(team)):
        ppl = team[i]

        for j in range(len(ppl)):
            if ppl[j] == (pr, pc):
                hr, hc = ppl[-1]
                tr, tc = ppl[0]

                matrix[hr][hc], matrix[tr][tc] = matrix[tr][tc], matrix[hr][hc]
                team[i] = ppl[::-1] # 반대 방향

                return (len(ppl) - j) ** 2

def ball():
    dir = (turn // N) % 4 # 공 방향
    start = turn % N

    # 시작 지점
    if dir == 0: # 오
        sr, sc = start, 0
    elif dir == 1: # 위
        sr, sc = N-1, start
    elif dir == 2: # 왼 (아래부터)
        sr, sc = N-1-start, N-1
    else: # 아 (왼부터)
        sr, sc = 0, N-1-start

    # 시작부터 사람 있을 수 있음
    if matrix[sr][sc] in (1, 2, 3):
        return sr, sc

    while True: # 벽 만나거나 사람 만나거나
        nr = sr + dr[dir]
        nc = sc + dc[dir]

        if not (0 <= nr < N and 0 <= nc < N):
            break

        if matrix[nr][nc] in (1, 2, 3):
            return nr, nc

        sr, sc = nr, nc

    return -1, -1

def move():
    # 꼬리 빼주고 앞만 추가
    for ppl in team:
        tr, tc = ppl.pop(0)
        matrix[tr][tc] = 4

        tr, tc = ppl[0]
        matrix[tr][tc] = 3

        hr, hc = ppl[-1]
        matrix[hr][hc] = 2

        # 새로운 머리 찾으러
        for d in range(4):
            nr = hr + dr[d]
            nc = hc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] == 4):
                continue

            ppl.append((nr, nc))
            matrix[nr][nc] = 1
            break

def find(): # 팀 찾기
    visited = [[0] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 3:
                new_team = [(i, j)] # 꼬리부터
                visited[i][j] = 1
                cr, cc = i, j

                while matrix[cr][cc] != 1:
                    for d in range(4):
                        nr = cr + dr[d]
                        nc = cc + dc[d]

                        if not (0 <= nr < N and 0 <= nc < N):
                            continue

                        if visited[nr][nc] or matrix[nr][nc] == 0:
                            continue

                        if (matrix[cr][cc] == 3 and matrix[nr][nc] == 2) or (matrix[cr][cc] == 2 and matrix[nr][nc] in (1, 2)):
                            new_team.append((nr, nc))
                            visited[nr][nc] = 1
                            cr, cc = nr, nc
                            break

                team.append(new_team)


dr = [0, -1, 0, 1] # 오위왼아
dc = [1, 0, -1, 0]

N, C, R = map(int, input().split()) # 격자 크기, 팀 개수, 라운드 수. 20, 5, 1000
matrix = [list(map(int, input().split())) for _ in range(N)] # 0=빈칸, 1=머리, 2=나머지, 3=꼬리, 4=이동선
score = 0

team = [] # 몇번째인지 알아야돼서 좌표 알아야됨
find()

for turn in range(R):
    # 1. 이동
    move()

    # 2. 공 굴러가유
    pr, pc = ball()

    # 3. 점수 -> 방향 반대
    if pr != -1: # 맞은 사람 있으면
        score += change()

print(score) # 점수 총합