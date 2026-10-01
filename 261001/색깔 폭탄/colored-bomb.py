# -1 = 검정, 0 = 빨강, 1~C = 다른 색
# 1. 가장 큰 폭탄 묶음 찾기
# 2개 이상의 폭탄으로 이뤄져 있어야 하고 다 같은 색이어야함 or 빨간색 포함
# 빨간색으로만 이뤄지면 안됨. 다 연결되어 있어야함
# 크기 같은 게 여러개일 경우
# - 빨간색이 제일 적게 포함
# - 빨간색이 아닌 애 중 행이 가장 큰 애, 열이 가장 작은 애

# 2. 선택된 폭탄 제거 -> 중력
# 돌은 떨어지지 않음

# 3. 반시계 방향으로 90도 회전 -> 중력

# 폭탄 묶음이 존재하지 않을 때까지
# 폭탄 개수 **2 만큼 점수

from collections import deque

def gravity():
    for j in range(N):
        pointer = N-1

        while pointer:
            if matrix[pointer][j] > -2: # 폭탄, 돌
                pointer -= 1
                continue

            for i in range(pointer-1, -1, -1):
                if matrix[i][j] == -1: # 돌 위로 이동
                    pointer = i-1
                    break

                if pointer != i and matrix[i][j] >= 0:
                    matrix[pointer][j] = matrix[i][j]
                    matrix[i][j] = -2 # 빈칸
                    pointer -= 1

            else: # 무사히 다 돌았으면 끝
                break


def find(r, c):
    q = deque([(r, c)])
    visited[r][c] = 1
    visited_red = [[0] * N for _ in range(N)] # 간 빨간색 표시

    color = matrix[r][c] # 같은 색 애들만
    count, red = 1, 0
    mr, mc = r, c # 빨간색 아닌 애 중에. 현재 포함

    new_matrix = [row[:] for row in matrix] # 폭탄 지우는 용
    new_matrix[r][c] = -2

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or visited_red[nr][nc]:
                continue

            if matrix[nr][nc] and matrix[nr][nc] != color: # 다른 색 제외, 돌 제외
                continue

            if matrix[nr][nc] == 0: # 빨간색
                red += 1
                visited_red[nr][nc] = 1
            else: # 같은 색
                visited[nr][nc] = 1

                if (mr, -mc) < (nr, -nc):
                    mr, mc = nr, nc

            count += 1
            q.append((nr, nc))
            new_matrix[nr][nc] = -2 # 빈칸 처리

    return count, red, mr, mc, new_matrix


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N, C = map(int, input().split()) # 격자, 색깔 개수
matrix = [list(map(int, input().split())) for _ in range(N)] # 빈칸 = -2
score = 0

while True:
    # 1. 폭탄 묶음 찾기
    visited = [[0] * N for _ in range(N)]
    max_count, min_red = 1, N*N # 가장 큰 묶음 개수. 최소 2개여야함
    maxr, minc = -1, N
    max_matrix = []

    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0 and not visited[i][j]:
                count, red, mr, mc, new_matrix = find(i, j)

                if (max_count, -min_red, maxr, -minc) < (count, -red, mr, -mc):
                    max_count, min_red, maxr, minc = count, red, mr, mc
                    max_matrix = new_matrix

    # 묶음 없으면 끝
    if max_count == 1:
        break

    # 2. 폭탄 제거 -> 중력
    matrix = max_matrix
    gravity()

    # 3. 회전 -> 중력
    matrix = list(map(list, zip(*matrix)))[::-1]
    gravity()

    # 점수
    score += max_count ** 2

print(score)