# N,M 격자
# 시공의 돌풍은 항상 0번 열, 크기 두칸
# -1로 표시되며 맨 윗행, 맨 아랫행과 최소 두칸 이상 떨어짐

# 1. 먼지 인접 4방으로 확산
# 인접한 방향에 시공의 돌풍이 있거나 방의 범위를 벗어난다면 해당 방향으로는 확산 일어나지 않음
# 확사되는 양은 원래 칸의 먼지 // 5
# 각 칸에 확산될 때마다 확산된 먼지만큼 줄어듬
# 확산된 먼지는 확산 다 끝난 다음에 더해짐

# 2. 청소 시작
# 윗칸은 반시계 방향으로, 아랫칸은 시계 방향으로
# 바람 불면 먼지 바람 방향대로 한칸씩 이동
# 시공으로 들어간 먼지는 사라짐

def clean():
    new_matrix = [row[:] for row in matrix]

    for idx in [top, bottom]:
        tr, tc, d = idx, 0, 0

        # 한칸 가고 시작
        tr += dr[d]
        tc += dc[d]
        new_matrix[tr][tc] = 0

        while True:
            nr = tr + dr[d]
            nc = tc + dc[d]

            if not (0 <= nr < N and 0 <= nc < M):
                if idx == top:
                    d += 1
                else:
                    d -= 1
                nr = tr + dr[d]
                nc = tc + dc[d]

            if matrix[nr][nc] == -1: # 다시 돌풍으로 옴
                break

            new_matrix[nr][nc] = matrix[tr][tc]

            tr, tc = nr, nc

    return new_matrix


def spread():
    new_matrix = [row[:] for row in matrix]

    for i in range(N):
        for j in range(M):
            if matrix[i][j] // 5 > 0: # 확산될 먼지가 있으면
                dust = matrix[i][j] // 5

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < M and matrix[nr][nc] != -1): # 돌풍 아니면
                        continue

                    new_matrix[i][j] -= dust
                    new_matrix[nr][nc] += dust

    return new_matrix


dr = [0, -1, 0, 1] # 오위왼아
dc = [1, 0, -1, 0]

N, M, T = map(int, input().split()) # 50, 50, 1000
matrix = [list(map(int, input().split())) for _ in range(N)]
top, bottom = None, None # 돌풍 위아래 위치

for i in range(N):
    if matrix[i][0] == -1:
        if top:
            bottom = i
        else:
            top = i

for _ in range(T):
    # 1. 먼지 확산
    matrix = spread()

    # 2. 청소
    matrix = clean()

print(sum(map(sum, matrix)) + 2) # t초 후의 남은 먼지의 양. 돌풍 더해주기