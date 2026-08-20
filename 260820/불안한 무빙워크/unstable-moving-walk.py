# 무빙워크 레일 시계방향
# 각 사람은 1번 칸에 올라서서 n번 칸에서 내림 (0부터 시작하니까 n-1 해주기)
# 사람이 올라가거나 이동하면 해당 칸 안정성 -1. 0인 칸에는 못 올라감
# 직접 무빙워크를 돌릴지, 포인터 쓸지

# 1. 무빙워크 한칸 회전
# 2. 먼저 올라간 사람부터 무빙워크가 회전하는 방향으로 한칸 이동. 앞에 사람 있거나 안정성 0인 경우 이동 X
# 3. 1번 칸에 사람이 없고 안정성 있으면 사람 올라감
# 4. 안정성 0 칸이 k 개 이상이면 종료
# 1~3. n번 칸에 사람이 위치하면 그 즉시 내림
from collections import deque

n, k = map(int, input().split()) # 무빙워크 길이, 안정성 0 개수. 100, 200
q = list(map(int, input().split())) # 안정성. 1000
ppl = deque() # 먼저 올라간 사람. 무빙워크 위치

times = 0 # 실험
point = 0 # 무빙워크 시작점 포인터

while q.count(0) < k:
    times += 1

    # 1. 무빙워크 회전
    point = (point-1) % (2*n)
    # n 위치에 사람 있으면 내림
    n_pos = (point + n - 1) % (2 * n)
    if n_pos in ppl:
        ppl.remove(n_pos)

    # 2. 먼저 올라간 사람부터 무빙워크가 회전하는 방향으로 한칸 이동. 앞에 사람 있거나 안정성 0인 경우 이동 X
    for _ in range(len(ppl)):
        idx = ppl.popleft()
        front = (idx+1)%(2*n)

        if not (q[front] == 0 or front in ppl):
            q[front] -= 1

            if front != n_pos: # n번 자리 아니면 넣기
                ppl.append(front)
        else:
            ppl.append(idx) # 이동 안 하고 그대로

    # 3. 1번 칸에 사람이 없고 안정성 있으면 사람 올라감
    if q[point] and point not in ppl:
        ppl.append(point)
        q[point] -= 1


print(times) # 종료될 때 몇번째 실험?