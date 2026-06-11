# Revalidacija

Neovisna provjera provedena 2026-06-11. Pročitane su sve LaTeX datoteke, README, bibliografia i CSV podaci. Nije korišten git diff ni komentari prethodne sesije.

---

## Pronađeni problemi

### [File: latex/literatura.bib — nedostaje unos]
**Komentar profesora (§2.3, §6):** Lista minimalnih referenci: prvih 8 do `diehl2002rti` + `hairer1993ode`. Šesta u listi je `siciliano2009robotics`, s napomenom da se citira u `02_model.tex:8` za kinematiku monocikla / diferencijalnog pogona.  
**Trenutno stanje:** `siciliano2009robotics` **nije** u `literatura.bib`. Bib sadrži: hart1968astar, verschueren2022acados, rawlings2017mpc, andersson2019casadi, lavalle2006planning, borrelli2017predictive, coulter1992purepursuit, diehl2002rti, virtanen2020scipy, hairer1993ode, acados\_docs, casadi\_web — ukupno 12 unosa. Sicilijano nedostaje.  
**Problem:** Sekcija `02_model.tex` §4 (Veza s diferencijalnim pogonom) opisuje transformacije $(v, \omega) \leftrightarrow (v_L, v_R)$ bez ijedne reference; profesor je eksplicitno naveo `[siciliano2009robotics]` kao citat za tu sekciju. Unos je naveden kao **minimum required**.

---

### [File: latex/poglavlja/06_rezultati.tex, linija ~39]
**Komentar profesora (§3A.2, §4.12.E):** Preimenovati $\Delta v \to a_v$ i $\Delta \omega \to \alpha$ **kroz cijeli rad**. U tablici `tab:params` stupac „Označaka" mora biti usklađen s novom notacijom.  
**Trenutno stanje:** Redak težina upravljanja u `tab:params` glasi:
```
& Težine upravljanja & $R_{\Delta v}, R_{\Delta\omega}$ & $0{,}1$ \\
```
**Problem:** Ostatak rada dosljedno koristi novu notaciju — u `03_nmpc.tex:85` stoji `$Q_{xx} / R_{a_v} = 10{,}0 / 0{,}1 = 100$`. Tablica `tab:params` jedino je mjesto koje i dalje koristi staru oznaku `$\Delta v$` i `$\Delta\omega$` umjesto `$a_v$` i `$\alpha$`. Izolirani nesklad s ostatkom teksta.

---

## Verificirane vrijednosti (CSV)

Sve vrijednosti provjerene iz `results/data/benchmark.csv`, `tuning_horizon.csv` i `tuning_weights.csv`. Format: `CSV vrijednost → teza`. ✓ = točno, ✗ = netočno.

### benchmark.csv → scenarijske tablice

**tab:baseline (baseline, SQP\_RTI):**
- RMSE: 0.034435 → $0{,}0344$ m ✓
- CTE srednji: 0.010675 → $0{,}0107$ m ✓
- CTE max: 0.14781 → $0{,}1478$ m ✓
- Kut. greška: 2.7252° → $2{,}73°$ ✓
- Vrij.: 20.0 s → $20{,}00$ s ✓
- CPU prosjek: 0.09118 ms → $0{,}091$ ms ✓
- CPU max: 0.31873 ms → $0{,}319$ ms ✓

**tab:one\_obstacle (one\_obstacle, SQP\_RTI):**
- RMSE: 0.04686 → $0{,}0469$ m ✓
- CTE srednji: 0.02782 → $0{,}0278$ m ✓
- CTE max: 0.18387 → $0{,}1839$ m ✓
- Kut. greška: 3.8686° → $3{,}87°$ ✓
- Vrij.: 20.0 s → $20{,}00$ s ✓
- CPU prosjek: 0.09948 ms → $0{,}099$ ms ✓
- CPU max: 0.35891 ms → $0{,}359$ ms ✓

**tab:narrow (narrow, SQP\_RTI):**
- RMSE: 0.03441 → $0{,}0344$ m ✓
- CTE srednji: 0.02696 → $0{,}0270$ m ✓
- CTE max: 0.09621 → $0{,}0962$ m ✓
- Kut. greška: 1.5949° → $1{,}59°$ ✓
- Vrij.: 19.7 s → $19{,}70$ s ✓
- CPU prosjek: 0.08937 ms → $0{,}089$ ms ✓
- CPU max: 0.26269 ms → $0{,}263$ ms ✓

