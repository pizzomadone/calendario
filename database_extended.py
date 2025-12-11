#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database extension with new features:
- Regional holidays
- Proverbs and quotes
- Seasonal recipes
- Agricultural tips
"""

import sqlite3
from database import DB_PATH


def extend_database():
    """Add new tables and populate with data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create new tables
    create_tables(cursor)

    # Populate with data
    populate_proverbs(cursor)
    populate_recipes(cursor)
    populate_agricultural_tips(cursor)
    populate_regional_holidays(cursor)

    conn.commit()
    conn.close()
    print("✅ Database extended successfully with new features!")


def create_tables(cursor):
    """Create new tables for extended features"""

    # Proverbs and quotes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proverbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT,
            day INTEGER,
            month INTEGER,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seasonal recipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            season TEXT NOT NULL,
            month INTEGER,
            region TEXT,
            difficulty TEXT,
            prep_time INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Agricultural tips table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agricultural_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            month INTEGER NOT NULL,
            category TEXT,
            moon_phase TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Extend holidays table is already there, just add more data

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_proverbs_date ON proverbs(month, day)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_recipes_season ON recipes(season, month)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tips_month ON agricultural_tips(month)')


def populate_proverbs(cursor):
    """Populate Italian proverbs and quotes"""
    proverbs_data = [
        # Gennaio
        (1, 1, "Il primo dell'anno, ognun mostra quel che è tutto l'anno.", None, "Tradizione"),
        (6, 1, "Epifania tutte le feste porta via.", None, "Tradizione"),
        (17, 1, "Sant'Antonio dalla barba bianca, se non piove la neve non manca.", None, "Meteo"),
        (None, 1, "Gennaio fa il ponte e febbraio lo rompe.", None, "Meteo"),

        # Febbraio
        (2, 2, "Per la santa Candelora dell'inverno semo fora, ma se piove e tira vento, nell'inverno semo dentro.", None, "Meteo"),
        (14, 2, "A San Valentino primavera sta vicino.", None, "Stagioni"),
        (None, 2, "Febbraio febbraietto, corto e maledetto.", None, "Tradizione"),

        # Marzo
        (None, 3, "Marzo pazzerello, guarda il sole e prendi l'ombrello.", None, "Meteo"),
        (19, 3, "Per San Giuseppe il freddo va a morire.", None, "Meteo"),
        (None, 3, "Chi vuol far buon formaggio, lo faccia a marzo e a maggio.", None, "Agricoltura"),

        # Aprile
        (None, 4, "Aprile dolce dormire.", None, "Tradizione"),
        (25, 4, "Per San Marco fiorisce il lino bianco.", None, "Natura"),
        (None, 4, "Acqua d'aprile, ogni goccia un barile.", None, "Agricoltura"),

        # Maggio
        (1, 5, "Maggio ortolano, molta paglia e poco grano.", None, "Agricoltura"),
        (None, 5, "Di maggio si sposa chi non ha coraggio.", None, "Tradizione"),
        (None, 5, "Nebbia di maggio, sole di raggio.", None, "Meteo"),

        # Giugno
        (13, 6, "Sant'Antonio la falce in mano.", None, "Agricoltura"),
        (24, 6, "San Giovanni non vuole inganni.", None, "Tradizione"),
        (None, 6, "Giugno la falce in pugno.", None, "Agricoltura"),

        # Luglio
        (None, 7, "Luglio dal gran caldo, butta il manico dal martello.", None, "Meteo"),
        (None, 7, "Quando canta il merlo luglio è bello.", None, "Natura"),

        # Agosto
        (15, 8, "Per l'Assunta l'uva è matura.", None, "Agricoltura"),
        (None, 8, "Agosto moglie mia non ti conosco.", None, "Tradizione"),

        # Settembre
        (None, 9, "Settembre, l'uva e il fico pendono.", None, "Agricoltura"),
        (29, 9, "San Michele manda l'acqua per i fossi e viottoli.", None, "Meteo"),

        # Ottobre
        (None, 10, "Ottobre, il vino è nelle doghe.", None, "Vendemmia"),
        (4, 10, "A San Francesco gran vento e gran fresco.", None, "Meteo"),

        # Novembre
        (1, 11, "Per Ognissanti castagne e vino santi.", None, "Tradizione"),
        (11, 11, "San Martino, ogni mosto diventa vino.", None, "Vendemmia"),
        (None, 11, "A novembre si taglia la legna da ardere e si scalda.", None, "Tradizione"),

        # Dicembre
        (13, 12, "Santa Lucia, il giorno più corto che ci sia.", None, "Tradizione"),
        (25, 12, "Natale con i tuoi, Pasqua con chi vuoi.", None, "Tradizione"),
        (None, 12, "Dicembre nevoso, anno fruttoso.", None, "Meteo"),
    ]

    for day, month, text, author, category in proverbs_data:
        cursor.execute('''
            INSERT OR IGNORE INTO proverbs (day, month, text, author, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (day, month, text, author, category))

    # Famous Italian quotes
    quotes_data = [
        ("L'Italia è il paese dove fioriscono i limoni.", "Johann Wolfgang von Goethe", "Italia"),
        ("Chi ha pane e vino sta meglio del suo vicino.", None, "Saggezza"),
        ("Tra il dire e il fare c'è di mezzo il mare.", None, "Saggezza"),
        ("Chi dorme non piglia pesci.", None, "Lavoro"),
        ("Non tutte le ciambelle riescono col buco.", None, "Vita"),
        ("Meglio un uovo oggi che una gallina domani.", None, "Saggezza"),
        ("Chi va piano va sano e va lontano.", None, "Saggezza"),
        ("L'abito non fa il monaco.", None, "Apparenza"),
        ("A caval donato non si guarda in bocca.", None, "Gratitudine"),
        ("Tutto è bene quel che finisce bene.", None, "Ottimismo"),
    ]

    for text, author, category in quotes_data:
        cursor.execute('''
            INSERT OR IGNORE INTO proverbs (text, author, category)
            VALUES (?, ?, ?)
        ''', (text, author, category))


def populate_recipes(cursor):
    """Populate seasonal Italian recipes"""
    recipes_data = [
        # Primavera
        ("Risotto agli Asparagi",
         "Il risotto primaverile per eccellenza, con asparagi freschi e mantecato a regola d'arte.",
         "riso Carnaroli 320g, asparagi 500g, cipolla, brodo vegetale, vino bianco, parmigiano, burro",
         "1. Pulire gli asparagi e lessarli. 2. Tostare il riso con cipolla. 3. Sfumare col vino. 4. Cuocere aggiungendo brodo. 5. Mantecare con burro, parmigiano e punte di asparagi.",
         "Primavera", 4, "Lombardia", "Media", 45),

        ("Frittata di Primavera",
         "Frittata con verdure primaverili fresche: piselli, fave, carciofi e mentuccia.",
         "uova 6, piselli 200g, fave 200g, carciofi 2, mentuccia, olio, sale, pepe",
         "1. Pulire le verdure. 2. Saltare in padella. 3. Sbattere le uova. 4. Unire verdure alle uova. 5. Cuocere la frittata da entrambi i lati.",
         "Primavera", 4, None, "Facile", 30),

        # Estate
        ("Panzanella Toscana",
         "Insalata di pane raffermo con pomodori, cetrioli, cipolla e basilico. Perfetta d'estate.",
         "pane toscano raffermo 400g, pomodori maturi 500g, cetriolo 1, cipolla rossa, basilico, olio EVO, aceto",
         "1. Bagnare il pane. 2. Strizzarlo. 3. Tagliare le verdure. 4. Mescolare tutto. 5. Condire con olio e aceto. 6. Lasciar riposare in frigo.",
         "Estate", 7, "Toscana", "Facile", 20),

        ("Pasta alla Norma",
         "Piatto siciliano estivo con melanzane fritte, pomodoro e ricotta salata.",
         "pasta 400g, melanzane 3, pomodori pelati 500g, ricotta salata, basilico, aglio, olio",
         "1. Friggere le melanzane. 2. Preparare sugo al pomodoro. 3. Cuocere la pasta. 4. Mantecare con sugo e melanzane. 5. Servire con ricotta salata.",
         "Estate", 8, "Sicilia", "Media", 40),

        # Autunno
        ("Risotto ai Funghi Porcini",
         "Il re dei risotti autunnali con funghi porcini freschi o secchi.",
         "riso Carnaroli 320g, funghi porcini 300g, cipolla, brodo, vino bianco, parmigiano, prezzemolo, burro",
         "1. Pulire i funghi. 2. Rosolare con aglio. 3. Tostare il riso. 4. Cuocere col brodo. 5. Aggiungere funghi. 6. Mantecare.",
         "Autunno", 10, "Piemonte", "Media", 50),

        ("Castagnaccio",
         "Dolce toscano autunnale con farina di castagne, pinoli, uvetta e rosmarino.",
         "farina di castagne 500g, acqua, pinoli 50g, uvetta 50g, rosmarino, olio EVO, sale",
         "1. Setacciare la farina. 2. Aggiungere acqua. 3. Unire uvetta, pinoli, rosmarino. 4. Versare in teglia. 5. Cuocere in forno 35 minuti.",
         "Autunno", 11, "Toscana", "Facile", 45),

        # Inverno
        ("Polenta e Spezzatino",
         "Piatto invernale sostanzioso con polenta fumante e spezzatino di manzo.",
         "polenta 400g, carne di manzo 800g, cipolla, carote, sedano, vino rosso, brodo, pomodoro",
         "1. Rosolare la carne. 2. Sfumare col vino. 3. Cuocere con verdure. 4. Aggiungere brodo. 5. Cuocere 2 ore. 6. Preparare polenta e servire.",
         "Inverno", 1, "Nord Italia", "Media", 150),

        ("Struffoli Napoletani",
         "Dolce natalizio napoletano con palline di pasta fritta e miele.",
         "farina 500g, uova 4, zucchero, burro, liquore, miele 300g, confettini colorati",
         "1. Impastare gli ingredienti. 2. Formare cordoncini. 3. Tagliare palline. 4. Friggere. 5. Mescolare col miele caldo. 6. Decorare.",
         "Inverno", 12, "Campania", "Difficile", 90),

        ("Minestrone Invernale",
         "Zuppa di verdure invernali ricca e nutriente.",
         "cavolo 300g, carote 2, patate 2, fagioli 200g, sedano, cipolle, pomodoro, brodo",
         "1. Tagliare le verdure. 2. Rosolare cipolla. 3. Aggiungere verdure. 4. Coprire con brodo. 5. Cuocere 45 minuti. 6. Servire caldo.",
         "Inverno", 2, None, "Facile", 60),
    ]

    for title, desc, ingr, instr, season, month, region, diff, time in recipes_data:
        cursor.execute('''
            INSERT OR IGNORE INTO recipes
            (title, description, ingredients, instructions, season, month, region, difficulty, prep_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, desc, ingr, instr, season, month, region, diff, time))


