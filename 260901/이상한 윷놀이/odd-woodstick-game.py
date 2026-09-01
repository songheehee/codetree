def move():
    for i in range(K):
        r, c, d = order[i]

        nr = r + dr[d]
        nc = c + dc[d]

        # 3, 4
        if not (0 <= nr < N and 0 <= nc < N) or matrix[nr][nc] == 2:
            # 방향 반대로 전환 뒤 이동
            # 반대쪽도 파랑일 경우 이동하지 않음
            d = change_dir(d)
            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N) or matrix[nr][nc] == 2: # 인덱스 오류가 날 수 있구나;
                order[i] = (r, c, d)
                continue

        if matrix[nr][nc] == 0 or matrix[nr][nc] == 1: # 흰/빨
            # 말 있으면 다 같이 이동
            idx = horses[(r, c)].index(i)
            lst = horses[(r, c)][idx:] if matrix[nr][nc] == 0 else horses[(r, c)][idx:][::-1]
            new_lst = horses[(r, c)][:idx]

            if new_lst:
                horses[(r, c)] = new_lst
            else:
                horses.pop((r, c), None)

            if (nr, nc) in horses:
                horses[(nr, nc)].extend(lst)

                if len(horses[(nr, nc)]) >= 4:
                    return True
            else:
                horses[(nr, nc)] = lst

            for num in lst:
                if i == num:
                    order[i] = (nr, nc, d)
                else:
                    order[num] = (nr, nc, order[num][2])


def change_dir(d):
    if d == 0 or d == 2:
        return d+1
    else:
        return d-1

dr = [0, 0, -1, 1] # 오왼위아
dc = [1, -1, 0, 0]

N, K = map(int, input().split()) # 판 크기, 말 개수
matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 흰, 1 = 빨, 2 = 파
horses = dict() # 몇번 말, 방향. 0번이 맨 밑
order = [0] * K # 말 순서. 위치, 방향

for i in range(K):
    X, Y, D = map(lambda x: int(x)-1, input().split())

    order[i] = (X, Y, D)
    horses[(X, Y)] = [i] # 처음엔 한 칸에 한 말

turn = 0

while True:
    if turn > 1000:
        turn = -1
        break

    turn += 1

    stop = move()

    if stop:
        break

print(turn) # 종료되는 순간의 턴 번호. 1000보다 크면 -1