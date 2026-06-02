"""
EFFETTO DELL'OZONO E VALIDAZIONE MONTE CARLO

Analizza l'assorbimento UV da parte dello strato di ozono atmosferico e
valida il metodo Monte Carlo confrontandolo con il calcolo analitico esatto.

Il file dei dati della sezione d'urto dell'ozono deve trovarsi nella stessa
cartella dello script: SCIA_O3_Temp_cross-section_V4.1.DAT

Produce tre grafici:
    1. Confronto della distribuzione spettrale al zenit con e senza ozono,
       evidenziando l'assorbimento UV.
    2. Sezione d'urto di assorbimento dell'ozono in funzione della lunghezza
       d'onda (scala logaritmica).
    3. Validazione: confronto pannello sinistro (calcolo analitico) e pannello
       destro (Monte Carlo) per le stesse condizioni.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from costanti import T_sole, n_samples, N_O3_col, FILE_OZONO
from atmosfera import simula_fotoni, fotoni_planck, beta_rayleigh, massa_aria
import stile_grafici

# --- Caricamento dati ozono ---
print(f"Carico dati da: {FILE_OZONO}")
dati_oz = np.loadtxt(FILE_OZONO, skiprows=20)
lam_oz  = dati_oz[:, 0]  # lambda (nm)
sig_oz  = dati_oz[:, 5]  # sezione d'urto a 293 K (cm^2)

# Conversione unità: nm -> m, cm^2 -> m^2
# Colonna a 293 K scelta come rappresentativa della temperatura ambiente
# Fuori dal range dei dati la funzione restituisce 0
sigma_interp = interp1d(lam_oz * 1e-9, sig_oz * 1e-4,
                        bounds_error=False, fill_value=0.0)

# --- Simulazione con e senza ozono allo zenit ---
n_iniz_s, n_rayleigh = simula_fotoni(0, T_sole, n_samples)
_, n_ray_oz          = simula_fotoni(0, T_sole, n_samples,
                                     sigma_oz=sigma_interp, N_oz=N_O3_col)
print(f"Fotoni generati da Planck: {len(n_iniz_s)}")

# Grafico 2: sezione d'urto dell'ozono
lam_plot = np.linspace(10e-9, 2000e-9, 5000)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(lam_plot * 1e9, sigma_interp(lam_plot), color='darkorange')
ax.set_yscale('log')
ax.axvspan(380, 750, alpha=0.2, color='yellow', label='Visibile')
ax.set_xlabel('lambda [nm]')
ax.set_ylabel('sigma_O3(lambda) [m^2]')
ax.set_title('Sezione d\'urto di assorbimento dell\'ozono (293 K)')
ax.legend()
plt.tight_layout()
plt.show()

# Grafico 1: confronto con e senza ozono
fig, ax = plt.subplots(figsize=(10, 6))
bins = np.linspace(10, 2000, 120)
ax.axvspan(380, 750, alpha=0.2, color='yellow', label='Visibile')
ax.axvline(380, color='purple',  linestyle='--', alpha=0.6)
ax.axvline(750, color='darkred', linestyle='--', alpha=0.6)
ax.hist(n_iniz_s   * 1e9, bins=bins, alpha=0.4, color='navy',       label='N_0 (spazio)')
ax.hist(n_rayleigh * 1e9, bins=bins, alpha=0.6, color='green',      label='Zenith (solo Rayleigh)')
ax.hist(n_ray_oz   * 1e9, bins=bins, alpha=0.6, color='darkorange', label='Zenith (Rayleigh + O3)')
ax.set_xlim(100, 800)
ax.set_xlabel('lambda [nm]')
ax.set_ylabel('Numero di fotoni')
ax.set_title(f'Effetto dell\'ozono - Sole (T = {T_sole} K) allo Zenith')
ax.legend()
plt.tight_layout()
plt.show()

# --- Validazione Monte Carlo vs analitico ---
lam       = np.linspace(10e-9, 2000e-9, 5000)
D_lam     = fotoni_planck(lam, T_sole)
S         = massa_aria(0)
D_rayleigh = D_lam * np.exp(-beta_rayleigh(lam) * S)
D_ozono    = D_lam * np.exp(-(beta_rayleigh(lam) * S + sigma_interp(lam) * N_O3_col))

D_lam_norm = D_lam     / np.max(D_lam)
D_ray_norm = D_rayleigh / np.max(D_lam)
D_oz_norm  = D_ozono   / np.max(D_lam)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

ax1.plot(lam * 1e9, D_lam_norm, label='N_0 (spazio)',           color='navy')
ax1.plot(lam * 1e9, D_ray_norm, label='Zenith (Rayleigh)',      color='green')
ax1.plot(lam * 1e9, D_oz_norm,  label='Zenith (Rayleigh + O3)', color='darkorange')
ax1.axvspan(380, 750, alpha=0.2, color='yellow')
ax1.axvline(380, color='purple',  linestyle='--', alpha=0.6)
ax1.axvline(750, color='darkred', linestyle='--', alpha=0.6)
ax1.set_xlabel('lambda [nm]')
ax1.set_ylabel('D(lambda, T) normalizzato')
ax1.set_title('Analitico')
ax1.set_yscale('log')
ax1.set_ylim(1e-6, 2)
ax1.set_xlim(100, 800)
ax1.legend()

bins = np.linspace(10, 2000, 120)
ax2.hist(n_iniz_s   * 1e9, bins=bins, alpha=0.4, color='navy',       label='N_0 (spazio)',           density=True)
ax2.hist(n_rayleigh * 1e9, bins=bins, alpha=0.6, color='green',      label='Zenith (Rayleigh)',      density=True)
ax2.hist(n_ray_oz   * 1e9, bins=bins, alpha=0.6, color='darkorange', label='Zenith (Rayleigh + O3)', density=True)
ax2.axvspan(380, 750, alpha=0.2, color='yellow')
ax2.axvline(380, color='purple',  linestyle='--', alpha=0.6)
ax2.axvline(750, color='darkred', linestyle='--', alpha=0.6)
ax2.set_xlabel('lambda [nm]')
ax2.set_ylabel('Densità normalizzata')
ax2.set_title('Monte Carlo')
ax2.set_yscale('log')
ax2.set_ylim(1e-8, 2)
ax2.set_xlim(100, 800)
ax2.legend()

fig.suptitle(f'Validazione: Sole (T = {T_sole} K) allo Zenith - analitico vs MC')
plt.tight_layout()
plt.show()
