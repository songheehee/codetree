# 상하좌우 한 방향 정하면 모든 수들이 해당 방향으로 전부 밀림
# 같은 숫자끼리 만나면 합쳐짐 (숫자 더하기)
# 이미 합쳐진 숫자는 또 합쳐지진 않음
# 3개 이상의 같은 숫자는 벽이랑 가장 가까운 숫자부터 두개씩만 합쳐짐
# 다섯번 움직인 이후에 격자판에서 가장 큰 값의 최댓값

def left(matrix):
    new_matrix = [row[:] for row in matrix]

    for i in range(N):
        row = new_matrix[i]
        new_row = []
        idx = -1 # 이미 합친 애 인덱스

        for j in range(N):
            if row[j] == 0:
                continue

            if new_row:
                if row[j] == new_row[-1] and len(new_row) != idx:
                    new_row[-1] += row[j]
                    idx = len(new_row)
                    continue

            new_row.append(row[j])

        new_matrix[i] = new_row + [0] * (N-len(new_row))

    return new_matrix

def right(matrix):
    new_matrix = [row[:] for row in matrix]

    for i in range(N):
        row = new_matrix[i]
        new_row = []
        idx = -1 # 이미 합친 애 인덱스

        for j in range(N-1, -1, -1):
            if row[j] == 0:
                continue

            if new_row:
                if row[j] == new_row[-1] and len(new_row) != idx:
                    new_row[-1] += row[j]
                    idx = len(new_row)
                    continue

            new_row.append(row[j])

        new_matrix[i] = [0] * (N-len(new_row)) + new_row[::-1]

    return new_matrix

def up(new_matrix):
    return list(map(list, zip(*left(list(zip(*new_matrix))))))

def down(new_matrix):
    return list(map(list, zip(*right(list(zip(*new_matrix))))))

def dfs(count, new_matrix): # 부분집합
    global max_num

    if count == 5:
        max_num = max(max_num, max(max(row) for row in new_matrix))
        return

    dfs(count+1, up(new_matrix)) # 위
    dfs(count+1, down(new_matrix)) # 아래
    dfs(count+1, left(new_matrix)) # 왼
    dfs(count+1, right(new_matrix)) # 오른

N = int(input())
matrix = [list(map(int, input().split())) for _ in range(N)]
max_num = 0

dfs(0, [row[:] for row in matrix])

print(max_num)