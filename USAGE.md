# 📖 Guida all'Uso - Calendario Italiano

## 🚀 Avvio Rapido

### 1. Installazione

```bash
# Installa le dipendenze
pip install -r requirements.txt

# Inizializza il database (solo la prima volta)
python database.py

# Avvia l'applicazione
python app.py
```

L'applicazione sarà disponibile su **http://localhost:8080**

### 2. Struttura del Progetto

```
calendario/
├── app.py                  # Applicazione principale Bottle
├── database.py             # Inizializzazione database
├── requirements.txt        # Dipendenze Python
├── data/
│   └── calendario.db       # Database SQLite (generato automaticamente)
├── templates/              # Template Jinja2
│   ├── base.html          # Template base
│   ├── day.html           # Vista giorno
│   ├── month.html         # Vista mese
│   ├── year.html          # Vista anno
│   ├── saint.html         # Dettaglio santo
│   ├── saints_list.html   # Lista santi
│   ├── holidays_list.html # Lista festività
│   └── error.html         # Pagina errore
├── static/
│   ├── css/
│   │   └── style.css      # Stili CSS
│   └── js/
│       └── main.js        # JavaScript
└── utils/
    ├── lunar.py           # Calcoli lunari
    ├── astronomy.py       # Calcoli astronomici
    └── seo.py             # Utilità SEO
```

## 🎯 Funzionalità Principali

### 📅 Vista Giorno

**URL**: `/giorno/{anno}/{mese}/{giorno}`

Mostra informazioni complete per un giorno specifico:
- 🙏 Santo del giorno con biografia completa
- 🎉 Festività italiane (nazionali e religiose)
- 🌙 Fase lunare corrente e prossime fasi
- ☀️ Orari alba/tramonto e durata del giorno
- 👤 Onomastici completi
- 📖 Eventi storici accaduti in questa data
- ♈ Segno zodiacale
- 🌸 Stagione corrente

**Esempio**: http://localhost:8080/giorno/2024/12/25

### 📆 Vista Mese

**URL**: `/mese/{anno}/{mese}/{nome-mese}`

Visualizza il calendario mensile con:
- Griglia calendario completa
- Santi per ogni giorno
- Festività evidenziate
- Fasi lunari del mese
- Navigazione mese precedente/successivo

**Esempio**: http://localhost:8080/mese/2024/12/dicembre

### 📊 Vista Anno

**URL**: `/anno/{anno}`

Panoramica annuale con:
- Tutte le festività dell'anno
- Griglia dei 12 mesi
- Date delle stagioni (equinozi e solstizi)
- Link rapidi ai mesi

**Esempio**: http://localhost:8080/anno/2024

### 🙏 Santi

**Lista completa**: `/santi`
**Dettaglio santo**: `/santo/{slug-santo}`

Ogni santo include:
- Biografia completa e dettagliata
- Storia breve
- Data della festa
- Patronati (di cosa è patrono)
- Structured data per SEO

**Esempio**: http://localhost:8080/santo/san-francesco-d-assisi

### 🎉 Festività

**URL**: `/feste`

Lista completa delle festività italiane:
- Feste nazionali
- Feste religiose
- Descrizione di ogni festività
- Date e informazioni

## 🔍 SEO e Ottimizzazione

### URL SEO-Friendly

Tutti gli URL sono ottimizzati per i motori di ricerca:
- `/giorno/2024/12/25` invece di `/day?y=2024&m=12&d=25`
- `/santo/san-francesco-d-assisi` con slug descrittivi
- `/mese/2024/12/dicembre` con nomi italiani

### Meta Tags

Ogni pagina include:
- Title e description ottimizzati
- Open Graph tags per social media
- Twitter Card tags
- Canonical URL
- Keywords rilevanti

### Structured Data

Schema.org JSON-LD per:
- Breadcrumb navigation
- Person (per i santi)
- Event (per le festività)
- Article (per i contenuti)

### Sitemap

**URL**: `/sitemap.xml`

Sitemap XML automatica con:
- Tutte le pagine principali
- Pagine anno/mese
- Tutti i santi
- Frequenza di aggiornamento
- Priorità delle pagine

### Robots.txt

**URL**: `/robots.txt`

File robots.txt con:
- Permessi per tutti i bot
- Link al sitemap

## 🌙 Calcoli Lunari

Il calendario include calcoli precisi delle fasi lunari:
- 🌑 Luna Nuova
- 🌓 Primo Quarto
- 🌕 Luna Piena
- 🌗 Ultimo Quarto
- Fasi intermedie (crescente, calante, gibbosa)
- Percentuale di illuminazione
- Età della luna in giorni
- Date delle prossime fasi

## ☀️ Calcoli Astronomici

Per ogni giorno viene calcolato:
- Alba e tramonto (per Roma come default)
- Durata del giorno
- Mezzogiorno solare
- Crepuscolo civile e nautico
- Stagione corrente
- Prossimi equinozi e solstizi
- Segno zodiacale

## 🎨 Interfaccia Utente

### Design Moderno

- Gradient backgrounds
- Card-based layout
- Responsive design
- Animazioni smooth
- Ombre ed effetti 3D

