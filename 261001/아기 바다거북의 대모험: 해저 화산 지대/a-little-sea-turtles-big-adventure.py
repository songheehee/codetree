# T 마리의 바다 거북
# 안식처를 향해 가는데 화산들이 있음
# 안식처는 N-1, N-1 좌표에 있음 (우하단)

# 1. 바다거북 이동 - 순서대로
# 순서대로 한 마리씩 이동
# 안식처까지 최단 경로
# 산호초, 바다거북, 화석 통과 불가
# 우하좌상 우선순위
# 최단 경로 없으면 제자리
# 안식처 도착하면 즉시 제외. 해당 턴이 도착 시간
# 해저 화산으로 갈 수 있음

# 2. 화산 압력 증가
# 화산 마그마 +10

# 3. 화산 분출 -> 연쇄 반응
# 분출 임계치 P 이상인 화산 분출
# 1) 열기 전파
# 열기는 4방으로 뻗어 나가며, 한칸 이동할 때마다 열기의 절반
# 산호초 만나거나 열기 0 되면 전파 끝
# 2) 연쇄 반응
# 분출되지 않은 화산 중 전파돼서 마그마+열기 분출 임계치 넘은 애들도 즉시 분출 시작
# 실제 마그마 압력 수치 자체를 증가시키지 않는다 << 뭔 소리
# 새로 분출하는 화산이 없을 때까지
# 3) 바다거북 화석
# 살아있는 거북이가 위치한 곳의 열기 합이 20 이상이면 화석 됨. 그 자리 고정

# 4. 환경 초기화
# 열기 정보 사라짐
# 분출 일으킨 화산 마그마 0 됨

# 안식처, 바다거북 초기 위치, 화산 위치 != 산호초
# 바다거북 초기 위치 겹치지 않음 != 안식처
# 화산 != 안식처. 화산 위치 서로 겹치지 않음
# 바다거북 초기 위치 != 화산
# 시뮬레이션 최대 100턴

# 마그마랑 열기 따로 관리
# 화산 딕셔너리로 할까 그리드로 할까. 매트릭스에 같이 할까
# 화석 != 산호초. 다른 번호로 관리해야됨
# 다음 칸 화석 잘 가는지, 다음 칸 바로 안식처 잘 가는지

from collections import deque


def spread():
    done = set()  # 이미 분출한 화산 위치
    q = deque()  # 분출할 화산들, 열기

    for (r, c), p in volcano.items():
        if magma[r][c] >= p:
            hot_grid[r][c] = p
            magma[r][c] = 0  # 분출한 화산 마그마 0
            done.add((r, c))

            if p // 2:
                q.append((r, c, p // 2))

    while q:  # 분출할 화산 남아있을 때까지
        cr, cc, cp = q.popleft()

        for d in range(4):
            sr, sc = cr, cc
            hot = cp

            while True:
                nr = sr + dr[d]
                nc = sc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    break

                if matrix[nr][nc] == 1 or hot == 0:  # 산호초 만나거나 열기 0 되면 끝
                    break

                hot_grid[nr][nc] += hot

                hot //= 2
                sr, sc = nr, nc

                # 분출되지 않은 화산 중 임계치 넘은 애도 추가
                if (nr, nc) in volcano and (nr, nc) not in done and magma[nr][nc] + hot_grid[nr][nc] >= volcano[
                    (nr, nc)]:
                    np = volcano[(nr, nc)]
                    hot_grid[nr][nc] += np
                    magma[nr][nc] = 0
                    done.add((nr, nc))

                    if np // 2:
                        q.append((nr, nc, np // 2))


def fossil():
    for i in range(1, T + 1):
        if turtle[i] is None:
            continue

        r, c = turtle[i]

        if hot_grid[r][c] >= 20:
            turtle[i] = None
            arrive[i] = -1
            matrix[r][c] = -1  # 화석 표시


def move(r, c):
    visited = [[0] * N for _ in range(N)]
    q = deque([(r, c, None)])  # 최단 경로의 첫칸
    visited[r][c] = 1

    while q:
        cr, cc, first = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or matrix[nr][nc] or (nr, nc) in turtle:  # 산호초, 화석, 바다거북 불가
                continue

            if nr == N - 1 and nc == N - 1:  # 안식처 도착
                return True, first if first else (nr, nc)

            q.append((nr, nc, first if first else (nr, nc)))
            visited[nr][nc] = visited[cr][cc] + 1

    # 최단 경로 존재하지 않음
    return False, (r, c)


dr = [0, 1, 0, -1]  # 우하좌상
dc = [1, 0, -1, 0]

N, T, V = map(int, input().split())  # 격자, 바다거북 수, 화산 수. 20, 10, 10
matrix = [list(map(int, input().split())) for _ in range(N)]  # 1 = 산호초. -1 = 화석
turtle = [None] + [tuple(map(int, input().split())) for _ in range(T)]  # 바다거북 초기 위치. 1번부터
volcano = dict()  # 화산 위치 : 임계치
magma = [[0] * N for _ in range(N)]  # 현재 마그마
arrive = [-1] * (T + 1)  # 각 거북이 도착한 턴 번호. 도착 못 했을 때 -1

for _ in range(V):
    r, c, p = map(int, input().split())
    volcano[(r, c)] = p

for turn in range(1, 101):  # 100턴까지 진행
    # 1. 거북이 순서대로 이동
    for i in range(1, T + 1):
        if turtle[i]:  # 남은 애들만
            can, (r, c) = move(*turtle[i])

            if can:  # 최단 거리 움직일 수 있으면
                if r == N - 1 and c == N - 1:  # 안식처 도착
                    turtle[i] = None
                    arrive[i] = turn
                else:
                    turtle[i] = (r, c)  # 새로운 위치

    # 2. 마그마 +10
    for r, c in volcano.keys():
        magma[r][c] += 10

    # 3. 열기 전파
    hot_grid = [[0] * N for _ in range(N)]  # 열기
    spread()

    # 4. 거북이 화석화
    fossil()

    # 다 나가면 끝
    if arrive[1:].count(-1) == 0:
        break

# 각 거북이 안식처에 도착한 턴 번호. 화석되거나 도착 못하면 -1
for num in arrive[1:]:
    print(num)