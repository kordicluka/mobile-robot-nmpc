import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

r = 0.2
x_min, y_min, x_max, y_max = 0.5, 0.5, 3.0, 2.5

def draw_rect(ax, label):
    rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                          facecolor='#888888', edgecolor='black', linewidth=1.5,
                          zorder=2, label=label)
    ax.add_patch(rect)

                                     
draw_rect(ax1, 'Pravokutna prepreka')
ax1.set_title('Pravokutna prepreka\n(direktno)', fontsize=11)
ax1.set_xlim(0, 4)
ax1.set_ylim(0, 3.5)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.set_xlabel('$x$ [m]', fontsize=10)
ax1.set_ylabel('$y$ [m]', fontsize=10)
ax1.annotate('min() nije\nderivabilna\nu kutovima!',
             xy=(x_min, y_min), xytext=(0.1, 0.1),
             fontsize=9, color='tomato',
             arrowprops=dict(arrowstyle='->', color='tomato'))

                                         
x = x_min + r
circles = []
while x <= x_max:
    y = y_min + r
    while y <= y_max:
        circles.append((x, y))
        y += r * 1.5
    x += r * 1.5

for (cx, cy) in circles:
    circle = plt.Circle((cx, cy), r, facecolor='#888888', edgecolor='black',
                         linewidth=0.5, alpha=0.7, zorder=2)
    ax2.add_patch(circle)

                                  
rect_outline = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                               facecolor='none', edgecolor='black',
                               linewidth=1.5, linestyle='--', zorder=3,
                               label='Originalni pravokutnik')
ax2.add_patch(rect_outline)

ax2.set_title(f'Aproksimacija mrežom kružnica\n({len(circles)} kružnica, $r = {r}$ m)', fontsize=11)
ax2.set_xlim(0, 4)
ax2.set_ylim(0, 3.5)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)
ax2.set_xlabel('$x$ [m]', fontsize=10)

                                             
cx0, cy0 = circles[len(circles)//2]
ax2.annotate('', xy=(cx0 + r, cy0), xytext=(cx0, cy0),
             arrowprops=dict(arrowstyle='->', color='steelblue', lw=1.5))
ax2.text(cx0 + r/2, cy0 + 0.12, f'$r={r}$ m', ha='center', fontsize=8, color='steelblue')

ax2.annotate('Glatka $h_i(\\mathbf{x})$\nza svaku kružnicu ✓',
             xy=(x_max + 0.1, (y_min + y_max)/2), xytext=(3.0, 0.3),
             fontsize=9, color='steelblue',
             arrowprops=dict(arrowstyle='->', color='steelblue'))

plt.tight_layout()
plt.savefig('latex/figures/rect_to_circles.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena: latex/figures/rect_to_circles.png")
