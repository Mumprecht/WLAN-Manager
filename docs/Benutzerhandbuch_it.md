# Manuale utente di WLAN-Manager

## Avvio

Nella directory del progetto:

```powershell
python src\main.py
```

All’avvio, Windows può richiedere i diritti di amministratore.

## Visualizzare i profili WLAN

Dopo l’avvio, tutti i profili WLAN salvati vengono visualizzati automaticamente.

Con `F5` è possibile aggiornare l’elenco.

## Copiare contenuti dall’elenco dei profili

Il contenuto di una cella della tabella può essere copiato negli appunti.

Fare clic con il pulsante destro del mouse sulla cella desiderata e selezionare dal menu contestuale:

```text
Copia    Ctrl+C
```

In alternativa, selezionare la cella desiderata e premere:

```text
Ctrl+C
```

In questo modo è possibile copiare, ad esempio, il nome del profilo WLAN, l’autenticazione o il contenuto della password visualizzato nella tabella.

## Visualizzare le password WLAN

Menu:

```text
WLAN > Mostra password
```

Scorciatoia da tastiera:

```text
Ctrl+P
```

Le password vengono visualizzate in chiaro.

## Connettersi a una WLAN

È possibile connettersi tramite un profilo salvato facendo doppio clic su di esso.

In alternativa:

```text
Profili > Connetti
```

oppure:

```text
Ctrl+Enter
```

## Eseguire il backup dei profili WLAN

Menu:

```text
File > Backup profili WLAN...
```

È possibile selezionare uno, più o tutti i profili.

Facoltativamente, è possibile creare una nuova sottocartella con data e ora.

Per aggiungere backup a una cartella esistente, disattivare questa opzione.

Se esiste già un file XML, sono disponibili le seguenti opzioni:

- Sovrascrivi
- Ignora
- Annulla

## Ripristinare i profili WLAN

Menu:

```text
File > Ripristina profili WLAN...
```

È possibile selezionare uno, più o tutti i file XML.

## Eliminare i profili WLAN

Menu:

```text
Profili > Elimina profili WLAN...
```

È possibile eliminare uno, più o tutti i profili.

Prima dell’eliminazione viene visualizzata una richiesta di conferma.

## Esportazione CSV

Menu:

```text
File > Esporta CSV...
```

Il file CSV può contenere password WLAN in chiaro.

## Connessione WLAN attuale

Menu:

```text
WLAN > Connessione attuale
```

Scorciatoia da tastiera:

```text
Ctrl+I
```

## Gestire le connessioni WLAN automatiche e la priorità

Menu:

```text
WLAN > Gestire le connessioni WLAN automatiche...
```

Questa funzione consente di gestire lo stato di connessione automatica e la priorità dei profili WLAN salvati.

La tabella mostra:

- **Priorità** – ordine con cui Windows preferisce i profili WLAN.
- **Profilo WLAN** – nome del profilo WLAN salvato.
- **Connessione automatica** – indica con **Sì** o **No** se Windows può connettersi automaticamente utilizzando questo profilo.

### Modificare la priorità WLAN

**La priorità 1 è la priorità più alta.**

Con **Sposta su** e **Sposta giù** è possibile spostare un profilo nell’ordine di priorità.

La modifica viene salvata immediatamente in Windows. WLAN-Manager legge quindi nuovamente l’elenco dei profili da Windows e visualizza l’ordine effettivamente memorizzato.

In Windows, la priorità WLAN è associata alla relativa interfaccia WLAN.

### Modificare la connessione automatica

Con **Modifica connessione automatica** si commuta il profilo selezionato tra **Sì** e **No**.

- **Sì** – Windows può connettersi automaticamente utilizzando questo profilo.
- **No** – Windows non si connette automaticamente utilizzando questo profilo. È comunque possibile stabilire manualmente la connessione.

La modifica viene salvata immediatamente in Windows e successivamente riletta da Windows.

### Note

I profili gestiti tramite criteri amministrativi o Criteri di gruppo potrebbero non essere modificabili.

**Aggiorna** rilegge lo stato corrente dei profili WLAN da Windows senza apportare modifiche.

## Scorciatoie da tastiera

