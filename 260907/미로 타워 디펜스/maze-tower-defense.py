# 3. 몬스터 종류가 네번 이상 연속되면 삭제 (동시에. 똥글뱅이) -> 점수
def delete(monsters):
    global score

    prev = 0
    count = 1
    delete_set = set()
    si = 0
    for i in range(len(monsters)):
        mon = monsters[i]

        if i == 0:
            prev = mon
            continue

        if mon == prev:
            count += 1
            continue

        if count >= 4:
            score += prev * count
            delete_set.update(set(i for i in range(si, si+count)))

        si = i
        prev = mon
        count = 1

    # 마지막꺼도
    if count >= 4:
        score += prev * count
        delete_set.update(set(i for i in range(si, si + count)))

    # 연속인 애들 삭제
    new_monsters = []
    for i in range(len(monsters)):
        if i not in delete_set:
            new_monsters.append(monsters[i])

    # 3-1. 삭제 후 다시 당겨주고 네번 이상 또 삭제 -> 4개 이상 짜리 없을 때까지
    if monsters == new_monsters:
        return new_monsters

    return delete(new_monsters) # 여기서도 리턴해줘야됨


def move():
    # 탑부터 돌면서 0 아닌 애들 저장해놓고 다시 그려주기
    snum, scount, ccount = 1, 0, 0 # 두개 되면 num+1
    sr, sc = tr, tc # 탑에서 시작
    idx = 0 # 왼 시작
    monsters = []

    while (sr, sc) != (0, 0):
        nr = sr + sdr[idx]
        nc = sc + sdc[idx]

        if matrix[nr][nc]:
            monsters.append(matrix[nr][nc])

        sr, sc = nr, nc

        # 달팽이
        ccount += 1
        if ccount == snum:
            # 방향 바꿔주기
            ccount = 0
            scount += 1
            idx = (idx+1) % 4

        if scount == 2:
            scount = 0
            snum += 1

    # 지운 애들 다시 그려주기
    draw(delete(monsters))


# 4. 몬스터 차례대로 나열했을 때 같은 숫자끼리 짝 -> (총 개수, 숫자)로 바꿔서 다시 미로. 격자 크기까지만
def draw(monsters):
    global matrix
    # 새로운 몬스터 배열
    new_monsters = []
    prev = 0
    count = 1

    for i in range(len(monsters)):
        mon = monsters[i]

        if i == 0:
            prev = mon
            continue

        if mon == prev:
            count += 1
            continue

        new_monsters.append(count)
        new_monsters.append(prev)

        prev = mon
        count = 1

    # 마지막꺼
    new_monsters.append(count)
    new_monsters.append(prev)

    # 새로 그려주기
    new_matrix = [[0] * N for _ in range(N)]
    snum, scount, ccount = 1, 0, 0  # 두개 되면 num+1
    sr, sc = tr, tc  # 탑에서 시작
    idx = 0  # 왼 시작

    while new_monsters and (sr, sc) != (0, 0):
        nr = sr + sdr[idx]
        nc = sc + sdc[idx]

        new_matrix[nr][nc] = new_monsters.pop(0)
        sr, sc = nr, nc

        # 달팽이
        ccount += 1
        if ccount == snum:
            # 방향 바꿔주기
            ccount = 0
            scount += 1
            idx = (idx + 1) % 4

        if scount == 2:
            scount = 0
            snum += 1

    matrix = new_matrix

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

sdr = [0, 1, 0, -1]  # 왼아오위
sdc = [-1, 0, 1, 0]

N, R = map(int, input().split()) # 격자 크기, 라운드 수. 25, 100
matrix = [list(map(int, input().split())) for _ in range(N)] # 몬스터. 0 = 빈칸
score = 0
tr, tc = N//2, N//2

for _ in range(R):
    D, P = map(int, input().split()) # 공격 방향, 공격 칸수

    # 1. 상하좌우 방향 중 주어진 공격 칸 수만큼 몬스터 공격 가능 -> 점수
    for i in range(1, P+1):
        nr = tr + (dr[D] * i)
        nc = tc + (dc[D] * i)

        if not (0 <= nr < N and 0 <= nc < N):
            continue

        score += matrix[nr][nc]
        matrix[nr][nc] = 0

    # 2. 비어있는 공간만큼 몬스터 앞으로 이동하여 공간 채움 (똥글뱅이)
    move()

print(score) # 얻게되는 점수