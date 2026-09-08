'''
소요시간 : 1시간 23분
수행 시간 : 52ms / 메모리 : 16MB

이해 및 구상 (16분) - 구현 및 디버깅 (1시간 7분)

[구상]
    - 또 이동 문제가 나왔따리. dict로 할까 리스트로 할까 나는 딕셔너리 파이긴 한데 알, 시체 많으니까 몬스터는 리스트로 할까
    - 처음에 매트릭스 크기가 안 나와있어서 딕셔너리로 하려다가 맨 첫 줄에;; 4*4 라길래 작아서 매트릭스로 바꿈
    - 딕셔너리로 하려고 할 때는 몬스터랑 알을 같은 딕셔너리로 처리해줄까 하다가 어차피 리스트로 해서 따로 처리해줬다
    - 그럼 이제 시체랑 알을 같은 딕셔너리로 해줄까 하다가 헷갈리니까 그냥 따로 처리해줌
    - 몬스터, 시체, 알 다 한 칸에 여러개 들어갈 수 있음!!! 유의
    - 혹시 몰라서 몬스터 초기 위치랑 팩맨 초기 위치 같을 수 있다는 거 적어놨는데 딱히 신경 안 써도 될듯?
    - 대신 팩맨이 이동 전에 몬스터랑 같이 있어도 얘는 안 먹는다는 거 인지했음

[구현]
    - 문제에서 아주 친절하게 1번 2번 이렇게 써놔줘서 고대로 따라갔다
    - 팩맨 이동할 때 격자 밖으로 나가는 건 ㄴㄴ 상하좌우 중에 3개 중복으로 고르는 거라 순열로 풀었다. 난 부분집합으로 푼 줄 알았는데 지금 보니까 순열이네; 띠용
    - 리스트도 min 되나 잠깐 디버깅에서 확인해봄 -> 된다!
    - 처음에 원복시켜주는거 귀찮아서 바로 len(matrix[nr][nc]) 더해주는걸로 했는데 그럼 왔다갔다 하면서 중복 카운트 될 수 있음; 하 귀찮아...
    - nr, nc가 pr, pc 가 아니어야 하는데 or 인지 and 인지 헷갈려서 그냥 튜플로 비교...or 일 거 같음
    - 헷갈렸던 건 시체 소멸이 이번 시체가 이번에 소멸인지 아닌지 헷갈...근데 예시 보니까 다다음까지 살아있길래 그냥 애초에 3으로 줌

[리팩토링]
    - 어차피 팩맨 이동 시 우선순위부터 보기 때문에 같을 경우 생각할 필요 없음
    - egg 딕셔너리 만들지 않고 그냥 복사하면 되잖아...?? 세상에 생각도 못했다;
    - 시체 딕셔너리가 낫나...리스트가 낫나...
'''
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

                    if (0 <= nr < 4 and 0 <= nc < 4) and (nr, nc) != (pr, pc) and (nr, nc) not in dead:
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
matrix = [[[] for _ in range(4)] for _ in range(4)] # 여러마리 일 수 있음
dead = dict() # 시체. 여러개 가능

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
            count = len(matrix[pr][pc]) # 몬스터 마리 수
            matrix[pr][pc] = []

            if (pr, pc) in dead:
                dead[(pr, pc)].extend([3] * count) # 2턴 동안 살아있음. 이번 턴 포함인겨..?
            else:
                dead[(pr, pc)] = [3] * count

    # 5. 시체 소멸
    for k, v in list(dead.items()):
        new_dead = []

        for left in v: # 한턴 빼주기
            left -= 1
            if left:
                new_dead.append(left)

        if new_dead:
            dead[k] = new_dead
        else:
            dead.pop(k)

    # 6. 알 부화
    for i in range(4):
        for j in range(4):
            if eggs[i][j]:
                matrix[i][j].extend(eggs[i][j]) # 여러 마리일 수 있음

print(sum(len(mon) for row in matrix for mon in row)) # 몬스터 마리 수