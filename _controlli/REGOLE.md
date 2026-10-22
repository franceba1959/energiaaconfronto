# Regole del controllo settimanale di Energia a Confronto

Questa cartella non viene pubblicata sul sito (GitHub Pages esclude le cartelle che iniziano con `_`).
Contiene lo script dei controlli automatici e le regole che chi esegue il controllo deve applicare.

## Regole editoriali del sito

1. Si pubblicano solo dati letti dentro documenti di enti pubblici o organismi internazionali. Fonti ammesse: IEA, IRENA, IPCC, Lazard (solo come modello USA dichiarato), Eurostat, JRC, ENTSO-E, GSE, Terna, ARERA, ENEA, ISPRA, ARPA, UN-ECE, Banca d'Italia, ministeri e Gazzetta Ufficiale. La stampa di settore serve solo per orientarsi; le fonti commerciali sono escluse. Una fonte non istituzionale si può citare solo con una nota gialla che dice chi è e perché la si riporta.
2. Un numero non letto in un documento non si pubblica: prima si cerca chi lo pubblica; se non lo si trova, il numero resta fuori. Scrivere «calcolato da noi» non basta. Niente sottrazioni, percentuali, conversioni di unità o somme fatte da noi.
3. Ogni citazione punta al documento e, per i PDF, alla pagina (`#page=N`), non alla home page dell'ente. Un link preciso ma sbagliato è peggio di uno vago: va aperto prima di pubblicarlo.
4. Nessuna classifica fra tecnologie, nessuna previsione, nessuna causa unica per fenomeni complessi. I confronti si riportano solo se li fa la fonte stessa.
5. Non si mettono accanto grandezze di base diversa (per esempio emissioni di combustione e di ciclo di vita, stime e conteggi, percentuali e valori assoluti) senza dirlo.
6. I vuoti si dichiarano con `[DA VERIFICARE: motivo]`. Un vuoto è un'affermazione da verificare come un numero: si scrive «non risulta reperito», mai «non esiste». Una nota DA VERIFICARE che parla di una frase già tolta va eliminata.
7. Termini tecnici in italiano, con l'inglese fra parentesi solo la prima volta; sigle sciolte la prima volta.
8. Nella stessa scheda, e nelle schede della home, uno stesso dato compare una volta sola e in una sola forma (per il funzionamento: ore equivalenti su 8.760). Home e scheda di dettaglio devono riportare lo stesso valore.
9. Ogni nota copiata da una scheda all'altra deve essere vera per la tecnologia della pagina in cui si trova.
10. La data «Aggiornato: mese anno» si aggiorna quando la pagina cambia nei contenuti.

## Procedura del controllo

1. Clonare il repository ed eseguire `python3 _controlli/controllo_sito.py --out report_automatico.md`.
2. Correggere subito e pubblicare gli **errori meccanici**: doppioni nella stessa scheda o in home, note DA VERIFICARE riferite a frasi già tolte, note copiate che citano un'altra tecnologia, valori diversi fra home e scheda quando la scheda riporta il valore con la fonte, tag HTML sbilanciati, date «Aggiornato» da allineare dopo una modifica.
3. **Non** correggere da soli, ma proporre nel report: dati nuovi o cambiati, testi riscritti, link da sostituire con il documento specifico, note DA VERIFICARE che sembrano risolvibili. Per ognuna: testo originale, correzione proposta, fonte con link e pagina.
4. Controllo di giudizio a rotazione: ogni settimana leggere per intero 3 pagine (la rotazione segue l'elenco qui sotto, ripartendo dall'inizio quando finisce; la settimana dell'anno modulo 7 dà il gruppo) e verificare le regole 1-7 aprendo almeno 5 fonti citate per pagina.
   - gruppo 0: index.html, schede/fotovoltaico.html, schede/eolico-onshore.html
   - gruppo 1: contesto.html (prima metà)
   - gruppo 2: contesto.html (seconda metà), dibattito.html
   - gruppo 3: schede/eolico-offshore.html, schede/idroelettrico.html, schede/geotermico.html
   - gruppo 4: schede/gas-naturale.html, schede/carbone.html, schede/biometano.html
   - gruppo 5: schede/nucleare-fissione-smr.html, schede/fusione-nucleare.html, schede/idrogeno-verde.html
   - gruppo 6: schede/comunita-energetiche.html, schede/risparmio-casa.html, schede/risparmio-trasporti.html, schede/risparmio-industria.html, schede/innovazioni-future.html
5. Ogni pubblicazione: commit con messaggio chiaro, push su `main`, poi verifica che il file online sia identico a quello locale.
6. Il report finale è un documento Word con: data, esito dei controlli automatici, correzioni fatte (testo originale accanto alla correzione), proposte in attesa di approvazione, pagine lette nel controllo di giudizio, note DA VERIFICARE ancora aperte. In fondo: numeri calcolati presenti (devono essere zero) e vuoti dichiarati senza verifica.
