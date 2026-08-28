# 각 칸에 5만큼의 양분. m개의 바이러스
# 1. 바이러스 나이만큼 양분 섭취. 칸에 바이러스 여러개면 어린 바이러스부터. 바이러스 나이+1. 만약 양분 부족하면 죽음
# 2. 죽은 바이러스가 양분으로 변함. 나이 // 2
# 3. 바이러스 번식. 나이가 5의 배수일 경우에만. 인접 8방향 나이 1인 바이러스 생김
# 4. 모든 칸에 양분 초기 매트릭스만큼 추가

dr = [-1, -1, -1, 0, 0, 1, 1, 1]
dc = [-1, 0, 1, -1, 1, -1, 0, 1]

N, M, K = map(int, input().split()) # 배지 크기, 바이러스 개수, 사이클 수
food = [list(map(int, input().split())) for _ in range(N)] # 양분 추가
matrix = [[5] * N for _ in range(N)] # 초기 상태 5
virus = dict() # 키 : 위치, 값 : 나이. 나이 순으로 정렬하기

for _ in range(M):
    r, c, age = map(int, input().split()) # 위치, 나이
    r -= 1
    c -= 1
    if (r, c) in virus:
        virus[(r, c)].append(age)
    else:
        virus[(r, c)] = [age]

for _ in range(K): # 1000
    # 1. 바이러스 나이만큼 양분 섭취. 칸에 바이러스 여러개면 어린 바이러스부터. 바이러스 나이+1. 만약 양분 부족하면 죽음
    for (r, c) in list(virus.keys()): # 100
        ages = sorted(virus[(r, c)])
        new_ages = []
        dead_idx = -1

        for i in range(len(ages)):
            a = ages[i] # 어린 애부터
            if matrix[r][c] >= a:
                matrix[r][c] -= a
                new_ages.append(a+1)

            else:
                dead_idx = i
                break

        if dead_idx != -1:
            dead = ages[dead_idx:]

        if new_ages:
            virus[(r, c)] = new_ages
        else:
            # 죽은 바이러스 빼주기
            virus.pop((r, c), None)

        # 2. 죽은 바이러스가 양분으로 변함. 나이 // 2
        if dead_idx != -1:
            for v in ages[dead_idx:]:
                matrix[r][c] += v//2

    if not virus: # 바이러스 없으면 끝
        break

    # 3. 바이러스 번식. 나이가 5의 배수일 경우에만. 인접 8방향 나이 1인 바이러스 생김
    for (r, c), ages in list(virus.items()):
        for a in ages:
            if a % 5 == 0:
                for d in range(8):
                    nr = r + dr[d]
                    nc = c + dc[d]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue

                    if (nr, nc) in virus:
                        virus[(nr, nc)].append(1)
                    else:
                        virus[(nr, nc)] = [1]

    # 4. 모든 칸에 양분 초기 매트릭스만큼 추가
    for i in range(N):
        for j in range(N):
            matrix[i][j] += food[i][j]

print(sum(len(v) for v in virus.values())) # 살아있는 바이러스 개수