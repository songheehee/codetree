# 인덱스를 생각하고도!!! N, M 잘못 해서 인덱스 오류남 ㅡㅡ 스튜핏

# 12시 방향부터 m개의 정수가 시계방향 순서대로
# 각 원판의 회전은 독립적
# x의 배수일 경우 회전
# 회전시킨 이후 원판에 수가 남아있으면 인접하면서 숫자가 같은 수 지움
# 지워지는 수가 없으면 원판 전체에 적힌 수의 평균을 구해서 정규화 << ???
# 전체 원판 평균보다 큰 수는 -1, 작은 수는 +1
from collections import deque

def delete():
    global circles
    # 회전시킨 이후 원판에 수가 남아있으면 인접하면서 숫자가 같은 수 지움
    result = False # 하나도 안 지워지면 정규화해줘야됨
    new_circle = [circles[i].copy() for i in range(N)]

    # 같은 원판 양옆, 양옆 원판 같은 위치
    # 하나의 숫자당 양옆, 앞뒤 확인
    for i in range(N):
        for j in range(M):
            if circles[i][j] == 0: # 없으면 확인 X
                continue

            if i > 0: # 앞 비교
                if circles[i][j] == circles[i-1][j]:
                    new_circle[i][j] = new_circle[i-1][j] = 0
                    result = True

            if i < N-1: # 뒤 비교
                if circles[i][j] == circles[i+1][j]:
                    new_circle[i][j] = new_circle[i+1][j] = 0
                    result = True

            # 같은 원판 비교
            if circles[i][j] == circles[i][j-1]:
                new_circle[i][j] = new_circle[i][j-1] = 0
                result = True

            if j == M-1: # 0이랑 비교
                if circles[i][j] == circles[i][0]:
                    new_circle[i][j] = new_circle[i][0] = 0
                    result = True
            else:
                if circles[i][j] == circles[i][j+1]:
                    new_circle[i][j] = new_circle[i][j+1] = 0
                    result = True

    circles = new_circle
    return result


def mean(): # 정규화
    # 평균 구하고 빼주기
    avg = sum(map(sum, circles)) // (N*M - sum(row.count(0) for row in circles))

    for i in range(N):
        for j in range(M):
            if circles[i][j] == 0:
                continue

            if circles[i][j] > avg:
                circles[i][j] -= 1
            elif circles[i][j] < avg:
                circles[i][j] += 1


N, M, Q = map(int, input().split()) # 원판의 개수, 원판 내의 수 개수, 회전 횟수. <= 50
circles = [deque(map(int, input().split())) for _ in range(N)]

for _ in range(Q):
    X, D, K = map(int, input().split()) # 원판 종류 (배수), 방향 (0=시계, 1=반시계), 회전 칸수

    # 회전
    for i in range(0, N+1, X):
        if i == 0:
            continue

        for _ in range(K):
            if D == 0: # 시계
                circles[i-1].rotate(1)
            else:
                circles[i-1].rotate(-1)

    # 숫자 삭제
    result = delete()

    # 숫자 안 남아있으면 끝내기
    if sum(row.count(0) for row in circles) == N*M: # 남아있는 수가 없음
        break

    # 정규화
    if not result: # 지워지는 수가 없었다면
        mean()

print(sum(map(sum, circles))) # 원판을 q번 회전시킨 후 남아있는 수의 합