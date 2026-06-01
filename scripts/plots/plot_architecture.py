import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

def box(ax, x, y, w, h, label, color='#ddeeff', fontsize=10):
    rect = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                    boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#336699',
                                    linewidth=1.5, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=fontsize, fontfamily='monospace', zorder=4)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#336699',
                                lw=1.5, connectionstyle='arc3,rad=0.0'),
                zorder=2)

                                   
box(ax, 6.0, 6.3, 2.8, 0.7, 'config/params.yaml', color='#fff3cd')

                                   
box(ax, 2.0, 4.8, 2.6, 0.7, 'scenarios.py')
box(ax, 2.0, 3.5, 2.6, 0.7, 'astar.py')
box(ax, 2.0, 2.2, 2.6, 0.7, 'path_smoother.py')

                                 
box(ax, 6.0, 3.5, 2.6, 0.7, 'model.py')
box(ax, 6.0, 2.2, 2.6, 0.7, 'mpc_solver.py')

                           
box(ax, 10.0, 2.2, 2.6, 0.7, 'simulation.py', color='#d4edda')

                          
box(ax, 7.5, 0.8, 2.6, 0.6, 'metrics.py', color='#f8d7da')
box(ax, 10.5, 0.8, 1.8, 0.6, 'plot.py', color='#f8d7da')

                  
                                        
arrow(ax, 6.0, 5.95, 2.0, 5.15)
arrow(ax, 6.0, 5.95, 6.0, 2.55)

                    
arrow(ax, 2.0, 4.45, 2.0, 3.85)

                        
arrow(ax, 2.0, 3.15, 2.0, 2.55)

                             
arrow(ax, 3.3, 2.2, 4.7, 2.2)

                     
arrow(ax, 6.0, 3.15, 6.0, 2.55)

                          
arrow(ax, 7.3, 2.2, 8.7, 2.2)

                             
arrow(ax, 10.0, 1.85, 8.8, 1.1)
arrow(ax, 10.0, 1.85, 10.4, 1.1)

                       
ax.text(4.9, 2.35, 'izglađena\nputanja', ha='center', fontsize=7.5,
        color='#336699', style='italic')
ax.text(8.8, 2.35, 'upravljanje\nu, stanja x', ha='center', fontsize=7.5,
        color='#336699', style='italic')

              
legend_items = [
    mpatches.Patch(facecolor='#ddeeff', edgecolor='#336699', label='Logički moduli'),
    mpatches.Patch(facecolor='#fff3cd', edgecolor='#336699', label='Konfiguracija'),
    mpatches.Patch(facecolor='#d4edda', edgecolor='#336699', label='Simulacijska petlja'),
    mpatches.Patch(facecolor='#f8d7da', edgecolor='#336699', label='Izlaz (CSV, PNG)'),
]
ax.legend(handles=legend_items, loc='lower left', fontsize=9, framealpha=0.9)

ax.set_title('Arhitektura sustava — tijek podataka', fontsize=12, pad=10)

plt.tight_layout()
plt.savefig('latex/figures/architecture.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena: latex/figures/architecture.png")
