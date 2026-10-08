# 좌상단 1,1

# 1. 택배 투입
# 직사각형 모양. 각 택배 번호 있음
# 중력에 의해 밑으로 떨어짐. 다른 짐 있으면 멈춤
# 모든 택배 무조건 다 격자 안으로 들어옴

# 2. 택배 하차 (좌측)
# 왼쪽에 다른 택배 없는 애들 하차
# 여러개일 경우 택배 번호 작은 순
# 하차 이후 떨어질 수 있는 애들 떨어짐

# 3. 택배 하차 (우측)

# 택배 모두 하차할 때까지 2, 3 반복
# 하차되는 택배 번호 순서대로 출력 (엔터)

def erase(idx): # 지워주기
    r, c, h, w = box[idx]
    box.pop(idx, None)  # 나간 택배
    ans.append(idx)

    for i in range(r, r+h):
        for j in range(c, c+w):
            matrix[i][j] = 0

    down(r, c, w)


def down(r, c, w): # 위로 싹 보기
    hubo = set() # 내려올 수 있는 애들

    for i in range(r-1, -1, -1):
        for j in range(c, c+w):
            if matrix[i][j]:
                hubo.add(matrix[i][j])

    for idx in hubo:
        r, c, h, w = box[idx]

        for j in range(c, c+w):
            if matrix[r+h][j]:
                break
        else: # 밑에 다 빔
            # 전 위치 삭제
            for i in range(r, r + h):
                for j in range(c, c + w):
                    matrix[i][j] = 0

            gravity(idx, r, c, h, w) # 내리고 그려주기
            down(r, c, w) # 얘 위도 보기


def get_off(end):
    for idx, (r, c, h, w) in sorted(box.items()):
        if c == end or c+w == end+1:
            return idx

        if end == 0:
            jrange = range(c)
        else:
            jrange = range(c+w, N)

        stop = False
        for i in range(r, r+h):
            for j in jrange: # 앞이나 뒤에 다 없으면 뺄 수 있음
                if matrix[i][j]:
                    stop = True
                    break
            if stop:
                break
        else:
            return idx  # 박스 인덱스


def gravity(k, r, c, h, w):
    sr = r + h # 끝점 기준
    stop = False

    while sr < N and not stop:
        for j in range(c, c+w):
            if matrix[sr][j]:
                stop = True
                break
        else:
            sr += 1

    for i in range(sr-h, sr):
        for j in range(c, c+w):
            matrix[i][j] = k

    box[k] = sr-h, c, h, w


N, D = map(int, input().split()) # 격자, 택배 개수. 50, 100
matrix = [[0] * N for _ in range(N)] # 택배 번호 표시
box = dict()
ans = [] # 하차되는 택배 번호

for _ in range(D):
    k, h, w, c = map(int, input().split())
    c -= 1
    r = 0

    # 1. 택배 떨어트리기
    gravity(k, r, c, h, w)

# 택배 빼기
while box:
    # 2. 택배 좌측
    idx = get_off(0)
    erase(idx)

    if not box: # 택배 다 하차
        break

    # 3. 택배 우측
    idx = get_off(N-1)
    erase(idx)

for num in ans:
    print(num)