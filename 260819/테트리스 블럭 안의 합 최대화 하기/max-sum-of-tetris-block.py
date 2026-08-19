# 다섯가지 종류의 테트리스 블럭 중 하나를 올려놓아 블럭이 놓인 칸 안에 적힌 수의 합이 최대가 될 때
# 테트리스는 자유롭게 회전, 뒤집기 가능
# 총 모양 19개
# 각 숫자마다 모양 해볼건지, 각 모양마다 매트릭스 전체 순회할건지

def straight(r, c): # 일자 모양
    global max_sum

    if c + 3 < m: # 가로
        max_sum = max(max_sum, sum(matrix[r][c:c+4]))

    if r + 3 < n: # 세로
        max_sum = max(max_sum, sum(row[c] for row in matrix[r:r+4]))

def square(r, c): # 네모
    global max_sum

    dr = [0, 1, 1]
    dc = [1, 0, 1]
    total = matrix[r][c]

    for i in range(3):
        nr = r + dr[i]
        nc = c + dc[i]

        if not (0 <= nr < n and 0 <= nc < m):
            return # 3개 다 안 되면 끝

        total += matrix[nr][nc]

    # 무사히 네모 모양 다 돔
    max_sum = max(max_sum, total)

def zigzag(r, c): # z모양
    global max_sum

    dr = [[1, 1, 2], [0, 1, 1], [1, 1, 2], [0, 1, 1]]
    dc = [[0, 1, 1], [-1, -1, -2], [0, -1, -1], [1, 1, 2]]

    for i in range(4): # 모양 네개
        total = matrix[r][c]

        for j in range(3):
            nr = r + dr[i][j]
            nc = c + dc[i][j]

            if not (0 <= nr < n and 0 <= nc < m):
                break  # 3개 다 안 되면 끝

            total += matrix[nr][nc]

        else: # 무사히 돌면 맥스 값 비교
            max_sum = max(max_sum, total)

def vowel(r, c): # ㅗ 모양. 제일 튀어나온 기준
    global max_sum

    dr = [[1, 1, 1], [1, 1, 2], [1, 1, 2], [0, 0, 1]]
    dc = [[-1, 0, 1], [0, 1, 0], [0, -1, 0], [1, 2, 1]]

    for i in range(4):  # 모양 네개
        total = matrix[r][c]

        for j in range(3):
            nr = r + dr[i][j]
            nc = c + dc[i][j]

            if not (0 <= nr < n and 0 <= nc < m):
                break  # 3개 다 안 되면 끝

            total += matrix[nr][nc]

        else:  # 무사히 돌면 맥스 값 비교
            max_sum = max(max_sum, total)

def line(r, c): # L 모양
    global max_sum

    dr = [[1, 2, 2], [1, 2, 2], [0, 0, 1], [0, 0, 1], [0, 1, 2], [0, 1, 2], [1, 1, 1], [1, 1, 1]]
    dc = [[0, 0, 1], [0, 0, -1], [-1, -2, -2], [1, 2, 2], [-1, -1, -1], [1, 1, 1], [0, 1, 2], [0, -1, -2]]

    for i in range(8): # 모양 여덟개
        total = matrix[r][c] # 모양마다 리셋
        
        for j in range(3):
            nr = r + dr[i][j]
            nc = c + dc[i][j]

            if not (0 <= nr < n and 0 <= nc < m):
                break  # 3개 다 안 되면 끝

            total += matrix[nr][nc]

        else:  # 무사히 돌면 맥스 값 비교
            max_sum = max(max_sum, total)


n, m = map(int, input().split()) # 4~200
matrix = [list(map(int, input().split())) for _ in range(n)]
max_sum = 0

for i in range(n):
    for j in range(m):
        # 숫자가 모양 시작 위치 기준
        straight(i, j)
        square(i, j)
        zigzag(i, j)
        vowel(i, j)
        line(i, j)

print(max_sum)