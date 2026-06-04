"""
TRAMONTI ESOTICI - CONFRONTO TRA STELLE DIVERSE

Simula come apparirebbe un tramonto su un pianeta con atmosfera terrestre
ma illuminato da stelle di temperatura diversa dal Sole.

Le stelle simulate sono:
    - Sole           (T = 5750 K)
    - Proxima Centauri (T = 2900 K)
    - Alkaid         (T = 15500 K)
    - v Ori          (T = 33000 K)

Produce due grafici:
    1. Distribuzione spettrale dei fotoni a zenit e orizzonte per ogni stella
       (pannello 2x2).
    2. Flusso integrato (totale e visibile) vs angolo zenitale per tutte le
       stelle, sovrapposto in un unico grafico per confronto diretto.

"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from costanti import n_samples, angoli, angoli_gradi, stelle, colori_stelle
from atmosfera import simula_fotoni, flusso_integrato
import stile_grafici

# --- Distribuzioni spettrali per ogni stella ---
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

for i, (nome, T) in enumerate(stelle.items()):
    ax = axes[i // 2, i % 2]

    n_0, n_zenith = simula_fotoni(0,       T, n_samples, 10e-9, 2000e-9)
    _, n_oriz     = simula_fotoni(np.pi/2, T, n_samples, 10e-9, 2000e-9)

    bins = np.linspace(10, 2000, 120)
    ax.axvspan(380, 750, alpha=0.2, color='yellow')
    ax.axvline(380, color='purple',   linestyle='--', alpha=0.6)
    ax.axvline(750, color='darkred',  linestyle='--', alpha=0.6)
    ax.hist(n_0      * 1e9, bins=bins, alpha=0.5, color='navy',     label='N_0 (spazio)')
    ax.hist(n_zenith * 1e9, bins=bins, alpha=0.8, color='green',    label='Zenith')
    ax.hist(n_oriz   * 1e9, bins=bins, alpha=0.8, color='orangered',label='Orizzonte')
    ax.set_xlabel('lambda [nm]')
    ax.set_ylabel('Numero di fotoni')
    ax.set_title(f'{nome} (T = {T} K)')
    ax.legend(fontsize=9)

plt.tight_layout()
plt.show()

# --- Flusso integrato vs angolo zenitale per tutte le stelle ---
flussi_vis_stelle = {}
flussi_tot_stelle = {}

for nome, T in stelle.items():
    f_tot = []
    f_vis = []
    for theta in tqdm(angoli, desc=nome):
        f_tot.append(flusso_integrato(theta, T, n_samples, 10e-9,  2000e-9))
        f_vis.append(flusso_integrato(theta, T, n_samples, 380e-9, 750e-9))
    flussi_tot_stelle[nome] = np.array(f_tot)
    flussi_vis_stelle[nome] = np.array(f_vis)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

for nome, T in stelle.items():
    ax1.plot(angoli_gradi, flussi_tot_stelle[nome], 'o-',
             color=colori_stelle[nome], label=f'{nome} ({T} K)', markersize=5)
    ax2.plot(angoli_gradi, flussi_vis_stelle[nome], 'o-',
             color=colori_stelle[nome], label=f'{nome} ({T} K)', markersize=5)

ax1.set_xlabel('Angolo zenitale theta [gradi]')
ax1.set_ylabel(r'$N_{obs} / N_0$')
ax1.set_title('Spettro totale (10 - 2000 nm)')
ax1.set_ylim(0, 1.05)

ax2.set_xlabel('Angolo zenitale theta [gradi]')
ax2.set_ylabel(r'$N_{obs} / N_0$')
ax2.set_title('Spettro visibile (380 - 750 nm)')
ax2.set_ylim(0, 1.05)
ax2.legend(loc='center left', bbox_to_anchor=(1.05, 0.5),
           borderaxespad=0., frameon=True, ncol=1)

plt.tight_layout()
plt.show()
