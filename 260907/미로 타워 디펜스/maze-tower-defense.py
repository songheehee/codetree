'''
소요시간 : 2시간 24분
수행 시간 : 125ms / 메모리 : 19MB
시도 : 2번

이해 및 구상 (8분) - 구현 및 디버깅 (2시간 5분) - 디버깅 (11분)

[구상]
    - 아...난 진짜 달팽이가 너ㅜㅁ너무눠무너뭐눠머눠 싫어!!!!!!!
    - 처음에 일단 공격부터 하고 음...당기는거 어케 하지 고민하다가 뒤에서부터 당길지, 앞에서부터 당길지 고민

[구현]
    - 몬스터를 1차원 배열로 만들자는 생각을 중간에 하기 시작했다; 그래서 중간에 수정함 띠용
    - 처음 공격도 1차원으로 먼가 할 수 있을거 같은데 음 모르겠다! 그 부분은 이미 짜놓은 상태라서 수정하지 않음 ㅎ
    - 처음엔 달팽이 돌면서 앞에서 당길지 뒤에서 당길지 하다가 도대체 여러번 당기는 걸 어떻게 짜는지 모르겠는 거임. 그래서 그냥 순서대로 받고 다시 그려야겠다! 근데 그냥 애초부터 1차원으로 했어도 됐을듯

[실수]
    - 아니 draw에서 똑같이 마지막꺼 해줬으면서 왜 delete에선 안 해줬냐...멍충이

[리팩토링]
    - 달팽이 좌표를 다 받고 시작하는 것도 좋겠다
    - 다시 그릴 필요 없게 애초부터 1차원으로 했어도 좋았을 듯. 근데 그럼 공격 때 어케 하지?
    - delete 랑 draw 때 쓸데없이 마지막꺼 따로 처리 안 하는 방법 없나?
'''
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

    return monsters


# 4. 몬스터 차례대로 나열했을 때 같은 숫자끼리 짝 -> (총 개수, 숫자)로 바꿔서 다시 미로. 격자 크기까지만
def draw(monsters):
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

    return new_matrix

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
    monsters = move()

    # 연속된 몬스터 삭제
    monsters = delete(monsters)

    # 새로 그려주기
    matrix = draw(monsters)


print(score) # 얻게되는 점수