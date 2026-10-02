# 0 = 바다, 1 = 암초
# 헤엄칠 수 있는 모든 바다 탐험

# 1. 인접 탐험
# 상하좌우 중 방문하지 않은 바다 칸이 있다면
# - 현재 방향 직진
# - 반시계 90도 회전 후 직진
# - 시계 90도 회전 후 직진
# - 180도 회전 후 직진
# 인접한 칸에 바다 없을 때까지

# 2. 가장 가까운 바다로 이동
# 방문하지 않은 바다 중 가장 가까운 곳으로
# 바다는 지나갈 수 있음, 암초는 못감
# 여러개면 행작, 열작
# 최단 거리로 이동. 좌하우상 우선순위

# 더 이상 갈 수 없는 바다 칸이 없을 때 종료. 바다 칸 있는데 못 갈 수도, 바다 칸 다 갔을 수도

from collections import deque

def close():
    global wr, wc, wd
    
    qvisited = [[0] * N for _ in range(N)] # bfs용 visited
    q = deque([(wr, wc)])
    qvisited[wr][wc] = 1
    minr, minc, mind = N, N, 0

    while q:
        for _ in range(len(q)):
            cr, cc = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if qvisited[nr][nc] or matrix[nr][nc]: # 큐에 있음, 암초
                    continue

                if visited[nr][nc] == 0 and (minr, minc) > (nr, nc): # 방문 안한 바다
                    minr, minc, mind = nr, nc, d
                else:
                    q.append((nr, nc))
                    qvisited[nr][nc] = qvisited[cr][cc] + 1

        if minr < N:
            wr, wc, wd = minr, minc, mind
            visited[wr][wc] = 1
            ans.append((wr, wc))
            
            return True # 이동했음

    return False # 가장 가까운 바다 없음


def near(): # 현재 위치 4방 다 보기
    global wr, wc, wd

    for d in [wd, (wd+1)%4, (wd-1)%4, (wd+2)%4]: # 직진, 좌회전, 우회전, 180
        nr = wr + dr[d]
        nc = wc + dc[d]

        if not (0 <= nr < N and 0 <= nc < N):
            continue

        if matrix[nr][nc] or visited[nr][nc]: # 암초거나 방문한 바다
            continue

        visited[nr][nc] = 1
        ans.append((nr, nc))
        wr, wc, wd = nr, nc, d

        return True # 인접한 칸 이동함

    return False # 4방 다 돌았는데도 못감


dr = [0, 1, 0, -1] # 좌하우상
dc = [-1, 0, 1, 0]
dirs = {0:3, 1:1, 2:0, 3:2} # 입력값 바꿔주기

N, wr, wc, wd = map(lambda x: int(x)-1, input().split()) # 고래 위치. 50
N, wd = N+1, dirs[wd]
matrix = [list(map(int, input().split())) for _ in range(N)]

visited = [[0] * N for _ in range(N)] # 방문한 바다 표시
visited[wr][wc] = 1
ans = [(wr, wc)] # 시작 위치 포함

while True:
    # 1. 인접 탐험
    move = near()

    # 2. 가장 가까운 바다
    if not move: # 인접 탐험 못함
        move = close()

    if not move: # 갈 수 있는 바다 없음
        break

for r, c in ans:
    print(r+1, c+1) # 바다 칸의 위치 순서대로 출력. 시작 위치 포함