- `F5` Aggiorna
- `Ctrl+C` Copia il contenuto della cella selezionata
- `Ctrl+S` Backup
- `Ctrl+R` Ripristina
- `Canc` Elimina
- `Ctrl+P` Mostra password
- `Ctrl+I` Connessione attuale
- `Ctrl+Enter` Connetti
- `Ctrl+Shift+S` Esporta CSV
- `Ctrl+Q` Esci
- `F1` Informazioni su WLAN-Manager

## Licenza e copyright

Copyright © 2026 Urs Mumprecht / Mumprecht Software.

WLAN-Manager è un software proprietario e può essere utilizzato gratuitamente per scopi privati e per altri scopi non commerciali.

L’uso commerciale, la modifica, la ridistribuzione, la ripubblicazione o la creazione di opere derivate non sono consentiti senza la previa autorizzazione scritta del titolare del copyright.

Si applica la seguente licenza:

**WLAN-Manager Non-Commercial License, Version 1.0**

Le condizioni complete della licenza sono contenute nel file `LICENSE`.

## Sicurezza

I file XML di backup contenenti chiavi in chiaro e i file CSV contenenti password devono essere trattati come riservati.

## Codice QR WLAN

Selezionare un profilo WLAN salvato e quindi:

```text
Profili > Mostra codice QR...
```

In alternativa, la funzione è disponibile nel menu contestuale del profilo.

La finestra di dialogo mostra:

- SSID
- Autenticazione
- Password WLAN mascherata
- Codice QR

Se necessario, è possibile visualizzare la password.

Il codice QR può essere salvato come PNG o copiato negli appunti come immagine. Smartphone e tablet possono utilizzare il codice per importare i dati di accesso WLAN.

I profili WLAN Enterprise non sono attualmente supportati.

## Aiuto

Con `F1` oppure tramite:

```text
Aiuto > Manuale utente
```

questo manuale utente viene visualizzato direttamente in WLAN-Manager.

In:

```text
Aiuto > Informazioni sul progetto
```

vengono visualizzate informazioni tecniche sulla versione installata, Python, PySide6, Windows e sulla directory dei log.

In:

```text
Aiuto > Informazioni su WLAN-Manager
```

vengono visualizzati il nome del programma, la versione, l’azienda, il copyright e l’autore.

## Creare un profilo WLAN

Tramite:

```text
Profili > Nuovo profilo WLAN...
```

è possibile creare un nuovo profilo WLAN.

Informazioni richieste:

- Nome profilo
- SSID
- Tipo di sicurezza
- Password per WLAN protette

Opzioni aggiuntive:

- Connetti automaticamente
- Consenti la connessione a un SSID nascosto

## Modificare un profilo WLAN

Selezionare un profilo esistente e scegliere:

```text
Profili > Modifica profilo WLAN...
```

oppure utilizzare la voce corrispondente nel menu contestuale.

È possibile modificare il nome del profilo, l’SSID, la sicurezza, la password e le opzioni di connessione.

### Ambito e modifica dei profili esistenti

Per un nuovo profilo è possibile scegliere:

- Tutti gli utenti
- Solo utente corrente

Quando si modifica un profilo esistente, WLAN-Manager mantiene automaticamente l’ambito corrente. Viene mantenuta anche la configurazione di sicurezza Windows esistente. In questo modo vengono preservati anche i profili WPA2/WPA3 più complessi; per i profili esistenti, l’editor modifica solo il nome del profilo, l’SSID, la password, la connessione automatica e l’impostazione per gli SSID nascosti.

I profili WLAN gestiti tramite Criteri di gruppo sono di sola lettura e non possono essere modificati.

### Password durante la modifica

Per una nuova WLAN protetta è necessario specificare una chiave WLAN valida.

Per un profilo protetto esistente:

- Se viene visualizzata la password esistente, è possibile modificarla.
- Se il campo della password viene svuotato completamente, la password esistente rimane invariata.
- Se Windows non ha potuto fornire la password in chiaro, il campo rimane vuoto. Anche in questo caso, un campo vuoto significa: mantenere la password esistente.
- Solo quando viene inserita una nuova password, WLAN-Manager sostituisce la chiave esistente.

Per le nuove chiavi WLAN Personal, WLAN-Manager accetta passphrase da 8 a 63 caratteri ASCII stampabili oppure un PSK esadecimale di 64 caratteri.

Per le WLAN aperte non viene memorizzata alcuna password.
