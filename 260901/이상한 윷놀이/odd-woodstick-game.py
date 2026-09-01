# 격자판 흰, 빨, 파
# 말 1~K번. 번호, 이동 방향 정해져있음
# 1. 말이 이동하려는 칸이 흰색이면 해당 칸으로 이동. 이미 말이 있으면 말 위에 올림. 여러번 올리기 가능
# 2. 빨간 칸이면 순서 말 순서 뒤집고 말 이동
# 3. 파란 칸이면 이동하지 않고 방향 반대로 전환 뒤 이동. 근데 반대쪽도 파랑이다 -> 이동하지 않음. 이동하려는 말만 방향 전환
# 4. 격자판 범위 벗어나면 방향 반대로 전환 뒤 이동
# 쌓여있는 말 다 같이 이동
# 말이 4개 이상 겹쳐지면 그 즉시 종료

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

        if matrix[nr][nc] == 0: # 흰
            # 말 있으면 다 같이 이동
            idx = horses[(r, c)].index(i)
            lst = horses[(r, c)][idx:] # 말 순서만 적혀있음
            new_lst = horses[(r, c)][:idx]

            if len(lst) > 1:
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

            else:
                order[i] = (nr, nc, d)

                if new_lst:
                    horses[(r, c)] = new_lst
                else:
                    horses.pop((r, c), None)

                if (nr, nc) in horses:
                    horses[(nr, nc)].append(i)

                    if len(horses[(nr, nc)]) >= 4:
                        return True
                else:
                    horses[(nr, nc)] = [i]

        elif matrix[nr][nc] == 1: # 빨강
            # 말 순서 뒤집고 이동
            idx = horses[(r, c)].index(i)
            lst = horses[(r, c)][idx:][::-1] # 거꾸로
            new_lst = horses[(r, c)][:idx]

            if len(lst) > 1:
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
            else:
                order[i] = (nr, nc, d)

                if new_lst:
                    horses[(r, c)] = new_lst
                else:
                    horses.pop((r, c), None)

                if (nr, nc) in horses:
                    horses[(nr, nc)].append(i)

                    if len(horses[(nr, nc)]) >= 4:
                        return True
                else:
                    horses[(nr, nc)] = [i]

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
    X, Y, D = map(int, input().split())
    X -= 1
    Y -= 1
    D -= 1

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