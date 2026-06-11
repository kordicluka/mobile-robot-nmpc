# Planiranje putanje mobilnog robota primjenom NMPC-a

Završni rad — FER Zagreb, 2026.  
**Luka Kordić** | Mentor: izv. prof. dr. sc. Branimir Novoselnik

---

## O projektu

Simulacija planiranja i praćenja putanje diferencijalnog mobilnog robota u poznatom statičkom prostoru primjenom nelinearnog modelskog prediktivnog upravljanja (NMPC).

Dvoslojni pristup:
- **A\*** — globalno planiranje putanje kroz poznatu mapu s preprekama
- **NMPC (acados)** — lokalno praćenje putanje s poštivanjem ograničenja

---

## Instalacija

### Zahtjevi

- Python 3.10+
- cmake, gcc

```bash
# Fedora/RHEL
sudo dnf install cmake gcc

# Ubuntu/Debian
sudo apt install cmake gcc
```

### acados

```bash
git clone https://github.com/acados/acados.git --recursive --depth 1
cd acados && mkdir build && cd build
cmake .. -DACADOS_WITH_QPOASES=OFF
make -j$(nproc)
cmake --install . --prefix ..
cd ../..
```

### Python paketi

```bash
pip install acados_template matplotlib scipy numpy pyyaml
```

### Environment varijable

Dodaj u `~/.bashrc` ili `~/.zshrc`:

```bash
export ACADOS_SOURCE_DIR="/putanja/do/acados"
export LD_LIBRARY_PATH="$ACADOS_SOURCE_DIR/lib:$LD_LIBRARY_PATH"
```

---

## Pokretanje

### Jedan scenarij

```bash
# prikaži grafove uživo
python scripts/run_simulation.py one_obstacle

# spremi grafove
python scripts/run_simulation.py narrow --save

# s animacijom
python scripts/run_simulation.py perturbation --animate

# sve odjednom
python scripts/run_simulation.py u_shape --save --animate --speed 5
```

### Kompletan benchmark

```bash
python scripts/run_benchmark.py
```

Pokreće sve scenarije, tuning analizu i sprema sve rezultate u `results/`.

---

## Scenariji

| Naziv | Opis |
|---|---|
| `baseline` | Ravna putanja bez prepreka |
| `one_obstacle` | Jedna kružna prepreka |
| `narrow` | Uski prolaz između dvije prepreke |
| `l_corridor` | L-hodnik, zaokret 90° |
| `u_shape` | U-oblik, demonstracija kratkovidnosti NMPC-a |
| `perturbation` | Guranje robota s putanje |
| `cluttered` | Sedam nasumično raspoređenih prepreka |
| `blocked` | Nedostižni cilj — A* ne pronalazi put |

---

## Struktura projekta

```
zavrsni/
├── config/
│   └── params.yaml          # svi parametri simulacije
├── src/
│   ├── model.py             # unicycle kinematički model (CasADi)
│   ├── mpc_solver.py        # NMPC solver (acados)
│   ├── simulation.py        # zatvorena simulacijska petlja
│   ├── obstacles.py         # definicija prepreka
│   ├── astar.py             # A* globalni planer
│   ├── path_smoother.py     # glađenje putanje splineom
│   ├── scenarios.py         # testni scenariji
│   ├── metrics.py           # kvantitativna analiza
│   ├── benchmark.py         # usporedba scenarija i solvera
│   ├── tuning.py            # analiza parametara N, Q, R
│   ├── plot.py              # vizualizacija
│   └── animate.py           # animacija simulacije
├── scripts/
│   ├── run_simulation.py    # pokretanje jednog scenarija
│   └── run_benchmark.py     # pokretanje kompletnog benchmarka
└── results/
    ├── data/                # CSV rezultati
    └── figures/             # grafovi i animacije
```

---

## Konfiguracija

Svi parametri se mijenjaju u `config/params.yaml`:

| Parametar | Opis |
|---|---|
| `mpc.N` | Horizont predviđanja (default: 20) |
| `mpc.dt` | Vremenski korak (default: 0.1s) |
| `mpc.Q` | Težine greške stanja `[x, y, θ]` |
| `mpc.R` | Težine upravljanja `[v, ω]` |
| `mpc.solver_type` | `SQP_RTI` (brži) ili `SQP` (točniji) |
| `mpc.constraints` | `soft` (robusno) ili `hard` (strogo) |
| `robot.v_max` | Maksimalna linearna brzina [m/s] |
| `robot.omega_max` | Maksimalna kutna brzina [rad/s] |

---

## Prevođenje LaTeX dokumenta

Završni rad nalazi se u mapi `latex/`. Paket `minted` (za isticanje koda) zahtijeva `pdflatex` s opcijom `-shell-escape` i instaliran Python paket `Pygments`.

### Preduvjeti

```bash
pip install Pygments
```

### Kompajliranje

```bash
cd latex
pdflatex -shell-escape zavrsni_rad
bibtex zavrsni_rad
pdflatex -shell-escape zavrsni_rad
pdflatex -shell-escape zavrsni_rad
```

Tri prolaza su potrebna da se ispravno razriješe sve reference i literatura.

### Alternativno s latexmk

Kreiraj datoteku `latex/.latexmkrc` sa sadržajem:

```perl
$pdflatex = "pdflatex -shell-escape %O %S";
```

Zatim:

```bash
cd latex
latexmk -pdf zavrsni_rad
```
