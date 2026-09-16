# S명의 산타 T개의 턴
# 1. 루돌프 이동. 탈락하지 않은 가장 가까운 산타를 향해 1칸 돌진. 거리는 빼기 제곱으로 계산
#   두명 이상이면 r 좌표가 큰 산타. 동일하면 c 좌표가 큰 산타
#   8방 중에 가장 가까워지는 방향으로 이동
# 2. 산타 이동. 순서대로 이동. 루돌프한테 가까워지는 방향으로 이동 (4방. 상우하좌 우선)
#   다른 산타가 있는 칸이나 격자 밖 안됨. 움직일 수 있는 칸 없으면 움직이지 않음
#   움직일 수 있어도 가까워지지 않으면 이동하지 않음
# 3. 충돌. 루돌프가 움직여서 충돌이면 산타 + C. 산타 루돌프가 이동해온 방향으로 C만큼 밀려남 << ??
#   산타가 움직여서 충돌 -> 산타 + D. 산타가 이동해온 반대 방향으로 D칸 밀려남
#   밀려난 위치가 격자 밖이면 탈락
#   밀려난 칸에 다른 산타 있으면 상호작용
# 4. 상호작용. 원래 칸에 있던 산타 한칸씩 밀려남. 연쇄적으로
# 5. 루돌프와 충돌 후 기절. 다음 턴까지 기절
#   움직이진 못하나 충돌이나 상호작용으로 밀려날 순 있음. 루돌프 기절 산타도 돌진 가능
# 6. 매 턴마다 탈락하지 않은 산타 +1
# 이미 기절했는데 또 기절할 수도 있나
# 연속해서 잘 밀리는지

from collections import deque

rdr = [-1, -1, -1, 0, 0, 1, 1, 1]
rdc = [-1, 0, 1, -1, 1, -1, 0, 1]

sdr = [-1, 0, 1, 0] # 상우하좌
sdc = [0, 1, 0, -1]

def santa_move():
    for idx in range(1, S+1):
        if santa[idx] is None: # 탈락한 산타
            continue

        sr, sc, f = santa[idx]
        min_dist = (rr-sr)**2 + (rc-sc)**2 # 현재 산타와의 거리
        nsr, nsc, nsd = sr, sc, 0

        if f > turn: # 기절한 산타
            continue

        for d in range(4): # 가장 가까운 거리 찾는 거임
            nr = sr + sdr[d]
            nc = sc + sdc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            dist = (rr-nr)**2 + (rc-nc)**2
            if matrix[nr][nc] or dist >= min_dist: # 다른 산타 있거나 거리 가까워지지 않음
                continue

            min_dist = dist
            nsr, nsc, nsd = nr, nc, d

        # 다 돌고 최단 거리
        matrix[sr][sc] = 0  # 전 위치 삭제

        if nsr == rr and nsc == rc: # 루돌프와 충돌
            points[idx] += D
            d = (nsd+2) % 4

            nsr += sdr[d] * D
            nsc += sdc[d] * D

            if not (0 <= nsr < N and 0 <= nsc < N):
                santa[idx] = None # 탈락
                continue

            f = turn + 2 # 기절

            if matrix[nsr][nsc]: # 산타 있음
                comm(matrix[nsr][nsc], nsr, nsc, d, 1)

        santa[idx] = (nsr, nsc, f)
        matrix[nsr][nsc] = idx

def comm(idx, cr, cc, d, drtype): # 상호작용. 재귀가 나을라나
    # 밀려날 산타가 없을 때까지
    if drtype == 0:
        dr, dc = rdr, rdc
    else:
        dr, dc = sdr, sdc

    while True:
        nr = cr + dr[d]
        nc = cc + dc[d]

        if not (0 <= nr < N and 0 <= nc < N):
            santa[idx] = None
            break

        # 산타 위치 변경
        santa[idx] = (nr, nc, santa[idx][2])
        nxt = matrix[nr][nc]
        matrix[nr][nc] = idx

        if not nxt: # 산타 없음
            break

        cr, cc = nr, nc
        idx = nxt

