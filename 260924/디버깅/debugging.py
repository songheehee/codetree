# 57분 30초

# 사다리 타기랑 비슷한데 i번 줄 -> 무조건 i번으로
# 가로선 = 메모리 유실선 있을 수 있음 (취약 지점). 이웃한 선과만 이어질 수 있음
# 해커들이 메모리 유실선 설치. 승용이는 메모리 유실선 추가해서 버그 고치려고 함
# 선 옆에 겹쳐지도록 추가 불가

# 유실선 양방향. 매트릭스에 표시할까? 딕셔너리로?
# 유실선 설치 가능한 곳 다 저장해두고 조합으로 뽑아서 하기 -> 어차피 최대 3개임
# 내려가면서 유실선 설치하는 건 너무 복잡할 거 같음

def check():
    new_lines = lines.copy()

    for r, c in select:
        if (r, c) in new_lines or (r, c+1) in new_lines:
            continue

        new_lines[(r, c)] = (r, c+1)
        new_lines[(r, c+1)] = (r, c)

    for j in range(C): # 사람별로 잘 내려오나
        sr, sc = 0, j # 시작 지점

        while sr < R:
            if (sr, sc) in new_lines:
                nr, nc = new_lines.pop((sr, sc)) # 다음 위치
                new_lines.pop((nr, nc), None) # 없을 수도 있음. 사용된 거 삭제 위해

                sr, sc = nr, nc
            else:
                sr += 1

        if sc != j:
            return False # 다른 곳으로 감

    return True # 다 자기 번호로 내려옴


def dfs(start):
    global min_count

    if len(select) >= min_count: # 이미 최소보다 큼
        return

    if check(): # 맞게 도착하면 끝
        min_count = min(min_count, len(select))
        return

    for i in range(start, len(possible)):
        select.append(possible[i])
        dfs(i+1)
        select.pop()


C, L, R = map(int, input().split()) # 고객 수 (열), 메모리 유실선 개수, 취약 지점 개수 (행)
lines = dict()

for _ in range(L):
    a, b = map(lambda x: int(x)-1, input().split()) # 취약지점, 고객. 행, 열
    lines[(a, b)] = (a, b+1)
    lines[(a, b+1)] = (a, b)

# 유실선 설치 가능한 곳. 무조건 오른쪽 설치
possible = []
for i in range(R):
    for j in range(C-1):
        if (i, j) in lines or (i, j+1) in lines: # 오른쪽에 있으면 불가
            continue

        possible.append((i, j))

min_count = 4 # 최대 3개임
select = [] # 선택한 유실선

dfs(0)

print(min_count if min_count < 4 else -1) # 필요한 메모리 유실선 개수의 최솟값. 3보다 크면 -1