def populate_agricultural_tips(cursor):
    """Populate agricultural calendar tips"""
    tips_data = [
        # Gennaio
        (1, "Potatura alberi da frutto",
         "Gennaio è il mese ideale per la potatura di meli, peri e viti. Rimuovere i rami secchi e danneggiati. Lavorare nei giorni di luna calante.",
         "Frutteto", "Calante"),
        (1, "Semina in semenzaio",
         "Seminare in ambiente protetto: melanzane, peperoni, pomodori. Mantenere temperatura 18-20°C.",
         "Orto", None),

        # Febbraio
        (2, "Preparazione terreno",
         "Vangare e concimare il terreno dell'orto. Preparare aiuole per semine primaverili.",
         "Orto", None),
        (2, "Potatura rosai",
         "Potare i rosai lasciando 3-5 gemme per ramo. Eliminare rami vecchi e malati.",
         "Giardino", "Calante"),

        # Marzo
        (3, "Prime semine all'aperto",
         "Seminare all'aperto: carote, ravanelli, lattuga, piselli, fave, spinaci.",
         "Orto", "Crescente"),
        (3, "Trapianto alberi",
         "Ultimo mese utile per trapiantare alberi e arbusti a radice nuda.",
         "Frutteto", None),

        # Aprile
        (4, "Semina ortaggi estivi",
         "Seminare: zucchine, fagiolini, basilico. Trapiantare pomodori, peperoni, melanzane.",
         "Orto", "Crescente"),
        (4, "Trattamenti preventivi",
         "Effettuare trattamenti preventivi contro parassiti su alberi da frutto con prodotti naturali.",
         "Frutteto", None),

        # Maggio
        (5, "Rincalzatura patate",
         "Rincalzare le patate coprendo la base con terra. Innaffiare regolarmente l'orto.",
         "Orto", None),
        (5, "Cimatura pomodori",
         "Cimare i pomodori eliminando i germogli ascellari. Legare le piante ai tutori.",
         "Orto", None),

        # Giugno
        (6, "Raccolta primizie",
         "Raccogliere: piselli, fave, fragole, ciliegie. Irrigare abbondantemente nelle ore serali.",
         "Orto", None),
        (6, "Potatura verde",
         "Effettuare la potatura verde della vite e degli alberi da frutto.",
         "Frutteto", None),

        # Luglio
        (7, "Raccolta e conservazione",
         "Raccogliere pomodori, zucchine, melanzane. Conservare erbe aromatiche essiccandole.",
         "Orto", None),
        (7, "Innesto a occhio",
         "Periodo ideale per l'innesto a occhio di piante da frutto.",
         "Frutteto", "Crescente"),

        # Agosto
        (8, "Semine autunnali",
         "Seminare: cavoli, finocchi, radicchio, rape. Preparare terreno per semine autunnali.",
         "Orto", "Crescente"),
        (8, "Raccolta frutta",
         "Raccogliere: pesche, albicocche, susine, fichi. Conservare marmellate e confetture.",
         "Frutteto", None),

        # Settembre
        (9, "Vendemmia",
         "Periodo di vendemmia. Raccogliere uva quando è matura. Preparare vino o conservare.",
         "Vigna", "Calante"),
        (9, "Semina prato",
         "Settembre è il mese ideale per seminare il prato. Temperatura ideale per germinazione.",
         "Giardino", None),

        # Ottobre
        (10, "Raccolta olive",
         "Inizia la raccolta delle olive. Scegliere il grado di maturazione desiderato.",
         "Oliveto", None),
        (10, "Semina aglio",
         "Seminare aglio e scalogno. Preparare bulbi per la primavera.",
         "Orto", "Crescente"),

        # Novembre
        (11, "Protezione dal freddo",
         "Proteggere piante sensibili con teli. Rientrare piante in vaso. Pacciamare aiuole.",
         "Giardino", None),
        (11, "Raccolta castagne",
         "Raccogliere castagne e noci. Conservare in luogo asciutto.",
         "Bosco", None),

        # Dicembre
        (12, "Pianificazione anno nuovo",
         "Pianificare le colture dell'anno successivo. Ordinare sementi. Controllare attrezzi.",
         "Orto", None),
        (12, "Pulizia e manutenzione",
         "Pulire l'orto da residui. Concimare con letame maturo. Riparare attrezzi.",
         "Orto", None),
    ]

    for month, title, desc, category, moon in tips_data:
        cursor.execute('''
            INSERT OR IGNORE INTO agricultural_tips (month, title, description, category, moon_phase)
            VALUES (?, ?, ?, ?, ?)
        ''', (month, title, desc, category, moon))


