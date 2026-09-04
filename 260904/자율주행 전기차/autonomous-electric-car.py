'''
소요시간 : 1시간 30분
수행 시간 : 59ms / 메모리 : 16MB
시도 : 2번

이해 및 구상 (14분) - 구현 및 디버깅 (1시간 14분) - 수정 (2분)

[구상]
    - 최단 거리 보자마자 bfs를 떠올렸다
    - 출발지가 계속 바뀌어서 visited를 초기화해줘야 하는데 while로 하자 생각
    - 처음에 승객 태워도 배터리 충전되는줄 알았는데 예시 보고 바로 아니란 거 깨달음
    - 왜 배터리 두배가 안되지? 생각했는데 간만큼 충전되는 거라 그냥 간만큼만 플러스 해주자
    - 엣지 여러개 생각난 거 적어둠

[구현]
    - 승객들 목적지, 출발지 어떻게 관리할까 생각하다가 처음엔 리스트로 하려다가 in 검사 자주 할거 같아서 딕셔너리로
    - 승객 찾는 거랑 목적지 데려다 주는거 따로 해야겠다 -> 함수화
    - 최단 거리 같은 승객이 있을 수 있음!!! << 중간에 수정함
    - 승객들 출발지 다 다른거랑 승객 출발지, 목적지 다른 건 생각했는데 누군가의 목적지가 출발지가 될 수 있을 거란 생각을 못 했다

[실수]
    - 문제에 대놓고 목적지가 누군가의 출발지일 수 있다고 써져있었건만 2번 테케 보기 전까지 생각 못함 ㅎㅎ....
    - 엣지 여러개 생각해놓고 풀었는데도 승객이 남아있지만 태우지 못할 경우를 생각 못함...ㅠ 멍충이
'''
# 승객 목적지에 무사히 도착하면 소모한 배터리 양의 두배만큼 충전
# 배터리 다 쓰면 그 즉시 종료. 도착하고 다 소모 돼도 충전. 마지막 승객 내려준 후에도 충전
# 승객 태우러 가는 길은 마이너스, 태우고 목적지 가는 건 플러스
# 현재 위치에서 최단 거리 승객. 같을 경우 가장 위, 가장 왼
# 출발지와 목적지는 다름. 승객 출발지 다 다름
# 엣지 : 배터리 다 쓴 경우, 도착했을 때 배터리 0인 경우, 목적지가 벽으로 둘러싸인 경우, 목적지 = 다른 사람 출발지, 손님이 벽에 둘러싸인 경우

from collections import deque

def search():
    global B

    # 현재 위치가 곧 출발지면
    if (r, c) in people:
        return ride(r, c)

    visited = [[0] * N for _ in range(N)] # 거리 계산용
    q = deque([(r, c)])
    visited[r][c] = 1

    # 최단 거리 손님
    pr, pc = -1, -1
    dist = N*N

    while q:
        cr, cc = q.popleft()

        if B < visited[cr][cc] and (pr, pc) == (-1, -1): # 연료 불가. 손님 찾았는지도 확인해야됨
            return False

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if matrix[nr][nc] == 1 or visited[nr][nc]: # 벽 제외
                continue

            # 손님 있으면
            if (nr, nc) in people:
                if (pr, pc) == (-1, -1):
                    pr, pc = nr, nc
                    dist = visited[cr][cc]

                elif (dist, pr, pc) > (visited[cr][cc], nr, nc):
                    dist, pr, pc = visited[cr][cc], nr, nc
            else:
                if visited[cr][cc] > dist: # 이미 최단 찾음. dist가 -1 상태라 같을 경우에도 끝
                    break

                q.append((nr, nc))
                visited[nr][nc] = visited[cr][cc] + 1

    # 택시 태우기
    # 배터리 다 쓰면 종료. 태워도 충전되는게 아니라 목적지까지 가야돼서 0 되면 그냥 종료
    B -= dist
    if B <= 0:
        return False

    if (pr, pc) != (-1, -1): # 다 돌았는데도 손님 못 찾음
        return ride(pr, pc)

def ride(sr, sc): # 목적지 가기
    global B, r, c

    visited = [[0] * N for _ in range(N)]
    q = deque([(sr, sc)]) # 손님 위치
    visited[sr][sc] = 1
    er, ec = people[sr, sc] # 도착지

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if matrix[nr][nc] == 1 or visited[nr][nc]: # 벽 제외
                continue

            if (nr, nc) == (er, ec): # 목적지 도착
                # 연료 남아있는지
                if B - visited[cr][cc] < 0: # 0이어도 괜찮음
                    return False

                B += visited[cr][cc] # 충전
                people.pop((sr, sc), None) # 손님 삭제
                r, c = nr, nc # 자동차 위치 변경

                return True

            else: # 아직 목적지 도착 전
                q.append((nr, nc))
                visited[nr][nc] = visited[cr][cc] + 1

    return False # 다 돌았는데도 목적지 못 찾음


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N, P, B = map(int, input().split()) # 격자 크기, 승객 수, 초기 배터리
matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 도로, 1 = 벽
r, c = map(lambda x: int(x)-1, input().split()) # 자동차 현재 위치
people = dict()

for _ in range(P):
    sr, sc, er, ec = map(lambda x: int(x)-1, input().split())
    people[(sr, sc)] = (er, ec) # 출발지 다 다름
    
while people:
    possible = search()

    if not possible:
        B = -1
        break

print(B) # 남은 연료의 양. 모든 손님 이동 불가 -1