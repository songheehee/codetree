# 0 = 빈칸, 1 = 함정, 2 = 벽, 격자 밖도 벽
# 1. 기사 이동 - 상하좌우 한칸 이동. 다른 기사가 있으면 같이 밀려남. 그 옆에도 있으면 또 밀려남. 근데 끝이 벽이면 이동 불가
# 2. 대결 대미지 - 밀려난 기사들은 피해 입음. 이동한 곳에서 직사각형 내에 놓여있는 함정 수만큼 << ??
#   체력 이상 대미지 받으면 기사 사라짐. 명령 받은 기사는 피해 입지 않음. 밀린 이후에 대미지 입음. 밀쳐진 곳에 함정 없으면 ㄱㅊ
# 기사들이 받은 대미지 캐리하고 있자. 죽은 애는 빼야돼서
# 기사 직사각형 다 옮겨야됨
# 함정 개수만큼 체력 깎임
# 기사 위치 겹치지 않음. 기사와 벽 겹쳐서 주어지지 않음
# 새로 그리자 어차피 체력 깎이는 거 보려면 for문 돌아야됨

from collections import deque

def move():
    global knight_grid, knights
    new_grid = [row[:] for row in knight_grid]
    new_knights = [row[:] if row else None for row in knights]

    q = deque([I])
    visited = [0] * (K+1) # 큐에 들어간 기사 표시. 기사 수 유의!
    visited[I] = 1
    change = [I]

    while q:
        idx = q.popleft()
        (r, c), h, w, *_ = knights[idx]

        for i in range(r, r+h):
            for j in range(c, c+w):
                nr = i + dr[D]
                nc = j + dc[D]

                if not (0 <= nr < N and 0 <= nc < N and matrix[nr][nc] != 2): # 벽이면 이동 불가
                    return False

                nxt = knight_grid[nr][nc] # 다음 기사 번호
                if nxt and not visited[nxt]: # 다른 기사 있음
                    q.append(nxt)
                    visited[nxt] = 1
                    change.append(nxt)

                new_grid[i][j] = 0 # 이동한 기사들 지워주기

                if i == r and j == c: # 초기좌표 바꿔주기
                    new_knights[idx][0] = nr, nc

    knight_grid = new_grid
    knights = new_knights
    return change


dr = [-1, 0, 1, 0] # 위오아왼
dc = [0, 1, 0, -1]

N, K, Q = map(int, input().split()) # 체스판 크기, 기사 수, 왕 명령. 40, 30, 100
matrix = [list(map(int, input().split())) for _ in range(N)] # 벽, 함정 표시
knights = [None] # 1번부터. K+1임
knight_grid = [[0] * N for _ in range(N)] # 기사 표시

for num in range(1, K+1): # 기사 1번부터
    R, C, H, W, P = map(int, input().split()) # 좌표, 세로, 가로, 체력
    R -= 1
    C -= 1

    knights.append([(R, C), H, W, P, 0]) # 입은 데미지

    for i in range(R, R+H):
        for j in range(C, C+W):
            knight_grid[i][j] = num

for _ in range(Q):
    I, D = map(int, input().split()) # 기사 번호, 방향
    
    if knights[I] is None: # 사라진 기사
        continue
        
    # 1. 이동
    res = move()
    
    # 2. 체력 깎임
    if res:
        # 바뀐 기사들 다시 그려주기
        for idx in res:
            (r, c), h, w, p, dam = knights[idx]

            for i in range(r, r+h):
                for j in range(c, c+w):
                    if idx != I and matrix[i][j] == 1: # 명령 기사 제외 함정 있으면
                        dam += 1
                        p -= 1

            if p <= 0:
                knights[idx] = None
            else: # 안 죽었을 때만 그려주기
                knights[idx] = [(r, c), h, w, p, dam]

                for i in range(r, r + h):
                    for j in range(c, c + w):
                        knight_grid[i][j] = idx

print(sum(val[4] for val in knights if val)) # 생존한 기사들이 받은 대미지 합