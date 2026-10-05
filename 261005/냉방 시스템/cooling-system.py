'''
소요시간 : 1시간 24분
수행 시간 : 345ms / 메모리 : 24MB
수행 시간 : 386ms / 메모리 : 24MB (해당 칸에서 가려는 방향 쪽에 벽 있으면 아예 nr, nc 계산 안 하게끔. 근데 어떻게 얘가 더 오래 걸리지)
시도 : 2번

[구상]
    - 에어컨 바람 퍼지는게 제일 까다로웠다
    - 에어컨 위치 저장해놓고 for문 돌면서 각각 bfs 돌자. 1 되면 끝
    - 공기 섞일 때 동시에 섞인다!!!

[구현]
    - 앞 세방향 검사할 때 None 인지 아닌지 검사할 것. 방향에 0도 있기 때문
    - 저번에 1 이후로도 계속 퍼지는 걸로 짜서 이번에 유의함!!!
    - 왼->위 가니까 그 전 위치 기억해놔야함. sr, sc 따로 변수 하자
    - 두번째 벽은 직진 ad 확인해야된다
    - 벽, 사무실 다 구해놓자. 벽은 오,아도 표시해주기
    - in 검사 때문에 벽 안의 방향 set으로 했어도 됐을듯? 근데 귀찮아서 바꾸지 않음
    - 사무실 K 이상 되는게 단계 별로 확인해줘야 하는지, 모든 단계 다 끝나고 확인해야 하는지 살짝 헷갈렸음. 확인해보니까 전체 끝나고임. 아니면 즉시 종료 라고 말해줬을듯
    - 공기 섞일 때 마이너스 될 수 있나? 생각해봤지만 되지 않을 거 같아서 그냥 바로 빼주는 걸로

[나아진 점]
    - 저번에는 벽 확인할 때 왼, 위만 표시해줘서 이동하고 오른쪽, 아래 검사해야했는데 한칸에 다 벽을 표시해줘서 검사가 더 편했음!
    - 저번에는 3방향을 룩업테이블로 했는데 계산해보니까 방향 양 옆 확인 후 직진하면 돼서 그렇게 해봤다. 더 깔끔한듯?

[오답노트]
    1. 틀린거 또 틀렸다면 :
    2. 새로운 것을 틀렸다면 :
    - 벽은 현재 위치에서 검사해줘야하는데 1번은 그렇게 해놓고 2번은 nr, nc를 검사해줌;
'''
# 0 = 빈공간, 1 = 사무실, 2 = 에어컨 왼, 3 = 에어컨 위, 4 = 에 오, 5 = 에 아
# 1. 에어컨 바람 퍼짐. 5부터
# 2. 공기 섞임. 시원함이 높은 곳에서 낮은 곳으로 시원함 차이 // 4. 동시에. 벽은 통과 안함
# 3. 외벽 시원함 -1. 0 은 감소하지 않음
# 모든 사무실 k 이상 되는 최소 시간. 100 분 넘으면 -1
# 벽 에어컨 바로 옆/앞에 없음. 벽 != 외벽
# 에어컨 바로 앞 격자 나가지 않음
# 사무실, 에어컨 최소 하나 이상

from collections import deque

def mix():
    new_cold = [row[:] for row in cold] # 동시에 전파, 벽 확인

    for i in range(N):
        for j in range(N):
            if cold[i][j]:
                for d in range(4):
                    if (i, j) in wall and d in wall[(i, j)]: # 벽 있으면
                        continue

                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N and cold[i][j] > cold[nr][nc]): # 나보다 작은 애만
                        continue

                    diff = (cold[i][j] - cold[nr][nc]) // 4
                    new_cold[nr][nc] += diff
                    new_cold[i][j] -= diff

    return new_cold


def wind(ar, ac, ad):
    visited = [[0] * N for _ in range(N)]
    q = deque()

    # 바로 앞 무조건 갈 수 있음
    nr = ar + dr[ad]
    nc = ac + dc[ad]
    q.append((nr, nc))
    visited[nr][nc] = 5
    cold[nr][nc] += 5

    while q:
        for _ in range(len(q)):
            cr, cc = q.popleft()

            for d in [(ad - 1 + 4) % 4, None, (ad + 1) % 4]:  # ad 기준 양옆 -> ad
                sr, sc = cr, cc

                if d is not None:
                    if (sr, sc) in wall and d in wall[(sr, sc)]: # 해당 위치에 벽 있으면 가지도 않음
                        continue

                    nr = sr + dr[d]
                    nc = sc + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                        continue

                    sr, sc = nr, nc

                # 여기까지 왔으면 직진
                if (sr, sc) in wall and ad in wall[(sr, sc)]: # 벽 있으면 안감
                    continue

                nr = sr + dr[ad]
                nc = sc + dc[ad]

                if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                    continue

                q.append((nr, nc))
                visited[nr][nc] = visited[cr][cc] - 1
                cold[nr][nc] += visited[nr][nc]

        if visited[cr][cc] == 1:
            break


dr = [0, -1, 0, 1] # 왼위오아
dc = [-1, 0, 1, 0]

# 왼 = 위->왼, 왼, 아->왼
# 위 = 왼->위, 위, 오->위
# 오 = 위->오, 오, 아->오
# 아 = 왼->아, 아, 오->아

N, W, K = map(int, input().split()) # 격자, 벽 개수, 사무실 시원함 정도
matrix = [list(map(int, input().split())) for _ in range(N)] # 사무실, 에어컨
wall = dict() # 해당 위치 위/왼 벽
air = [] # 에어컨 위치, 방향
office = [] # 사무실 위치. K 이상인지 확인 위함
cold = [[0] * N for _ in range(N)] # 시원함

for i in range(N):
    for j in range(N):
        if matrix[i][j] == 1:
            office.append((i, j))
        elif matrix[i][j]: # 에어컨
            air.append((i, j, matrix[i][j]-2))

for _ in range(W): # 벽 설치
    x, y, s = map(lambda x: int(x)-1, input().split()) # -1=위, 0=왼
    s = -s

    if (x, y) in wall:
        wall[(x, y)].add(s)
    else:
        wall[(x, y)] = {s}

    if s == 0: # 해당 위치 왼쪽에는 오른쪽 벽임
        y -= 1
    else:
        x -= 1 # 위쪽은 아래

    if 0 <= x < N and 0 <= y < N:
        s += 2

        if (x, y) in wall:
            wall[(x, y)].add(s)
        else:
            wall[(x, y)] = {s}

ans = -1

for time in range(1, 101):
    # 1. 에어컨 바람 퍼짐
    for ar, ac, ad in air:
        wind(ar, ac, ad)

    # 2. 공기 섞임. 높은 곳 -> 낮은 곳
    cold = mix()

    # 3. 외벽 -1
    for i in range(N):
        if i in (0, N-1):
            jrange = range(N)
        else:
            jrange = (0, N-1)

        for j in jrange:
            if cold[i][j]:
                cold[i][j] -= 1

    # 마지막에 체크하는 거 맞나?
    for r, c in office:
        if cold[r][c] < K:
            break
    else:  # 다 K 넘음
        ans = time
        break

print(ans) # 사무실 시원해지는 시간. 100 넘으면 -1