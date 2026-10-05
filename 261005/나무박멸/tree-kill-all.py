# 제초제는 K 범위만큼 대각선으로 퍼짐. 벽이 있는 경우 전파되지 않음
# 1. 나무 있는 칸에서 인접한 네 칸 중 나무가 있는 칸 수만큼 나무 성장. 동시에
# 2. 나무는 인접한 4개 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식
#    각 칸의 나무 그루 수에서 총 번식이 가능한 칸의 개수 만큼 나누어진 수만큼 번식. 동시에
# 3. 나무가 가장 많이 박멸되는 칸에 제초제 뿌림. 나무가 있는 칸에 뿌리면 4개의 대각선 방향으로 k 칸만큼 전파
#    전파 도중 벽이 있거나 나무가 아예 없으면 그 칸까지만 제초제. c년만큼 제초제 남았다가 c+1년에 사라짐
#    이미 제초제 있는 곳은 다시 c년 동안
#    개수 동일할 경우 행작, 열작
# Y년 동안 총 박멸한 나무
# 제초제 범위 넘어갈 수 있음

def die():
    mdr = [-1, -1, 1, 1] # 제초제용 대각선
    mdc = [-1, 1, -1, 1]
    max_dead = 0 # 가장 많이 죽는 나무 수
    minr, minc = N, N # 개수 동일할 경우 행작, 열작

    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0: # 나무 있는 곳만
                dead = matrix[i][j] # 본인 포함

                for d in range(4):
                    for dist in range(1, K+1):
                        nr = i + (mdr[d] * dist)
                        nc = j + (mdc[d] * dist)

                        if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] > 0): # 격자 밖, 나무 있어야함
                            break

                        dead += matrix[nr][nc]

                if (-max_dead, minr, minc) > (-dead, i, j):
                    max_dead, minr, minc = dead, i, j

    if max_dead: # 제초제 뿌리기
        med[minr][minc] = year+C+1
        matrix[minr][minc] = 0

        for d in range(4):
            for dist in range(1, K + 1):
                nr = minr + (mdr[d] * dist)
                nc = minc + (mdc[d] * dist)

                if not (0 <= nr < N and 0 <= nc < N):  # 격자 밖
                    break

                if matrix[nr][nc] <= 0:  # 나무 없거나 벽이면 해당 칸까지 제초제
                    med[nr][nc] = year+C+1  # 이때부터 사라짐
                    break

                med[nr][nc] = year+C+1
                matrix[nr][nc] = 0 # 나무도 없애주기

    return max_dead


def reproduce():
    new_matrix = [row[:] for row in matrix]

    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0:
                dirs = [] # 벽, 나무, 제초제 모두 없는 방향

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if matrix[nr][nc] or med[nr][nc] > year: # 벽, 나무, 제초제
                        continue

                    dirs.append(d)

                if dirs: # 번식될 수 있음
                    tree = matrix[i][j] // len(dirs) # 번식될 나무 수

                    for d in dirs:
                        nr = i + dr[d]
                        nc = j + dc[d]

                        new_matrix[nr][nc] += tree

    return new_matrix


def grow():
    for i in range(N):
        for j in range(N):
            if matrix[i][j] > 0: # 나무 있는 칸만
                tree = 0 # 주변 나무 칸 개수

                for d in range(4):
                    nr = i + dr[d]
                    nc = j + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if matrix[nr][nc] > 0: # 근처에 나무 있으면
                        tree += 1

                matrix[i][j] += tree


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N, Y, K, C = map(int, input().split()) # 격자, 년 수, 제초제 확산 범위, 제초제 남아있는 년 수. 20, 1000, 20, 10
matrix = [list(map(int, input().split())) for _ in range(N)] # -1 = 벽, 0 = 빈칸, 1~100 = 나무
total = 0 # 총 박멸한 나무 수
med = [[0] * N for _ in range(N)] # 제초제 언제 턴부터 가능한지

for year in range(1, Y+1):
    # 1. 성장. 동시
    grow()

    # 2. 번식. 동시
    matrix = reproduce()

    # 3. 가장 나무 많이 죽는 곳에 제초제. 행작 열작
    dead = die()
    total += dead

    # 더 이상 나무 없으면 끝
    if not dead:
        break

print(total)