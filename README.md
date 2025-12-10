# 📅 Calendario Italiano - Italian Calendar Web App

Un'applicazione web completa per il calendario italiano con santi, fasi lunari, festività comandate e molto altro.

## ✨ Caratteristiche

- 🙏 **Santo del giorno** con storia e biografia
- 🌙 **Calendario lunare** con fasi della luna
- 🇮🇹 **Feste comandate italiane** e festività regionali
- 📖 **Eventi storici** accaduti in questa data
- 👤 **Onomastici** completi per ogni giorno
- 🌅 **Dati astronomici** (alba, tramonto, durata del giorno)
- 🔍 **Ottimizzazione SEO** completa con URL parlanti
- 📱 **Design responsive** e interfaccia moderna
- 📊 **Structured data** per i motori di ricerca

## 🚀 Installazione

```bash
pip install -r requirements.txt
python database.py  # Inizializza il database
python app.py       # Avvia l'applicazione
```

L'applicazione sarà disponibile su `http://localhost:8080`

## 📖 Utilizzo

- Home: `/`
- Giorno specifico: `/giorno/2024/12/25/natale`
- Mese: `/mese/2024/12/dicembre`
- Anno: `/anno/2024`
- Santo del giorno: `/santo/san-francesco-assisi`

## 🛠️ Tecnologie

- **Backend**: Bottle (Python microframework)
- **Database**: SQLite
- **Template**: Jinja2
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Calcoli astronomici**: PyEphem

## 📄 Licenza

MIT License
