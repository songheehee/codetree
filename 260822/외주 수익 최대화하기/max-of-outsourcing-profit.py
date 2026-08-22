import sys
sys.stdin = open("input.txt", "r")

# n일 동안 개발하여 수익 최대화
# 하루에 한개씩 작업. 각 작업은 걸리는 기한 t, 수익 p
# 동시에 수행 불가. 휴가 이후로는 일 못함

def dfs(day, money): # 사실상 인덱스
    # 해당 일에 일 할지말지. 부분집합
    # 기간 끝나지 않아도 최대값일 수 있음
    global max_money

    if day > n: # 기간 넘어가면 끝
        return

    max_money = max(max_money, money) # 종료조건 뒤에 작성해야함
    
    if day == n: # 맥스값 업데이트 해주고 종료
        return

    dfs(day+work[day][0], money+work[day][1]) # 일함 -> 끝나는 날로 이동
    dfs(day+1, money) # 일 안함 -> 다음날

n = int(input()) # 휴가 기간
work = [tuple(map(int, input().split())) for _ in range(n)] # 각 일자에 수행할 수 있는 작업의 기한, 수익
max_money = 0

dfs(0, 0)

print(max_money) # 외주 수익 최대화