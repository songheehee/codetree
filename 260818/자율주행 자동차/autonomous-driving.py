# 1. 현재 방향 기준으로 왼쪽으로 한번도 간적 없다면 좌회전 +1
# 2. 왼쪽이 인도거나 이미 방문했으면 좌회전하고 1번 다시 시도
# 3. 2번에서 4방향 다 확인했으나 전진 불가 -> 바라보는 방향 유지한 채로 한칸 후진 -> 다시 1번
# 4. 3번 과정 시도 but 뒷 공간 인도여서 후진 못한다면 작동 멈춤
# 거쳐간 도로의 총 면적. 처음 위치 포함

dr = [-1, 0, 1, 0] # 북동남서
dc = [0, 1, 0, -1]

n, m = map(int, input().split()) # 도로 세로, 가로
x, y, d = map(int, input().split()) # 자동차 초기 위치, 방향
matrix = [list(map(int, input().split())) for _ in range(n)] # 0=도로, 1=인도
# 첫번째 행, 마지막 행, 첫번째 열, 마지막 열 항상 인도
visited = [[0] * m for _ in range(n)]
visited[x][y] = 1

# 4방향 돌았는지 확인 -> for문 돌린 다음 break
cr, cc = x, y

while True:
    for i in range(4):
        d = (d-1) % 4 # 좌회전
        nr = cr + dr[d]
        nc = cc + dc[d]

        if not (0 <= nr < n and 0 <= nc < m):
            continue

        if visited[nr][nc] or matrix[nr][nc] == 1: # 인도거나 이미 방문
            continue

        # 한칸 전진
        visited[nr][nc] = 1
        cr, cc = nr, nc
        break

    else: # 4방향 모두 확인했으나 전진 불가
        # 후진하기
        nr = cr - dr[d]
        nc = cc - dc[d]

        if not (0 <= nr < n and 0 <= nc < m and matrix[nr][nc] == 0):
            break

        visited[nr][nc] = 1
        cr, cc = nr, nc

print(sum(map(sum, visited)))