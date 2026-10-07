# 2분

# 좌상단 1,1
# 빈칸, 함정, 벽, 격자 밖도 벽
# 기사 = 직사각형 형태. 체력 k
# 기사 체스판에서 사라질 수 있음

# 1. 기사 이동
# 다른 기사 있으면 연쇄적으로 밀림. 근데 끝에 벽이 있으면 모든 기사는 이동 불가

# 2. 대결 대미지
# 밀려난 기사들 피해 입음
# 이동한 곳에서 직사각형 내에 놓여있는 함정의 수만큼 체력 깎임
# 체력 이상의 대미지 받으면 체스판에서 사라짐
# 명령 받은 기사는 피해 입지 않음. 함정 없어도 피해 안 입음

# 처음 기사 위치 겹치지 않음
# 기사 != 벽
# 초기에 기사 범위 체크 안 해도 되겠지

from collections import deque

def draw(num, d): # 함정 파악 후 다시 그려주기
    r, c, h, w, k, dam = knights[num]
    count = 0 # 함정 개수

    nr = r + dr[d]
    nc = c + dc[d]

    for i in range(nr, nr+h):
        for j in range(nc, nc+w):
            if matrix[i][j] == 1: # 함정 있으면
                count += 1

    if num != idx: # 명령 받은 애 아니면
        k -= count # 체력 - 함정
        dam += count # 받은 대미지

    if k > 0: # 체력 남아있으면 그려주기
        knights[num] = nr, nc, h, w, k, dam

        for i in range(nr, nr + h):
            for j in range(nc, nc + w):
                knights_grid[i][j] = num
    else:
        knights[num] = None # 죽음


def move(idx, d):
    q = deque([idx]) # 연쇄작용 기사
    moved = {idx} # 이미 이동한 기사
    new_grid = [row[:] for row in knights_grid]

    while q:
        ci = q.popleft()
        r, c, h, w, *_ = knights[ci]

        # 직사각형 전체 이동해야됨
        for i in range(r, r+h):
            for j in range(c, c+w):
                new_grid[i][j] = 0 # 전 위치 삭제

                nr = i + dr[d]
                nc = j + dc[d]

                if not (0 <= nr < N and 0 <= nc < N) or matrix[nr][nc] == 2: # 격자 밖, 벽 이동 불가
                    return False, None # 못 움직임

                nidx = knights_grid[nr][nc]
                if nidx and nidx != ci and nidx not in moved: # 기사 있고 나랑 다른 애임
                    q.append(nidx)
                    moved.add(nidx)

    # 다 이동 가능
    return moved, new_grid


dr = [-1, 0, 1, 0] # 위오아왼
dc = [0, 1, 0, -1]

N, K, Q = map(int, input().split()) # 격자, 기사 수, 명령
matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 빈칸, 1 = 함정, 2 = 벽
knights = [None] # 1번부터
knights_grid = [[0] * N for _ in range(N)] # 기사 번호표시

for num in range(1, K+1): # 기사 입력
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1

    knights.append((r, c, h, w, k, 0)) # 받은 대미지

    for i in range(r, r+h):
        for j in range(c, c+w):
            knights_grid[i][j] = num

for _ in range(Q):
    idx, d = map(int, input().split()) # 기사 번호, 방향

    if knights[idx] is None: # 이미 죽음
        continue

    # 1. 명령 기사 이동
    can, new_grid = move(idx, d)

    # 2. 이동 가능하면 함정 체크 후 새로 그려주기
    if can:
        knights_grid = new_grid # 이동한 애들 삭제
        for num in can: # 기사 번호
            draw(num, d)

print(sum(val[5] for val in knights[1:] if val)) # 생존한 기사들이 받은 대미지 합