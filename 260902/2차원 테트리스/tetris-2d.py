# 타일 종류 3개. 1=하나, 2=열 두개, 3=행 두개
# 파란색 보드 -> 빨강은 오른쪽으로 쭉, 노랑은 아래로 쭉
# 노랑 : 다 채워지면 그 행 지워짐, 빨강 : 열 지워짐 (꼭 끝자리 아니어도 됨)
# 지워질 때마다 1점. 여러줄 한번에 지워질 수 있음
# 연한 부분에 타일이 위치하게 되면 열/행만큼 지워짐 << 뭔 말
# 다 채워진거 없앤 후에 연한 칸 처리해야됨
# 0부터 채우고 끝 두개가 연한 블록

def fill(matrix, type, col):
    if type == 2: # 열 두칸
        lr = 0
        for i in range(5, -1, -1):  # 마지막 인덱스 찾아주기
            if matrix[i][col] == 1 or matrix[i][col+1] == 1:
                lr = i + 1
                break

        matrix[lr][col] = matrix[lr][col+1] = 1

    else:
        lr = 0
        for i in range(5, -1, -1):  # 마지막 인덱스 찾아주기
            if matrix[i][col] == 1:
                lr = i + 1
                break

        if type == 1:
            matrix[lr][col] = 1
        else: # 행 두칸
            matrix[lr][col] = matrix[lr+1][col] = 1

def delete(matrix):
    global score

    for i in range(3, -1, -1): # 거꾸로 삭제
        if sum(matrix[i]) == 4: # 해당 열 삭제
            score += 1

            matrix.pop(i)
            matrix.append([0] * 4)

def check(matrix):
    for i in range(5, 3, -1): # 얘도 끝에서부터
        if sum(matrix[i]) > 0: # 해당 칸에 타일이 있음
            matrix.pop(0) # 맨 앞 삭제
            matrix.append([0] * 4)


K = int(input()) # 블록 입력 횟수
red = [[0] * 4 for _ in range(6)]
yellow = [[0] * 4 for _ in range(6)] # 4,5 행
score = 0

for _ in range(K): # 10,000
    T, R, C = map(int, input().split()) # 블록 종류, 위치

    # 1. 빨/노 칸 채우기
    if T == 1:
        fill(red, 1, R)
    elif T == 2:
        fill(red, 3, R)
    elif T == 3:
        fill(red, 2, R)

    fill(yellow, T, C)

    # 2. 다 채워진 열/행 확인 -> 없애기 (점수)
    delete(red)
    delete(yellow)

    # 3. 연한 블록 확인
    check(red)
    check(yellow)

print(score) # 얻는 점수
print(sum(map(sum, red)) + sum(map(sum, yellow))) # 타일 있는 칸의 개수