# 1. 첫번째 열부터 탐색
# 2. 위에서 아래로 내려가며 제일 빨리 발견한 곰팡이 채취 -> 빈칸. 해당 열에 곰팡이 없을 수도 있음
# 3. 채취 끝나면 곰팡이 이동
# 4. 방향과 속력대로 이동. 벽에 도달하면 방향 반대로
# 5. 한칸에 곰팡이 두마리 이상이면 크기가 큰 곰팡이가 잡아먹음 (걔만 남음)
# 6. 오른쪽 열 이동해서 반복

def move(): # 곰팡이들 움직이기
    global virus
    new_virus = dict()

    for (r, c), (size, d, s) in list(virus.items()):
        if s == 0:
            # 이 때도 이미 있을 수 있음!
            if (r, c) in new_virus:
                exist, *_ = new_virus[(r, c)]

                if exist > size:
                    continue

            new_virus[(r, c)] = (size, d, s)
            continue

        nr = r + (dr[d] * s)
        nc = c + (dc[d] * s)

        if 0 <= nr < N and 0 <= nc < M:
            # 바이러스 있을 경우 크기 비교
            if (nr, nc) in new_virus:
                exist, *_ = new_virus[(nr, nc)]

                if exist > size:
                    continue

            new_virus[(nr, nc)] = (size, d, s)

        else: # 방향 전환해줘야함
            cr, cc = r, c

            for _ in range(s):
                nr = cr + dr[d]
                nc = cc + dc[d]

                if not (0 <= nr < N and 0 <= nc < M):
                    d = change_dir(d)
                    nr = cr + dr[d]
                    nc = cc + dc[d]

                cr, cc = nr, nc

            if (nr, nc) in new_virus:
                exist, *_ = new_virus[(nr, nc)]

                if exist > size:
                    continue

            new_virus[(nr, nc)] = (size, d, s)

    virus = new_virus


def change_dir(d): # 반대로 바꿔주기
    if d == 0 or d == 2:
        return d+1

    if d == 1 or d == 3:
        return d-1


dr = [-1, 1, 0, 0] # 위아오왼
dc = [0, 0, 1, -1]

N, M, K = map(int, input().split())
virus = dict() # 크기, 방향, 속력
total = 0

for _ in range(K):
    x, y, s, d, b = map(int, input().split()) # 위치, 속력, 이동 방향, 크기
    x -= 1
    y -= 1
    d -= 1

    virus[(x, y)] = (b, d, s) # 초기엔 무조건 한칸에 하나

for j in range(M): # 열 검사
    keys = list((r, c) for (r, c) in virus.keys() if c == j)

    if keys: # 해당 열에 곰팡이 있음
        # 곰팡이 채취
        keys.sort()
        size, *_ = virus.pop(keys[0], None)
        total += size

    move() # 채취 안 하더라도 곰팡이 움직임

print(total) # 채취한 곰팡이 총합