import sys
import time
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# 1. Đọc dữ liệu 
with open('input.txt', 'r') as f:
    data = f.read().strip().split()
if not data:
    print("Không có dữ liệu đầu vào!")
    sys.exit()

it = iter(data)

n = int(next(it))                   
nodes = [next(it) for _ in range(n)] 

start = next(it)                     
goal = next(it)                      

m = int(next(it))                   

graph = defaultdict(list)
cost = {}

for _ in range(m):
    u = next(it)
    v = next(it)
    w = int(next(it))
    graph[u].append((v, w))
    cost[(u, v)] = w

# Nếu còn dữ liệu trong file, coi là các giá trị heuristic theo thứ tự `nodes`
heuristic = {}
remaining = list(it)
if len(remaining) >= len(nodes):
    # đọc n giá trị heuristic
    for i, node in enumerate(nodes):
        try:
            heuristic[node] = float(remaining[i])
        except Exception:
            heuristic[node] = 0.0
else:
    # nếu không có heuristic, khởi tạo bằng 0
    heuristic = {node: 0.0 for node in nodes}

# 2. Thuật toán Depth First Search (DFS)
def Best_First_Search(start, goal, graph, heuristic):
    open_list = []
    heapq.heappush(open_list, (heuristic.get(start, 0.0), start))

    parent = {start: None}
    visited = set()
    visit_order = []

    while open_list:
        _, current = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)
        visit_order.append(current)

        if current == goal:
            break

        for neighbor, w in graph.get(current, []):
            if neighbor in visited:
                continue
            if neighbor not in parent:
                parent[neighbor] = current
                heapq.heappush(open_list, (heuristic.get(neighbor, 0.0), neighbor))

    # Truy vết đường đi
    if goal not in parent and start != goal:
        return None, visit_order, None

    path = []
    node = goal if goal in parent else start
    while node is not None:
        path.append(node)
        node = parent.get(node)
    path.reverse()

    # Tính tổng chi phí theo đường tìm được
    total_cost = 0
    for u, v in zip(path, path[1:]):
        total_cost += cost.get((u, v), 0)

    return path, visit_order, total_cost


# 3. Vẽ đồ thị 
def draw_graph_with_path(cost, path):
    G = nx.DiGraph()
    for (u, v), w in cost.items():
        G.add_edge(u, v, weight=w)

    pos = {
        'S': (2, 5),
        'A': (0, 4), 'B': (2, 4), 'C': (4, 4),
        'D': (2, 2.5), 'E': (5, 3), 'F': (4, 2),
        'H': (0, 1), 'I': (2, 1), 'G': (6, 1),
        'J': (1, 0), 'K': (4, 0)
    }

    plt.figure(figsize=(12, 8))
    
    nx.draw_networkx_edges(G, pos, edge_color='#bdc3c7', width=1.5, 
                           arrowsize=20, arrowstyle='-|>')
 
    nx.draw_networkx_nodes(G, pos, node_size=1800, node_color='#ecf0f1', 
                           edgecolors='#34495e', linewidths=1.5)
 
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', font_family='sans-serif')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.4)

    if path:
        path_edges = list(zip(path, path[1:]))
        
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_size=1800, 
                               node_color='#e67e22', edgecolors='#c0392b', linewidths=2)
        
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#e74c3c', 
                               width=4,arrows = True, arrowstyle='-|>',arrowsize=28,
                               connectionstyle='arc3,rad=0.0',min_source_margin=15,min_target_margin=17)

    plt.title("ĐỒ THỊ TÌM KIẾM TỐT NHẤT (BEST-FIRST)", pad=20, fontsize=15)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# 4. In kết quả
start_time = time.time()
path, traversal, total_cost = Best_First_Search(start, goal, graph, heuristic)
end_time = time.time()

print("==== KẾT QUẢ TÌM KIẾM TỐT NHẤT (BEST-FIRST) ====")
print(f"Trạng thái: {start} -> {goal}")
print(f"Quá trình duyệt: {' -> '.join(traversal)}")

if path:
    print(f"Đường đi: {' -> '.join(path)}")
    print(f"Chi phí tìm được: {total_cost}")
else:
    print("Kết quả: Không tìm thấy đường đi!")

elapsed_time = (end_time - start_time) * 1_000_000 
print(f"Thời gian: {elapsed_time:.6f} micro-giây")

#Luu ket qua ra file
def save_results_to_file(filename, start, goal, traversal, path, total_cost, elapsed_time):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("==== KẾT QUẢ TÌM KIẾM TỐT NHẤT (BEST-FIRST) ====\n")
        f.write(f"Trạng thái: {start} -> {goal}\n")
        f.write(f"Quá trình duyệt: {' -> '.join(traversal)}\n")
        
        if path:
            f.write(f"Đường đi: {' -> '.join(path)}\n")
            f.write(f"Chi phí tìm được: {total_cost}\n")
        else:
            f.write("Kết quả: Không tìm thấy đường đi!\n")
            
        f.write(f"Thời gian: {elapsed_time:.6f} micro-giây\n")
    print(f"\n Đã lưu kết quả vào file: {filename}")

# Gọi hàm để lưu file
save_results_to_file("ketqua.txt", start, goal, traversal, path, total_cost, elapsed_time)

# Hiển thị đồ thị
draw_graph_with_path(cost, path)

