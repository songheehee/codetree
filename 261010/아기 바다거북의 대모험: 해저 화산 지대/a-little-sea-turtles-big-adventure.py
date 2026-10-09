# 안식처는 N-1, N-1
# 최대 100턴 동안 진행

# 1. 바다거북 이동 - 순서대로
# 1번부터 한 마리씩 이동
# 최단 경로 탐색 -> 한칸 이동
# 산호초(1), 다른 바다거북, 화석 - 이동 불가
# 우하좌상 우선순위
# 최단 경로 없다면 이동하지 않음
# 안식처에 도착하면 즉시 사라짐. 도착 시간 기록
# 화산 있는 칸 진입 가능

# 2. 화산 압력 증가
# 화산 마그마 +10

# 3. 화산 분출, 연쇄 반응
# 분출 임계치 이상이면 분출
# 1) 열기 전파 - 분출 임계치 만큼의 열기 발생
# 열기 4방으로 뻗어나가는데 한칸 이동할 때마다 열기 절반
# 산호초 만나거나 열기 0 되면 끝
# 2) 연쇄 반응
# 분출하지 않은 화산 중 마그마 + 열기 >= 분출 임계치 되면 즉시 분출
# 마그마 압력 수치 자체 증가는 아님
# 새로 분출하는 화산 없을 때까지
# 3) 바다거북 화석화
# 열기 합이 20 이상이면 거북이 화석됨 - 위치 고정

# 4. 환경 초기화
# 모든 열기 정보 사라짐
# 분출 일으킨 화산 마그마 0

# M개의 줄에 걸쳐 각 바다거북 (id 순) 안식처에 도착한 턴 번호 출력
# 100턴 안에 도착하지 못했거나 화석 됐으면 -1

# 안식처, 바다거북 초기 위치, 화산 위치 != 산호초
# 바다거북 초기 위치 안 겹침. 안식처도 아님
# 화산 위치도 안 겹침. 안식처도 아님
# 바다거북과 화산 초기 위치 안 겹침

from collections import deque

def erupt():
    q = deque()
    out = set() # 분출한 화산들

    for (r, c), p in volcano.items():
        if magma[r][c] >= p:
            hot[r][c] = p
            q.append((r, c, p//2))
            out.add((r, c))

    while q:
        cr, cc, cp = q.popleft()

        for d in range(4): # 4방으로 뻗어나감
            sr, sc, sp = cr, cc, cp

            while sp > 0: # 열기 남아있을 때까지
                nr = sr + dr[d]
                nc = sc + dc[d]

                if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] != 1): # 벽/산호초
                    break

                hot[nr][nc] += sp

                if (nr, nc) in volcano and (nr, nc) not in out and magma[nr][nc] + hot[nr][nc] >= volcano[(nr, nc)]: # 분출하지 않은 화산이면서 마그마+열기가 임계치 넘은 애들 연쇄 작용
                    np = volcano[(nr, nc)]
                    hot[nr][nc] += np
                    q.append((nr, nc, np//2))
                    out.add((nr, nc))

                sr, sc = nr, nc
                sp //= 2

    # 마그마 초기화
    for r, c in out:
        magma[r][c] = 0


def move(r, c):
    visited = [[0] * N for _ in range(N)]
    q = deque([(r, c, None)])
    visited[r][c] = 1

    while q:
        cr, cc, first = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or matrix[nr][nc] or (nr, nc) in turtle: # 산호초, 화석, 다른 거북이 위치 못감
                continue

            if nr == N-1 and nc == N-1: # 안식처 도착
                return first if first else (nr, nc)

            q.append((nr, nc, first if first else (nr, nc)))
            visited[nr][nc] = visited[cr][cc] + 1

    return r, c # 안식처 못 가면 원래 위치


dr = [0, 1, 0, -1] # 우하좌상
dc = [1, 0, -1, 0]

N, T, V = map(int, input().split()) # 격자, 거북 수, 화산 수
matrix = [list(map(int, input().split())) for _ in range(N)] # 1 = 산호초. 마이너스 = 화석
turtle = [None] + [tuple(map(int, input().split())) for _ in range(T)] # 거북 위치. 순서대로 1번부터
volcano = dict() # 화산 위치 : 임계치
magma = [[0] * N for _ in range(N)] # 마그마
ans = [-1] * (T+1) # 1번부터

for _ in range(V):
    r, c, p = map(int, input().split())
    volcano[r, c] = p

for turn in range(1, 101): # 100턴까지
    # 1. 바다거북 순서대로 이동
    for i in range(1, T+1):
        if turtle[i]: # 살아있으면
            r, c = move(*turtle[i])

            if r == N-1 and c == N-1: # 안식처 도착
                turtle[i] = None
                ans[i] = turn
            else:
                turtle[i] = r, c

    # 2. 화산 압력 증가
    for r, c in volcano.keys():
        magma[r][c] += 10

    # 3. 화산 분출, 연쇄 반응
    hot = [[0] * N for _ in range(N)]  # 열기
    erupt()

    # 4. 바다거북 화석
    for i in range(1, T+1):
        if turtle[i]: # 살아있는 애 중에
            r, c = turtle[i]

            if hot[r][c] >= 20:
                turtle[i] = None
                matrix[r][c] = -1 # 화석 표시

    # 바다거북 다 나가면 종료
    if turtle[1:].count(None) == T:
        break

for n in ans[1:]:
    print(n)