# 📅 Calendario Italiano - Italian Calendar Web App

Un'applicazione web completa per il calendario italiano con santi, fasi lunari, festività comandate e molto altro.

## ✨ Caratteristiche Principali

### 🗓️ Calendario Base
- 🙏 **Santo del giorno** con storia e biografia completa
- 🌙 **Calendario lunare** con fasi della luna e calcoli precisi
- 🇮🇹 **Feste comandate italiane** e festività regionali
- 📖 **Eventi storici** accaduti in questa data
- 👤 **Onomastici** completi per ogni giorno
- 🌅 **Dati astronomici** (alba, tramonto, durata del giorno)
- ♈ **Segni zodiacali** e stagioni
- 📊 **Structured data** per i motori di ricerca

### ✨ Nuove Funzionalità (v2.0)
- 🔍 **Ricerca avanzata** - Cerca santi, festività, ricette, proverbi
- 📄 **Export PDF** - Scarica calendario in PDF (giorno/mese/anno)
- 💭 **Proverbi e citazioni** - Saggezza popolare italiana
- 🍝 **Ricette stagionali** - Piatti tradizionali per ogni stagione
- 🌱 **Calendario dell'orto** - Consigli agricoli mensili
- 🎉 **Festività regionali** - Patroni e feste locali di ogni regione

### 🎨 Design e UX
- 📱 **Design responsive** moderno e accattivante
- 🔍 **Ottimizzazione SEO** completa con URL parlanti
- ⚡ **Performance** ottimizzate
- ⌨️ **Navigazione da tastiera** (←→H)

## 🚀 Avvio Rapido

```bash
# 1. Installa dipendenze
pip install -r requirements.txt

# 2. Inizializza database (automatico al primo avvio)
python init_database.py

# 3. Avvia applicazione
python app.py
```

L'applicazione sarà disponibile su **http://localhost:8080**

📖 **Per istruzioni dettagliate vedi [AVVIO.md](AVVIO.md)**

## 📖 Utilizzo Completo

### Calendario Base
- **Home/Oggi**: `/` o `/oggi`
- **Giorno specifico**: `/giorno/2024/12/25`
- **Mese**: `/mese/2024/12/dicembre`
- **Anno**: `/anno/2024`
- **Santo**: `/santo/san-francesco-assisi`

### Nuove Funzionalità
- **Ricerca**: `/cerca?q=natale`
- **PDF Giorno**: `/pdf/giorno/2024/12/25`
- **PDF Mese**: `/pdf/mese/2024/12`
- **PDF Anno**: `/pdf/anno/2024`
- **Proverbi**: `/proverbi`
- **Ricette**: `/ricette` o `/ricette?stagione=Inverno`
- **Orto**: `/orto` o `/orto?mese=3`
- **Feste Regionali**: `/feste/regionali?regione=Sicilia`

## 🛠️ Tecnologie

- **Backend**: Bottle (Python microframework)
- **Database**: SQLite
- **Template**: Jinja2
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Calcoli astronomici**: PyEphem
- **PDF Export**: ReportLab
- **Ricerca**: SQLite FTS

## 📊 Contenuti Database

- **27+ Santi** italiani con biografie complete
- **10 Festività nazionali** italiane
- **15+ Festività regionali** (patroni e sagre)
- **30+ Proverbi** tradizionali italiani
- **100+ Onomastici**
- **9 Ricette stagionali** della cucina italiana
- **24+ Consigli agricoli** (uno per ogni mese)
- **10+ Eventi storici** importanti

## 📚 Documentazione

- **[AVVIO.md](AVVIO.md)** - Guida completa per avviare l'applicazione
- **[USAGE.md](USAGE.md)** - Manuale d'uso dettagliato
- **[CHANGELOG.md](CHANGELOG.md)** - Storia delle versioni

## 🌟 Caratteristiche Tecniche

- ✅ **SEO perfetto** - Sitemap, meta tags, structured data
- ✅ **URLs parlanti** - /giorno/2024/12/25/natale
- ✅ **Responsive** - Mobile, tablet, desktop
- ✅ **Performance** - Database indicizzato
- ✅ **Accessibilità** - Navigazione da tastiera
- ✅ **Estendibile** - Architettura modulare
- ✅ **100% Italiano** - Completamente localizzato

## 📄 Licenza

MIT License
