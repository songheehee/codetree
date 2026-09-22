# 0 = 도로, 1 = 도로 아님
# 메두사 집 -> 공원. 도로 따라서 최단 경로로 이동
# 집, 공원 무조건 도로 위에 있음. 둘 좌표는 무조건 다름
# 전사들 메두사 향해 최단 경로로 이동. 전사는 도로, 비도로 다 이동 가능
# 전사 초기 위치 != 집
# 메두사 전사 움직이기 전에 바라봐서 돌로 만들 수 있음

# 1. 메두사 이동
# 도로 따라 한칸 이동 -> 공원까지 최단 경로. 상하좌우 우선순위
# 전사가 있을 경우 전사 사라짐
# 공원까지 도달하는 경로 없을 수도 있음

# 2. 메두사 시선
# 상하좌우 하나 선택해 바라봄. 전사 가장 많이 볼 수 있는 방향으로. 여러개면 상하좌우 우선순위
# 90도 시야각. 다른 전사에 가려진 전사는 메두사한테 안 보임
# 전사가 메두사랑 같은 행/열 -> 직선으로 가려짐
# 전사가 대각 방향에 있다면 -> 삼각형 모양으로
# 돌로 변하면 현재 턴에는 못 움직이고 다음 턴부터 움직이기 가능
# 같은 칸에 전사 두명 이상 -> 모두 돌로 변함

# 3. 전사 이동
# 메두사를 향해 최대 두칸. 전사 같은 칸 여러명 가능
# 첫번째 이동 : 거리 줄일 수 있는 방향으로 한칸 이동. 상하좌우 우선순위.
# 격자 밖 안됨, 메두사 시야 들어오는 곳 안됨
# 두번째 이동 : 거리 줄일 수 있는 방향으로 한칸 더 이동. 좌우상하 우선순위 (2,3,0,1)

# 4. 전사 공격
# 메두사 칸에 도달하면 사라짐

# 최단 경로는 맨해튼 거리 기준
# 모든 전사가 이동한 거리의 합, 돌이 된 전사 수, 공격한 전사 수
# 공원 도착하면 0 출력 끝
# 메두사 집에서 공원까지 가는 도로 없으면 -1

# 사라진 전사 pop 하기. 메두사 시선 때 in 검사 해야돼서 dict로
# 집 -> 공원 여러 맨해튼 거리 최단 경로 가능한가? 따로 조건 봐야되나?
# 전사들 이동 안 할 수도 있음
# 어차피 같은 위치의 전사면 다 같이 이동
# 한 턴만 기절하니까 그냥 set으로 검사하자

from collections import deque

def move(): # 전사 이동
    new_warriors = dict() # 새로운 전사 위치
    total = 0 # 이동한 거리
    count = 0 # 죽은 전사

    for (r, c), ppl in warriors.items():
        if (r, c) in stone: # 기절 한 애들
            if (r, c) in new_warriors:
                new_warriors[(r, c)] += ppl
            else:
                new_warriors[(r, c)] = ppl
            continue

        min_dist = abs(sr-r) + abs(sc-c) # 현재 메두사와의 거리
        minr, minc = r, c
        warrior_grid[r][c] = 0 # 전 위치 삭제

        # 한번 이동
        for d in range(4): # 0,1,2,3 or 2,3,0,1
            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            # 메두사 시야 들어오는 곳 안됨. 메두사 있는 곳은 갈 수 있음
            dist = abs(sr-nr) + abs(sc-nc)
            if eyes[nr][nc] == 1 or dist >= min_dist: # 거리 좁혀지지 않음
                continue

            min_dist = dist
            minr, minc = nr, nc
            total += ppl # 있는 애들 다 이동
            break

        # 두번 이동
        for d in [2, 3, 0, 1]: # 좌우상하
            nr = minr + dr[d]
            nc = minc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            # 메두사 시야 들어오는 곳 안됨. 메두사 있는 곳은 갈 수 있음
            dist = abs(sr-nr) + abs(sc-nc)
            if eyes[nr][nc] == 1 or dist >= min_dist: # 거리 좁혀지지 않음
                continue

            min_dist = dist
            minr, minc = nr, nc
            total += ppl
            break

        if minr == sr and minc == sc: # 메두사 마주침 -> 사라짐
            count += ppl # 해당 칸 애들 다
        else:
            warrior_grid[minr][minc] += ppl

            if (minr, minc) in new_warriors:
                new_warriors[(minr, minc)] += ppl
            else:
                new_warriors[(minr, minc)] = ppl

    return count, total, new_warriors


