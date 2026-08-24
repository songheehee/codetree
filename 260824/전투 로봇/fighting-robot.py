# 전투로봇은 자신의 레벨보다 큰 몬스터 칸은 지나칠 수 없고 나머지 칸은 가능
# 전투로봇은 자신보다 레벨 낮은 몬스터만 없앨 수 있음. 레벨 같은 몬스터는 못 없앰 but 지나칠 수는 있음
# 힙큐로 할까? 리스트 인덱스로 할까? 딕셔너리로 할까?

# 1. 몬스터 없앨 수 있으면 없애러 감
# 2. 없앨 수 있는 몬스터 여러개면 가장 가까운 애
#   - 지나야하는 칸 개수의 최소값
#   - 가까운 거리도 여러명이면 가장 위 -> 가장 왼쪽
#   - 없앨 수 없는 몬스터 없으면 일 끝
# 몬스터 없애면 해당 칸 빈칸
# 레벨과 같은 수의 몬스터를 없애면 레벨 + 1
from collections import deque

def search():
    # 다 탐색해서 제일 가까운 데로. 장애물 있을 수 있으니까
    # 가까운 거리도 여러명이면 가장 위 -> 가장 왼쪽
    global time

    visited = [[0] * n for _ in range(n)]
    q = deque([(sr, sc)])
    visited[sr][sc] = 1

    mr, mc, mdist = -1, -1, n*n

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < n and 0 <= nc < n):
                continue

            if visited[nr][nc] or matrix[nr][nc] > level: # 몬스터 레벨보다 크면 못감
                continue

            if (nr, nc) in low:
                if (mdist, mr, mc) > (visited[cr][cc], nr, nc):
                    mdist, mr, mc = visited[cr][cc], nr, nc

            visited[nr][nc] = visited[cr][cc] + 1
            q.append((nr, nc))

    # 시간 더해주기
    if mr != -1 and mc != -1:
        time += mdist
    return (mr, mc)

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

n = int(input()) # 2~20
matrix = [list(map(int, input().split())) for _ in range(n)]
# 9 = 전투로봇. 초기레벨 = 2. 몬스터 1~6레벨 0은 빈칸

# 전투로봇 위치 파악
# 몬스터 위치, 레벨 파악
sr, sc, level = -1, -1, 2
monster = [[] for _ in range(7)] # 최대 레벨 6

for i in range(n):
    for j in range(n):
        if matrix[i][j] == 9:
            sr, sc = i, j
            matrix[i][j] = 0
        elif matrix[i][j]: # 몬스터
            lv = matrix[i][j]
            monster[lv].append((i, j))

time = 0
kill = 0  # 몬스터 죽인 개수

while True:
    # 로봇보다 > 레벨 낮은 몬스터 중에 제일 가까운 곳으로 이동
    low = [loc for lst in monster[1:level] for loc in lst] # flatten
    low = set(low)

    if not low: # 레벨 낮은 몬스터 없으면 끝
        break

    sr, sc = search() # 위치 이동

    if sr == -1 and sc == -1:
        break

    kill += 1

    if kill == level:
        kill = 0 # 초기화 되는거 맞겠지?
        level += 1

    # 해당 몬스터 없애주기
    lv = matrix[sr][sc]
    monster[lv].remove((sr, sc))
    matrix[sr][sc] = 0

print(time) # 전투로봇 일 끝날 때까지 걸린 시간