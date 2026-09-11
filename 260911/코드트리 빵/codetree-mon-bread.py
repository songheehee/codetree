# 자기 번호 때 출발 -> 편의점 이동. 목표 편의점 다 다름
# 1. 격자에 있는 경우, 편의점 방향을 향해 1칸 이동. 최단 거리로 이동. 위왼오아 우선
# 2. 격자에 있는 경우, 편의점에 도착하면 멈춤. 다른 사람들 못 지나감. 해당 시간에 모두 이동한 뒤에
# 3. T <= M 만족한다면 편의점과 가장 가까운 베이스캠프 들어감. 최단거리 같은 경우에는 행작, 열작
# 3-1. 베이스캠프 갈 때는 시간 소요되지 않음. 갔던 베이스캠프 칸 평생 못 지나감. 모두 이동한 뒤에
# 편의점에 도달 못하게 되는 경우는 없음
# 이동 중에 동일 칸 여러명 가능
# 편의점 위치 겹치지 않음. 편의점, 베이스캠프 위치 겹치지 않음
# 가야할 편의점이 정해져 있는데 최단거리 우선순위가 먼 소리지
# 원래는 갈 수 있었는데 중간에 베캠이나 편의점 땜에 못 갈 수도 있나?
# 계속 bfs 돌리는게 맞나??

from collections import deque

def bfs(r, c, i):
    visited = [[0] * N for _ in range(N)]
    q = deque() # 첫번째로 디딘 칸 가지고 다니기
    visited[r][c] = 1

    for d in range(4):
        nr = r + dr[d]
        nc = c + dc[d]

        if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] >= 0):
            continue

        if (nr, nc) == store[i]:  # 자기 편의점 도착
            return nr, nc

        visited[nr][nc] = 1
        q.append((nr, nc, (nr, nc)))

    while q:
        cr, cc, first = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or matrix[nr][nc] < 0:  # 못 가는 길
                continue

            if (nr, nc) == store[i]:  # 자기 편의점 도착
                return first

            visited[nr][nc] = 1
            q.append((nr, nc, first))


def move():
    new_matrix = [row[:] for row in matrix] # 다 이동한 뒤에 갈아끼기

    for i in range(1, min(turn, P+1)): # 직전 사람까지만 이동
        if not player[i]:
            continue

        pr, pc = bfs(*player[i], i) # 플레이어 새 위치. 받을 때 튜플로 받아야됨

        if (pr, pc) == store[i]:  # 자기 편의점 도착
            new_matrix[pr][pc] = -2
            player[i] = 0
        else: # 다음 위치로 이동
            player[i] = pr, pc

    return new_matrix


def find_store(r, c):
    visited = [[0] * N for _ in range(N)]
    q = deque([(r, c)]) # 갔던 방향 저장
    visited[r][c] = 1
    minr, minc = N, N

    while q:
        for _ in range(len(q)):
            cr, cc = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if visited[nr][nc] or matrix[nr][nc] < 0: # 못 가는 길
                    continue

                if matrix[nr][nc] == 1: # 베이스캠프
                    if (minr, minc) > (nr, nc):
                        minr, minc = nr, nc

                    continue

                q.append((nr, nc))
                visited[nr][nc] = 1

        if minr < N:
            return minr, minc


dr = [-1, 0, 0, 1] # 위왼오아
dc = [0, -1, 1, 0]

N, P = map(int, input().split()) # 15, 30
matrix = [list(map(int, input().split())) for _ in range(N)]
# 0 = 빈칸, 1 = 베이스캠프, 2 = 편의점, -1 = 이용한 베캠, -2 = 도착한 편의점
player = [0] * (P+1)
store = [0] + [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(P)] # 편의점이랑 플레이어 번호 매핑

turn = 0

while True:
    turn += 1

    # 1. 해당 턴 전 플레이어들 한칸 이동
    matrix = move()

    # 2. 본인 편의점에서 가장 가까운 베캠 찾기 -> 이동
    if turn <= P:
        br, bc = find_store(*store[turn])
        player[turn] = br, bc
        matrix[br][bc] = -1  # 모두 이용한 뒤에 이용 처리

    if player.count(0) == P+1:
        break

print(turn) # 모든 사람이 편의점에 도착하는 시간