def look():
    front = [[(-1, -1), (-1, 0), (-1, 1)],
             [(1, -1), (1, 0), (1, 1)],
             [(-1, -1), (0, -1), (1, -1)],
             [(-1, 1), (0, 1), (1, 1)]]  # 상하좌우. 앞에 세방향만 보면 됨
    max_count = 0  # 전사 수
    max_stone = [] # 돌 된 전사들
    max_eyes = []

    for idx, dirs in enumerate(front):  # 상하좌우 세방향 보기
        eyes = [[0] * N for _ in range(N)]  # 메두사 시야 닿는 곳 체크. 메두사 위치 제외
        q = deque()
        count = 0  # 전사 수
        stone = set() # 돌 된 전사 위치

        # 처음 메두사 기준 앞 세방향 넣기
        for ndr, ndc in dirs:
            nr = sr + ndr
            nc = sc + ndc

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if (nr, nc) in warriors:  # 전사 있음
                count += warriors[(nr, nc)]
                stone.add((nr, nc))
                # 그 뒤 싹 다 막기
                block(idx, nr, nc, eyes)

            q.append((nr, nc))
            eyes[nr][nc] = 1

        while q:
            cr, cc = q.popleft()

            for ndr, ndc in dirs:
                nr = cr + ndr
                nc = cc + ndc

                if not (0 <= nr < N and 0 <= nc < N and not eyes[nr][nc]):
                    continue

                if (nr, nc) in warriors:  # 전사
                    count += warriors[(nr, nc)] # 그 칸에 있는 애 전부
                    stone.add((nr, nc))
                    block(idx, nr, nc, eyes)

                q.append((nr, nc))
                eyes[nr][nc] = 1

        if count > max_count:
            max_count = count
            max_stone = stone
            max_eyes = eyes

    return max_count, max_stone, max_eyes


def block(idx, nr, nc, eyes): # 전사 뒤 막기
    if idx == 0:  # 상하 -> 열 막기
        for i in range(nr - 1, -1, -1):
            if nc == sc:
                eyes[i][nc] = -1

            elif nc < sc:  # 전사가 메두사보다 왼쪽
                for j in range(max(nc - 1 - (nr - 1 - i), 0), nc + 1):
                    eyes[i][j] = -1

            elif nc > sc:  # 전사가 메두사보다 오른쪽
                for j in range(nc, min(nc + 2 + (nr - 1 - i), N)):
                    eyes[i][j] = -1

    elif idx == 1:  # 하
        for i in range(nr + 1, N):
            if nc == sc:
                eyes[i][nc] = -1

            elif nc < sc:  # 전사가 메두사보다 왼쪽
                for j in range(max(nc - 1 - (i - nr - 1), 0), nc + 1):
                    eyes[i][j] = -1

            elif nc > sc:  # 전사가 메두사보다 오른쪽
                for j in range(nc, min(nc + 2 + (i - nr - 1), N)):
                    eyes[i][j] = -1

    elif idx == 2:  # 좌
        for j in range(nc - 1, -1, -1):
            if nr == sr:
                eyes[nr][j] = -1

            elif nr < sr:  # 전사가 메두사보다 위
                for i in range(max(nr - 1 - (nc - 1 - j), 0), nr + 1):
                    eyes[i][j] = -1

            elif nr > sr:  # 전사가 메두사보다 아래
                for i in range(nr, min(nr + 2 + (nc - 1 - j), N)):
                    eyes[i][j] = -1
    else:  # 우
        for j in range(nc + 1, N):
            if nr == sr:
                eyes[nr][j] = -1

            elif nr < sr:  # 전사가 메두사보다 위
                for i in range(max(nr - 1 - (j - nc - 1), 0), nr + 1):
                    eyes[i][j] = -1

            elif nr > sr:  # 전사가 메두사보다 아래
                for i in range(nr, min(nr + 2 + (j - nc - 1), N)):
                    eyes[i][j] = -1


def go_park(): # 집 -> 공원 최단 거리
    q = deque([(sr, sc, [])])
    visited = [[0] * N for _ in range(N)]
    visited[sr][sc] = 1

    while q:
        cr, cc, path = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or matrix[nr][nc] == 1: # 비도로 못감
                continue

            if nr == er and nc == ec:
                return path + [(nr, nc)] # 도착하면 그게 최단

            visited[nr][nc] = visited[cr][cc] + 1
            q.append((nr, nc, path+[(nr, nc)]))

    return False # 공원까지 못 감

dr = [-1, 1, 0, 0] # 상하좌우. 좌우상하 (2,3,0,1)
dc = [0, 0, -1, 1]

N, W = map(int, input().split()) # 마을 크기, 전사 수. 50, 300
sr, sc, er, ec = map(int, input().split()) # 메두사 집, 공원
lst = list(map(int, input().split())) # 전사
matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 도로, 1 = 비도로
warriors = dict() # 좌표 : 몇명. 여러명 가능
warrior_grid = [[0] * N for _ in range(N)] # 전사 위치. 몇명인지

for i in range(0, W*2, 2):
    wr, wc = lst[i], lst[i+1]

    if (wr, wc) in warriors:
        warriors[(wr, wc)] += 1
    else:
        warriors[(wr, wc)] = 1

    warrior_grid[wr][wc] += 1

# 1. 메두사 집 -> 공원 갈 수 있는지. 메두사 경로는 바뀌지 않으니 저장해놓기
path = go_park()

if not path:
    print(-1) # 공원 못감
else:
    turn = 0

    while True:
        turn += 1
        ans = [0, 0, 0] # 전사 이동 거리, 돌 전사, 공격 전사

        # 2. 메두사 경로 따라 이동, 전사 만나면 전사 사라짐
        # 메두사 공원 도착하면 0
        sr, sc = path.pop(0)

        if sr == er and sc == ec:
            print(0)
            break

        if (sr, sc) in warriors: # 전사 있으면 다 사라짐
            warriors.pop((sr, sc), None)
            warrior_grid[sr][sc] = 0

        # 3. 메두사 시선
        count, stone, eyes = look()
        ans[1] += count

        # 4. 전사 이동
        dead, total, warriors = move()
        ans[0] += total
        ans[2] += dead

        print(*ans) # 각 턴마다 모든 전사가 이동한 거리의 합, 돌 전사 수, 공격 전사 수