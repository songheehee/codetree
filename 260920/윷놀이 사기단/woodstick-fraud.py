# +3분
# 윷 던지는 횟수 10번
# 시작칸에 말 4개
# 파랑칸은 빨간색 화살표, 다른 칸은 검정색 화살표
# 도착칸 이동하면 이동 횟수랑 상관 없이 이동 끝
# 도착하지 않은 말 골라서 원하는 이동 횟수만큼 이동 가능
# 시작칸, 도착칸 제외하고는 말 겹칠 수 없음. 40은 도착칸이 아님 41부터
# 칸에 있는 점수에 추가
# 이동 칸 수는 최대 5
# 말 None 아닌 것 중에 골라서 이동. 한 칸에 한 마리만

def dfs(count, score):
    global max_score

    if count == 10:
        max_score = max(max_score, score)
        return

    for i in range(1, 5): # 말 고르기
        if horses[i] is None: # 말 판 나감
            continue

        # 해당 말 이동 + 판 기록, 파랑칸 체크, 점수 더해주기
        roll_horse = horses[i] # 원복용

        num, bk, bi = horses[i] # 판 번호, 파랑칸 키, 파랑칸 인덱스
        pan[num] = 0 # 전에 있던 자리

        if bk: # 파랑칸
            bi += moves[count]

            if bi >= len(blues[bk]): # 판 나감
                num = 41

            else:
                num = blues[bk][bi]

                if pan[num]: # 해당 칸에 다른 말 있음
                    continue
        else:
            num += moves[count] * 2

            if num <= 40 and pan[num]: # 말 있음
                continue

            if num in blues: # 파랑칸 도착
                bk, bi = num, 0

        if num > 40: # 판 나감
            horses[i] = None
            num = 0
        else:
            horses[i] = (num, bk, bi)
            pan[num] = i

        dfs(count+1, score+num)

        # 원복
        horses[i] = roll_horse
        pan[roll_horse[0]] = i
        pan[num] = 0


pan = [0] * 41 # 41번부터 도착
horses = [None] + [(0, 0, 0)] * 4 # 말 현재 위치, 파랑칸 키. 나가면 None 표시. 1번 말부터
blues = {10: [10, 13, 16, 19, 25, 30, 35, 40], 20: [20, 22, 24, 25, 30, 35, 40], 30: [30, 28, 27, 26, 25, 30, 35, 40]}
moves = list(map(int, input().split()))
max_score = 0

dfs(0, 0)

print(max_score) # 얻을 수 있는 점수의 최댓값