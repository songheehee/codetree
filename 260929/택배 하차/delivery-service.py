# 1. 택배 투입
# 직사각형 모양. 왼쪽 열 위치, 가로 크기, 세로 크기, 택배 번호 있음
# 중력에 의해 하단으로 떨어짐. 다른 짐 만나면 멈춤
# 무조건 격자 안으로 다 들어옴

# 2. 택배 좌측 하차
# 왼쪽으로 이동했을 때 다른 택배 없는 거 먼저 뺌
# 여러개면 택배 번호 작은 거 먼저 뺌. 하나 뺌!
# 뺀 이후 떨어질 수 있는 애들 떨어짐

# 3. 택배 우측 하차
# 좌측이랑 똑같은데 오른쪽에서 뺌
# 하나 빼고 떨어짐

# 택배 다 뺄 때까지 2, 3 반복
# 택배 못 뺄 수도 있나?

def get_off(side):
    # 택배들 돌면서 옆에 다른 번호 있는지 확인
    min_box = 101 # 제일 작은 택배 번호

    for k, (r, c, h, w) in box.items():
        if c == side: # 제일 끄트머리에 있음
            min_box = min(min_box, k)
            continue

        possible = True # 빠질 수 있음

        for i in range(r, r+h):
            if side == 0:
                crange = range(c) # 앞에 다른 애 없는지
            else:
                crange = range(c+w, N) # 뒤에 다른 애 없는지

            for j in crange:
                if matrix[i][j]:
                    possible = False
                    break

            if not possible:
                break

        if possible:
            min_box = min(min_box, k)

    # 박스 빼기
    if min_box < 101:
        r, c, h, w = box.pop(min_box, None)

        for i in range(r, r+h):
            for j in range(c, c+w):
                matrix[i][j] = 0

        down(r, c, w)

        return min_box


def down(r, c, w): # 빠진 곳 찾아보고 내려올 수 있는 거 있으면 내려오기
    chk = set() # 내려올 수 있는 택배들

    for i in range(r-1, -1, -1):
        for j in range(N):
            if matrix[i][j]:
                chk.add(matrix[i][j])

    for num in chk: # 내려올 수 있는 애들 지우고 다시 그리기
        nr, nc, nh, nw = box.pop(num, None)

        for i in range(nr, nr+nh):
            for j in range(nc, nc+nw):
                matrix[i][j] = 0

        gravity(num, nr, nc, nh, nw)


def gravity(k, r, c, h, w):
    pointer = r+h # 마지막 위치
    stop = False

    while pointer < N:
        for j in range(c, c+w):
            if matrix[pointer][j]:
                stop = True
                break

        if stop:
            break

        pointer += 1

    # 마지막 위치 정해졌으면 그려주기
    for i in range(pointer-h, pointer):
        for j in range(c, c+w):
            matrix[i][j] = k

    box[k] = (pointer-h, c, h, w)


N, D = map(int, input().split()) # 격자 크기, 택배 개수. 50, 100
matrix = [[0] * N for _ in range(N)] # 택배 번호 적기
box = dict() # 택배 번호 : 택배 위치, height, width

for _ in range(D):
    k, h, w, c = map(int, input().split())
    c -= 1

    # 1. 택배 투입 -> 중력
    gravity(k, 0, c, h, w)

while box:
    # 3. 택배 좌측
    ans = get_off(0)
    if ans:
        print(ans)

    # 4. 택배 우측
    ans = get_off(N-1)
    if ans:
        print(ans)