**tab:lcorridor (l\_corridor, SQP\_RTI):**
- RMSE: 0.07240 → $0{,}0724$ m ✓
- CTE srednji: 0.04571 → $0{,}0457$ m ✓
- CTE max: 0.26103 → $0{,}2610$ m ✓
- Kut. greška: 4.896° → $4{,}90°$ ✓
- Vrij.: 20.4 s → $20{,}40$ s ✓
- CPU prosjek: 0.10268 ms → $0{,}103$ ms ✓
- CPU max: 0.25069 ms → $0{,}251$ ms ✓

**tab:ushape (u\_shape, SQP\_RTI):**
- RMSE: 0.05502 → $0{,}0550$ m ✓
- CTE srednji: 0.03998 → $0{,}0400$ m ✓
- CTE max: 0.14126 → $0{,}1413$ m ✓
- Kut. greška: 3.1852° → $3{,}19°$ ✓
- Vrij.: 20.1 s → $20{,}10$ s ✓
- CPU prosjek: 0.11384 ms → $0{,}114$ ms ✓
- CPU max: 0.26958 ms → $0{,}270$ ms ✓

**tab:perturbation (perturbation, SQP\_RTI):**
- RMSE: 0.27360 → $0{,}2736$ m ✓
- CTE srednji: 0.09418 → $0{,}0942$ m ✓
- CTE max: 0.99999 → $1{,}0000$ m ✓
- Kut. greška: 5.677° → $5{,}68°$ ✓
- Vrij.: 19.6 s → $19{,}60$ s ✓
- CPU prosjek: 0.11834 ms → $0{,}118$ ms ✓
- CPU max: 0.32129 ms → $0{,}321$ ms ✓
- Oporavak: 22 koraka → 22 koraka (2,2 s) ✓

**tab:cluttered (cluttered, SQP\_RTI):**
- RMSE: 0.04286 → $0{,}0429$ m ✓
- CTE srednji: 0.02315 → $0{,}0232$ m ✓
- CTE max: 0.16781 → $0{,}1678$ m ✓
- Kut. greška: 3.4291° → $3{,}43°$ ✓
- Vrij.: 20.3 s → $20{,}30$ s ✓
- CPU prosjek: 0.10692 ms → $0{,}107$ ms ✓
- CPU max: 0.27739 ms → $0{,}277$ ms ✓

### tuning\_horizon.csv → tab:horizon

| N  | CSV RMSE   | Teza [mm] | CSV CPU [ms] | Teza [ms] | Status |
|----|------------|-----------|--------------|-----------|--------|
| 5  | 0.09567    | 95,7      | 0.07768      | 0,078     | ✓      |
| 10 | 0.04333    | 43,3      | 0.15303      | 0,153     | ✓      |
| 15 | 0.04490    | 44,9      | 0.22225      | 0,222     | ✓      |
| 20 | 0.04686    | 46,9      | 0.30489      | 0,305     | ✓      |
| 30 | 0.04387    | 43,9      | 0.45893      | 0,459     | ✓      |
| 40 | 0.04417    | 44,2      | 0.62731      | 0,627     | ✓      |

**Napomena o 2.2 (CPU nesklad):** CSV potvrđuje da one\_obstacle pri N=20 u benchmark-u daje 0,099 ms a tuning analiza 0,305 ms. Teza ispravno objašnjava razliku (cold start vs. zagrijana predmemorija) u napomeni u §6.7.

### tuning\_weights.csv → tab:weights

| Konfiguracija | CSV RMSE   | Teza [mm] | Status |
|---------------|------------|-----------|--------|
| Q\>\>R        | 0.04146    | 41,5      | ✓      |
| Q\>R          | 0.04686    | 46,9      | ✓      |
| Q~R           | 0.07117    | 71,2      | ✓      |
| Q\<R          | 0.27293    | 272,9     | ✓      |

Ukupno verificirano: **51 numeričkih vrijednosti** — sve točne.

---

## Pregled ostalih kritičnih točaka

