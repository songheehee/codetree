# 초반에는 무기 없는 칸에 플레이어 있음. 플레이어는 초기 능력치 가짐. 모두 다름
# 1. 플레이어 순서대로 본인 방향대로 한칸 이동. 격자 벗어나면 정반대 방향으로 한칸
# 1-1. 이동한 방향에 플레이어가 없다면 총 있는지 확인, 있으면 더 센 총 획득. 나머지는 냅둠
# 1-2. 만약 플레이어가 있다면 싸움. 능력치+총 더 큰 사람이 이김. 같을 경우 초기 능력치 더 높은 사람이 이김. 차이만큼 포인트 획득
# 1-3. 진 플레이어는 총 내려놓고 자기 방향대로 한칸 이동
#      이동하려는 칸에 다른 플레이어가 있거나 격자 밖이면 오른쪽으로 90도씩 회전하면서 빈칸일 때까지
#      해당 칸에 총 있으면 총 획득
# 1-4. 이긴 플레이어는 칸의 총과 본인 총 중 가장 센 거. 나머지는 내려놓음

def get_gun(r, c, gun): # 가장 센 총
    if matrix[r][c]: # 칸에 총 있을 경우만
        matrix[r][c].sort()
        max_gun = matrix[r][c][-1] # 해당 칸에서 제일 센 총

        if max_gun > gun:
            matrix[r][c].pop() # 빼주고
            matrix[r][c].append(gun) # 원래 갖고 있던 거 놔두기

            return max_gun

    return gun # 내가 가진 총이 제일 셈


def move():
    for i in range(1, P+1):
        r, c, d, power, gun = player[i]
        nr = r + dr[d]
        nc = c + dc[d]
        ppl[r][c] = 0 # 전 위치 삭제

        if not (0 <= nr < N and 0 <= nc < N): # 격자 벗어나면 정반대
            d = (d+2) % 4
            nr = r + dr[d]
            nc = c + dc[d]

        if not ppl[nr][nc]: # 사람 없음 -> 총 챙기기
            player[i] = nr, nc, d, power, get_gun(nr, nc, gun)
            ppl[nr][nc] = i
            continue

        # 플레이어 있음 -> 싸우기
        you = ppl[nr][nc]
        *_, youd, you_power, you_gun = player[you]
        diff = abs(power+gun - (you_power+you_gun)) # 차이만큼 포인트 획득

        if power+gun > you_power+you_gun or (power+gun == you_power+you_gun and power > you_power): # 내가 이김
            # 진 사람 총 두고 이동
            if you_gun: # 총 있으면 총 냅두기
                matrix[nr][nc].append(you_gun)

            lose(you, youd, nr, nc)

            # 이긴 사람 포인트, 총 줍기
            points[i] += diff
            player[i] = nr, nc, d, power, get_gun(nr, nc, gun)
            ppl[nr][nc] = i

        else: # 너가 이김
            if gun: # 총 있으면 총 냅두기
                matrix[nr][nc].append(gun)

            lose(i, d, nr, nc)

            points[you] += diff
            player[you] = nr, nc, youd, you_power, get_gun(nr, nc, you_gun)
            ppl[nr][nc] = you


def lose(idx, d, cr, cc): # 진 사람 이동
    ppl[cr][cc] = 0 # 전 위치 삭제

    for i in range(4): # 빈칸 찾을 때까지 90도 회전
        nd = (d+i) % 4
        nr = cr + dr[nd]
        nc = cc + dc[nd]

        if not (0 <= nr < N and 0 <= nc < N) or ppl[nr][nc]: # 격자 밖/다른 플레이어 있음
            continue

        # 찾으면 해당 칸으로 이동. 총 있으면 총 줍기
        player[idx] = nr, nc, nd, player[idx][3], get_gun(nr, nc, 0)
        ppl[nr][nc] = idx

        break


dr = [-1, 0, 1, 0] # 위오아왼
dc = [0, 1, 0, -1]

N, P, R = map(int, input().split()) # 격자, 플레이어 수, 라운드 수
matrix = [list(map(lambda x: [int(x)] if int(x) else [], input().split())) for _ in range(N)] # 총 공격력
player = [None] # 1번부터. 위치, 방향, 초기 능력치, 총
ppl = [[0] * N for _ in range(N)] # 플레이어 번호
points = [0] * (P+1) # 1번부터

for i in range(1, P+1):
    x, y, d, s = map(int, input().split()) # 위치, 방향, 초기 능력치
    x -= 1
    y -= 1

    player.append((x, y, d, s, 0))
    ppl[x][y] = i

for _ in range(R):
    # 1. 플레이어 이동
    move()

print(*points[1:]) # 각 플레이어들 획득 포인트