def populate_regional_holidays(cursor):
    """Add regional Italian holidays to existing holidays table"""
    regional_holidays = [
        # Sicilia
        (7, 11, "Santa Rosalia", "santa-rosalia", None, 0, 1, "Sicilia",
         "Patrona di Palermo. Grande festa con processione e fuochi d'artificio."),
        (12, 13, "Santa Lucia", "santa-lucia-siracusa", None, 0, 1, "Sicilia",
         "Patrona di Siracusa. Processione della statua d'argento."),

        # Lombardia
        (12, 7, "Sant'Ambrogio", "sant-ambrogio", None, 0, 1, "Lombardia",
         "Patrono di Milano. Festa cittadina con Fiera degli Oh Bej! Oh Bej!"),

        # Veneto
        (4, 25, "San Marco", "san-marco-venezia", None, 0, 1, "Veneto",
         "Patrono di Venezia. Tradizionale dono del bocolo (rosa rossa)."),

        # Campania
        (9, 19, "San Gennaro", "san-gennaro", None, 0, 1, "Campania",
         "Patrono di Napoli. Celebre per il miracolo dello scioglimento del sangue."),
        (12, 6, "San Nicola", "san-nicola-bari", None, 0, 1, "Puglia",
         "Patrono di Bari. Grande festa con processione in mare."),

        # Emilia
        (10, 4, "San Petronio", "san-petronio", None, 0, 1, "Emilia-Romagna",
         "Patrono di Bologna. Festa con mercatini e eventi culturali."),

        # Toscana
        (6, 24, "San Giovanni Battista", "san-giovanni-firenze", None, 0, 1, "Toscana",
         "Patrono di Firenze. Calcio storico fiorentino e fuochi d'artificio."),

        # Piemonte
        (6, 24, "San Giovanni", "san-giovanni-torino", None, 0, 1, "Piemonte",
         "Patrono di Torino. Tradizionale falò e festa lungo il Po."),

        # Liguria
        (6, 24, "San Giovanni Battista", "san-giovanni-genova", None, 0, 1, "Liguria",
         "Patrono di Genova. Processione e benedizione del mare."),

        # Sardegna
        (5, 1, "Sant'Efisio", "sant-efisio", None, 0, 1, "Sardegna",
         "Patrono di Cagliari. Una delle processioni più belle d'Italia."),

        # Umbria
        (1, 29, "Sant'Emidio", "sant-emidio", None, 0, 1, "Marche",
         "Patrono di Ascoli Piceno. Festa con corteo storico."),

        # Carnevale (data variabile, esempio)
        (2, None, "Carnevale di Venezia", "carnevale-venezia", None, 0, 0, "Veneto",
         "Celebre carnevale con maschere veneziane e feste nei palazzi storici."),
        (2, None, "Carnevale di Viareggio", "carnevale-viareggio", None, 0, 0, "Toscana",
         "Famoso per i carri allegorici giganti che sfilano sul lungomare."),

        # Palio
        (7, 2, "Palio di Siena", "palio-siena-luglio", None, 0, 0, "Toscana",
         "Corsa di cavalli in Piazza del Campo. Tradizione medievale."),
        (8, 16, "Palio di Siena", "palio-siena-agosto", None, 0, 0, "Toscana",
         "Secondo Palio dell'anno, dedicato alla Madonna Assunta."),
    ]

    for month, day, name, slug, year, is_nat, is_rel, region, desc in regional_holidays:
        cursor.execute('''
            INSERT OR IGNORE INTO holidays
            (month, day, name, slug, year, is_national, is_religious, region, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (month, day, name, slug, year, is_nat, is_rel, region, desc))


if __name__ == '__main__':
    extend_database()
