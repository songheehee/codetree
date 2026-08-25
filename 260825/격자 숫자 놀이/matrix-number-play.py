# 행의 개수가 열의 개수보다 크거나 같은 경우
# 1. 모든 행 정렬. 출현 빈도가 적은 순서대로
# 2. 출현하는 횟수가 같을 경우 숫자가 작은 순서대로
# 3. 정렬할 때 숫자랑 출현 빈도 수 append

# 행의 개수가 열의 개수보다 작은 경우
# 모든 열에 대하여 1~3

def sort_rows(row_num):
    for i in range(row_num):
        count = dict()  # 각 숫자에 대한 개수

        for num in matrix[i]:
            if num == 0:
                continue

            if num in count:
                count[num] += 1
            else:
                count[num] = 1

        sort_count = dict()
        for k, v in count.items():
            if v in sort_count:
                sort_count[v].append(k)
            else:
                sort_count[v] = [k]

        new_row = []
        for k in sorted(sort_count.keys()):
            for v in sorted(sort_count[k]):
                new_row.extend([v, k])

        matrix[i] = new_row

    # 0 붙여주기. 안 붙여주려다가 열 계산할 때 힘들 거 같아서
    max_col = max(len(row) for row in matrix)
    for row in matrix:
        if len(row) < max_col:
            row.extend([0] * (max_col - len(row)))


R, C, K = map(int, input().split())
R -= 1
C -= 1
matrix = [list(map(int, input().split())) for _ in range(3)]
time = 0

while True:
    if time > 100:
        time = -1
        break

    row_num = len(matrix)
    col_num = len(matrix[0])

    if row_num > R and len(matrix[R]) > C:
        if matrix[R][C] == K:
            break

    # 행이나 열의 길이가 100을 넘어갈 경우 100제외 하고 모두 버림
    if row_num > 100:
        matrix = matrix[:101]

    if col_num > 100:
        matrix = [row[:101] for row in matrix]

    # 행의 개수가 열의 개수보다 크거나 같을 경우
    if row_num >= col_num:
        sort_rows(row_num)

    else: # 열 > 행
        matrix = list(map(list, zip(*matrix)))
        sort_rows(col_num)
        matrix = list(map(list, zip(*matrix)))

    time += 1

print(time) # matrix[R][C] 값이 K가 될때까지 걸리는 시간. 불가능하거나 답이 100초 넘으면 -1