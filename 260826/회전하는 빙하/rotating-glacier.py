from collections import deque

def bfs(r, c): # 얼음군집 찾기
    q = deque([(r, c)])
    visited[r][c] = 1
    count = 1 # 군집 개수

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                continue

            if matrix[nr][nc]:
                count += 1
                visited[nr][nc] = 1
                q.append((nr, nc))

    return count


def melt():
    chk = [[0] * N for _ in range(N)] # 한번에 녹이려고

    for i in range(N):
        for j in range(N):
            count = 0

            for d in range(4):
                nr = i + dr[d]
                nc = j + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if matrix[nr][nc]:
                    count += 1

            if matrix[i][j] and count < 3:
                chk[i][j] = 1

    for i in range(N):
        for j in range(N):
            if chk[i][j]:
                matrix[i][j] -= 1


dr = [0, 1, -1, 0] # 오아위왼
dc = [1, 0, 0, -1]

n, Q = map(int, input().split()) # 회전 가능 레벨, 회전 횟수. 격자 크기 2^N
N = 2**n # 한 변의 길이
matrix = [list(map(int, input().split())) for _ in range(N)]
levels = list(map(int, input().split()))

for level in levels:
    if level == 0:
        melt()
        continue

    length = 2**level
    half = length//2
    new_matrix = [[0] * N for _ in range(N)]
    for i in range(0, N, length):
        for j in range(0, N, length): # 좌측 상단 시작점
            for d in range(4): # 4등분. 방향 인덱스
                if d == 0:
                    si, sj = i, j
                elif d == 1:
                    si, sj = i, j+half
                elif d == 2:
                    si, sj = i+half, j
                else:
                    si, sj = i+half, j+half

                for k in range(si, si+half):
                    for l in range(sj, sj+half):
                        nr = k + (dr[d] * half)
                        nc = l + (dc[d] * half)

                        new_matrix[nr][nc] = matrix[k][l]

    matrix = new_matrix
    # 회전 끝나고 빙하 녹음
    melt()

max_ice = 0
visited = [[0] * N for _ in range(N)]

for i in range(N):
    for j in range(N):
        if matrix[i][j] and not visited[i][j]:
            max_ice = max(max_ice, bfs(i, j))

print(sum(map(sum, matrix)))
print(max_ice)