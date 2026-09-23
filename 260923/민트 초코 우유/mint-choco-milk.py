# N*N 책상 배열. 각 책상에는 한명의 학생
# 1,1 부터 시작 -> 총 N*N명의 학생
# 각 학생은 민트, 초코, 우유 중 하나의 음식 신봉
# T = 민트, C = 초코, M = 우유
# CM (초코우유), MT (민트우유), CT (민트초코), CMT (민트초코우유)
# 영향 받아서 초코우유, 민트우유, 민트초코, 민트초코우유 신봉할 수도 있음

# 1. 아침 시간
# 신앙심 +1

# 2. 점심 시간
# 인접한 학생들과 신봉 음식이 완전히 같은 경우 그룹 형성
# 대표자 한명 선정
# - 신앙심이 가장 큰 사람
# - 동일한 경우 행작 열작 (r 작, c 작)
# 대표자 제외 각자 신앙심 1씩 대표자에게 넘김 - 대표자 신앙 += 그룹원수-1. 나머지 -1

# 3. 저녁 시간
# 대표자들이 신앙심 전파
# 단일 음식, 이중 조합, 삼중 조합 순으로 전파
# - 대표자 신앙심 높은 순
# - 대표자 행 번호 작은 순
# - 대표자 열 번호 작은 순
# 전파자는 신앙심 1만 남기고 나머지를 간절함으로 바꿔 전파에 사용
# 신앙심을 4로 나눈 나머지에 따라 0 = 위, 1 = 아래, 2 = 왼, 3 = 오
# 전파할 방향으로 한칸씩 이동하면서 전파 시도 -> 격자 밖으로 나가거나 간절함 0 되면 끝
# 전파 대상의 음식 같으면 패스
# x > y 전파 대상의 신앙심보다 전파가 높으면 강한 전파 -> 동일한 음식 신봉. 전파자 간절함 y+1 만큼 깎임. 전파 대상 신앙심 +1. 0 되면 끝
# x <= y -> 본인 신봉 음식 + 전파자 기본 음식 모두 합친거. 전파자 0, 대상 신앙심 +x
# 전파 당하면 방어 상태가 되어 당일에는 전파하지 않음 but 추가로 전파 받는 건 가능

# 방어 상태 때도 전파 당하는지, 방어 상태 때 전파 안 하는지 확인하기
# 다 전파자인 경우

from collections import deque

def spread(): # 신앙심 전파
    defense = set() # 전파 당해서 방어 상태인 애들

    for (r, c), B, f in leader:
        if (r, c) in defense: # 방어 상태
            continue

        x = B-1 # 간절함
        d = B % 4 # 전파 방향

        spirit[r][c] -= x # 간절함 빼줘야함. 그 전에 전파 당했을 수도

        while x > 0: # 격자 밖, 간절함 0 되면 종료
            nr = r + dr[d]
            nc = c + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                break

            if food[nr][nc] != f: # 음식 다른 경우에 전파 진행
                if x > spirit[nr][nc]: # 강한 전파
                    food[nr][nc] = set(f) # 얕은 복사 주의
                    spirit[nr][nc] += 1 # 원래 있던 신앙심 +1
                    x -= spirit[nr][nc]

                else: # 약한 전파
                    food[nr][nc].update(f)
                    spirit[nr][nc] += x
                    x = 0

                # 전파 당하면 방어 상태
                defense.add((nr, nc))

                if x <= 0: # 방어 상태 넣어주고 종료하기ㅠ
                    break

            r, c = nr, nc


def make_group(r, c):
    q = deque([(r, c)])
    visited[r][c] = idx
    f = food[r][c] # 신봉 음식
    max_spirit, minr, minc = spirit[r][c], r, c # 대표자. 신앙심 큰, 행작, 열작
    count = 1 # 그룹원 수. 본인 포함
    spirit[r][c] -= 1

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if visited[nr][nc] or food[nr][nc] != f: # 신봉 음식 다르면 패스
                continue

            if (-max_spirit, minr, minc) > (-spirit[nr][nc], nr, nc):
                max_spirit, minr, minc = spirit[nr][nc], nr, nc

            visited[nr][nc] = idx
            q.append((nr, nc))
            count += 1
            spirit[nr][nc] -= 1 # 신앙심 감소

    # 대표자 신앙심 추가
    spirit[minr][minc] += count
    leader.append(((minr, minc), spirit[minr][minc], food[minr][minc])) # 좌표, 신앙심, 음식 종류


def food_index(f):
    # 삼중 / 이중 - 초우,민우,민초 / 단일 - 민,초,우
    types = {0:{'C','M','T'}, 1:{'C','T'}, 2:{'M','T'}, 3:{'C','M'}, 4:{'M'}, 5:{'C'}, 6:{'T'}} # 인덱스 매칭

    for k, v in types.items():
        if f == v:
            return k


dr = [-1, 1, 0, 0] # 위아왼오
dc = [0, 0, -1, 1]

N, T = map(int, input().split()) # 50, 30
food = [list(map(set, input().strip())) for _ in range(N)] # 각 학생 신봉 음식
spirit = [list(map(int, input().split())) for _ in range(N)] # 각 학생 신앙심

for _ in range(T):
    leader = [] # (대표자 좌표, 신앙심, 음식 종류)

    # 1. 아침
    for i in range(N):
        for j in range(N):
            spirit[i][j] += 1

    # 2. 점심. 그룹 형성
    visited = [[0] * N for _ in range(N)]
    idx = 1

    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                make_group(i, j)
                idx += 1

    # 3. 저녁. 신앙심 전파
    # 대표자 전파 순서
    leader.sort(key=lambda x: (len(x[2]), -x[1], x[0])) # 단일 음식, 신앙심, 행작 열작 순
    spread()

    total = [0] * 7

    for i in range(N):
        for j in range(N):
            total[food_index(food[i][j])] += spirit[i][j]

    print(*total) # 저녁 시간 끝난 후 민초우, 민초, 민우, 초우, 우, 초, 민 순서대로 신앙심 총합