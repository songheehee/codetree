'''
소요시간 : 1시간 50분
수행 시간 : 121ms / 메모리 : 20MB
시도 : 3번

이해 및 구상 (13분) - 구현 및 디버깅 (1시간 26분) - 수정 (11분)

[구상]
    - 일단 문제를 읽자마자 조화로움의 합...? 구하는 걸 보고 바로 튀튀
    - 그룹 카운트 하는건 bfs로 해야겠다 바로 떠오름. 보기 쉽게 matrix에 그룹 별로 써놓자
    - 맞닿은 변 개수 세는 건 matrix 그리고 난 뒤에 생각하자
    - 회전도 일단 구현하면서 생각하는 걸로 넘김

[구현]
    - 그룹 파악 -> 점수 계산 -> 회전 순으로 풀었는데 회전이 너무 어려웠음 ㅜㅜㅜ 나는 90도 회전을 어떻게 깔끔하고 예쁘게 짜는지 모르겠다...
    - 처음엔 group에 시작 좌표도 넣으려고 했는데 모든 좌표가 있지 않은 이상...별 필요 없을 거 같아서 뺌
    - 초기, 1회전, 2회전, 3회전 하니까 for문 돌리고 함수화 해야겠다
    - 회전에 한시간 쓴거 같다. 전에 강사님이 알려주신 좌표 그리는 걸로 했는데 규칙 알아내는데 시간이 좀 걸렸음 ㅠ

[실수]
    - if group_matrix[nr][nc] != -1 or matrix[nr][nc] != color << 처음에 and로 해서 무한루프 걸림. 뭐가 틀렸는지 한참 생각했다. 조건을 항상 잘 생각하자!!!
    - 원래는 두개 조합 선택하는거 dfs로 짜고 변 개수 세는 거 그냥 선택된 조합으로 이중 for문 돌렸는데 시간 초과 뜸...N이 30이었는데 대충 본 죄다
    
[리팩토링]
    - 회전 뭔가 더 깔끔하게 for문 하나로 할 수 있을거 같은데 방법 없나ㅜ
    - 맞닿은 변의 수도 그냥 group에 넣으면 좋을 거 같은데 시간 없어서 그냥 쉽고 빨리 했다...
'''
# 동일한 숫자 상하좌우 인접 -> 동일한 그룹
# 초기 예술 점수 -> 회전
# 정중앙 기준으로 십자 모양 -> 반시계 90도
# 4개 정사각형 시계 90도

from collections import deque

def bfs(r, c):
    q = deque([(r, c)])
    color = matrix[r][c]
    idx = len(groups)
    group_matrix[r][c] = idx
    count = 1

    while q:
        cr, cc = q.popleft()

        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]

            if not (0 <= nr < N and 0 <= nc < N):
                continue

            if group_matrix[nr][nc] != -1 or matrix[nr][nc] != color: # 이미 방문했거나 다른 색이면
                continue

            group_matrix[nr][nc] = idx
            q.append((nr, nc))
            count += 1

    return color, count

def side(): # 맞닿은 변의 수
    for k in range(len(groups)):
        count = [0] * len(groups)

        for i in range(N):
            for j in range(N):
                if group_matrix[i][j] == k:
                    for d in range(4):
                        nr = i + dr[d]
                        nc = j + dc[d]

                        if not (0 <= nr < N and 0 <= nc < N):
                            continue

                        if group_matrix[nr][nc] != k:
                            count[group_matrix[nr][nc]] += 1

        group_side.append(count)

def calc(a, b):
    # (그룹 a 칸의 수 + b 칸의 수) * 그룹 a 숫자 * 그룹 b 숫자 * 맞닿아 있는 변의 수
    return (groups[a][1] + groups[b][1]) * groups[a][0] * groups[b][0] * group_side[a][b]

def rotate():
    new_matrix = [[0] * N for _ in range(N)]
    half = N//2
    
    # 십자가 반시계
    hor = matrix[half][::-1]
    ver = [row[half] for row in matrix]

    new_matrix[half] = ver
    for i in range(N):
        new_matrix[i][half] = hor[i]

    # 정사각형들 90도
    for i in range(half):
        for j in range(half):
            new_matrix[i][j] = matrix[half-1-j][i]

    for i in range(half+1, N):
        for j in range(half):
            new_matrix[i][j] = matrix[N-1-j][i-(half+1)]

    for i in range(0, half):
        for j in range(half+1, N):
            new_matrix[i][j] = matrix[N-1-j][half+1+i]

    for i in range(half+1, N):
        for j in range(half+1, N):
            new_matrix[i][j] = matrix[N+half-j][i]


    # 쉬운 방법
    # narr = [[0]*N for _ in range(N)]
    # for i in range(N):              # '+' 부분 시계
    #     narr[M][i]=arr[i][M]
    # for j in range(N):
    #     narr[j][M]=arr[M][N-j-1]

    # for (si,sj) in ((0,0),(0,M+1),(M+1,0),(M+1,M+1)):
    #     for i in range(M):
    #         for j in range(M):
    #             narr[si+i][sj+j]=arr[si+M-j-1][sj+i]

    return new_matrix

dr = [1, 0, -1, 0]
dc = [0, 1, 0, -1]

N = int(input()) # 격자 크기. 홀수. 30
matrix = [list(map(int, input().split())) for _ in range(N)]
score = 0

for turn in range(4):
    groups = [] # 색깔, 칸수
    group_matrix = [[-1] * N for _ in range(N)] # 각 그룹 인덱스
    group_side = [] # 맞닿은 변의 수 미리 계산

    if turn > 0:
        # 1. 회전
        matrix = rotate()

    # 2. 그룹 파악
    for i in range(N):
        for j in range(N):
            if group_matrix[i][j] == -1:
                groups.append(bfs(i, j))

    # 3. 점수 계산
    side()
    # 두개 조합 선택
    for i in range(len(groups)):
        for j in range(i+1, len(groups)):
            score += calc(i, j)

print(score) # 초기 + 1회전 + 2회전 + 3회전 점수 합