### Responsive

Ottimizzato per:
- Desktop (1200px+)
- Tablet (768px-1199px)
- Mobile (< 768px)

### Navigazione

- Header sticky sempre visibile
- Breadcrumb navigation
- Pulsanti prev/next per navigazione
- Footer con link utili

### Scorciatoie da Tastiera

- **←** Giorno/mese/anno precedente
- **→** Giorno/mese/anno successivo
- **H** Vai a oggi

## 💾 Database

### Struttura

Il database SQLite contiene 4 tabelle principali:

1. **saints** - Santi del calendario
   - name, slug, day, month
   - biography (biografia completa)
   - short_story (storia breve)
   - patronage (patronati)

2. **holidays** - Festività italiane
   - name, slug, day, month
   - is_national, is_religious
   - description

3. **name_days** - Onomastici
   - name, day, month

4. **historical_events** - Eventi storici
   - title, day, month, year
   - description, category

### Aggiungere Dati

Per aggiungere nuovi santi o festività, modifica `database.py`:

```python
# In populate_saints()
saints_data.append((
    day, month, "Nome Santo", "slug-santo",
    "Biografia completa...",
    "Storia breve...",
    "Festa del giorno",
    "Patronati"
))

# In populate_holidays()
holidays_data.append((
    month, day, "Nome Festa", "slug-festa",
    None,  # year (None per ricorrente)
    1,     # is_national
    0,     # is_religious
    None,  # region
    "Descrizione..."
))
```

Poi rigenera il database:
```bash
rm data/calendario.db
python database.py
```

## 🌍 Localizzazione

L'applicazione è completamente in italiano:
- Nomi dei mesi in italiano
- Giorni della settimana in italiano
- Tutte le etichette e testi in italiano
- Date formattate all'italiana (gg/mm/aaaa)

## 🔧 Personalizzazione

### Cambiare Colori

Modifica `static/css/style.css` variabili CSS:

```css
:root {
    --primary-color: #2563eb;    /* Blu primario */
    --secondary-color: #7c3aed;  /* Viola secondario */
    --accent-color: #f59e0b;     /* Arancione accento */
    /* ... altri colori ... */
}
```

### Cambiare Posizione Geografica

Per calcoli astronomici diversi da Roma, modifica `utils/astronomy.py`:

```python
DEFAULT_LATITUDE = '45.4642'   # Milano
DEFAULT_LONGITUDE = '9.1900'
```

### Cambiare Porta

Modifica `app.py`:

```python
run(app, host='localhost', port=8080, debug=True)
```

## 📱 Progressive Web App (PWA)

Il file `main.js` include supporto per Service Worker (commentato).
Per abilitare PWA:

1. Crea `static/sw.js` (Service Worker)
2. Crea `static/manifest.json` (Web Manifest)
3. Decomenta la registrazione in `main.js`

## 🚀 Deploy in Produzione

### Considerazioni

1. **Cambia debug mode**:
   ```python
   run(app, host='0.0.0.0', port=8080, debug=False)
   ```

2. **Usa un server WSGI** (gunicorn, uWSGI):
   ```bash
   gunicorn -w 4 app:app
   ```

3. **Aggiorna SITE_URL** in `utils/seo.py`:
   ```python
   SITE_URL = "https://tuodominio.it"
   ```

4. **Usa un reverse proxy** (nginx, Apache)

5. **HTTPS** obbligatorio per SEO

## 🎯 Possibili Estensioni

### Funzionalità Aggiuntive Suggerite

1. **Ricerca**
   - Cerca santi per nome
   - Cerca giorni per festività
   - Cerca onomastici

2. **Preferiti**
   - Salva giorni preferiti
   - Notifiche per onomastici

3. **Esportazione**
   - Esporta in PDF
   - Esporta in iCal
   - Stampa calendario

4. **Widget**
   - Widget desktop
   - Widget mobile
   - API REST

5. **Multi-lingua**
   - Inglese
   - Altre lingue

6. **Temi**
   - Tema chiaro/scuro
   - Temi personalizzati
   - Temi stagionali

7. **Calendario Gregoriano vs Giuliano**
   - Supporto calendario giuliano
   - Confronto date

8. **Festività Regionali**
   - Patroni regionali
   - Feste locali
   - Sagre e eventi

## 🐛 Troubleshooting

### Il database non si crea

```bash
# Assicurati che la directory data esista
mkdir -p data
python database.py
```

### Errore: Module not found

```bash
# Reinstalla le dipendenze
pip install -r requirements.txt
```

### Porta 8080 già in uso

Cambia porta in `app.py` o termina il processo:
```bash
# Linux/Mac
lsof -ti:8080 | xargs kill -9

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Template non trovati

Assicurati che la directory `templates/` esista e contenga tutti i file .html

## 📞 Supporto

Per problemi o domande:
1. Controlla la documentazione
2. Verifica i log dell'applicazione
3. Controlla i file di configurazione
4. Verifica le dipendenze installate

## 🎉 Buon Utilizzo!

Il Calendario Italiano è pronto per essere utilizzato. Goditi tutte le funzionalità e personalizzalo secondo le tue esigenze!
