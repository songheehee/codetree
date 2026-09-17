# 4*4 격자
# 술래말은 하나, 도둑말 잡을 때마다 도둑말의 방향을 갖게됨
# 도둑말 1~16 번호. 겹치지 않음
# 1. 0,0 도둑말 잡고 시작
# 2. 도둑말 번호 순으로 한칸 이동. 빈칸 or 도둑말 있는 칸 이동 가능. 술래말/격자 벗어나면 ㄴㄴ
#   이동할 수 있는 칸 찾을 때까지 45도 반시계 회전. 없으면 이동하지 않음
#   해당 칸에 다른 도둑말 있으면 위치 변경
# 3. 술래말 이동. 한번에 여러칸도 이동 가능. 이동할 때 지나가는 말은 잡지 않음. 도둑말 없는 곳으로 못감
# 술래말 이동할 수 있는 곳에 도둑말이 존재하지 않으면 게임 끝

def dfs(r, c, d, score): # 백트래킹
    global max_score, matrix, runner
    # 술래가 갈 수 있는 좌표 찾아주기
    possible = []
    for i in range(1, 4):  # 최대 3칸밖에 못감
        nr = r + (dr[d] * i)
        nc = c + (dc[d] * i)

        if 0 <= nr < 4 and 0 <= nc < 4 and matrix[nr][nc]: # 도둑말이 있어야함
            possible.append((nr, nc))

    if not possible: # 갈 수 있는 곳 없음
        max_score = max(max_score, score)
        return

    # 갈 수 있으면 도둑말 먹고 다시 dfs. 원복 잘하기
    for nr, nc in possible:
        roll_matrix = [row[:] for row in matrix]
        roll_runner = runner[:]

        num, nd = matrix[nr][nc]
        matrix[nr][nc] = 0
        runner[num] = None

        run(nr, nc)
        dfs(nr, nc, nd, score+num)

        matrix = roll_matrix
        runner = roll_runner


def run(sr, sc):
    for num in range(1, 17):
        if not runner[num]: # 살아있는 도둑말만
            continue

        r, c = runner[num]
        _, d = matrix[r][c]

        for i in range(8):
            nd = (d + i) % 8
            nr = r + dr[nd]
            nc = c + dc[nd]

            if not (0 <= nr < 4 and 0 <= nc < 4):
                continue

            if nr == sr and nc == sc:
                continue

            matrix[r][c] = (num, nd) # 바뀐 방향 저장
            runner[num] = (nr, nc)

            if matrix[nr][nc]: # 해당 도망자 좌표 변경
                nnum, _ = matrix[nr][nc]
                runner[nnum] = (r, c)

            # 위치 변경
            matrix[r][c], matrix[nr][nc] = matrix[nr][nc], matrix[r][c]
            break


dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, -1, -1, -1, 0, 1, 1, 1]

matrix = [] # (번호, 방향)
sr, sc, sd = 0, 0, 0 # 술래
runner = [None] * 17 # 도망자 위치 저장. 1부터 시작 유의
ans = 0

for i in range(4):
    row = list(map(int, input().split()))
    new_row = []

    for j in range(0, len(row), 2):
        p, d = row[j], row[j+1]
        new_row.append((p, d-1))
        runner[p] = (i, j // 2)

    matrix.append(new_row)

# 1. 0,0 잡고 시작
ans += matrix[0][0][0]
sd = matrix[0][0][1]
runner[matrix[0][0][0]] = None
matrix[0][0] = 0

# 2. 도망
run(sr, sc)

# 3. 술래 이동
max_score = 0
dfs(sr, sc, sd, 0)

print(ans+max_score) # 획득할 수 있는 점수 최댓값