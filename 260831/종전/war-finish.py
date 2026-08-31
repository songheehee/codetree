# 1~100 수로만 이뤄져있음. 지역별 인구수
# 다섯개의 부족이 땅을 나누기로 함. 기울어진 직사각형 이용
# 대각선으로 움직이며 반시계 순회를 했을 때 지나왔던 지점들의 집합
# 아래에서 시작. 각 방향으로 최소 1번은 움직여야함. 격자 밖으로 넘어가면 안됨

def calc(points):
    global min_diff

    ppl = [0] * 5
    br, bc = points[0] # 아래
    rr, rc = points[1]
    tr, tc = points[2] # 위
    lr, lc = points[3]

    # 1번 부족 = 직사각형 안 지역
    sj, ej = tc, tc+1
    for i in range(tr, br+1):
        if tr < i <= lr:
            sj -= 1
        elif lr < i <= br:
            sj += 1

        if tr < i <= rr:
            ej += 1
        elif rr < i <= br:
            ej -= 1

        for j in range(sj, ej):
            ppl[0] += matrix[i][j]

    # 2번 부족 = 좌측 상단 윗부분. 위쪽 포함. 왼쪽 낫 포함
    ej = tc + 1
    for i in range(lr):
        if i >= tr:
            ej -= 1

        for j in range(ej):
            ppl[1] += matrix[i][j]

    # 3번 부족 = 우측 상단 윗부분. 오른쪽 포함. 위쪽 낫 포함
    sj = tc + 1
    for i in range(rr if rc == N-1 else rr+1):
        if i > tr:
            sj += 1

        for j in range(sj, N):
            ppl[2] += matrix[i][j]

    # 4번 부족 = 좌측 하단 아랫부분. 왼쪽 포함. 아래 낫 포함
    ej = lc
    for i in range(lr+1 if lc == 0 else lr, N):
        if i > lr and ej < bc:
            ej += 1

        for j in range(ej):
            ppl[3] += matrix[i][j]

    # 5번 부족 = 우측 하단 아랫부분. 아래 포함. 오른 낫 포함
    sj = rc
    for i in range(rr+1, N):
        if i > rr+1 and sj > bc:
            sj -= 1

        for j in range(sj, N):
            ppl[4] += matrix[i][j]

    min_diff = min(min_diff, max(ppl)-min(ppl))


def dfs(sr, sc, idx, lst): # 아랫점 기준
    if idx == 2:
        # 마지막 위치 찾아주기
        mr, mc = lst[1][0] - lst[0][0], lst[1][1] - lst[0][1]
        lr, lc = lst[2][0] - mr, lst[2][1] - mc

        if not (0 <= lr < N and 0 <= lc < N):
            return

        lst.append((lr, lc))

        calc(lst) # 부족 수 계산
        return

    for l in range(1, N):  # N 최대 크기 20
        nr = sr + (dr[idx] * l)
        nc = sc + (dc[idx] * l)

        if not (0 <= nr < N and 0 <= nc < N):
            break

        dfs(nr, nc, idx+1, lst+[(nr, nc)])




dr = [-1, -1, 1, 1]
dc = [1, -1, -1, 1]

N = int(input()) # 나라 크기
matrix = [list(map(int, input().split())) for _ in range(N)]
min_diff = 100*N*N

# 1. 가능한 네개 꼭지점 다 선택하기
# 2. 각 다섯 부족 min, max 구해보기
# 아래 꼭지점 기준
for i in range(2, N):
    for j in range(1, N-1): # 어차피 끄트머리는 안됨
        # 격자 밖 안됨, 최소 한번은 이동해야됨, 여러번 이동도 가능
        dfs(i, j, 0, [(i, j)])

print(min_diff) # 각 부족장이 관리하는 인구수의 최댓값과 최솟값의 차이가 가장 최소