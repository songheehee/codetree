# 16분 30초

# 1 이상 100 이하 수로 이뤄져 있는 N*N 격자 -> 지역별 인구수
# 다섯개의 부족이 땅을 나눠가짐
# 아래에서 시작해서 기울어진 직사각형 만들기. 모든 방향 최소 한번은 가야함. 격자 밖 안됨

# 1번 : 직사각형 경계 + 그 안
# 2번 : 좌측 상단. 위 포함, 왼 안 포함
# 3번 : 우측 상단. 오른 포함, 위 안 포함
# 4번 : 좌측 하단. 왼 포함, 아래 안 포함
# 5번 : 우측 하단. 아래 포함, 오른 안 포함

def tribe(): # 다섯 부족 나누기
    global min_diff

    tmatrix = [[1] * N for _ in range(N)] # 부족 표시
    tr, tc = points[2] # 위
    br, bc = points[0] # 아래
    rr, rc = points[1] # 오
    lr, lc = points[3] # 왼

    ppl = [0] * 5

    # 2번 부족
    for i in range(lr):
        for j in range(tc+1-max(i+1-tr, 0)):
            tmatrix[i][j] = 2
            ppl[1] += matrix[i][j]

    # 3번 부족
    for i in range(rr if rc == N-1 else rr+1):
        for j in range(tc+1+max(i-tr, 0), N):
            tmatrix[i][j] = 3
            ppl[2] += matrix[i][j]

    # 4번 부족
    for i in range(lr+1 if lc == 0 else lr, N):
        for j in range(min(lc+i-lr, bc)):
            tmatrix[i][j] = 4
            ppl[3] += matrix[i][j]

    # 5번 부족
    for i in range(rr+1, N):
        for j in range(max(rc+1-(i-rr), bc), N):
            tmatrix[i][j] = 5
            ppl[4] += matrix[i][j]

    ppl[0] = sum(map(sum, matrix)) - sum(ppl)
    min_diff = min(min_diff, max(ppl) - min(ppl))

# 직사각형 다 그려보고 차이 구해보기
def dfs(r, c, d):
    if d == 2: # 직사각형 다 그림
        # 마지막 좌표 찾아주기
        size = abs(points[0][0] - points[1][0])
        nr = r + (dr[d] * size)
        nc = c + (dc[d] * size)

        if not (0 <= nr < N and 0 <= nc < N):
            return

        points.append((nr, nc))
        tribe()
        points.pop()
        return

    for size in range(1, N-1):
        nr = r + (dr[d] * size)
        nc = c + (dc[d] * size)

        if not (0 <= nr < N and 0 <= nc < N):
            return # break인가

        points.append((nr, nc))
        dfs(nr, nc, d+1)
        points.pop()


dr = [-1, -1, 1, 1] # 대각선 방향
dc = [1, -1, -1, 1]

N = int(input()) # 20
matrix = [list(map(int, input().split())) for _ in range(N)]
min_diff = N*N*100

# 시작점 찾고 직사각형 그려주기
for i in range(2, N):
    for j in range(1, N-1):
        points = [(i, j)]
        dfs(i, j, 0)

print(min_diff) # 인구수 차이 최솟값