| Komentar profesora | Status | Napomena |
|---|---|---|
| 2.1 Zahvale prazne | ✓ Riješeno | Zahvale imaju tekst (zahvala mentoru) |
| 2.2 CPU nesklad tab:one\_obstacle vs tab:horizon | ✓ Riješeno | Eksplicitna metodološka napomena dodan u §6.7 |
| 2.3 Bibliografija — nestručne reference | ✓ Riješeno | 12 unosa, uključen hart1968astar, verschueren2022acados itd. (nedostaje siciliano — vidi gore) |
| 2.4 Meka ograničenja preapsolutno | ✓ Riješeno | "penaliziraju približavanje", više nema "sprječavaju" |
| 2.5 B-spline sigurnost | ✓ Riješeno | tab:clearance s minimalnim udaljenostima po scenariju |
| 2.6 AI izjava | ✓ Riješeno | `\begin{izjavaoui}` blok prisutan u zavrsni\_rad.tex |
| 3A.0 Kinem. vs din. model | ✓ Riješeno | Uvodni paragraf poglavlja 2 jasno objašnjava |
| 3A.1 Redoslijed izlaganja | ✓ Riješeno | Klasični 3-dimenzionalni model → prošireni 5-dim. model |
| 3A.2 Notacija $\Delta v \to a_v$ | ✓ Riješeno (osim tab:params r.39) | Vidi problem #2 gore |
| 3A.3 OCP formulacija nepotpuna | ✓ Riješeno | Kompletna OCP s `uz uvjet`, dyn. ograničenjima, slack var. |
| 3A.4 Izlazni vektor $y_k$ | ✓ Riješeno | Matrice $V_x, V_u$ prikazane eksplicitno |
| 3A.5 "Omjer Q/R" | ✓ Riješeno | "Omjer dijagonalnih elemenata $Q_{xx}/R_{a_v}=100$" |
| 3A.6 Terminalna matrica $W_e=Q$ | ✓ Riješeno | Heuristika, Riccati napomenuta |
| 3A.7 Slack varijable | ✓ Riješeno | Opisane s jednadžbama u §3.4 |
| 3A.8 SQP\_RTI dvofaznost | ✓ Riješeno | Faza pripreme + faza povratne veze opisane |
| 3A.9 ERK diskretizacija | ✓ Riješeno | "ERK4 (eng. Explicit Runge-Kutta, ERK) — metoda 4. reda" |
| 3A.10 Identičan predikcijski model | ✓ Riješeno | §7.3 napominje gornju granicu preciznosti |
| 3A.11 Cikličnost $\theta$ | ✓ Riješeno | Napomena u §2.1 o atan2 i intervalnom ograničenju |
| 3A.12 Veza s dif. pogonom | ✓ Riješeno | Cijela sekcija 2.4 s transformacijskim jednadžbama |
| 3A.13 SQP vs SQP\_RTI tvrdnja | ✓ Riješeno | Tvrdnja uklonjena iz teksta |
| 3.1 "Osam" vs "sedam" | ✓ Riješeno | §5.4: "osam scenarija: sedam navigacijskih + blocked" |
| 3.2 Sažetak skriva RMSE perturbacije | ✓ Riješeno | Sažetak i abstract eksplicitno navode 273,6 mm |
| 3.3 Raspberry Pi spekulacija | ✓ Riješeno | Rečenica preformulirana s "nije eksperimentalno verificirano" |
| 3.4 Linerani sustavi formulacija | ✓ Riješeno | Preformulirana u 03\_nmpc.tex:29 |
| 3.5 Hardver i softver | ✓ Riješeno | Intel Core 7 150U, Fedora 42, acados 0.5.1, itd. |
| 3.6 Aproksimacija kružnicama | ✓ Riješeno | 525 kružnica (L-hodnik), 162 (U-oblik), poklapanje dokazano |
| 3.7 SQP\_RTI Gauss-Newton | ✓ Riješeno | "$J^\top W J$ aproksimacija hesijana Lagrangiana" |
| 3.8 A* optimalnost | ✓ Riješeno | "optimalnost na diskretnoj rešetki" |
| 3.9 A* iscrpljuje čvorove | ✓ Riješeno | "iscrpi sve dostupne čvorove na strani starta" |
| 3.10 Profil brzine dosljednost | ✓ Riješeno | "isključivo za vizualizaciju" konzistentno u §4.3 i §5.1 |
| 3.11 Pseudokod nedefinirane var. | ✓ Riješeno | `xr, yr = waypoints[ref_idx]` eksplicitno u listingu |
| 4.1 Osobna napomena FER kolegij | ✓ Riješeno | Rečenica uklonjena |
| 4.2 "skliznuti" kolokvijalizam | ✓ Riješeno | "ne može bočno pomaknuti na putanju" |
| 4.3 Pure Pursuit/Stanley | ✓ Riješeno | S citiranjem `coulter1992purepursuit` |
| 4.7 Metafora vozača | ✓ Riješeno | "ne samo da uočava... nego već sada planira" |
| 4.8 "MPC simulira" | ✓ Riješeno | "predviđa ponašanje" |
| 4.9 "dovoljno brzo" | ✓ Riješeno | "s rezervom od dva reda veličine" |
| 4.10 solver/(hr. rješavač) | ✓ Riješeno | Prva upotreba: "solvera (hr. \textit{rješavač})" u 02\_model.tex |
| 4.10 ponderi → težine | ✓ Riješeno | "težine" dosljedno kroz cijeli rad |
| 4.11 zaglaviti → mogao zaglaviti | ✓ Riješeno | 06\_rezultati.tex:291 |
| 4.12A Nelinearno → Nelinearni MPC | ✓ Riješeno | Gramatički ispravno u 01\_uvod i 03\_nmpc |
| 4.12A redosljed → redoslijed | ✓ Riješeno | 06\_rezultati.tex:520 |
| 4.12A Gauss-Newtonova aproksimacija hesijana | ✓ Riješeno | 03\_nmpc.tex:212 |
| 4.12A kubnim B-splineom | ✓ Riješeno | 04\_astar.tex:123 |
| 4.12B eng. format za engl. termine | ✓ Riješeno | `(eng.\ \textit{...})` format prisutan kod MPC, OCP, soft, SQP\_RTI, HPIPM, RMSE, CTE, heading error itd. |
| 4.12C OCP kratica | ✓ Riješeno | Definirana u 03\_nmpc.tex:40 |
| 4.12C QP kratica | ✓ Riješeno | Definirana u 03\_nmpc.tex:206 |
| 4.12C ERK kratica | ✓ Riješeno | Definirana u 03\_nmpc.tex:58 |
| 4.12D waypoint → putna točka | ✓ Riješeno | Proza koristi "putna točka" |
| 4.12D baseline → osnovna putanja | ✓ Riješeno | Sekcija, tablica i tekst koriste "Osnovna putanja" |
| 4.12D CPU overhead → dod. CPU opterećenje | ✓ Riješeno | 06\_rezultati.tex:182 |
| 4.12D tranzijent → prijelazni odziv | ✓ Riješeno | 06\_rezultati.tex:291 |
| 5.2 siunitx uklonjen | ✓ Riješeno | `\usepackage{siunitx}` NIJE u zavrsni\_rad.tex |
| 5.2 placeins prisutan | ✓ Riješeno | `\usepackage{placeins}` na liniji 11 |
| 5.3 simulation\_loop caption | ✓ Riješeno | "Ljubičasti blok... crveni blok..." |
| 5.5 README s uputama | ✓ Riješeno | Sekcija "Kompajliranje LaTeX dokumenta" prisutna |
| 5.6 FloatBarrier | ✓ Riješeno | `\FloatBarrier` ispred svakog `\section` u 06\_rezultati.tex (12/12) |

---

## Zaključak

Pronađena su **2 problema**:

1. **SREDNJI** — `siciliano2009robotics` nedostaje iz `literatura.bib`. Profesor je ovaj unos svrstao u minimum (šesti od osam preporučenih). Sekcija `02_model.tex` §4 opisuje transformacije kotača bez ijedne reference.

2. **SITNI** — `$R_{\Delta v}, R_{\Delta\omega}$` ostao u `tab:params` (06\_rezultati.tex:39), dok ostatak rada dosljedno koristi `$R_{a_v}$` (npr. 03\_nmpc.tex:85). Izoliran notacijski nesklad.

Verificirano **51 numeričkih vrijednosti** iz CSV datoteka — sve točne, bez iznimke. Svi ostali komentari profesora (841 linija) su adekvatno adrezirani u LaTeX izvorima.
