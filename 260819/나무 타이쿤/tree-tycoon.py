# 영양제 : 나무 높이 + 1 / 씨앗 -> 높이 1 나무
# 영양제 이동 시 행, 열 끝과 끝 연결되어있음
# 1. 영양제 이동 규칙에 따라 이동
# 2. 이동 시킨 뒤 땅에 영양제 투입 -> 영양제 사라짐
# 3. 대각선으로 인접한 방향에 높이가 1 이상인 리브로수가 있는 만큼 높이 성장. 격자 벗어나면 안 셈
# 4. 특수 영양제 맞은 곳 제외하고 높이 2 이상인 리브로수는 높이 -2, 해당 위치에 영양제

def inject():
    # 해당 위치 기준 +1
    for r, c in medic:
        matrix[r][c] += 1

    # 3. 대각선으로 리브로수 있는 개수만큼 성장
    ddr = [-1, -1, 1, 1]
    ddc = [-1, 1, -1, 1]

    for r, c in medic:
        for d in range(4):
            nr = r + ddr[d]
            nc = c + ddc[d]

            if not (0 <= nr < n and 0 <= nc < n): # 격자 n,n 주의
                continue

            if matrix[nr][nc]: # 대각선에 있으면
                matrix[r][c] += 1 # 어차피 무조건 1 이상 오르기 때문에 한꺼번에 안 해줘도 됨

def cut():
    global medic
    # 잘라내고 영양제 추가
    new_medic = set()

    for i in range(n):
        for j in range(n):
            if (i, j) in medic: # 영양제 맞은 땅 제외
                continue

            if matrix[i][j] >= 2:
                new_medic.add((i, j))
                matrix[i][j] -= 2

    medic = new_medic # 영양제 바꿔주기


# 영양제 이동 규칙
mdr = [0, -1, -1, -1, 0, 1, 1, 1]
mdc = [1, 1, 0, -1, -1, -1, 0, 1]

n, m = map(int, input().split()) # 격자 크기 (3~15), 총 년 수 (1~100)
matrix = [list(map(int, input().split())) for _ in range(n)] # 나무 높이
medic = {(n-1, 0), (n-2, 0), (n-1, 1), (n-2, 1)} # 영양제 위치. 최초 좌하

for _ in range(m): # 년마다 이동
    d, p = map(int, input().split()) # 방향, 칸수
    d -= 1

    # 1. 영양제 이동
    medic = {((r + mdr[d] * p) % n, (c + mdc[d] * p) % n) for r, c in medic}

    # 2. 영양제 투입
    inject()

    # 4. 리브로수 잘라내기
    cut()


print(sum(map(sum, matrix))) # m년 이후 남아있는 리브로수 총 높이의 합