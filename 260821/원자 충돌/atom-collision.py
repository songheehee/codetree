dr = [-1, -1, 0, 1, 1, 1, 0, -1]
dc = [0, 1, 1, 1, 0, -1, -1, -1]

n, a, t = map(int, input().split()) # 격자 크기, 원자 개수, 시간. 50, 50^2, 1000
loc = dict() # 좌표값으로 원자 인덱스 저장. atoms에서 삭제해야되니까
atoms = [] # 덱으로 하는게 낫나

for i in range(a):
    # 초기 위치, 질량, 속력, 방향
    x, y, m, s, d = map(int, input().split())
    atoms.append([x-1, y-1, m, s, d]) # 값 변경해야됨

time = 0
while time < t:
    time += 1

    # 1. 원자 자신의 방향, 자신의 속력만큼 이동
    for i in range(len(atoms)):
        r, c, m, s, d = atoms[i]
        nr = (r + (dr[d] * s)) % n # 행열 끝 연결되어있음
        nc = (c + (dc[d] * s)) % n

        atoms[i] = [nr, nc, m, s, d]
        if loc.get((nr, nc)):
            loc[(nr, nc)].append(i)
        else:
            loc[(nr, nc)] = [i]

    # 2. 모든 이동이 끝난 뒤 한칸에 2개 이상의 원자가 있는 경우
    #   a. 질량, 속력 모두 합한 하나의 원자
    #   b. 4개의 원자로 나눠짐
    #   c. 모두 해당 칸에 위치. 소숫점 버림
    #       - 질량은 합쳐진 질량 / 5
    #       - 속력은 합쳐진 속력 / 합쳐진 원자 개수
    #       - 방향이 모두 상하좌우 중 하나거나 대각선 중에 하나면, 각각 상하좌우, 그렇지 않으면 대각선 네방향
    #   d. 질량이 0이면 소멸

    remove_k = [] # 소멸시킬 키
    remove_a = [] # 원자에서 없앨 인덱스
    new_atoms = [] # 새로 추가할 원자

    for k, v in loc.items():
        if len(v) == 1:
            remove_k.append(k)
            continue

        m_sum = 0 # 질량 합
        s_sum = 0 # 속력 합
        d_count = 0 # 상하좌우 카운트

        for idx in v:
            *_, m, s, d = atoms[idx]

            m_sum += m
            s_sum += s
            d_count += d % 2 == 0

        m_sum //= 5

        if m_sum > 0: # 4개로 나누기
            s_sum //= len(v)

            if d_count == 0 or d_count == len(v): # 모두 상하좌우거나 모두 대각선
                d = [0, 2, 4, 6]
            else:
                d = [1, 3, 5, 7]

            for di in d:
                new_atoms.append([k[0], k[1], m_sum, s_sum, di])

        # 다 지워줘야함
        remove_k.append(k)
        for idx in v:
            remove_a.append(idx)

    # 소멸
    if atoms:
        remove_a.sort(reverse=True)
        for idx in remove_a: # 끝에서부터 지워야함
            atoms.pop(idx)

    for k in remove_k:
        loc.pop(k)

    # atoms에 추가 - 소멸시키고 해줘야 인덱스 제대로 저장할 수 있음
    for atom in new_atoms:
        atoms.append(atom)

print(sum(row[2] for row in atoms)) # k초가 될때 남아있는 원자 질량 합