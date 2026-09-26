'''
소요시간 : 1시간 15분
수행 시간 : 285ms / 메모리 : 30MB
시도 : 2번

[구상]
    - 원자를 그리드에 그려줄지 말지 고민하다가 안 그려줬는데 역시나 디버깅 할 때 보기가 힘들었다

[구현]
    - 이동할 때 개수를 합쳐주는 걸로 해서 좀 쉽게 짠 거 같다
    - 이때 방향도 같이 계산해서 같을 경우 원래 방향, 다를 경우 -1 넣는다거나 하면 좋았을 거 같은데 풀 때는 더 이상 생각하기를 포기했음

[실수]
    - 모두 상하좌우거나 모두 대각선 처리를 더해서 짝수인 걸로 했는데 대각선 두개면 짝수가 돼서 안 되는 걸 늦게 깨달았다
    - 뭔가 set 말고 넣을 때 처리해줄 수 있을 거 같은데 더 이상 생각하기를 포기

[나아진 점]
    - 저번보다는 더 깔끔하게 짠 것 같다
'''
# A개의 원자는 질량, 방향, 속력을 가지고 있음
# 위치 1,1 시작
# 격자 끝과 끝 연결되어 있음
# 원자 초기 위치 겹치지 않음

# 1. 원자 자신의 방향, 자신의 속력만큼 이동
# 2. 한 칸에 원자 두개 이상이면 합성
# 2-1. 질량, 속력 모두 합친 하나의 원자 됨
# 2-2. 4개의 원자로 나눠짐
#      질량은 합쳐진 원자의 질량 // 5
#      속력은 합쳐진 원자의 속력 // 합쳐진 원자의 개수
#      방향은 모두 상하좌우거나 모두 대각선 -> 각각 상하좌우. 아닐 경우 대각선 네 방향
# 3. 질량 0인 원소 소멸

dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, 1, 1, 1, 0, -1, -1, -1]

N, A, K = map(int, input().split()) # 격자 크기, 원자 개수, 실험 시간. 50, 2500, 1000
atoms = dict()

for _ in range(A):
    x, y, m, s, d = map(int, input().split()) # 위치, 질량, 속력, 방향
    x -= 1
    y -= 1

    atoms[(x, y)] = [(m, s, d)] # 질량, 속력, 방향

for _ in range(K):
    # 1. 원자 이동
    new_atoms = dict()

    for (r, c), val in atoms.items():
        for m, s, d in val:
            nr = ((r + (dr[d] * s)) % N + N) % N
            nc = ((c + (dc[d] * s)) % N + N) % N

            if (nr, nc) in new_atoms:
                nm, ns, nd, count = new_atoms[(nr, nc)]
                if nd % 2 != d % 2: # 방향 다를 경우
                    nd = -1
                new_atoms[(nr, nc)] = (nm+m, ns+s, nd, count+1)
            else:
                new_atoms[(nr, nc)] = (m, s, d, 1)

    # 2. 2개 이상이면 합성
    atoms = dict()

    for (r, c), (m, s, d, count) in new_atoms.items():
        if count == 1:
            atoms[(r, c)] = [(m, s, d)]
            continue

        if m // 5 == 0: # 소멸
            continue

        m //= 5
        s //= count

        if d != -1: # 모두 상하좌우/대각선
            atoms[(r, c)] = [(m, s, i*2) for i in range(4)]
        else:
            atoms[(r, c)] = [(m, s, i*2+1) for i in range(4)]

print(sum(val[0] for lst in atoms.values() for val in lst)) # 남아있는 원자 질량