# 처음에는 무기 없는 빈 격자에 플레이어들. 초기 능력치 모두 다름. 격자에는 무기 있을 수도, 없을 수도
# 1-1. 첫번째 플레이어부터 본인 방향대로 한칸 이동. 만약 격자 벗어나면 정반대로
# 2-1. 이동한 방향에 플레이어가 없으면 총이 있는 경우 총 획득. 이미 총 있는 경우 더 쎈 총 갖고 나머지 격자에 둠
# 2-2. 이동한 방향에 플레이어가 있는 경우 싸움. 능력치 + 총 비교. 같을 경우 초기 능력치가 더 높은 사람 승리
#      진 사람은 총 내려놓고 방향대로 한칸 이동. 만약 격자 밖/다른 플레이어 있으면 90도 회전 후 이동. 총 있으면 획득
#      이긴 사람은 공격력 차이만큼 포인트 획득. 총 비교 후 제일 센거. 나머지 내려놓음
# 칸에 총이 두개일 수 있나? yes
# 이동했는데 플레이어, 총 있으면 총 줍나? 안 주울 것이라 가정
# 플레이어 번호 중요

def fight(i, you): # 둘 위치 동일
    *_, d, power, gun = player[i]
    nr, nc, _, fp, fg = player[you]

    if (power + gun > fp + fg) or (power + gun == fp + fg and power > fp):  # 내가 더 쎔. 상대방 이동
        # 점수 획득
        points[i] += (power + gun) - (fp + fg)

        # 진 사람 총 내려놓고 이동
        if fg:
            matrix[nr][nc].append(fg)
            player[you][4] = 0

        lose(you)

        # 이긴 사람 총 비교
        player[i][4] = get_gun(nr, nc, gun)
        player_loc[(nr, nc)] = i

    else:  # 상대가 더 쎔. 내가 이동
        # 점수 획득
        points[you] += abs((power + gun) - (fp + fg))

        # 진 사람 총 내려놓고 이동
        if gun:
            matrix[nr][nc].append(gun)
            player[i][4] = 0

        lose(i)

        # 이긴 사람 총 비교
        player[you][4] = get_gun(nr, nc, fg)


def lose(idx): # 진 사람 이동. 만약 다 돌았는데도 빈칸 없으면 어케 하지
    r, c, d, power, gun = player[idx]

    for i in range(4):
        nd = (d+i) % 4
        nr = r + dr[nd]
        nc = c + dc[nd]

        if not (0 <= nr < N and 0 <= nc < N and (nr, nc) not in player_loc):
            continue

        player[idx] = [nr, nc, nd, power, get_gun(nr, nc, gun)]
        player_loc[(nr, nc)] = idx

        return


def get_gun(r, c, gun):
    if not matrix[r][c]:
        return gun

    matrix[r][c].sort()  # 제일 큰거 뽑기 위해

    if not gun:  # 총 없음
        return matrix[r][c].pop()

    # 총 비교
    if matrix[r][c][-1] > gun:
        new_gun = matrix[r][c].pop()
        matrix[r][c].append(gun)
        return new_gun
    else:
        return gun

def move():
    for i in range(len(player)):
        r, c, d, power, gun = player[i]
        nr = r + dr[d]
        nc = c + dc[d]

        if not (0 <= nr < N and 0 <= nc < N):
            d = (d+2) % 4
            nr = r + dr[d]
            nc = c + dc[d]

        # 일단 이동
        player[i] = [nr, nc, d, power, gun]
        player_loc.pop((r, c), None)

        # 사람 있으면 싸움
        if (nr, nc) in player_loc:
            idx = player_loc[(nr, nc)]  # 싸울 대상
            fight(i, idx)

        # 총 줍기, 이동
        else:
            player[i][4] = get_gun(nr, nc, gun)
            player_loc[(nr, nc)] = i


dr = [-1, 0, 1, 0] # 위오아왼
dc = [0, 1, 0, -1]

N, P, R = map(int, input().split()) # 격자 크기, 플레이어 수, 라운드 수. 20, 30, 500
matrix = [list(map(lambda x: [int(x)] if x != '0' else [], input().split())) for _ in range(N)] # 총 정보. 여러개 가능
points = [0] * P
player = [] # 위치, 방향, 능력치, 총
player_loc = dict() # 위치 : 플레이어 번호

for _ in range(P):
    X, Y, D, S = map(int, input().split()) # 위치, 방향, 초기 능력치
    X -= 1
    Y -= 1

    player_loc[(X, Y)] = len(player)
    player.append([X, Y, D, S, 0])

for _ in range(R):
    # 1. 순서대로 이동
    move()

print(*points) # 플레이어 포인트