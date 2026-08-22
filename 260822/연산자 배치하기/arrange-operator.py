import sys
sys.stdin = open("input.txt", "r")

# n개의 정수, n-1개의 연산자 정수 사이에 하나씩
# 정수 순서 못 바꿈. 연산자는 덧셈, 뺄셈, 곱셈
# 연산자 우선순위 무시. 앞에서부터 차례대로 연산
# 식의 최솟값과 최댓값

def dfs(idx, val, ac, mc, muc): # 계산값, 연산자 개수
    global min_val, max_val

    if idx == n:
        min_val = min(min_val, val)
        max_val = max(max_val, val)
        return

    # 더하기
    if ac:
        dfs(idx + 1, val+nums[idx], ac-1, mc, muc)
    # 빼기
    if mc:
        dfs(idx + 1, val-nums[idx], ac, mc-1, muc)
    # 곱하기
    if muc:
        dfs(idx + 1, val*nums[idx], ac, mc, muc-1)

n = int(input())
nums = list(map(int, input().split()))
add, minus, mul = map(int, input().split()) # 개수
min_val = 1000000000
max_val = -1000000000

dfs(1, nums[0], add, minus, mul)

print(min_val, max_val)