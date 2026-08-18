'''
소요시간 : 22분
수행 시간: 1421ms / 메모리 25MB

이해 및 구상 (5분) - 구현 및 디버깅 (17분 30초)

[구상]
    - 방화벽 3개 무조건 설치. 빈칸인 곳 중 3개 고르는 거라 조합이라고 생각함 -> 2차원 배열이라 visited로 처리
    - 8*8 이라 조합이 가능하나 bfs도 돌려야 해서 시간 초과가 조금 걱정됐지만 진행함

[구현]
    - 3개 고르는 것은 dfs로, 불이 퍼지는 건 bfs로 구현함
    - 이 과정에서 이중 for문을 많이 돌렸는데, 확실히 시간이 오래 걸리긴 함. 근데 다른 방법이 떠오르지 않았음...
    - n, m 크기도 8이라서 돌아갈 수 있었던듯. 만약 숫자가 더 커지면 다른 방법으로 풀어야할 것 같음

[리팩토링]
    - dfs에서 이중 for문 돌면서 고르지 않고 빈칸인 곳의 리스트를 만들어서 거기서 세개 뽑아도 됐을듯. 최대 64개라 이게 나을 것 같음
    - 마지막에 안전 영역을 for문 돌면서 세지 말고 빈칸 개수 미리 세놓고 불 번질 때마다 -1 하기
'''
# 불은 상하좌우로 '모두' 번짐. 방화벽 뚫을 수는 없음
# 방화벽 추가로 3개 설치 가능. 불 있는 위치에는 불가
# 불이 퍼지지 않는 영역이 최대일 때 크기
from collections import deque

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

def bfs():
    new_matrix = [row[:] for row in matrix] # 원본꺼 안 건드리기

    for r, c in select:
        new_matrix[r][c] = 1 # 방화벽

    q = deque()
    q.extend(fire)

    fire_count = 0

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < n and 0 <= nc < m):
                continue

            if new_matrix[nr][nc] == 0:
                new_matrix[nr][nc] = 2 # 불
                q.append((nr, nc))
                fire_count += 1

    return fire_count


def dfs(start): # 방화벽 설치할 곳 3개 고르기. 3중 for문 돌려도 됨
    global max_area

    if len(select) == 3:
        # 방화벽 설치 후 불 퍼트리기
        count = bfs()
        max_area = max(max_area, safe_count - count - 3)
        return

    for i in range(start, len(wall)):
        select.append(wall[i])
        dfs(i+1)
        select.pop()


n, m = map(int, input().split()) # 3~8
matrix = [list(map(int, input().split())) for _ in range(n)]
# 2 = 불, 1 = 방화벽, 0 = 빈칸
fire = []
wall = [] # 방화벽 넣을 수 있는 위치

for i in range(n):
    for j in range(m):
        if matrix[i][j] == 2:
            fire.append((i, j))
        elif matrix[i][j] == 0:
            wall.append((i, j))

select = []
max_area = 0
safe_count = len(wall)

dfs(0)

print(max_area)