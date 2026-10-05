# 1번 사람 1분에 2번 사람에 2분에 출발...출발 전에는 모두 격자 밖에 있음
# 베이스캠프에서 편의점으로. 각자 목표로 하는 편의점 다 다름
# 1. 편의점 방향을 향해 1칸. 최단거리로 가는데 방법 여러가지면 위왼오아 우선순위
# 2. 편의점에 도착하면 멈추고 해당 편의점 못 지나감. 모두 지나간 뒤에!
# 3. t <= m 을 만족한다면 t번 사람은 편의점과 가장 가까운 베이스캠프에 들어감. 최단거리 가장 짧은
# 가까운 베캠이 여러개면 행작, 열작. 베캠 들어가면 앞으로 절대 지나갈 수 없음. 모두 지나간 뒤에
# 편의점 위치 겹치지 않음. 편의점 != 베캠 위치
# 한칸에 둘 이상 있을 수 있음

from collections import deque

def find(r, c):
    visited = [[0] * N for _ in range(N)]
    q = deque([(r, c)])
    visited[r][c] = 1
    minr, minc = N, N # 베캠 행작 열작

    while q:
        for _ in range(len(q)):
            cr, cc = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if visited[nr][nc] or matrix[nr][nc] < 0: # 못 가는 베캠, 편의점
                    continue

                if matrix[nr][nc] == 1: # 베이스캠프 도착
                    if (minr, minc) > (nr, nc):
                        minr, minc = nr, nc
                else:
                    q.append((nr, nc))
                    visited[nr][nc] = visited[cr][cc] + 1

        if minr < N: # 베캠 찾음
            player[time] = (minr, minc) # 베캠으로 이동
            matrix[minr][minc] = -1 # 앞으로 못 지나감
            return




def move():
    new_matrix = [row[:] for row in matrix]

    for p in range(1, min(time, S+1)):
        if player[p] is None: # 이미 도착한 사람
            continue

        r, c = player[p]
        er, ec = store[p] # 목표 편의점
        nextp = None # 한 칸 이동한 다음 위치

        visited = [[0] * N for _ in range(N)]
        q = deque([(r, c, None)])
        visited[r][c] = 1

        while q:
            cr, cc, first = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if visited[nr][nc] or matrix[nr][nc] < 0: # 못 가는 베캠, 편의점
                    continue

                if nr == er and nc == ec: # 편의점 도착
                    nextp = first if first else (nr, nc)
                    break
                else:
                    q.append((nr, nc, first if first else (nr, nc)))
                    visited[nr][nc] = visited[cr][cc] + 1

            if nextp: # 이미 최단 찾음
                nr, nc = nextp

                if nr == er and nc == ec: # 편의점 도착
                    player[p] = store[p] = None
                    new_matrix[er][ec] = -1  # 못 지나가게 표시
                else:
                    player[p] = (nr, nc) # 한칸 이동

                break

    return new_matrix


dr = [-1, 0, 0, 1] # 위왼오아
dc = [0, -1, 1, 0]

N, S = map(int, input().split()) # 격자, 편의점. 15, 30
matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 빈 공간, 1 = 베캠. 못 지나가면 -1
store = [None] # 1번부터. 편의점 위치. 도착하면 None 처리
player = [None] * (S+1) # 사람들 위치. 도착하면 None 처리

for _ in range(S):
    x, y = map(lambda x: int(x)-1, input().split())
    store.append((x, y))

time = 0
while True:
    time += 1

    # 1. 편의점 최단거리로 한칸 이동
    matrix = move()

    # 다 도착하면 끝
    if store[1:].count(None) == S:
        break

    # 2. 가장 가까운 베캠 찾기
    if time <= S:
        find(*store[time])

print(time) # 모든 사람이 편의점에 도착하는 시간. 못 가는 경우는 절대 없음