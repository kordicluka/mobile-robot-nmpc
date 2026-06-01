import numpy as np
import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

                           
ROWS, COLS = 12, 16
START = (1, 1)
GOAL  = (10, 14)

                            
BLOCKED = set()
for r in range(3, 9):
    for c in range(5, 8):
        BLOCKED.add((r, c))
for r in range(5, 10):
    for c in range(10, 13):
        BLOCKED.add((r, c))

def heuristic(a, b):
    return np.hypot(a[0]-b[0], a[1]-b[1])

def astar(start, goal):
    open_set = [(heuristic(start, goal), 0.0, start)]
    came_from = {}
    g_score = {start: 0.0}
    expanded = []

    while open_set:
        _, g, current = heapq.heappop(open_set)
        expanded.append(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], expanded

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nb = (current[0]+dr, current[1]+dc)
            if not (0 <= nb[0] < ROWS and 0 <= nb[1] < COLS):
                continue
            if nb in BLOCKED:
                continue
            step = np.hypot(dr, dc)
            new_g = g + step
            if new_g < g_score.get(nb, np.inf):
                g_score[nb] = new_g
                came_from[nb] = current
                f = new_g + heuristic(nb, goal)
                heapq.heappush(open_set, (f, new_g, nb))

    return [], expanded

path, expanded = astar(START, GOAL)
expanded_set = set(expanded)
path_set = set(path)

fig, ax = plt.subplots(figsize=(11, 8))

for r in range(ROWS):
    for c in range(COLS):
        node = (r, c)
        if node in BLOCKED:
            color = '#555555'
        elif node in path_set:
            color = 'steelblue'
        elif node in expanded_set:
            color = '#d4e8f5'
        else:
            color = 'white'

        rect = plt.Rectangle((c - 0.5, r - 0.5), 1, 1,
                              facecolor=color, edgecolor='lightgray',
                              linewidth=0.5, zorder=1)
        ax.add_patch(rect)

                          
path_arr = np.array(path)
ax.plot(path_arr[:, 1], path_arr[:, 0], 'o-',
        color='steelblue', linewidth=2.5, markersize=5, zorder=3)

              
ax.plot(START[1], START[0], 's', color='limegreen', markersize=14, zorder=4)
ax.plot(GOAL[1],  GOAL[0],  '*', color='tomato',    markersize=16, zorder=4)
ax.text(START[1], START[0]-0.7, 'Start', ha='center', fontsize=9, color='limegreen', fontweight='bold')
ax.text(GOAL[1],  GOAL[0]-0.7,  'Cilj',  ha='center', fontsize=9, color='tomato',    fontweight='bold')

         
legend_items = [
    mpatches.Patch(facecolor='#d4e8f5', edgecolor='gray', label=f'Pretraživane ćelije ({len(expanded_set)})'),
    mpatches.Patch(facecolor='steelblue', label=f'Pronađena putanja ({len(path)} koraka)'),
    mpatches.Patch(facecolor='#555555', label='Prepreka'),
    mpatches.Patch(facecolor='white', edgecolor='gray', label=f'Nepretraživane ćelije ({ROWS*COLS - len(BLOCKED) - len(expanded_set)})'),
]
ax.legend(handles=legend_items, loc='lower right', fontsize=9, framealpha=0.95)

total_free = ROWS * COLS - len(BLOCKED)
pct = len(expanded_set) / total_free * 100
ax.set_title(f'A* pretraga — pregledano {len(expanded_set)} od {total_free} slobodnih ćelija ({pct:.0f}%)\n'
             f'Heuristika usmjerava pretragu prema cilju i preskače neperspektivne ćelije',
             fontsize=10)

ax.set_xlim(-0.5, COLS - 0.5)
ax.set_ylim(-0.5, ROWS - 0.5)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.savefig('latex/figures/astar_search.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena: latex/figures/astar_search.png")
