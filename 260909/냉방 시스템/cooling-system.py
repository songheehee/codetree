'''
소요시간 : 3시간 17분
수행 시간 : 380ms / 메모리 : 24MB
시도 : 2번

이해 및 구상 (45분) - 구현 및 디버깅 (1시간 22분) - 디버깅 (1시간 10분)

[구상]
    - 역대급으로 구상이 오래 걸린 문제였다...아니 시원함 어케 퍼지게 하냐고. 벽은 왜 있냐고.
    - 처음에는 저번에 푼 청소기 문제가 기억나서 다 좌표로 만든 다음에 하려고 했는데 그러면 벽 조건 하는 게 너무 빡셀 거 같았다
    - 근데 또 보다 보니까 뭔가 bfs 같이 생긴거임. 그래서 어머나 세상에 바로 bfs

[구현]
    - 사무실 위치를 따로 할까 말까 했는데 그냥 했다. 종료 조건 매번 검사해야되는데 이중 for문 오래 걸릴 거 같아서
    - 처음에 벽을 딕셔너리 안에 리스트로 해줬는데 in 검사 해야되니까 set으로 바꿔줌. 근데 어차피 두개라 리스트로 했어도 상관 없었을듯
    - 벽 조건이 까다로워서 그것도 그냥 배열에 넣고 이동할 때마다 계산해줬음. 하 먼가 더러운 거 같지만...다른 방법이 떠오르지 않았음
    - 저번에 bfs 단계 별로 도는 게 기억나서 그렇게 해봤당. 근데 for문 보다 while pop이 더 시간이 적게 걸린다 머지???
    - 그리고 난 또 while문 종료 조건을 어디에다 써야되나 백번 고민했다
    - 동시에 시원함 퍼지는거 어떻게 할까 고민하다가 저번에 지호님 코드 보고 일단 다 해주고 // 2 하는 걸로 했다
    - 그냥 원래꺼 복사해서 할까 하다가 어차피 0 미만인거 계산해줘야되니까. 근데 그냥 무조건 나보다 작은 애랑만 하면 안되나?

[실수]
    - 계속 공기가 마이너스 안 되게 신경 써야됐는데 하 중간에 놓쳤음
    - bfs로 하고 테케는 작다 보니까 신경을 못 썼는데 이게 계속 전파돼서 마이너스가;;; 되는 경우도 있었음. 바보냐?
    - 처음 에어컨도 대각선, 앞, 대각선 계산해서 바꿔줌. 그리고 이게 에어컨 바로 앞에 벽이 있으면 어떡하지? 했는데 문제에 그런 경우 없다고 써있었음;; -> 그래서 조건 줬다가 뺌. 문제를 잘 읽자!
    - 벽 검사에서 진짜 오백번 틀렸다...오아는 -2 해줘야 된다!!!
    - 처음에 cr, cc로 하다가 움직여야 되니까 새로운 변수로 만들어놓고 왜 wall 검사는 cr, cc로 하냐고.
'''
# 0 = 빈칸, 1 = 사무실, 2 = 에어컨 (왼), 3 = 에어컨 (위), 4 = 에어컨 (오), 5 = 에어컨 (아래)
# 1. 공기 시원하게 함 but 벽 있으면 ㄴㄴ. 위 45도는 위->오, 아래 45도는 아래->오. 에어컨 있는 곳도 전파 가능
# 2. 시원한 공기들 섞임. 인접한 칸 차이 // 4. 벽 사이에 두고는 일어나지 않음
# 3. 바깥쪽 칸 -1. 0이면 0
# 모든 사무실이 k 이상일 때까지
# 벽 != 외벽, 에어컨 바로 앞에 노 벽 & 격자 안 나감, 사무실이랑 에어컨 최소 하나씩
# 모든 칸에 대해서 대각선 위, 앞, 대각선 아래
from collections import deque

