# 나무와 도망자 겹칠 수 있음. 술래랑은?
# 술래는 처음 위 방향 -> 달팽이 모양. 끝에 도달하면 다시 거꾸로 중심으로
# 점수 = 턴 * 잡힌 도망자의 수

def run():
    # 도망자 움직일 때 술래랑 거리가 3 이하인 애들만 이동 (맨해튼 거리)
    new_runner = dict()

    for (r, c), dirs in list(runner.items()):
        dist = abs(sr-r) + abs(sc-c)

        if dist > 3: # 이동 안함
            if (r, c) in new_runner:
                new_runner[(r, c)].extend(dirs)
            else:
                new_runner[(r, c)] = dirs
            continue

        for d in dirs:
            nr = r + sdr[d]
            nc = c + sdc[d]

            # - 격자 벗어나는 경우
            #   방향 반대 후 술래 없다면 이동
            if not (0 <= nr < N and 0 <= nc < N):
                d = (d + 2) % 4
                nr = r + sdr[d]
                nc = c + sdc[d]

            # - 격자 벗어나지 않는 경우
            #   다음 칸에 술래가 있으면 움직이지 않음. 나무는 있어도 이동 가능
            if (nr, nc) == (sr, sc): # 다음칸 술래
                if (r, c) in new_runner:
                    new_runner[(r, c)].append(d)
                else:
                    new_runner[(r, c)] = [d]
                continue

            # 다음 칸 이동
            if (nr, nc) in new_runner:
                new_runner[(nr, nc)].append(d)
            else:
                new_runner[(nr, nc)] = [d]
            continue

    return new_runner


def move():
    # 술래 한칸 이동. 방향 틀어지는 지점이면 방향 바로 틀어줌. 정중앙, 0,0도 방향 바로 전환
    global sr, sc, sd, snail, dnum, dcount, scount
    dr, dc = (sdr, sdc) if snail == 1 else (odr, odc)

    nr = sr + dr[sd]
    nc = sc + dc[sd]
    sr, sc = nr, nc

    # 정중앙 도착, 0,0 도착
    if (nr, nc) == (0, 0):
        sd, snail = 0, -1
        dnum, dcount, scount = N-1, -1, 0 # 반시계 방향은 처음에 세번 돌아야됨
        return
    elif (nr, nc) == (N//2, N//2):
        sd, snail = 0, 1
        dnum, dcount, scount = 1, 0, 0
        return

    scount += 1

    if scount == dnum:
        scount = 0
        dcount += 1
        # 방향 틀어주기
        sd = (sd+1) % 4

    if dcount == 2:
        dcount = 0
        if snail == 1:
            dnum += 1
        else:
            dnum -= 1


def catch():
    # 술래 시야 (현재 방향) = 현재 칸 포함하여 3칸 but 나무 있으면 나무 칸에 있는 사람은 가려짐
    dr, dc = (sdr, sdc) if snail == 1 else (odr, odc)
    count = 0 # 잡은 도망자 수

    for i in range(3):
        nr = sr + (dr[sd] * i)
        nc = sc + (dc[sd] * i)

        if not (0 <= nr < N and 0 <= nc < N):
            continue

        if (nr, nc) in runner and matrix[nr][nc] == 0:
            count += len(runner[(nr, nc)])
            runner.pop((nr, nc), None) # 해당 칸 도망자 다 삭제

    return count


sdr = [-1, 0, 1, 0] # 위오아왼
sdc = [0, 1, 0, -1]

odr = [1, 0, -1, 0] # 아오위왼
odc = [0, 1, 0, -1]

N, R, H, K = map(int, input().split()) # 격자 크기(홀수), 도망자 수, 나무 수, 턴 수. 100, 10,000, 10,000, 100
matrix = [[0] * N for _ in range(N)] # 나무 = 1
runner = dict() # 좌표 : 방향. 한 칸에 여러명일 수 있음
sr, sc = N//2, N//2 # 술래 좌표
sd, snail = 0, 1 # 술래 현재 방향 인덱스, 달팽이 시계방향인지 반대인지 (1, -1)
dnum, dcount, scount = 1, 0, 0 # 이동 칸수, 두번되면 +1, 술래가 해당 칸수로 몇칸 갔는지
score = 0

for _ in range(R):
    X, Y, D = map(int, input().split())

    # 처음에는 도망자 위치 겹치지 않음
    runner[(X-1, Y-1)] = [D] # 오/아 시작. sdr 쓰기

for _ in range(H):
    X, Y = map(lambda x: int(x)-1, input().split())
    matrix[X][Y] = 1 # 나무 표시

for turn in range(1, K+1):
    # 1. 도망자 동시에 이동
    runner = run()

    # 2. 술래 이동
    move()

    # 3. 술래 잡기
    score += catch() * turn

print(score) # 술래 얻게된 점수