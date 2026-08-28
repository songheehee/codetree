# 17분 +
# 끝점에서 여태 그려진 드래곤 커브 90도 회전한거 연결
# 단위 정사각형 개수. 꼭지점이 드래곤 커브에 있으면 됨
# 드래곤 커브 직전 모양 기억해야하고 꼭지점을 저장해놔야함
# 꼭지점 체크할 때 visited로 하자
# 진심 무슨 말인지 모르겠다

dr = [0, -1, 0, 1] # 오위왼아
dc = [1, 0, -1, 0]

N = int(input()) # 드래곤 커브 개수
matrix = [[0] * 100 for _ in range(100)] # 최대로 그려놓자
max_r, max_c = 0, 0

for _ in range(N):
    r, c, d, g = map(int, input().split()) # 위치, 방향, 차수
    # 여태 그린거 기억할 배열. 방향을 스택에 넣기
    # 끝점 기억하기
    stk = [d]
    matrix[r][c] = 1
    er, ec = r + dr[d], c + dc[d]
    matrix[er][ec] = 1

    max_r = max(max_r, r, er)
    max_c = max(max_c, c, ec)

    for _ in range(g):
        # 끝에서부터 빼기
        for i in range(len(stk)-1, -1, -1):
            nd = (stk[i] + 1) % 4
            stk.append(nd)

            er, ec = er + dr[nd], ec + dc[nd]
            matrix[er][ec] = 1

            max_r = max(max_r, er)
            max_c = max(max_c, ec)

# 정사각형 개수 세기
visited = [[0] * (max_c+1) for _ in range(max_r+1)]
sdr = [[-1, -1, 0], [-1, -1, 0], [0, 1, 1], [1, 1, 0]] # 왼위, 오위, 왼아, 오아
sdc = [[-1, 0, -1], [0, 1, 1], [-1, -1, 0], [0, 1, 1]]
ans = 0

for i in range(max_r+1):
    for j in range(max_c+1):
        if matrix[i][j]: # 선분 있는 곳만
            visited[i][j] = 1

            for k in range(4):
                kdr = sdr[k]
                kdc = sdc[k]

                count = 0

                for d in range(3):
                    nr = i + kdr[d]
                    nc = j + kdc[d]

                    if not (0 <= nr < max_r+1 and 0 <= nc < max_c+1):
                        continue

                    if matrix[nr][nc] and not visited[nr][nc]:
                        count += 1

                if count == 3:
                    ans += 1

print(ans)