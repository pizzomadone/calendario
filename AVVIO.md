# 🚀 Come Avviare il Calendario Italiano

## 📋 Prerequisiti

- **Python 3.7+** installato sul sistema
- **pip** (Python package installer)
- Connessione internet per scaricare dipendenze (solo prima volta)

## ⚡ Avvio Rapido (3 passi)

### 1️⃣ Installa le Dipendenze

```bash
pip install -r requirements.txt
```

Questo installerà:
- `bottle` - Web framework
- `ephem` - Calcoli astronomici
- `jinja2` - Template engine
- `python-dateutil` - Gestione date
- `reportlab` - Generazione PDF
- `pillow` - Elaborazione immagini

### 2️⃣ Inizializza il Database

Il database viene creato automaticamente al primo avvio, ma puoi inizializzarlo manualmente con:

```bash
python database.py
python database_extended.py
```

Vedrai i messaggi:
```
✅ Database initialized successfully at /home/user/calendario/data/calendario.db
✅ Database extended successfully with new features!
```

### 3️⃣ Avvia l'Applicazione

```bash
python app.py
```

Vedrai questo output:

```
🚀 Starting Calendario Italiano...
📅 Open your browser at http://localhost:8080

🎯 Nuove funzionalità disponibili:
   🔍 Ricerca: /cerca
   📄 Export PDF: /pdf/mese/YYYY/MM o /pdf/anno/YYYY
   💭 Proverbi: /proverbi
   🍝 Ricette: /ricette
   🌱 Orto: /orto
   🎉 Feste regionali: /feste/regionali

Bottle v0.12.25 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
```

### 4️⃣ Apri il Browser

Vai su: **http://localhost:8080**

L'applicazione è ora attiva! 🎉

## 🛑 Fermare l'Applicazione

Per fermare il server, premi:
- **Linux/Mac**: `Ctrl + C` nel terminale
- **Windows**: `Ctrl + C` nel prompt dei comandi

## 🌐 Accedere da Altri Dispositivi

Se vuoi accedere al calendario da altri dispositivi nella tua rete locale:

1. Modifica `app.py` alla riga finale:
   ```python
   run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)
   ```

2. Trova il tuo IP locale:
   - **Linux/Mac**: `ifconfig` o `ip addr show`
   - **Windows**: `ipconfig`

3. Accedi da altri dispositivi usando: `http://TUO_IP:8080`

## 📱 Tutte le Funzionalità Disponibili

Una volta avviata l'app, puoi accedere a:

### 🗓️ Calendario Base
- **Home/Oggi**: `http://localhost:8080/` o `/oggi`
- **Giorno specifico**: `/giorno/2024/12/11`
- **Mese**: `/mese/2024/12/dicembre`
- **Anno**: `/anno/2024`

### 🔍 Ricerca
- **Ricerca**: `/cerca` o `/search`
- **Ricerca con query**: `/cerca?q=natale`
- **Ricerca per mese**: `/cerca?q=santo&month=12`

### 📄 Export PDF
- **PDF Giorno**: `/pdf/giorno/2024/12/11`
- **PDF Mese**: `/pdf/mese/2024/12`
- **PDF Anno**: `/pdf/anno/2024`

### 🙏 Santi e Festività
- **Tutti i Santi**: `/santi`
- **Santo specifico**: `/santo/san-francesco-d-assisi`
- **Festività Nazionali**: `/feste`
- **Festività Regionali**: `/feste/regionali`
- **Festività per regione**: `/feste/regionali?regione=Sicilia`

### 💭 Proverbi
- **Tutti i Proverbi**: `/proverbi`

### 🍝 Ricette
- **Tutte le Ricette**: `/ricette`
- **Ricette per stagione**: `/ricette?stagione=Inverno`
- **Dettaglio ricetta**: `/ricetta/1`

### 🌱 Orto e Agricoltura
- **Calendario Orto**: `/orto` o `/agricoltura`
- **Consigli per mese**: `/orto?mese=3`

### 🗺️ SEO
- **Sitemap**: `/sitemap.xml`
- **Robots**: `/robots.txt`

## 🔧 Risoluzione Problemi

### Il database non si crea

```bash
# Crea manualmente la directory
mkdir -p data

# Inizializza database
python database.py
python database_extended.py
```

### Errore: Module not found

