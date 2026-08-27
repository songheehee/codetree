# 경사로는 높이 차이가 1이 나는 보도블럭에 설치 가능, 낮은 칸에 설치
# 경사로의 길이 L 동안 바닥에 접촉해야하며 경사로가 놓인 보도블럭의 높이는 모두 같아야함
# 행/열 경사로 여러개 깔 수 있으나 이미 깐 곳은 ㄴㄴ

# 놓을 수 없는 경우
# 높이 차이가 1보다 큼
# 경사로의 길이만큼 낮은 칸의 보도블럭이 없음
# 경사로 놓은 곳

def walk(): # 가다가 높이 1보다 크면 그 행 안됨
    global possible

    for i in range(N):
        row = matrix[i]
        prev = -1  # 직전 높이
        count = 1  # 직전이랑 높이 같은 블럭 개수

        for j in range(N):
            if visited[i][j]:
                continue

            height = row[j]
            if j == 0:
                prev = height
                continue

            if height > prev + 1 or height < prev - 1:
                break

            if height == prev:
                count += 1

            elif height == prev+1:
                if count >= L:
                    prev = height
                    count = 1
                else:
                    break

            elif height == prev-1:
                # 남은 땅이 L만큼 있어야하고 높이가 같아야함
                if j+L > N or row[j:j+L].count(row[j]) < L:
                    break

                for k in range(L): # 경사로 설치
                    visited[i][j+k] = 1

                prev = height
                count = 0

        else: # break 안 만났으면 끝까지 갈 수 있음
            possible += 1


N, L = map(int, input().split()) # 매트릭스 크기, 경사로 길이
matrix = [list(map(int, input().split())) for _ in range(N)]
visited = [[0] * N for _ in range(N)] # 경사로 설치
possible = 0

walk()

matrix = list(zip(*matrix))
visited = [[0] * N for _ in range(N)]
# 열 확인
walk()

print(possible) # 지나갈 수 있는 열과 행 총 개수