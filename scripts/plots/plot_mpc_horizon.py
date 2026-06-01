import numpy as np
import matplotlib.pyplot as plt

N = 20
t = np.linspace(0, 26, 400)
ref = np.sin(t * 0.3) * 0.5 + 0.35 * t

def draw_horizon(ax, k_now, show_xlabel=False):
    dt = 1.0

    ax.plot(t, ref, 'k--', linewidth=1.5, label='Referentna putanja', zorder=2)

                       
    t_past = np.linspace(0, k_now, 80)
    past = np.sin(t_past * 0.3) * 0.5 + 0.35 * t_past + np.random.RandomState(42).randn(80) * 0.04
    ax.plot(t_past, past, color='steelblue', linewidth=2.0, label='Prijeđena putanja', zorder=3)

                                                        
    t_pred = np.arange(k_now, k_now + N + 1, dtype=float) * dt
    pred = np.sin(t_pred * 0.3) * 0.5 + 0.35 * t_pred
    ax.plot(t_pred, pred, 'o-', color='tomato', linewidth=1.8,
            markersize=4, label='Predviđena putanja', zorder=4)

                        
    ax.axvspan(k_now, k_now + N, alpha=0.08, color='tomato', zorder=1)

                    
    curr_val = np.sin(k_now * 0.3) * 0.5 + 0.35 * k_now
    ax.axvline(x=k_now, color='steelblue', linewidth=1.5, linestyle=':', zorder=3)
    ax.plot(k_now, curr_val, 'o', color='steelblue', markersize=9, zorder=5)

    ax.annotate(f'$k = {k_now}$', xy=(k_now, curr_val),
                xytext=(k_now + 0.4, curr_val - 0.9),
                fontsize=10, color='steelblue')

                        
    arrow_y = curr_val + 0.5
    ax.annotate('', xy=(k_now + N, arrow_y),
                xytext=(k_now, arrow_y),
                arrowprops=dict(arrowstyle='<->', color='tomato', lw=1.5))
    ax.text(k_now + N / 2, arrow_y + 0.35, f'$N = {N}$',
            ha='center', fontsize=10, color='tomato')

                                    
    for k in range(0, 26):
        ax.axvline(x=k, color='gray', linewidth=0.4, linestyle='-', alpha=0.4, zorder=0)

    ax.set_ylabel('Pozicija', fontsize=10)
    ax.set_ylim(-1.0, 12.0)
    ax.set_xlim(-0.5, 25.5)
    ax.set_xticks(range(0, 26))
    ax.tick_params(axis='x', labelsize=8)
    ax.grid(axis='y', alpha=0.3)

    if show_xlabel:
        ax.set_xlabel('Vremenski korak $k$', fontsize=10)

fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
fig.subplots_adjust(hspace=0.35)

draw_horizon(axes[0], k_now=2)
axes[0].set_title('Korak $k = 2$: horizont pokriva korake 2–22', fontsize=11, pad=8)

draw_horizon(axes[1], k_now=3, show_xlabel=True)
axes[1].set_title('Korak $k = 3$: horizont se pomaknuo na korake 3–23', fontsize=11, pad=8)

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, fontsize=9,
           bbox_to_anchor=(0.5, -0.01), framealpha=0.9)

plt.savefig('latex/figures/mpc_receding_horizon.png', dpi=150, bbox_inches='tight')
plt.close()
print("Slika spremljena.")
