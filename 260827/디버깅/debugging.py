# i번 줄의 결과는 무조건 i번으로 가야함
# 사다리타기 같은거
# 유실선 추가할때 바로 옆에 설치 불가능
# 최소한의 유실선 추가하기
# matrix 만들어야하나? 유실선 정보 set으로 할까 adjList로 할까
# 유실선 일단 고르고 시작

def reach():
    global ans
    # 유실선 설치
    new_line = dict()
    new_line.update(line)

    for pr, pc in select:
        new_line[(pr, pc)] = (pr, pc + 1)  # 무조건 하나씩 밖에 없음
        new_line[(pr, pc + 1)] = (pr, pc)

    cus = 0 # 고객 번호 시작

    while cus < C:
        col = cus

        for row in range(R):
            if (row, col) in new_line:
                prev_col = col
                _, col = new_line[(row, col)]
                # 사용했으면 삭제
                new_line.pop((row, prev_col), None)
                new_line.pop((row, col), None)

        if col != cus:
            return

        cus += 1

    ans = len(select) # 모두 고객한테 도달 완
    return


def dfs(idx): # 유실선 골라주기
    if ans != -1: # 이미 최소한의 유실선
        return

    if len(select) > 3:
        return

    if idx == len(possible): # 선택 가능한 유실선 다 훑어봄
        # 모든 고객한테 도달 가능한지 체크
        reach()
        return

    dfs(idx+1) # 선택 안 하는거 먼저

    select.append(possible[idx])
    dfs(idx+1)
    select.pop()


C, M, R = map(int, input().split()) # 고객 수, 유실선 개수, row 개수
line = dict()
visited = [[0] * C for _ in range(R)] # 유실선 설치 불가능한 곳 표시
possible = [] # 유실선 설치 가능한 곳. 오른쪽으로만 설치

if M == 0: # 유실선 없으면 무조건 가능
    print(0)

else:
    for _ in range(M):
        a, b = map(lambda x: int(x)-1, input().split())
        # 양방향
        line[(a, b)] = (a, b+1) # 무조건 하나씩 밖에 없음
        line[(a, b+1)] = (a, b)

        visited[a][b] = 1
        visited[a][b+1] = 1
        # 왼쪽도 설치 불가. 무조건 오른쪽으로 설치할 거임
        if b-1 >= 0:
            visited[a][b-1] = 1

    for i in range(R):
        for j in range(C-1):
            if not visited[i][j]:
                possible.append((i, j))

    ans = -1 # 필요한 선의 개수
    select = []

    dfs(0)

    print(ans) # 필요한 선의 개수가 3개를 넘거나 불가능하면 -1
