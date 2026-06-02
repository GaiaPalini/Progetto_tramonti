# Tramonti
La cartella contiene i codici necessari a simulare la propagazione di fotoni solari attraverso l'atmosfera terrestre tramite il metodo Monte Carlo, per studiare il fenomeno del tramonto e l'effetto dell'ozono.

## Struttura del progetto

  ### Moduli
  * costanti.py — costanti fisiche fondamentali e parametri atmosferici usati da tutti gli script
  * atmosfera.py — funzioni fisiche della simulazione: distribuzione di Planck, coefficiente di Rayleigh, spessore di massa d'aria e campionamento Monte Carlo
  * stile_grafici.py — impostazione di stile comune a tutti i grafici

  ### Script

  * simulazione_sole.py

    Simula la distribuzione spettrale dei fotoni solari (T = 5750 K) dopo l'attraversamento dell'atmosfera a diversi angoli zenitali.

    Produce due grafici:
      * Distribuzione spettrale fuori atmosfera, allo zenit e all'orizzonte
      * Flusso integrato (spettro totale e visibile) in funzione dell'angolo zenitale

  * tramonti_esotici.py

    Ripete la simulazione per stelle di temperatura diversa dal Sole: Proxima Centauri (2900 K), Alkaid (15500 K) e v Ori (33000 K). Permette di confrontare come cambierebbe il tramonto su un pianeta con atmosfera terrestre che orbita attorno a stelle diverse.

    Produce due grafici:
      * Distribuzione spettrale per ogni stella (pannello 2x2)
      * Flusso integrato vs angolo zenitale per tutte le stelle a confronto

  * ozono.py

    Studia l'effetto dell'assorbimento UV da parte dello strato di ozono e valida il metodo Monte Carlo confrontandolo con il calcolo analitico esatto. I dati della sezione d'urto dell'ozono sono presi da misure satellitari SCIAMACHY.
    Fonte dati: https://www.iup.uni-bremen.de/UVSAT_material/data/xsections/

    Produce tre grafici:
      * Sezione d'urto dell'ozono in funzione della lunghezza d'onda
      * Confronto spettrale con e senza ozono allo zenit
      * Validazione analitico vs Monte Carlo

## Come eseguire il progetto

I moduli costanti.py e atmosfera.py non vanno eseguiti direttamente ma vengono importati automaticamente dagli script. Per eseguire la simulazione completa lanciare i tre script nell'ordine seguente:

     simulazione_sole.py
     tramonti_esotici.py
     ozono.py

Il file SCIA_O3_Temp_cross-section_V4.1.DAT deve trovarsi nella stessa cartella degli script, ed è richiesto solo da ozono.py.

