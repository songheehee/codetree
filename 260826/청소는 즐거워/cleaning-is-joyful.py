import sys
sys.stdin = open("input.txt", "r")

# 66분
# 정가운데 격자에는 먼지 없음. 정가운데에서 시작. 항상 왼쪽 위에서 끝
# 빗자루가 이동할 때마다 빗자루가 이동한 위치의 격자에 있는 먼지 함께 이동 << 뭔 소리냐
# 이동한 먼지는 기존의 먼지 양에 더해짐. 빗자루가 이동한 위치는 0
# a는 다른 격자에 이동한 먼지의 양을 모두 합친 것을 빼고 남은 거 << 뭔 말임
# 비율 곱해줄 때 소수점 버림
# 1 -> 1 -> 2 -> 2

dr = [0, 1, 0, -1] # 왼아오위
dc = [-1, 0, 1, 0]

adr = [-2, -1, -1, 0, 0, 0, 0, 1, 1, -1]
adc = [0, -1, 1, -2, -1, 1, 2, -1, 1, 0]
mul = [0.05, 0.1, 0.1, 0.02, 0.07, 0.07, 0.02, 0.01, 0.01]

N = int(input())
matrix = [list(map(int, input().split())) for _ in range(N)]
sr, sc = N // 2, N // 2
didx = 0 # 시작 인덱스
ans = 0 # 격자 밖으로 떨어진 먼지
rotate = 1 # 같은 방향 갈 개수
count = 0 # 두개 되면 방향 바꿔주기

while True:
    for _ in range(rotate):
        nr = sr + dr[didx]
        nc = sc + dc[didx]

        ash = matrix[nr][nc] # 먼지 양
        matrix[nr][nc] = 0

        total_ash = 0 # 총 퍼져나간 먼지 양
        for i in range(10):
            if didx == 0:
                ar = nr + adc[i]
                ac = nc + adr[i]
            elif didx == 1:
                ar = nr - adr[i]
                ac = nc - adc[i]
            elif didx == 2:
                ar = nr - adc[i]
                ac = nc - adr[i]
            else:
                ar = nr + adr[i]
                ac = nc + adc[i]

            if not (0 <= ar < N and 0 <= ac < N):
                if i == 9:
                    ans += ash - total_ash
                else:
                    total_ash += int(ash * mul[i]) # 나간 먼지도 계산
                    ans += int(ash * mul[i])
                continue

            if i == 9:
                matrix[ar][ac] += ash - total_ash
            else:
                matrix[ar][ac] += int(ash * mul[i])
                total_ash += int(ash * mul[i])

        sr, sc = nr, nc

        if sr == 0 and sc == 0:
            break

    if sr == 0 and sc == 0:
        break

    # 방향 바꿔주기
    didx = (didx + 1) % 4
    count += 1

    if count == 2:
        rotate += 1
        count = 0


print(ans) # 격자 밖으로 떨어진 먼지의 총합