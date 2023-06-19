import heapq

# kota disimbolkan dengan huruf A - H
graph = {
    'A': {'B': 2, 'C': 3},
    'B': {'D': 5, 'E': 6},
    'C': {'F': 4},
    'D': {'G': 7},
    'E': {'H': 8},
    'F': {'H': 6},
    'G': {'H': 3},
    'H': {}
}

start = input("Masukkan kota awal (masukkan salah satu huruf dari  A - H): ").upper()
goal = input("Masukkan kota tujuan (masukkan salah satu huruf dari  A - H): ").upper()

SLD = {
    'A': 14,
    'B': 12,
    'C': 7,
    'D': 8,
    'E': 11,
    'F': 6,
    'G': 5,
    'H': 0
}

def Astar(graph, start, goal, SLD):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = SLD[start]
    
    while len(open_set) > 0:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            path = []
            total_cost = g_score[current]
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, total_cost
        
        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + graph[current][neighbor]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + SLD[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    return None, float('inf')

path, total_cost = Astar(graph, start, goal, SLD)

if path == None:
    print(f"Tidak ditemukan jalur dari {start} ke {goal}")
else:
    print(f"Jalur terpendek dari {start} ke {goal} adalah {path}")
    print(f"Total cost: {total_cost}")
