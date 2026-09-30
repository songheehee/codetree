# 배터리 양 다 소진되면 움직일 수 없음
# 벽은 못 지나감
# 승객 태우러 갈 때, 목적지 이동할 때 모두 최단 거리로 이동
# 한칸 이동 시 배터리 1 소요
# 목적지 도착하면 이동한 배터리 양 두배 충전
# 이동하는 중에 배터리 다 소모되면 즉시 종료. 목적지 도착했으면 충전 가능
# 마지막 승객 종료 시에도 충전 이뤄짐
# 현재 위치에서 최단 거리 가장 짧은 승객 먼저 태움
# 여러명일 경우 행작, 열작
# 모든 손님 데려다 줄 수 있으면 남은 배터리 양, 없다면 -1 출력

# 출발지, 목적지는 도로 빈칸
# 각 승객의 출발지 != 목적지. 무조건 이동
# 다른 승객의 출발지와 다른 승객의 목적지는 같을 수 있음
# 출발지는 모두 다름
# 승객을 못 찾을 수도, 목적지 못 갈 수도

from collections import deque

def move(er, ec): # 목적지로 이동
    visited = [[0] * N for _ in range(N)]
    q = deque([(carr, carc)])
    visited[carr][carc] = 1

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or matrix[nr][nc]:  # 벽 못감
                continue

            if nr == er and nc == ec:  # 도착
                return visited[cr][cc]

            q.append((nr, nc))
            visited[nr][nc] = visited[cr][cc] + 1

    return False


def find():
    if (carr, carc) in rider: # 현재 위치에 승객 있음
        return carr, carc, 0

    visited = [[-1] * N for _ in range(N)]
    q = deque([(carr, carc)])
    visited[carr][carc] = 0
    minr, minc = N, N # 승객. 행작 열작

    while q:
        for _ in range(len(q)):
            cr, cc = q.popleft()

            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if visited[nr][nc] != -1 or matrix[nr][nc]: # 벽 못감
                    continue

                if (nr, nc) in rider: # 승객 찾음
                    if (minr, minc) > (nr, nc):
                        minr, minc = nr, nc

                q.append((nr, nc))
                visited[nr][nc] = visited[cr][cc] + 1
                    
        if minr < N: # 승객 찾음
            return minr, minc, visited[minr][minc] # 걸린 배터리 양
            
    # 승객 못 찾음
    return -1, -1, -1


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N, P, B = map(int, input().split()) # 격자, 승객 수, 초기 배터리. 20, 400, 500,000
matrix = [list(map(int, input().split())) for _ in range(N)] # 도로 정보. 1 = 벽
carr, carc = map(lambda x: int(x)-1, input().split()) # 자동차 위치
rider = dict() # 출발지 : 도착지

for _ in range(P):
    sr, sc, er, ec = map(lambda x: int(x)-1, input().split())
    rider[(sr, sc)] = (er, ec)

while rider:
    # 1. 제일 가까운 승객 찾기. 현재 위치일 수 있음. 행작, 열작
    carr, carc, rb = find()
    B -= rb

    if carr == -1 or B < 0: # 승객 못 태우거나 배터리 부족
        B = -1
        break

    # 2. 목적지 최단 거리로. 연료 소진 -> 충전
    er, ec = rider.pop((carr, carc), None)
    rb = move(er, ec) # 필요한 배터리

    if not rb or B - rb < 0: # 못 감
        B = -1
        break

    # 충전, 이동
    B += rb
    carr, carc = er, ec

print(B) # 데려다 줄 수 있으면 남은 연료 양, 불가능하면 -1