# def rudolph(): # 한칸만 이동임!!!!
#     visited = [[0] * N for _ in range(N)]
#     q = deque([(rr, rc, None)])
#     visited[rr][rc] = 1
#
#     min_dist = N*N*2
#     maxr, maxc = 0, 0
#     new_rudolph = None # 새로운 루돌프 좌표
#
#     while q:
#         for _ in range(len(q)):
#             cr, cc, dirs = q.popleft()
#
#             for d in range(8):
#                 nr = cr + rdr[d]
#                 nc = cc + rdc[d]
#
#                 if not (0 <= nr < N and 0 <= nc < N):
#                     continue
#
#                 dist = (nr-cr)**2 + (nc-cc)**2
#                 if visited[nr][nc] or dist > min_dist:
#                     continue
#
#                 if matrix[nr][nc] > 0: # 산타
#                     if (-min_dist, maxr, maxc) < (-dist, nr, nc): # 거리는 작고 행열은 더 큰거
#                         min_dist, maxr, maxc = dist, nr, nc
#                         new_rudolph = dirs if dirs else (nr, nc, d)
#                     continue
#
#                 visited[nr][nc] = visited[cr][cc] + 1
#                 q.append((nr, nc, dirs if dirs else (nr, nc, d)))
#
#         if min_dist < N*N*2:
#             return new_rudolph

def rudolph(): # 산타 다 돌자
    min_dist = N*N*2 # 산타와의 거리
    maxr, maxc = 0, 0

    for s in santa[1:]:
        if s is None:
            continue

        sr, sc, _ = s
        dist = (sr-rr)**2 + (sc-rc)**2

        if (-min_dist, maxr, maxc) < (-dist, sr, sc):  # 거리는 작고 행열은 더 큰거
            min_dist, maxr, maxc = dist, sr, sc

    # 해당 산타로 가장 가까워지는 방향으로 이동
    min_dist = (maxr-rr)**2 + (maxc-rc)**2
    nrr, nrc, nrd = 0, 0, 0

    for d in range(8):
        nr = rr + rdr[d]
        nc = rc + rdc[d]

        if not (0 <= nr < N and 0 <= nc < N):
            continue

        dist = (maxr-nr)**2 + (maxc-nc)**2
        if min_dist > dist: # 무조건 작은 데가 있겠지...
            min_dist = dist
            nrr, nrc, nrd = nr, nc, d

    return nrr, nrc, nrd


def bump(): # 루돌프가 움직여서 충돌한 경우
    idx = matrix[rr][rc]
    sr, sc, f = santa[idx]
    points[idx] += C

    matrix[sr][sc] = 0
    nr = sr + (rdr[rd] * C)
    nc = sc + (rdc[rd] * C)

    if not (0 <= nr < N and 0 <= nc < N):
        santa[idx] = None
        return

    if matrix[nr][nc]: # 산타 있음
        comm(matrix[nr][nc], nr, nc, rd, 0)

    f = turn + 2  # 이 턴부터 기절 풀림
    santa[idx] = (nr, nc, f)
    matrix[nr][nc] = idx


N, T, S, C, D = map(int, input().split()) # 격자, 턴수, 산타수, 루돌프+, 산타+. 50, 1000, 30
matrix = [[0] * N for _ in range(N)] # 루돌프, 산타 표시
rr, rc = map(lambda x: int(x)-1, input().split()) # 루돌프 위치
rd = 0 # 루돌프 방향
santa = [None] * (S+1) # 산타 위치. 1번부터. 기절도 같이 표시
points = [0] * (S+1) # 1번부터

for _ in range(S):
    idx, r, c = map(int, input().split())
    r -= 1
    c -= 1

    santa[idx] = (r, c, 0)
    matrix[r][c] = idx

for turn in range(T):
    # 1. 루돌프 이동
    rr, rc, rd = rudolph()

    # 2. 산타 있으면 충돌
    if matrix[rr][rc]:
        bump()

    # 3. 산타 이동
    santa_move()

    if santa.count(None) == S+1: # 산타 다 탈락했으면 종료
        break

    # 4. 탈락하지 않은 산타 +1
    for i in range(1, S+1):
        if santa[i]:
            points[i] += 1

print(*points[1:]) # 각 산타가 얻은 최종 점수