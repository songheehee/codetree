import sys
sys.stdin = open("input.txt", "r")

# 아침과 저녁 업무 강도 차이의 최솟값
# 아침과 저녁 일 반반
# n이 20이니까 부분집합으로

def dfs(count):
    global min_diff

    if len(select) == n // 2:
        # 고른 것과 안 고른 것 차이 구하기
        not_select = [i for i in range(n) if i not in select]
        total = 0
        not_total = 0

        for i in range(len(select)-1):
            for j in range(i+1, len(select)):
                r, c = select[i], select[j]
                total += matrix[r][c]
                total += matrix[c][r]

        for i in range(len(not_select)-1):
            for j in range(i+1, len(not_select)):
                r, c = not_select[i], not_select[j]
                not_total += matrix[r][c]
                not_total += matrix[c][r]

        min_diff = min(min_diff, abs(total-not_total))

        return

    if count == n:
        return

    select.append(count)
    dfs(count+1)
    select.pop()

    dfs(count+1)

n = int(input()) # 일의 양
matrix = [list(map(int, input().split())) for _ in range(n)]

select = []
min_diff = 100 * n

dfs(0)

print(min_diff)