```bash
# Reinstalla tutte le dipendenze
pip install -r requirements.txt
```

### Porta 8080 già in uso

**Opzione 1**: Cambia porta in `app.py` (ultima riga):
```python
run(app, host='localhost', port=8081, debug=True, reloader=True)
```

**Opzione 2**: Termina processo che usa porta 8080:
```bash
# Linux/Mac
lsof -ti:8080 | xargs kill -9

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID_NUMBER> /F
```

### Errori Python

Assicurati di usare Python 3.7+:
```bash
python --version
# oppure
python3 --version
```

## 📊 Contenuto Database

Il database include:

- **27+ Santi** italiani con biografie complete
- **10 Festività nazionali** italiane
- **15+ Festività regionali** (patroni e feste locali)
- **30+ Proverbi** tradizionali italiani
- **100+ Onomastici**
- **9 Ricette stagionali** tradizionali
- **24+ Consigli agricoli** (uno per ogni mese)
- **10+ Eventi storici**

## 🎨 Personalizzazione

### Cambiare Colori

Modifica `static/css/style.css` variabili CSS:
```css
:root {
    --primary-color: #2563eb;    /* Blu */
    --secondary-color: #7c3aed;  /* Viola */
    --accent-color: #f59e0b;     /* Arancione */
}
```

### Cambiare Porta

Modifica `app.py` ultima riga:
```python
run(app, host='localhost', port=TUA_PORTA, debug=True)
```

### Disabilitare Debug Mode

Per produzione, cambia:
```python
run(app, host='localhost', port=8080, debug=False, reloader=False)
```

## 🚀 Deploy Produzione

Per deploy in produzione:

1. **Usa un server WSGI** come gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8080 app:app
   ```

2. **Imposta reverse proxy** (nginx/Apache)

3. **Aggiorna SITE_URL** in `utils/seo.py`:
   ```python
   SITE_URL = "https://tuodominio.it"
   ```

4. **Usa HTTPS** per sicurezza e SEO

## 💡 Comandi Utili

### Pulire e Ricreare Database

```bash
rm data/calendario.db
python database.py
python database_extended.py
```

### Vedere i Log

L'applicazione mostra log nel terminale. Per salvare in un file:
```bash
python app.py > logs.txt 2>&1
```

### Avvio in Background

**Linux/Mac**:
```bash
nohup python app.py > logs.txt 2>&1 &
```

**Windows**:
Usa Task Scheduler o crea un servizio Windows

## 📚 Documentazione Completa

Per maggiori dettagli:
- **README.md** - Panoramica progetto
- **USAGE.md** - Guida utilizzo completa
- **CHANGELOG.md** - Storia versioni
- **AVVIO.md** - Questo file (istruzioni avvio)

## ✅ Checklist Primo Avvio

- [ ] Python 3.7+ installato
- [ ] Dipendenze installate (`pip install -r requirements.txt`)
- [ ] Database inizializzato (automatico o manuale)
- [ ] Porta 8080 libera
- [ ] Server avviato (`python app.py`)
- [ ] Browser aperto su `http://localhost:8080`
- [ ] Tutto funziona! 🎉

## 🆘 Supporto

Se hai problemi:

1. Controlla che tutte le dipendenze siano installate
2. Verifica che la porta sia libera
3. Controlla i log nel terminale
4. Leggi la sezione "Risoluzione Problemi"
5. Controlla USAGE.md per dettagli funzionalità

## 🎯 Prossimi Passi

Una volta avviata l'app:

1. **Esplora il calendario** - Vai a oggi: `/oggi`
2. **Prova la ricerca** - Cerca un santo: `/cerca?q=francesco`
3. **Scarica un PDF** - Export mese: `/pdf/mese/2024/12`
4. **Scopri le ricette** - Piatti stagionali: `/ricette`
5. **Consulta l'orto** - Consigli agricoli: `/orto`
6. **Esplora le regioni** - Feste locali: `/feste/regionali`

## 🎉 Buon Utilizzo!

Il Calendario Italiano è pronto all'uso con tutte le funzionalità avanzate!

**Novità Versione 2.0:**
✅ Ricerca avanzata
✅ Export PDF
✅ Proverbi e citazioni
✅ Ricette stagionali
✅ Calendario dell'orto
✅ Festività regionali
