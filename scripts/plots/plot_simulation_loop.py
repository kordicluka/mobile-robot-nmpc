import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(7, 13))
ax.set_xlim(0, 7)
ax.set_ylim(0, 13)
ax.axis('off')

def box(ax, x, y, w, h, text, color='#ddeeff', fontsize=9.5):
    rect = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                    boxstyle="round,pad=0.15",
                                    facecolor=color, edgecolor='#336699',
                                    linewidth=1.5, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, zorder=4, multialignment='center')

def diamond(ax, x, y, w, h, text, color='#fff3cd', fontsize=9):
    diamond_pts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
    poly = plt.Polygon(diamond_pts, facecolor=color,
                       edgecolor='#336699', linewidth=1.5, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, zorder=4, multialignment='center')

def arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#336699', lw=1.5),
                zorder=2)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.15, my, label, fontsize=8, color='#336699', style='italic')

cx = 3.5

                             
box(ax, cx, 12.2, 4.0, 0.7,
    r'POČETAK KORAKA $k$' + '\n' + r'izmjeri stanje $\mathbf{x}_k = [x, y, \theta, v, \omega]$',
    color='#d4edda', fontsize=9)

box(ax, cx, 11.0, 4.0, 0.7,
    'pronađi najbliži sljedeći waypoint\n' + r'(usporedba udaljenosti $d_{curr}$ i $d_{next}$)',
    color='#ddeeff')

box(ax, cx, 9.8, 4.0, 0.7,
    r'postavi $\mathbf{y}_{ref,0}, \ldots, \mathbf{y}_{ref,N}$' + '\n' + r'(sljedećih $N=20$ točaka putanje)',
    color='#ddeeff')

box(ax, cx, 8.6, 4.0, 0.7,
    'fiksiraj početni uvjet OCP-a\n' + r'$\mathbf{x}_0 = \mathbf{x}_k$',
    color='#ddeeff')

box(ax, cx, 7.4, 4.0, 0.7,
    'solver.solve()\n(jedna SQP_RTI iteracija)',
    color='#e8d5f5')

box(ax, cx, 6.2, 4.0, 0.7,
    r'uzmi prvi upravljački signal' + '\n' + r'$\mathbf{u}_0^* = [\Delta v_0^*, \Delta\omega_0^*]$',
    color='#ddeeff')

box(ax, cx, 5.0, 4.0, 0.7,
    'integriraj robot (RK4)\n' + r'$\mathbf{x}_{k+1} = f_{RK4}(\mathbf{x}_k, \mathbf{u}_0^*, \Delta t)$',
    color='#ddeeff')

diamond(ax, cx, 3.7, 4.2, 0.9,
        r'korak $k$ = korak perturbacije?',
        color='#fff3cd')

box(ax, cx, 2.6, 4.0, 0.6,
    'primijeni poremećaj\n' + r'$\mathbf{x}_{k+1} \mathrel{+}= [\Delta x,\ \Delta y]$'.replace(r'\mathrel{+}=', r'+\!='),
    color='#f8d7da')

diamond(ax, cx, 1.6, 4.2, 0.9,
        r'$\|\mathbf{x}_{k+1}^{pos} - \mathbf{p}_{cilj}\| < d_{tol}$?',
        color='#fff3cd')

box(ax, cx, 0.4, 4.0, 0.6,
    'KRAJ — cilj dosegnut',
    color='#d4edda', fontsize=9.5)

                      
arrow(ax, cx, 11.85, cx, 11.35)
arrow(ax, cx, 10.65, cx, 10.15)
arrow(ax, cx, 9.45, cx, 8.95)
arrow(ax, cx, 8.25, cx, 7.75)
arrow(ax, cx, 7.05, cx, 6.55)
arrow(ax, cx, 5.85, cx, 5.35)
arrow(ax, cx, 4.65, cx, 4.15)

                                 
arrow(ax, cx, 3.25, cx, 2.90)
ax.text(cx + 0.15, 3.07, 'Da', fontsize=8, color='#336699', style='italic')

arrow(ax, cx, 2.30, cx, 1.95)

                         
arrow(ax, cx, 1.15, cx, 0.70)
ax.text(cx + 0.15, 0.92, 'Da', fontsize=8, color='#336699', style='italic')

                                                   
ax.annotate('', xy=(5.8, 3.7), xytext=(5.55, 3.7),
            arrowprops=dict(arrowstyle='->', color='#336699', lw=1.5))
ax.plot([5.55, 5.8, 5.8, 5.55], [3.7, 3.7, 1.6, 1.6],
        color='#336699', lw=1.5, zorder=2)
ax.text(5.85, 2.65, 'Ne', fontsize=8, color='#336699', style='italic')

                                              
ax.annotate('', xy=(1.0, 12.2), xytext=(1.0, 1.6),
            arrowprops=dict(arrowstyle='->', color='#336699', lw=1.5))
ax.plot([1.3, 1.0], [1.6, 1.6], color='#336699', lw=1.5, zorder=2)
ax.text(0.15, 7.0, 'Ne\n(sljedeći\nkorak $k$)', fontsize=8,
        color='#336699', style='italic', ha='center')

ax.set_title('Simulacijska petlja zatvorene petlje', fontsize=12, pad=8)
plt.savefig('latex/figures/simulation_loop.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena: latex/figures/simulation_loop.png")
