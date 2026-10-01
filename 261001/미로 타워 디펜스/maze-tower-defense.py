# 1. 상하좌우 방향 중 주어진 공격 칸 수만큼 몬스터 공격
# 2. 비어있는 만큼 몬스터 앞으로 이동
# 3. 몬스터 종류가 4번 이상 반복되면 해당 몬스터 삭제
# 삭제 이후 당기고 또 4번 이상 되면 삭제 -> 4번 이상 없을 때까지
# 4. 몬스터를 차례대로 나열했을 때 같은 숫자끼리 짝 지어줌. 개수, 몬스터 번호
# 격자 범위 넘어가면 잘림

def draw():
    new_matrix = [[0] * N for _ in range(N)]
    sr, sc, sd = tr, tc, 2  # 시작 왼
    length = 1  # 가야하는 길이
    count = 0  # 두번 돌면 바꾸기
    cur = 0  # 현재 위치
    idx = 0 # 몬스터 배열 위치

    while True:
        nr = sr + dr[sd]
        nc = sc + dc[sd]

        cur += 1

        if cur == length:
            cur = 0
            count += 1
            sd = (sd - 1) % 4

        if count == 2:
            length += 1
            count = 0

        new_matrix[nr][nc] = monster[idx]
        idx += 1

        sr, sc = nr, nc

        if idx == len(monster) or (sr == 0 and sc == 0):
            break

    return new_matrix


def pair():
    new_mon = []

    prev = 0
    count = 1  # 자기 자신

    for m in monster:
        if not prev:
            prev = m
            continue

        if m == prev:
            count += 1
            continue

        # 다른 경우
        new_mon.append(count)
        new_mon.append(prev)

        prev = m
        count = 1

    # 마지막꺼 추가
    new_mon.append(count)
    new_mon.append(prev)

    return new_mon


def flatten():
    # 탑에서부터 달팽이 돌면서 일차원 배열에 저장
    new_mon = []

    sr, sc, sd = tr, tc, 2 # 시작 왼
    length = 1 # 가야하는 길이
    count = 0 # 두번 돌면 바꾸기
    cur = 0 # 현재 위치

    while sr != 0 or sc != 0:
        nr = sr + dr[sd]
        nc = sc + dc[sd]

        cur += 1

        if cur == length:
            cur = 0
            count += 1
            sd = (sd-1) % 4

        if count == 2:
            length += 1
            count = 0

        if matrix[nr][nc]:
            new_mon.append(matrix[nr][nc])

        sr, sc = nr, nc

    return new_mon


def check():
    global monster, score
    new_mon = []

    prev = 0
    count = 1 # 자기 자신

    for m in monster:
        if not prev:
            prev = m
            continue

        if m == prev:
            count += 1
            continue

        # 다른 경우
        if count < 4:
            new_mon.extend([prev] * count)
        else:
            score += prev * count

        prev = m
        count = 1

    # 마지막꺼 추가
    if count < 4:
        new_mon.extend([prev] * count)
    else:
        score += prev * count

    if monster != new_mon: # 달라졌으면 다시 체크
        monster = new_mon
        check()


dr = [0, 1, 0, -1] # 오아왼위
dc = [1, 0, -1, 0]

N, R = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(N)]
tr, tc = N//2, N//2 # 탑 위치
score = 0

for _ in range(R):
    d, p = map(int, input().split())

    # 1. 공격 칸 수만큼 공격. 점수
    cr, cc = tr, tc
    for _ in range(p):
        nr = cr + dr[d]
        nc = cc + dc[d]

        if not (0 <= nr < N and 0 <= nc < N):
            break

        score += matrix[nr][nc]
        matrix[nr][nc] = 0

        cr, cc = nr, nc

    # 2. 돌면서 몬스터 있는 것만 1차원 배열에 저장
    monster = flatten()

    # 3. 연속된거 있는지 확인
    check()

    # 4. 숫자끼리 짝 지어주기
    monster = pair()

    # 5. 다시 2차원에 넣어주기
    matrix = draw()

print(score) # 삭제되는 몬스터 개수 * 번호