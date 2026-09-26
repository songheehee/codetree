# 1번부터 S명의 산타들
# 좌상단 1,1
# 루돌프 이동 -> 산타 이동
# 기절하거나 탈락한 산타는 안 움직임
# 거리는 맨해튼 제곱으로 계산

# 1. 루돌프 이동
# 가장 가까운 산타를 향해 1칸 돌진. 탈락하지 않은 산타 중
# 가까운 산타가 여러명이면 행이 큰 산타, 같을 경우 열이 큰 산타
# 8방 중 하나로 돌진. 우선순위가 높은 산타 중 8방 중 가장 가까워지는 방향

# 2. 산타 이동
# 순서대로 이동
# 기절했거나 탈락한 산타는 안 움직임
# 루돌프에게 가장 가까워지는 방향으로 1칸 이동
# 다른 산타가 있거나 격자 밖이면 못 감
# 움직일 수 있는 칸이 없으면 움직이지 않음
# 움직일 수 있어도 루돌프랑 가까워지지 않으면 움직이지 않음
# 상우하좌 우선순위

# 3. 충돌
# 루돌프가 움직여서 충돌 일어나면 C 만큼의 점수. 산타는 루돌프가 이동해온 방향으로 C 칸 밀려남
# 산타가 움직여서 충돌 일어나면 D 만큼의 점수. 산타는 자신이 이동해온 반대 방향으로 D 칸 밀려남
# 밀려난 위치가 격자 밖 -> 탈락
# 밀려난 칸에 산타 있으면 상호작용

# 4. 상호작용
# 산타 해당 방향으로 1칸씩 밀림
# 격자 밖으로 밀려나면 탈락

# 5. 기절
# 루돌프랑 충돌한 산타는 기절 k+2번째 턴부터 정상 상태
# 움직일 수는 없지만 충돌, 상호작용은 가능
# 루돌프 기절한 산타로 돌진 가능

# 산타가 모두 게임에서 탈락하면 즉시 종료
# 매 턴마다 탈락하지 않은 산타들 1점 추가

def move():
    for i in range(1, S+1):
        if santa[i] is None: # 탈락한 산타
            continue

        sr, sc, sf = santa[i]
        min_dist = (sr-rr)**2 + (sc-rc)**2
        minr, minc, nd = -1, -1, 0

        if sf > turn: # 기절한 산타
            continue

        for d in [0,2,4,6]: # 상우하좌
            nr = sr + dr[d]
            nc = sc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N): # 격자 밖
                continue

            dist = (nr-rr)**2 + (nc-rc)**2
            if matrix[nr][nc] or dist >= min_dist: # 다른 산타 있거나 가까워지지 않으면 가지 않음
                continue

            min_dist, minr, minc, nd = dist, nr, nc, d # 다 돌면서 가장 가까운 곳 찾기

        # 4방 다 돌면 산타 이동
        if minr != -1:
            if minr == rr and minc == rc: # 루돌프랑 충돌
                bump(i, (nd+4)%8, D) # 반대 방향
            else:
                matrix[sr][sc] = 0  # 이전 위치 삭제
                santa[i] = (minr, minc, sf)
                matrix[minr][minc] = i


def bump(idx, d, num): # 산타 번호, 방향, 점수
    sr, sc, _ = santa[idx]
    matrix[sr][sc] = 0 # 전 위치 비워주기
    score[idx] += num

    nr = rr + (dr[d] * num)
    nc = rc + (dc[d] * num)

    if not (0 <= nr < N and 0 <= nc < N):
        santa[idx] = None
        return

    # 기절, 새로운 위치
    if matrix[nr][nc]: # 산타 있음 -> 상호작용
        interact(nr, nc, d)

    matrix[nr][nc] = idx
    santa[idx] = (nr, nc, turn+2)


def interact(r, c, d): # 상호작용
    idx = matrix[r][c] # 원래 해당 칸에 있던 산타
    nr = r + dr[d]
    nc = c + dc[d]

    if not (0 <= nr < N and 0 <= nc < N): # 탈락
        santa[idx] = None
        return

    if matrix[nr][nc]: # 다음 칸에 산타 있음
        interact(nr, nc, d)

    matrix[nr][nc] = idx
    santa[idx] = (nr, nc, santa[idx][2])


def rudolph():
    global rr, rc
    # 탈락하지 않은 산타 중 가장 가까운 산타. 행큰, 열큰
    min_dist, maxr, maxc = 2*N*N, 0, 0

    for i in range(1, S+1):
        if santa[i] is None: # 탈락한 산타
            continue

        sr, sc, _ = santa[i]
        dist = (rr-sr)**2 + (rc-sc)**2

        if (min_dist, -maxr, -maxc) > (dist, -sr, -sc):
            min_dist, maxr, maxc = dist, sr, sc

    # 가장 가까운 산타 방향으로 한칸 전진
    for d in range(8):
        nr = rr + dr[d]
        nc = rc + dc[d]

        if not (0 <= nr < N and 0 <= nc < N):
            continue

        dist = (nr-maxr)**2 + (nc-maxc)**2 # 루돌프 다음 위치와 산타와의 거리
        if dist < min_dist:
            min_dist = dist
            nrr, nrc, nd = nr, nc, d # 다음 루돌프 위치

    rr, rc = nrr, nrc
    if rr == maxr and rc == maxc: # 루돌프 산타 충돌
        bump(matrix[maxr][maxc], nd, C)

    return nrr, nrc


dr = [-1, -1, 0, -1, 1, 1, 0, 1] # 상우하좌 (0,2,4,6)
dc = [0, -1, 1, 1, 0, -1, -1, 1]

N, T, S, C, D = map(int, input().split()) # 격자, 턴수, 산타 수, 루돌프 힘, 산타 힘. 50, 1000, 30
rr, rc = map(lambda x: int(x)-1, input().split()) # 루돌프 위치
matrix = [[0] * N for _ in range(N)] # 산타 번호 표시
santa = [None] * (S+1) # 1번부터
score = [0] * (S+1) # 1번부터

for _ in range(S):
    idx, r, c = map(int, input().split())
    r -= 1
    c -= 1

    santa[idx] = (r, c, 0) # 기절까지 같이 관리
    matrix[r][c] = idx

for turn in range(1, T+1):
    # 1. 루돌프 이동
    rudolph()

    # 2. 산타 순서대로 이동
    move()

    # 남은 산타 없으면 종료
    if santa.count(None) == S+1:
        break

    # 3. 탈락하지 않은 산타 +1
    for i in range(1, S+1):
        if santa[i]:
            score[i] += 1

print(*score[1:]) # 각 산타가 얻은 최종 점수