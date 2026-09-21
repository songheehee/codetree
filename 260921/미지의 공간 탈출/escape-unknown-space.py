# N*N 2차원 평면인데 그 사이 어딘가에 M 길이 정육면체 시간의 벽이 세워져있음
# 위에서 본 미지의 공간의 평면도, 위+동서남북 시간의 벽의 단면도
# 0 = 빈 공간, 1 = 장애물, 2 = 타임머신, 3 = 시간의 벽 위치, 4 = 탈출구 (미지의 공간 바닥)
# 타임머신은 빈 공간만 이동 가능
# 타임머신 시간의 벽 윗면 어딘가에 있음. 2로 표시
# 시간의 벽과 맞닿은 미지의 공간의 바닥은 장애물로 둘러싸여있음. 한칸만 뚫려 있음 -> 출구 하나
# 시간 이상 현상 매 v 배수 턴마다 방향 d로 한칸씩 확산. 빈 공간으로만 확산. 동시에
# 타임머신 상하좌우로 한칸씩 이동. 장애물과 시간 이상 현상 피해서 탈출구까지
# 시간 이상 현상 -> 타임머신 이동
# 한칸 뚫려있는 곳 최단거리 bfs로 찾아야됨
# 엣지 : 타임머신이 시간의 벽에서 못 나올 경우, 탈출구 장애물로 둘러싸인 경우. 이상현상이 벽 탈출구 막으면?
# 이상현상 -> 이상현상 갈 수 있나?
# 시간의 벽은 장애물인가?

from collections import deque

def spread(turn): # 이상현상 확산. 더 이상 못 가면 None 처리. 동시에 처리
    for i in range(F):
        if strange[i] is None:
            continue

        r, c, d, v = strange[i]

        if turn % v == 0:
            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N): # 범위 체크 해야지...
                strange[i] = None
                continue

            if matrix[nr][nc] == 0 or matrix[nr][nc] == 5: # 빈 공간으로만 확산
                strange[i] = [nr, nc, d, v]
                matrix[nr][nc] = 5 # 이상현상 처리
            else:
                strange[i] = None


def bfs(): # 바닥에서 타임머신 이동
    visited = [[0] * N for _ in range(N)]
    q = deque([(tr, tc)])
    visited[tr][tc] = time
    turn = time

    while q:
        # 이상현상 먼저 이동
        turn += 1
        spread(turn)

        for _ in range(len(q)):
            cr, cc = q.popleft()

            for i in range(4):
                nr = cr + dr[i]
                nc = cc + dc[i]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if visited[nr][nc] or matrix[nr][nc] in (1, 3, 5): # 장애물, 벽, 이상현상
                    continue

                if matrix[nr][nc] == 4: # 탈출
                    return turn

                visited[nr][nc] = turn
                q.append((nr, nc))

    return -1 # 탈출구 못 찾음


def search(): # 벽 탈출구 찾기. 시작점 기준 동서남북 빈칸 찾기. 무조건 하나
    global tr, tc
    wallr, wallc = -1, -1

    # 시간의 벽 시작점 찾기
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 3:
                wallr, wallc = i, j # 시간의벽 시작 지점
                break
        if wallr > -1:
            break

    for i in range(wallr, wallr+M):
        if wallc+M < N and matrix[i][wallc+M] == 0: # 동
            tr, tc = i, wallc+M
            return 0, M-1-(i-wallr)

        if wallc > 0 and matrix[i][wallc-1] == 0: # 서
            tr, tc = i, wallc-1
            return 1, i-wallr

    for j in range(wallc, wallc+M):
        if wallr+M < N and matrix[wallr+M][j] == 0: # 남
            tr, tc = wallr+M, j
            return 2, j-wallc

        if wallr > 0 and matrix[wallr-1][j] == 0: # 북
            tr, tc = wallr-1, j
            return 3, M-1-(j-wallc)


