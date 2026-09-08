# 1. 밀가루 제일 적은 곳에 밀가루 +1 (여러개면 모두)
# 2. 도우를 말아줘 = 접어서 위로 회전. 위에 있는 밀가루가 더 넓으면 중단
# 3. 도우를 눌러줘 = 상하좌우로 인접한 밀가루 빼서 // 5. 큰 값은 빼주고 작은 값은 더해줌 (동시에)
# 3-1. 나랑 상하좌우에 있는 애랑 비교하는데 이미 비교했으면 패스
# 3-2. 열 작 행 큰 것부터 좌측에 배치해서 일자로
# 4. 두번 접어줘
# 5. 3번 반복

def roll():
    top = [[flour[0]]]
    bottom = flour[1:]

    while True:
        if len(bottom) - len(top[0]) < len(top) + 1:
            break

        lst = []
        for _ in range(len(top[0])):
            lst.append(bottom.pop(0))

        top.append(lst)
        top = list(map(list, zip(*top[::-1])))

    top.append(bottom)
    return top

def push():
    max_col = max(len(row) for row in flour)
    visited = [[0] * max_col for _ in range(len(flour))]
    new_flour = [row[:] for row in flour] # 한번에 더해주기

    for i in range(len(flour)):
        for j in range(len(flour[i])):
            for d in range(4):
                nr = i + dr[d]
                nc = j + dc[d]

                if not (0 <= nr < len(flour) and 0 <= nc < len(flour[nr]) and not visited[nr][nc]):
                    continue

                D = abs(flour[i][j] - flour[nr][nc]) // 5

                if flour[i][j] > flour[nr][nc]:
                    new_flour[i][j] -= D
                    new_flour[nr][nc] += D
                else:
                    new_flour[i][j] += D
                    new_flour[nr][nc] -= D

            visited[i][j] = 1

    # 1차원 배열로 만들기
    return one_line(new_flour, max_col)

def one_line(flour, max_col):
    new_flour = []

    for j in range(max_col):
        for i in range(len(flour)-1, -1, -1):
            if not (0 <= i < len(flour) and 0 <= j < len(flour[i])):
                continue

            new_flour.append(flour[i][j])

    return new_flour

def fold():
    # 한번 접기
    half = len(flour) // 2
    new_flour = []
    top = flour[:half][::-1]
    bottom = flour[half:]

    new_flour.append(top)
    new_flour.append(bottom)

    # 두번 접기
    half = len(new_flour[0]) // 2
    top = [row[:half][::-1] for row in new_flour][::-1]
    bottom = [row[half:] for row in new_flour]

    return top + bottom


dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N, K = map(int, input().split()) # 배열 크기, 차이 K
flour = list(map(int, input().split()))
turn = 0

while True:
    turn += 1

    # 1. 밀가루 적은 곳에 +1
    minf = min(flour)
    for i in range(N):
        if flour[i] == minf:
            flour[i] += 1

    # 2. 도우를 말아줘......어케 말지
    flour = roll()

    # 3. 도우를 눌러줘
    flour = push()

    # 4. 두번 반으로 접기
    flour = fold()

    # 5. 3번 반복
    flour = push()

    # 최대, 최소 차이가 K 이하 되면 끝
    if max(flour) - min(flour) <= K:
        break

print(turn) # 밀가루 양의 최댓값과 최솟값의 차이가 k 이하가 되는 최소 연산 횟수