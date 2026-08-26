'''
소요시간 : 2시간 13분
수행 시간 : 1051ms / 25MB

이해 및 구상 (18분) - 구현 및 디버깅 (1시간 55분)

[구상]
    - 일단 문제 이해하는 데에 10분 걸렸음. 뭔 소린지 모르겠어서 예시 그림 보고 이해함
    - 구상을 하고 시작했다고 생각했는데 아니었음. 2등분의 4등분의 아주 그냥 미쳐버리는줄
    - 그리고 2^6 테이블을 많이 만드는데 괜찮나 싶었음. 메모리가 2^6인지 10^6인지 헷갈렸음. 하지만 다른 방법도 딱히 없었기 때문에 그냥 킵고잉했음

[구현]
    - 처음에는 막연히 슬라이싱해서 갈아끼어야겠다고 생각함. 근데 그러니까 new_matrix 인덱스 오류가 남. % 해줬는데 이게 더 헷갈리는거 같아서 그냥 아예 똑같은 크기로 함
    - 슬라이싱 하려다가 도저히 못하겠어서 4중 ㄷㄷ for문으로 바꿈. 이중 for문도 안 좋아하는데 4중?? ㅎㅎㅎ ㅜㅜㅜ
    - range 하기가 까다로웠음. 2**level도 있고 2**(level-1) 도 있고 하 ^^
    - 그리고 하나의 섹션은 같은 방향으로 움직여야되는데 이게 자꾸 이상해짐 ㅜ 그래서 방향을 아예 for문으로 돌려주자 싶었는데 시작점 찾는게 빡셌음. 다른 방법이 분명 있을 거 같긴 한데 모르겠어서 그냥 하드코딩 ^^
    - 회전 시키는 데에만 두시간이 걸림 ㅎ...나머지는 쉬웠음

[실수]
    - 각 회전 끝날 때마다 얼음 녹는다는 걸 뒤늦게 깨달음
    - 회전 0일 때도 얼음 녹는다는 걸 뒤늦게 깨달음
    - 얼음 개수 빼줄 때 얼음 있는 곳만 빼야했는데 그거 체크를 안함. 테케에서 이상한 점 알아챔
    - 군집 수 셀 때 이미 센 군집에 있는 거 안 세도 됨
    - 그리고 자꾸 큐에 넣을 때 visited 넣는 걸 까먹음 왜 그러냐...
'''
# 좌측 상단에 있는 빙하를 회전시키게 되면 다른 상하좌우의 인접한 격자도 똑같은 크기만큼 회전
# 상하좌우 얼음이 3개 이상이면 녹지 않음. 그렇지 않으면 -1. 녹는 건 동시에 진행
# 남아있는 빙하의 총 양과 가장 큰 얼음 군집 크기
# 사등분 해서 2^레벨을 시계방향으로 회전

from collections import deque

def bfs(r, c): # 얼음군집 찾기
    q = deque([(r, c)])
    visited[r][c] = 1
    count = 1 # 군집 개수

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N and not visited[nr][nc]):
                continue

            if matrix[nr][nc]:
                count += 1
                visited[nr][nc] = 1
                q.append((nr, nc))

    return count


def melt():
    chk = [[0] * N for _ in range(N)] # 한번에 녹이려고

    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 0: # 빙하 있는 곳만 체크하면 됨
                continue

            count = 0

            for d in range(4):
                nr = i + dr[d]
                nc = j + dc[d]

                if not (0 <= nr < N and 0 <= nc < N):
                    continue

                if matrix[nr][nc]:
                    count += 1

            if count < 3:
                chk[i][j] = 1

    for i in range(N):
        for j in range(N):
            if chk[i][j]:
                matrix[i][j] -= 1


dr = [0, 1, -1, 0] # 오아위왼
dc = [1, 0, 0, -1]

n, Q = map(int, input().split()) # 회전 가능 레벨, 회전 횟수. 격자 크기 2^N
N = 2**n # 한 변의 길이
matrix = [list(map(int, input().split())) for _ in range(N)]
levels = list(map(int, input().split()))

for level in levels:
    if level == 0:
        melt()
        continue

    length = 2**level
    half = length//2
    new_matrix = [[0] * N for _ in range(N)]
    
    for i in range(0, N, length):
        for j in range(0, N, length): # 좌측 상단 시작점
            for d in range(4): # 4등분. 방향 인덱스
                if d == 0:
                    si, sj = i, j
                elif d == 1:
                    si, sj = i, j+half
                elif d == 2:
                    si, sj = i+half, j
                else:
                    si, sj = i+half, j+half

                for k in range(si, si+half):
                    for l in range(sj, sj+half):
                        nr = k + (dr[d] * half)
                        nc = l + (dc[d] * half)

                        new_matrix[nr][nc] = matrix[k][l]

    matrix = new_matrix
    # 회전 끝나고 빙하 녹음
    melt()

max_ice = 0
visited = [[0] * N for _ in range(N)]

for i in range(N):
    for j in range(N):
        if matrix[i][j] and not visited[i][j]:
            max_ice = max(max_ice, bfs(i, j))

print(sum(map(sum, matrix)))
print(max_ice)