

N, M = input("Nhap so so dinh va canh cua do thi").split()
N = int(N)
M = int(M)

adj = [list() for i in range(N)]

for i in range(M):
    u, v = input().split()
    u = int(u)
    v = int(v)
    adj[u].append(v)
    adj[v].append(u)

for i in range(N):
    print(f"Danh sach ke cua dinh {i} la: {sorted(adj[i])}")