def find_out(): # 시간의 벽 탈출
    md, mr, mc = 4, -1, -1  # 타임머신 위치. 동서남북위, 좌표
    visited = [[[0] * M for _ in range(M)] for _ in range(5)] # 동서남북위
    ed, ei = search()  # 동서남북, 몇번째 인덱스인지

    # 타임머신 찾기
    for i in range(M):
        for j in range(M):
            if wall[4][i][j] == 2:
                mr, mc = i, j
                break
        if mr != -1:
            break

    q = deque([(md, mr, mc)])
    visited[md][mr][mc] = 1

    while q:
        cd, cr, cc = q.popleft()

        for i in range(4):
            nd = cd
            nr = cr + dr[i]
            nc = cc + dc[i]

            if not (0 <= nr < M and 0 <= nc < M):
                res = change_dir(cd, cr, cc, i)

                if not res: # 동서남북 밑으로 못감
                    continue

                nd, nr, nc = res

            if visited[nd][nr][nc] or wall[nd][nr][nc]: # 벽 있으면 못감
                continue

            if nd == ed and nr == M-1 and nc == ei:
                return visited[cd][cr][cc] + 1

            visited[nd][nr][nc] = visited[cd][cr][cc] + 1
            q.append((nd, nr, nc))

    return -1 # 바닥으로 못 내려감


def change_dir(cd, cr, cc, idx): # 4방으로 움직였을 때 어떤 면으로 오는지
    if cd == 4: # 현재면이 위
        if idx == 0:  # 오른쪽 이동
            return 0, 0, M-1-cr
        elif idx == 1:  # 왼쪽 이동
            return 1, 0, cr
        elif idx == 2: # 아래
            return 2, 0, cc
        elif idx == 3: # 위
            return 3, 0, M-1-cc

    elif cd == 0: # 동
        if idx == 0: # 오른쪽 이동 -> 북
            return 3, cr, 0
        elif idx == 1: # 왼쪽 이동 -> 남
            return 2, cr, M-1
        elif idx == 3: # 위 -> 위
            return 4, M-1-cc, M-1

    elif cd == 1: # 서
        if idx == 0: # 오른쪽 이동 -> 남
            return 2, cr, 0
        elif idx == 1: # 왼쪽 이동 -> 북
            return 3, cr, M-1
        elif idx == 3: # 위 -> 위
            return 4, cc, 0

    elif cd == 2: # 남
        if idx == 0: # 오른쪽 이동 -> 동
            return 0, cr, 0
        elif idx == 1: # 왼쪽 이동 -> 서
            return 1, cr, M-1
        elif idx == 3: # 위 -> 위
            return 4, M-1, cc

    elif cd == 3: # 북
        if idx == 0: # 오른쪽 이동 -> 서
            return 1, cr, 0
        elif idx == 1: # 왼쪽 이동 -> 동
            return 0, cr, M-1
        elif idx == 3: # 위 -> 위
            return 4, 0, M-1-cc


dr = [0, 0, 1, -1] # 동서남북
dc = [1, -1, 0, 0]

N, M, F = map(int, input().split()) # 평면도, 시간의벽, 시간 이상 현상. 20, 10, 10
matrix = [list(map(int, input().split())) for _ in range(N)] # 2차원 평면도
wall = [[list(map(int, input().split())) for _ in range(M)] for _ in range(5)] # 시간의 벽. 동,서,남,북,위
strange = [list(map(int, input().split())) for _ in range(F)]
tr, tc = -1, -1 # 바닥에서의 타임머신 좌표

# 1. 윗면에서 내려와서 시간의 벽 탈출구 찿기
time = find_out() # 윗면 -> 바닥 오는 시간. 이 시간 이후부터 바닥에서 이동

if time == -1: # 탈출구로 못감
    print(-1)
else:
    for r, c, d, v in strange:
        matrix[r][c] = 5 # 초기 이상현상 처리

    for i in range(1, time+1): # 타임머신 바닥 도착할 때까지 이상현상 처리
        spread(i)

    if matrix[tr][tc] == 5: # 움직이기 전에 이상현상 먼저 체크
        print(-1)
    else:
        print(bfs()) # 탈출구까지 이동하는 데 필요한 최소 시간, 불가능하면 -1