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
                nd.add(d)
                new_atoms[(nr, nc)] = (nm+m, ns+s, nd, count+1)
            else:
                new_atoms[(nr, nc)] = (m, s, {d}, 1)

    # 2. 2개 이상이면 합성
    atoms = dict()

    for (r, c), (m, s, d, count) in new_atoms.items():
        if count == 1:
            atoms[(r, c)] = [(m, s, d.pop())]
            continue

        if m // 5 == 0: # 소멸
            continue

        m //= 5
        s //= count

        if d <= {0,2,4,6} or d <= {1,3,5,7}: # 모두 상하좌우/대각선
            atoms[(r, c)] = [(m, s, i*2) for i in range(4)]
        else:
            atoms[(r, c)] = [(m, s, i*2+1) for i in range(4)]

print(sum(val[0] for lst in atoms.values() for val in lst)) # 남아있는 원자 질량