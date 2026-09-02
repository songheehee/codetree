'''
소요시간 : 2시간
수행 시간 : 81ms / 메모리 1MB

이해 및 구상 (10분) - 구현 및 디버깅 (1시간 50분)

[구상]
    - 말 위치랑 말 순서를 어떻게 관리할까 고민...dict랑 리스트로 하자
    - 말 방향을 처음에 리스트에 저장할까 고민했는데 리스트는 말 번호만 저장하는 걸로 (모르겠음 더 좋은 방법이 있을수도)
    - 쌓여있는 말은 0번이 맨 밑으로 함
    - 말 네개 쌓이면 끝나는 걸 while 문 안에서 검사해줄지 아니면 말 쌓을 때 검사해줄지 고민했는데 쌓을 때 해주는 걸로 함
    
[구현]
    - 그냥...했다. 흰이 제일 쉬워서 흰 -> 빨 -> 파 순으로 함
    - 파랑색은 방향 바꿔준 다음에 다음 칸이 흰/빨일 수 있어서 elif 말고 if문으로 해줌
    - 사실 흰, 빨 거의 코드가 같아서 함수로 빼줄 수 있겠지만...귀찮아서 안 함
    - 그래서!!! 복붙하다가 빨강 이상한 걸 나중에 알았다 샤갈~ 복붙할거면 제발 제대로 보자ㅜㅜㅜㅜㅜㅜ

[실수]
    - 진짜 나는 스튜핏 애스홀이다...제ㅔㅔㅔㅔㅔ발 복붙을 잘하자 제발 ㅜㅠㅜㅠㅠ 제발~!!!!!!!
    - 그리고 범위 밖이라 방향 바꾸면 범위 또 체크할 필요 없다고 생각했는데 인덱스 오류나서 추가함 왜지?
    - 나의 크나큰 단점은 너무 세세한 조건..? 까지 생각하려다가 불필요한 조건문이 많아지는 거다!!! 반복되는 코드가 있으니까 복붙 실수도 생기는 거고 ㅠ 한번에 할 수 있는건 그냥 한번에 하자...어차피 시간 차이도 많이 안 난다
    - turn +1 을 먼저 해주고 1000 체크해야된다!!!!! 경계값 생각할것

[리팩토링]
    - 머리가 너무 딕셔너리에 매몰되어있는데 horses를 그냥 매트릭스로 했어도 됐을 듯...이동하는 위치가 더 잘 보일 거 같긴 하다. 딕셔너리로 하니까 위치를 하나하나 그려줘야됨
    - 경계 밖이랑 파랑이랑 똑같으니까 파랑 벽으로 패딩 처리해도 된다 ㄷㄷ
'''
# 격자판 흰, 빨, 파
# 말 1~K번. 번호, 이동 방향 정해져있음
# 1. 말이 이동하려는 칸이 흰색이면 해당 칸으로 이동. 이미 말이 있으면 말 위에 올림. 여러번 올리기 가능
# 2. 빨간 칸이면 순서 말 순서 뒤집고 말 이동
# 3. 파란 칸이면 이동하지 않고 방향 반대로 전환 뒤 이동. 근데 반대쪽도 파랑이다 -> 이동하지 않음. 이동하려는 말만 방향 전환
# 4. 격자판 범위 벗어나면 방향 반대로 전환 뒤 이동
# 쌓여있는 말 다 같이 이동
# 말이 4개 이상 겹쳐지면 그 즉시 종료

def move():
    for i in range(K):
        r, c, d = order[i]

        nr = r + dr[d]
        nc = c + dc[d]

        # 3, 4
        if not (0 <= nr < N and 0 <= nc < N) or matrix[nr][nc] == 2:
            # 방향 반대로 전환 뒤 이동
            # 반대쪽도 파랑일 경우 이동하지 않음
            d = change_dir(d)
            nr = r + dr[d]
            nc = c + dc[d]

            order[i] = (r, c, d) # 방향 저장

            if not (0 <= nr < N and 0 <= nc < N) or matrix[nr][nc] == 2: # 인덱스 오류가 날 수 있구나;
                continue

        # 조건 없어도 여긴 어차피 흰/빨이구나
        # 말 있으면 다 같이 이동
        idx = horses[(r, c)].index(i)
        lst = horses[(r, c)][idx:] if matrix[nr][nc] == 0 else horses[(r, c)][idx:][::-1] # 업힌 애들
        new_lst = horses[(r, c)][:idx]

        if new_lst: # 기존꺼
            horses[(r, c)] = new_lst
        else:
            horses.pop((r, c), None) # 없으면 없애기

        if (nr, nc) in horses:
            horses[(nr, nc)].extend(lst)

            if len(horses[(nr, nc)]) >= 4:
                return True
        else:
            horses[(nr, nc)] = lst

        for num in lst:
            order[num] = (nr, nc, order[num][2])


def change_dir(d):
    if d == 0 or d == 2:
        return d+1
    else:
        return d-1

dr = [0, 0, -1, 1] # 오왼위아
dc = [1, -1, 0, 0]

N, K = map(int, input().split()) # 판 크기, 말 개수
matrix = [list(map(int, input().split())) for _ in range(N)] # 0 = 흰, 1 = 빨, 2 = 파
horses = dict() # 몇번 말, 방향. 0번이 맨 밑
order = [0] * K # 말 순서. 위치, 방향

for i in range(K):
    X, Y, D = map(lambda x: int(x)-1, input().split())

    order[i] = (X, Y, D)
    horses[(X, Y)] = [i] # 처음엔 한 칸에 한 말

turn = 0 # 이거 0부터 시작하는거 맞나

while True:
    turn += 1 # 얘를 먼저 해줘야 됐음;;;

    if turn > 1000:
        turn = -1
        break

    stop = move()

    if stop:
        break

print(turn) # 종료되는 순간의 턴 번호. 1000보다 크면 -1