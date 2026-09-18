# N * M 상자. 빨강, 파랑 하나씩. 장애물 여러개. 구멍은 하나
# 사탕 빼내기 위해서 위, 아래, 왼, 오른 기울일 수 있음
# 기울이면 장애물 or 사탕 부딪히기 전까지 미끌어짐
# 빨강을 빼야되고 파랑은 나오면 안됨. 동시도 안됨
# 상자 바깥 부분은 다 장애물
# 그냥 사탕 좌표만 옮기면 된다!
# 아 빨강, 파랑 순서대로 하면 안되고 앞에 있는 애 먼저 해야된다
# 아 전에꺼는 또 해도 소용이 없겠군

def dfs(count, matrix, candy, prev):
    global min_count

    if count >= min_count or count > 10:  # 가지치기
        return
    
    if candy.count(None): # 둘 중 하나라도 나가면 끝
        for can in candy:
            if can is not None:
                if matrix[can[0]][can[1]] == 'B': # 나간 애가 빨강
                    min_count = min(min_count, count)
        return

    # 위
    if prev != 0:
        dfs(count+1, *up(matrix, candy), 0)
    # 아래
    if prev != 1:
        dfs(count+1, *down(matrix, candy), 1)
    # 왼
    if prev != 2:
        dfs(count+1, *left(matrix, candy), 2)
    # 오른
    if prev != 3:
        dfs(count+1, *right(matrix, candy), 3)


def left(matrix, candy):  # 사탕 좌표
    new_matrix = [row[:] for row in matrix]
    new_candy = candy[:]
    new_candy.sort() # 앞에 있는 애 먼저 돌기

    for idx, (r, c) in enumerate(new_candy):
        pointer = 1

        for j in range(1, M - 1):
            if new_matrix[r][pointer] in ('R', 'B'):
                pointer += 1
                continue

            if new_matrix[r][j] == '#':
                pointer = j + 1
                continue

            if pointer != j and j == c:
                if exitr == r and pointer <= exitc < j: # 출구가 가는 길에 있음
                    new_candy[idx] = None
                    new_matrix[r][c] = '.' # 빈칸으로 비워주기
                    break

                new_matrix[r][pointer], new_matrix[r][j] = new_matrix[r][j], new_matrix[r][pointer]
                new_candy[idx] = r, pointer
                pointer += 1
                break

    return new_matrix, new_candy


def right(matrix, candy):  # 사탕 좌표
    new_matrix = [row[:] for row in matrix]
    new_candy = candy[:]
    new_candy.sort(reverse=True)

    for idx, (r, c) in enumerate(new_candy):
        pointer = M - 2

        for j in range(M - 2, 0, -1):
            if new_matrix[r][pointer] in ('R', 'B'):
                pointer -= 1
                continue

            if new_matrix[r][j] == '#':
                pointer = j - 1
                continue

            if pointer != j and j == c:
                if exitr == r and j < exitc <= pointer: # 출구가 가는 길에 있음
                    new_candy[idx] = None
                    new_matrix[r][c] = '.' # 빈칸으로 비워주기
                    break

                new_matrix[r][pointer], new_matrix[r][j] = new_matrix[r][j], new_matrix[r][pointer]
                new_candy[idx] = r, pointer
                pointer -= 1
                break

    return new_matrix, new_candy


def down(matrix, candy):
    new_matrix = [row[:] for row in matrix]
    new_candy = candy[:]
    new_candy.sort(reverse=True)

    for idx, (r, c) in enumerate(new_candy):
        pointer = N - 2

        for i in range(N - 2, 0, -1):
            if new_matrix[pointer][c] in ('R', 'B'):
                pointer -= 1
                continue

            if new_matrix[i][c] == '#':
                pointer = i - 1
                continue

            if pointer != i and i == r:
                if exitc == c and i < exitr <= pointer: # 출구가 가는 길에 있음
                    new_candy[idx] = None
                    new_matrix[r][c] = '.' # 빈칸으로 비워주기
                    break

                new_matrix[pointer][c], new_matrix[i][c] = new_matrix[i][c], new_matrix[pointer][c]
                new_candy[idx] = pointer, c
                pointer -= 1
                break

    return new_matrix, new_candy


def up(matrix, candy):
    new_matrix = [row[:] for row in matrix]
    new_candy = candy[:]
    new_candy.sort()

    for idx, (r, c) in enumerate(new_candy):
        pointer = 1

        for i in range(1, N - 1):
            if new_matrix[pointer][c] in ('R', 'B'):
                pointer += 1
                continue

            if new_matrix[i][c] == '#':
                pointer = i + 1
                continue

            if pointer != i and i == r:
                if exitc == c and pointer <= exitr < i: # 출구가 가는 길에 있음
                    new_candy[idx] = None
                    new_matrix[r][c] = '.' # 빈칸으로 비워주기
                    break

                new_matrix[pointer][c], new_matrix[i][c] = new_matrix[i][c], new_matrix[pointer][c]
                new_candy[idx] = pointer, c
                pointer += 1
                break

    return new_matrix, new_candy


N, M = map(int, input().split())  # 상자 크기
matrix = [list(input().strip()) for _ in range(N)]
# . = 빈칸, # = 장애물, B = 파랑, R = 빨강, O = 출구
candy = [] # 순서 없음
exitr, exitc = 0, 0  # 출구 좌표

for i in range(N):
    for j in range(M):
        if matrix[i][j] == 'R' or matrix[i][j] == 'B':
            candy.append((i, j))
        elif matrix[i][j] == 'O':
            exitr, exitc = i, j

min_count = 11
dfs(0, matrix, candy, -1)

print(min_count if min_count < 11 else -1)  # 기울여야 하는 최소 횟수. 10번 이내에 불가능하면 -1