def blow():
    for (r, c), d in air.items():
        visited = [[0] * N for _ in range(N)]
        q = deque([(r, c)])
        visited[r][c] = 6

        while q:
            nq = deque([])

            while q:
                cr, cc = q.popleft()

                if visited[cr][cc] == 1:
                    break

                if visited[cr][cc] == 6: # 맨 처음은 앞만 검사
                    nr = cr + dr[d]
                    nc = cc + dc[d]

                    # 에어컨 바로 옆/앞 벽 없음
                    visited[nr][nc] = visited[cr][cc] - 1
                    cold[nr][nc] += visited[nr][nc]
                    nq.append((nr, nc))
                    break

                for lst in wind[d]:
                    # 벽 검사 후 둘 다 이동
                    ccr, ccc = cr, cc
                    for ndr, ndc, nw in lst:
                        nr = ccr + ndr
                        nc = ccc + ndc

                        if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]): # visited 여기서 검사해도 다른 애가 해줄거임
                            break

                        if nw in (0, 1): # 왼위 체크
                            if (ccr, ccc) in wall and nw in wall[(ccr, ccc)]: # 움직인 걸로 체크해야지...
                                break
                        else: # 오아 체크. 다음칸
                            if (nr, nc) in wall and nw-2 in wall[(nr, nc)]:
                                break

                        ccr, ccc = nr, nc

                    else: # 다 갔음
                        visited[nr][nc] = visited[cr][cc] - 1
                        cold[nr][nc] += visited[nr][nc]
                        nq.append((nr, nc))

            q = nq

def mix():
    new_cold = [row[:] for row in cold] # 동시에

    for i in range(N):
        for j in range(N):
            for d in range(4):
                nr = i + dr[d]
                nc = j + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if cold[nr][nc] >= cold[i][j]:
                    continue

                if d in (0, 1):  # 왼위 체크
                    if (i, j) in wall and d in wall[(i, j)]:
                        continue
                else:  # 오아 체크. 다음칸
                    if (nr, nc) in wall and d-2 in wall[(nr, nc)]:
                        continue

                diff = (cold[i][j] - cold[nr][nc]) // 4

                new_cold[i][j] -= diff
                new_cold[i][j] = max(new_cold[i][j], 0)
                new_cold[nr][nc] += diff

    return new_cold


dr = [0, -1, 0, 1] # 왼위오아
dc = [-1, 0, 1, 0]
# 에어컨 시원함 퍼지는 정도
wind = [[[(-1, 0, 1), (0, -1, 0)], [(0, -1, 0)], [(1, 0, 3), (0, -1, 0)]],
        [[(0, -1, 0), (-1, 0, 1)], [(-1, 0, 1)], [(0, 1, 2), (-1, 0, 1)]],
        [[(-1, 0, 1), (0, 1, 2)], [(0, 1, 2)], [(1, 0, 3), (0, 1, 2)]],
        [[(0, -1, 0), (1, 0, 3)], [(1, 0, 3)], [(0, 1, 2), (1, 0, 3)]]]

N, W, K = map(int, input().split()) # 격자 크기, 벽 개수, 시원함 정도. 20, 400, 1000
matrix = [list(map(int, input().split())) for _ in range(N)]
cold = [[0] * N for _ in range(N)]
wall = dict() # 좌표 : 방향(위/왼). 여러개 가능
air = dict() # 에어컨 위치. 한칸에 하나. 좌표 : 방향
office = [] # 사무실 위치
time = 0

for i in range(N):
    for j in range(N):
        if matrix[i][j] > 1:
            air[(i, j)] = matrix[i][j] - 2
        elif matrix[i][j] == 1:
            office.append((i, j))

for _ in range(W):
    x, y, s = map(lambda x: int(x)-1, input().split())
    s = -s # 좌표에 맞춤. 1 = 위, 0 = 왼

    if (x, y) in wall:
        wall[(x, y)].add(s)
    else:
        wall[(x, y)] = {s}

while True:
    if time > 100: # 100분까지도 도나?
        time = -1
        break

    # k 이상 되면 끝. 시작하자마자 이미 사무실 k일 수 있음
    for r, c in office:
        if cold[r][c] < K:
            break
    else:
        break

    # 1. 공기 시원하게 함
    blow()

    # 2. 공기 섞임
    cold = mix()

    # 3. 외벽 -1
    for i in range(N):
        for j in range(N):
            if (i in (0, N-1) or j in (0, N-1)) and cold[i][j] > 0:
                cold[i][j] -= 1

    time += 1

print(time) # k 이상 되는 최초의 시간. 100분 넘으면 -1
