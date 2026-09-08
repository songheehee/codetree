# 몬스터 상하좌우, 대각선
# 1. 몬스터 복제 시도 - 현재 몬스터 위치에서 같은 방향 알
# 2. 몬스터 이동 - 몬스터 시체/팩맨/격자 벗어남 -> 반시계 45도 회전 가능할때까지. 다 못가면 이동하지 않음
# 3. 팩맨 이동 - 3칸 이동. 몬스터 가장 많이 먹을 수 있는 방향으로 세칸. 여러개면 상좌하우 우선
# 3-1. 이동하면서 몬스터 먹고 시체 남김. 알은 안 먹음. 시작 위치의 몬스터도 안 먹음
# 4. 몬스터 시체 소멸 - 시체는 2턴 동안 유지
# 5. 몬스터 복제 완성 - 알 깨어남
# 몬스터 초기 위치랑 팩맨 초기 위치 같을 수 있음

def pac_move(r, c, move, count):
    global max_count, min_move

    if move == 3:
        if count > max_count:
            max_count = count
            min_move = dirs[:]
        return

    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]

        if not (0 <= nr < 4 and 0 <= nc < 4):
            continue

        tmp = matrix[nr][nc]
        matrix[nr][nc] = []
        dirs.append(i)
        pac_move(nr, nc, move+1, count+len(tmp))
        dirs.pop()
        matrix[nr][nc] = tmp


def monster_move():
    new_matrix = [[[] for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            if not matrix[i][j]:
                continue

            for d in matrix[i][j]:
                # 반시계 45도 회전
                for k in range(8): # 처음이 원래 방향
                    nd = (d + k) % 8
                    nr = i + ddr[nd]
                    nc = j + ddc[nd]

                    if (0 <= nr < 4 and 0 <= nc < 4) and (nr, nc) != (pr, pc) and not dead[nr][nc]:
                        d = nd
                        break

                else: # 그럼에도 못 찾으면 이동하지 않음
                    nr, nc = i, j

                new_matrix[nr][nc].append(d)

    return new_matrix

# 팩맨
dr = [-1, 0, 1, 0] # 상좌하우
dc = [0, -1, 0, 1]
# 몬스터 대각선
ddr = [-1, -1, 0, 1, 1, 1, 0, -1]
ddc = [0, -1, -1, -1, 0, 1, 1, 1]

M, T = map(int, input().split()) # 몬스터 마리 수, 턴 수. 10, 25
pr, pc = map(lambda x: int(x)-1, input().split()) # 팩맨 위치
matrix = [[[] for _ in range(4)] for _ in range(4)] # 몬스터 여러마리 일 수 있음
dead = [[[] for _ in range(4)] for _ in range(4)] # 시체. 여러개 가능

for _ in range(M):
    R, C, D = map(lambda x: int(x)-1, input().split())
    matrix[R][C].append(D)

for _ in range(T):
    # 1. 몬스터 복제
    eggs = [[mon[:] for mon in row] for row in matrix]

    # 2. 몬스터 이동
    matrix = monster_move()

    # 3. 팩맨 이동
    dirs = [] # 선택한 방향
    max_count = 0 # 최대 먹은 몬스터 개수
    min_move = [0, 0, 0] # 상좌하우 우선
    pac_move(pr, pc, 0, 0)

    # 4. 몬스터 먹고 시체
    for d in min_move:
        pr += dr[d]
        pc += dc[d]

        if matrix[pr][pc]:
            dead[pr][pc].extend([3] * len(matrix[pr][pc])) # 몬스터 마리 수만큼
            matrix[pr][pc] = []

    # 5. 시체 소멸
    for i in range(4):
        for j in range(4):
            new_dead = []

            for left in dead[i][j]:
                left -= 1
                if left:
                    new_dead.append(left)

            if new_dead:
                dead[i][j] = new_dead
            else:
                dead[i][j] = []

    # 6. 알 부화
    for i in range(4):
        for j in range(4):
            if eggs[i][j]:
                matrix[i][j].extend(eggs[i][j]) # 여러 마리일 수 있음

print(sum(len(mon) for row in matrix for mon in row)) # 몬스터 마리 수