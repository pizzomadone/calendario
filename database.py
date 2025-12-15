#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database initialization and management for Italian Calendar
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'calendario.db')


def init_db():
    """Initialize database with schema and initial data"""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            biography TEXT NOT NULL,
            short_story TEXT NOT NULL,
            feast_day TEXT,
            patronage TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER,
            is_national BOOLEAN DEFAULT 1,
            is_religious BOOLEAN DEFAULT 0,
            region TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS name_days (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historical_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER,
            description TEXT NOT NULL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_saints_date ON saints(month, day)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_holidays_date ON holidays(month, day)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_namedays_date ON name_days(month, day)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_date ON historical_events(month, day)')

    conn.commit()

    # Populate with initial data
    populate_saints(cursor)
    populate_holidays(cursor)
    populate_name_days(cursor)
    populate_historical_events(cursor)

    conn.commit()
    conn.close()

    print(f"✅ Database initialized successfully at {DB_PATH}")


def populate_saints(cursor):
    """Populate saints table with Italian saints"""
    saints_data = [
        # Gennaio
        (1, 1, "Maria Santissima Madre di Dio", "maria-santissima-madre-di-dio",
         "Maria Santissima Madre di Dio è una solennità liturgica della Chiesa cattolica. La festa celebra la maternità divina di Maria, proclamata dal Concilio di Efeso nel 431. Maria è venerata come Theotókos (Madre di Dio) per aver dato alla luce Gesù Cristo, vero Dio e vero uomo. Questa solennità cade otto giorni dopo il Natale e apre l'anno liturgico con la contemplazione del mistero dell'incarnazione. La festa sottolinea il ruolo unico di Maria nella storia della salvezza come colei che ha accolto il Verbo di Dio nel suo grembo.",
         "Il primo giorno dell'anno è dedicato a Maria, madre di Gesù. La Chiesa celebra la sua divina maternità.",
         "Primo giorno dell'anno, otto giorni dopo Natale", "Maternità, madri, inizio dell'anno"),

        (1, 6, "Epifania del Signore", "epifania-del-signore",
         "L'Epifania celebra la manifestazione di Gesù Cristo al mondo, rappresentata dalla visita dei Magi. Secondo il Vangelo di Matteo, i Magi giunsero dall'Oriente seguendo una stella per adorare il neonato re dei Giudei. Portarono doni simbolici: oro (regalità), incenso (divinità) e mirra (passione futura). La festa ha origini antichissime ed è celebrata il 6 gennaio. Nella tradizione italiana, la Befana porta doni ai bambini. L'Epifania conclude il tempo di Natale e sottolinea l'universalità della salvezza offerta a tutti i popoli.",
         "I tre Re Magi, seguendo la stella, portano doni a Gesù Bambino: oro, incenso e mirra.",
         "6 gennaio", "Viaggiatori, esploratori"),

        (1, 17, "Sant'Antonio Abate", "sant-antonio-abate",
         "Sant'Antonio Abate (250-356) è considerato il padre del monachesimo cristiano. Nato in Egitto, a vent'anni vendette tutti i suoi beni per ritirarsi nel deserto della Tebaide, dove visse in preghiera e penitenza per oltre ottant'anni. Subì numerose tentazioni demoniache, che ispirarono innumerevoli opere d'arte. Fondò comunità monastiche e la sua regola influenzò tutto il monachesimo orientale e occidentale. È patrono degli animali domestici e degli allevatori. Morì ultracentenario il 17 gennaio 356. La sua festa è celebrata con la benedizione degli animali.",
         "Il grande eremita del deserto, padre dei monaci, che vinse le tentazioni del demonio. Protettore degli animali.",
         "17 gennaio", "Animali domestici, allevatori, macellai, contadini"),

        (2, 2, "Presentazione del Signore - Candelora", "presentazione-del-signore",
         "La Candelora commemora la presentazione di Gesù al Tempio di Gerusalemme, quaranta giorni dopo la nascita, secondo la legge mosaica. Maria e Giuseppe portarono il bambino al tempio per consacrarlo a Dio e per la purificazione rituale di Maria. Il vecchio Simeone, guidato dallo Spirito Santo, riconobbe in Gesù il Messia e pronunciò il Nunc Dimittis. La profetessa Anna rese grazie a Dio. La festa è chiamata Candelora per la tradizionale benedizione delle candele, simbolo di Cristo luce del mondo. Nella tradizione popolare segna la fine dell'inverno.",
         "Gesù viene presentato al tempio. Il vecchio Simeone lo riconosce come luce delle nazioni.",
         "2 febbraio", "Vergini consacrate, cerai"),

        (2, 14, "Santi Cirillo e Metodio", "santi-cirillo-e-metodio",
         "Cirillo (827-869) e Metodio (815-885) furono due fratelli greci, missionari tra i popoli slavi. Crearono l'alfabeto glagolitico (precursore del cirillico) per tradurre la Bibbia e i testi liturgici in lingua slava. Il loro operato favorì l'evangelizzazione e lo sviluppo culturale dei popoli slavi. Affrontarono opposizioni per l'uso della lingua volgare nella liturgia ma ottennero l'approvazione papale. Cirillo morì a Roma nel 869, Metodio continuò l'opera missionaria in Moravia. Nel 1980 Giovanni Paolo II li proclamò compatroni d'Europa insieme a San Benedetto.",
         "I due fratelli missionari che evangelizzarono i popoli slavi creando il loro alfabeto.",
         "14 febbraio", "Europa, ecumenismo, missionari"),

        (3, 19, "San Giuseppe", "san-giuseppe",
         "San Giuseppe, sposo di Maria e padre putativo di Gesù, è uno dei santi più venerati. Carpentiere di Nazareth, discendente della casa di Davide, accolse il mistero dell'Incarnazione con fede e obbedienza. Protesse Maria e Gesù, guidando la Sacra Famiglia in Egitto per sfuggire alla persecuzione di Erode. I Vangeli lo descrivono come uomo giusto e discreto. La tradizione lo considera patrono della Chiesa universale, dei lavoratori e delle famiglie. Morì assistito da Gesù e Maria, per questo è patrono della buona morte. La sua festa è celebrata il 19 marzo.",
         "Il padre putativo di Gesù, falegname di Nazareth, uomo giusto e protettore della Sacra Famiglia.",
         "19 marzo", "Padri di famiglia, lavoratori, falegnami, moribondi, Chiesa universale"),

        (4, 25, "San Marco Evangelista", "san-marco-evangelista",
         "San Marco, autore del secondo Vangelo, fu discepolo e interprete di San Pietro a Roma. Il suo Vangelo, il più antico, presenta Gesù come Messia operante, con un linguaggio diretto e vivace. Accompagnò Paolo e Barnaba nel primo viaggio missionario. Secondo la tradizione fondò la Chiesa di Alessandria d'Egitto e vi subì il martirio intorno al 68 d.C. Le sue reliquie furono traslate a Venezia nell'828, dove è patrono. Il suo simbolo evangelico è il leone alato. Il Vangelo di Marco è caratterizzato da immediatezza narrativa e sottolinea la divinità di Cristo rivelata nelle sue opere.",
         "L'evangelista autore del Vangelo più antico, compagno di San Pietro, patrono di Venezia.",
         "25 aprile", "Venezia, notai, scrivani, vetrai"),

        (5, 1, "San Giuseppe Lavoratore", "san-giuseppe-lavoratore",
         "La festa di San Giuseppe Lavoratore fu istituita da Pio XII nel 1955 per celebrare la dignità del lavoro alla luce del Vangelo. Giuseppe, carpentiere di Nazareth, è modello per tutti i lavoratori: svolse il suo umile mestiere con dedizione, santificando il lavoro quotidiano. Insegnò il mestiere a Gesù, che trascorse circa trent'anni come falegname. Questa festa, celebrata il 1° maggio, assume particolare significato in contrapposizione alle ideologie materialiste, proponendo una visione cristiana del lavoro come vocazione e partecipazione all'opera creatrice di Dio. Giuseppe è patrono universale dei lavoratori.",
         "San Giuseppe celebrato come modello e patrono di tutti i lavoratori nel giorno della festa del lavoro.",
         "1 maggio", "Lavoratori, operai, artigiani"),

        (6, 13, "Sant'Antonio di Padova", "sant-antonio-di-padova",
         "Sant'Antonio di Padova (1195-1231), portoghese di nascita, fu frate francescano, teologo e predicatore straordinario. Nato a Lisbona come Fernando, entrò nei francescani dopo aver visto le reliquie dei primi martiri dell'ordine. Predicò in Italia e Francia con grande efficacia, combattendo le eresie e convertendo numerosi peccatori. Era chiamato 'Arca del Testamento' per la sua profonda conoscenza delle Scritture. Celebre per i miracoli, in particolare il ritrovamento di oggetti smarriti. Morì a Padova a soli 36 anni. Fu canonizzato nel 1232, solo un anno dopo la morte. È dottore della Chiesa.",
         "Il grande predicatore francescano, taumaturgo invocato per ritrovare le cose smarrite.",
         "13 giugno", "Cose smarrite, poveri, viaggiatori, naufraghi, Padova"),

        (6, 24, "Natività di San Giovanni Battista", "nativita-san-giovanni-battista",
         "San Giovanni Battista, cugino di Gesù, fu il precursore del Messia. Nacque da Zaccaria ed Elisabetta in età avanzata, come annunciato dall'arcangelo Gabriele. Visse nel deserto conducendo vita ascetica, vestito di peli di cammello e nutrendosi di locuste e miele selvatico. Predicò la conversione e battezzò nel Giordano, preparando la venuta di Cristo. Battezzò Gesù riconoscendolo come l'Agnello di Dio. Fu decapitato per ordine di Erode Antipa per aver denunciato la sua unione illecita con Erodiade. La sua natività si celebra il 24 giugno, vicino al solstizio d'estate.",
         "Il Precursore del Signore, voce che grida nel deserto, battezzò Gesù nel fiume Giordano.",
         "24 giugno", "Battesimo, conversione, Firenze, Genova, Torino"),

        (6, 29, "Santi Pietro e Paolo", "santi-pietro-e-paolo",
         "Pietro e Paolo, le due colonne della Chiesa, martirizzati a Roma sotto Nerone (64-67 d.C.). Pietro, pescatore di Galilea, fu il primo papa, custode delle chiavi del Regno. Rinnegò Gesù tre volte ma si convertì profondamente. Guidò la prima comunità cristiana e morì crocifisso a testa in giù sul colle Vaticano. Paolo, fariseo persecutore convertito sulla via di Damasco, divenne l'apostolo delle genti. Compì tre grandi viaggi missionari fondando comunità in tutto il Mediterraneo. Scrisse 13 lettere del Nuovo Testamento. Fu decapitato sulla via Ostiense. Entrambi sono patroni di Roma.",
         "I principi degli Apostoli: Pietro primo papa e Paolo apostolo delle genti, martiri a Roma.",
         "29 giugno", "Roma, pescatori, teologi, missionari"),

        (7, 11, "San Benedetto da Norcia", "san-benedetto-da-norcia",
         "San Benedetto (480-547), padre del monachesimo occidentale, nacque a Norcia. Studiò a Roma ma, disgustato dalla corruzione, si ritirò in una grotta a Subiaco per tre anni. Fondò dodici monasteri e infine Montecassino nel 529, dove scrisse la celebre Regola benedettina: 'Ora et labora' (prega e lavora). La Regola, equilibrata e saggia, regolò la vita monastica europea per secoli. I monasteri benedettini furono centri di preghiera, cultura e civilizzazione. Benedetto morì il 21 marzo 547 ma è commemorato l'11 luglio. Paolo VI lo proclamò patrono d'Europa nel 1964.",
         "Padre del monachesimo occidentale, fondatore dell'ordine benedettino e patrono d'Europa.",
         "11 luglio", "Europa, monaci, speleologi, architetti, ingegneri"),

        (8, 10, "San Lorenzo", "san-lorenzo",
         "San Lorenzo, diacono della Chiesa di Roma, subì il martirio nel 258 sotto Valeriano. Era responsabile dei beni ecclesiastici e dell'assistenza ai poveri. Quando gli fu ordinato di consegnare i tesori della Chiesa, presentò i poveri dicendo: 'Questi sono i veri tesori della Chiesa'. Per questo fu condannato a morte sulla graticola ardente. Durante il supplizio mantenne il coraggio, tanto da dire: 'Sono cotto da questa parte, girami'. È uno dei santi più venerati. Il suo martirio ispirò la costruzione di numerose basiliche. Patrono di cuochi, librai e pompieri.",
         "Il diacono martire che distribuì i tesori della Chiesa ai poveri e morì sulla graticola.",
         "10 agosto", "Cuochi, librai, pompieri, poveri, Roma"),

        (8, 15, "Assunzione della Beata Vergine Maria", "assunzione-beata-vergine-maria",
         "L'Assunzione di Maria in cielo, in anima e corpo, è un dogma proclamato da Pio XII nel 1950, basato su un'antica tradizione. Al termine della sua vita terrena, Maria fu assunta in cielo dove regna con Cristo. L'Assunzione è conseguenza dell'Immacolata Concezione: preservata dal peccato, fu anche preservata dalla corruzione del sepolcro. La festa, celebrata il 15 agosto (Ferragosto), è una delle solennità mariane più importanti. Maria è coronata Regina del cielo e intercede per l'umanità. Questa verità di fede esprime la destinazione finale di ogni cristiano: la risurrezione e la vita eterna.",
         "Maria è assunta in cielo in anima e corpo al termine della sua vita terrena.",
         "15 agosto", "Italia, madri, assunzionisti"),

        (9, 29, "Santi Arcangeli Michele, Gabriele e Raffaele", "santi-arcangeli",
         "Michele, Gabriele e Raffaele sono i tre arcangeli nominati nella Bibbia. Michele ('Chi è come Dio?') è il guerriero celeste che combatte contro Satana e i demoni, protettore del popolo di Dio. Gabriele ('Forza di Dio') è il messaggero delle annunciazioni: annunciò a Zaccaria la nascita di Giovanni Battista e a Maria l'incarnazione del Verbo. Raffaele ('Dio guarisce') accompagnò Tobia nel suo viaggio e guarì il padre Tobit dalla cecità. Gli arcangeli sono spiriti celesti che stanno alla presenza di Dio ed eseguono le sue missioni. La loro festa unificata fu istituita nel 1969.",
         "I tre arcangeli: Michele combattente, Gabriele messaggero e Raffaele guaritore.",
         "29 settembre", "Polizia, malati, farmacisti, viaggiatori"),

        (10, 4, "San Francesco d'Assisi", "san-francesco-d-assisi",
         "San Francesco (1182-1226), patrono d'Italia, rivoluzionò la spiritualità cristiana medievale. Figlio di mercante, dopo una giovinezza spensierata e una prigionia di guerra, si convertì abbracciando la povertà assoluta. Nel 1208 fondò l'Ordine dei Frati Minori (francescani). Predicò l'amore universale, chiamando creature 'fratello sole, sorella luna'. Nel 1224 ricevette le stimmate sul monte della Verna. Compose il Cantico delle Creature, primo testo poetico in italiano. Realizzò il primo presepe a Greccio. Morì il 3 ottobre 1226, fu canonizzato nel 1228. È patrono d'Italia e dell'ecologia.",
         "Il Poverello d'Assisi, patrono d'Italia, che parlava agli animali e ricevette le stimmate.",
         "4 ottobre", "Italia, ecologia, animali, commercianti"),

        (11, 1, "Tutti i Santi", "tutti-i-santi",
         "La solennità di Tutti i Santi celebra la comunione dei santi, la moltitudine innumerevole di coloro che hanno raggiunto la beatitudine eterna. Non solo i santi canonizzati, ma tutti i giusti che hanno vissuto secondo il Vangelo e ora godono della visione di Dio. La festa ha origini antichissime, fu fissata al 1° novembre da Gregorio IV nell'835. Celebra la chiamata universale alla santità e la meta finale della vita cristiana. È giorno di gioia per la vittoria della grazia sul peccato. Si rinnova la fede nella risurrezione e nella vita eterna.",
         "Festa di tutti i santi, conosciuti e sconosciuti, che godono della gloria del Paradiso.",
         "1 novembre", "Santità universale"),

        (11, 2, "Commemorazione dei Defunti", "commemorazione-defunti",
         "La Commemorazione dei Defunti fu istituita nel 998 da Sant'Odilone di Cluny. La Chiesa prega per le anime del Purgatorio, in attesa della beatitudine eterna. È giorno di suffragio: preghiere, messe e opere di carità vengono offerte per i defunti. Secondo la dottrina cattolica, le anime non ancora perfettamente purificate compiono in Purgatorio un cammino di purificazione prima di entrare in Paradiso. Il 2 novembre si visitano i cimiteri per onorare i propri cari defunti. È giorno di speranza nella risurrezione. La liturgia usa paramenti viola e testi consolatori sulla vita eterna.",
         "Giorno di preghiera per le anime dei defunti in attesa della gloria del Paradiso.",
         "2 novembre", "Defunti, anime del Purgatorio"),

        (12, 8, "Immacolata Concezione", "immacolata-concezione",
         "L'Immacolata Concezione è il dogma secondo cui Maria fu preservata dal peccato originale fin dal primo istante del suo concepimento. Proclamato da Pio IX nel 1854, si basa sulla pienezza di grazia di Maria. Dio la preparò così ad essere degna Madre del Salvatore. La festa, celebrata l'8 dicembre, nove mesi prima della natività di Maria (8 settembre), è molto sentita in Italia. Maria Immacolata è patrona d'Italia e degli Stati Uniti. L'apparizione di Lourdes (1858) confermò il dogma: Maria si presentò come 'l'Immacolata Concezione'. È simbolo della vittoria della grazia sul peccato.",
         "Maria fu concepita senza peccato originale, tutta pura e immacolata fin dal primo istante.",
         "8 dicembre", "Italia, Stati Uniti, concezione"),

        (12, 13, "Santa Lucia", "santa-lucia",
         "Santa Lucia (283-304), vergine e martire di Siracusa, subì il martirio durante la persecuzione di Diocleziano. Secondo la tradizione, consacrò la sua verginità a Cristo e distribuì i suoi beni ai poveri. Promessa sposa contro la sua volontà, rifiutò il matrimonio. Fu denunciata come cristiana e condannata al supplizio. Resistette miracolosamente ai tormenti prima di essere uccisa con la spada. La tradizione la rappresenta con gli occhi su un piatto, per questo è invocata contro le malattie degli occhi. Il suo nome significa 'luce'. Molto venerata in Scandinavia e nel Nord Italia.",
         "La giovane martire di Siracusa, protettrice della vista, la cui festa porta la luce nell'inverno.",
         "13 dicembre", "Vista, oculisti, ciechi, Siracusa"),

        (12, 25, "Natale del Signore", "natale-del-signore",
         "Il Natale celebra la nascita di Gesù Cristo a Betlemme. Secondo i Vangeli, Maria e Giuseppe giunsero a Betlemme per il censimento. Non trovando posto nell'albergo, Gesù nacque in una grotta-stalla e fu posto in una mangiatoia. Gli angeli annunciarono l'evento ai pastori che andarono ad adorarlo. L'incarnazione del Verbo è il mistero centrale della fede cristiana: Dio si fa uomo per salvare l'umanità. La data del 25 dicembre fu fissata nel IV secolo. Il Natale è preceduto dall'Avvento e seguito dall'Epifania. È la festa cristiana più popolare, celebrata con presepi, canti e riunioni familiari.",
         "Gesù, il Figlio di Dio, nasce a Betlemme dalla Vergine Maria. Dio si fa uomo per noi.",
         "25 dicembre", "Famiglia, bambini, pace nel mondo"),

        (12, 26, "Santo Stefano", "santo-stefano",
         "Santo Stefano fu il primo martire (protomartire) della Chiesa. Uno dei sette diaconi eletti dagli apostoli a Gerusalemme, era 'pieno di grazia e di fortezza'. Predicava con eloquenza e compiva prodigi. Accusato di blasfemia dal Sinedrio, pronunciò un lungo discorso sulla storia della salvezza, denunciando la durezza di cuore dei suoi accusatori. Fu condannato alla lapidazione. Durante il supplizio, imitando Cristo, pregò per i suoi persecutori: 'Signore, non imputare loro questo peccato'. Tra i lapidatori c'era Saulo, futuro San Paolo. Morì intorno al 36 d.C. La sua festa il 26 dicembre sottolinea il legame tra Natale e martirio.",
         "Il primo martire cristiano, diacono lapidato che perdonò i suoi uccisori.",
         "26 dicembre", "Diaconi, muratori, tagliapietre")
    ]

    for month, day, name, slug, biography, short_story, feast_day, patronage in saints_data:
        cursor.execute('''
            INSERT OR IGNORE INTO saints (month, day, name, slug, biography, short_story, feast_day, patronage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (month, day, name, slug, biography, short_story, feast_day, patronage))


def populate_holidays(cursor):
    """Populate Italian holidays"""
    holidays_data = [
        (1, 1, "Capodanno", "capodanno", None, 1, 0, None,
         "Il primo giorno dell'anno è festa nazionale in Italia dal 1948. Si celebra con festeggiamenti che iniziano la sera del 31 dicembre (Veglione di San Silvestro)."),

        (1, 6, "Epifania", "epifania", None, 1, 1, None,
         "L'Epifania celebra la visita dei Re Magi a Gesù Bambino. In Italia è il giorno della Befana, una vecchina che porta doni ai bambini buoni e carbone a quelli cattivi."),

        (4, 25, "Festa della Liberazione", "festa-della-liberazione", None, 1, 0, None,
         "Anniversario della liberazione d'Italia dal nazifascismo (1945). Si commemora la fine dell'occupazione tedesca e del regime fascista."),

        (5, 1, "Festa del Lavoro", "festa-del-lavoro", None, 1, 0, None,
         "Festa internazionale dei lavoratori, celebra le lotte operaie per i diritti del lavoro. In Italia è festa nazionale dal 1945."),

        (6, 2, "Festa della Repubblica", "festa-della-repubblica", None, 1, 0, None,
         "Celebra il referendum del 2 giugno 1946 che sancì la nascita della Repubblica Italiana e la fine della monarchia."),

        (8, 15, "Ferragosto - Assunzione di Maria", "ferragosto", None, 1, 1, None,
         "Festa religiosa dell'Assunzione di Maria al cielo. Coincide con Ferragosto, antica festa romana di mezza estate. Giorno di riposo e gite fuori porta."),

        (11, 1, "Tutti i Santi - Ognissanti", "tutti-i-santi", None, 1, 1, None,
         "Solennità cristiana che onora tutti i santi. Giorno di raccoglimento e visita ai cimiteri."),

        (12, 8, "Immacolata Concezione", "immacolata-concezione", None, 1, 1, None,
         "Solennità dell'Immacolata Concezione di Maria. Tradizionalmente segna l'inizio del periodo natalizio con l'allestimento di presepi e alberi di Natale."),

        (12, 25, "Natale", "natale", None, 1, 1, None,
         "Celebra la nascita di Gesù Cristo. È la festa cristiana più importante, celebrata con riunioni familiari, pranzi tradizionali e scambio di doni."),

        (12, 26, "Santo Stefano", "santo-stefano", None, 1, 1, None,
         "Commemora il primo martire cristiano. In Italia è il secondo giorno di festa natalizia, dedicato a pranzi familiari e riposo.")
    ]

    for month, day, name, slug, year, is_national, is_religious, region, description in holidays_data:
        cursor.execute('''
            INSERT OR IGNORE INTO holidays (month, day, name, slug, year, is_national, is_religious, region, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (month, day, name, slug, year, is_national, is_religious, region, description))


def populate_name_days(cursor):
    """Populate common Italian name days"""
    name_days_data = [
        # Gennaio
        (1, 1, "Mario"), (1, 1, "Maria"),
        (2, 1, "Basilio"),
        (3, 1, "Genoveffa"),
        (6, 1, "Epifanio"),
        (17, 1, "Antonio"),
        (20, 1, "Sebastiano"),
        (21, 1, "Agnese"),
        (24, 1, "Francesco"),
        (28, 1, "Tommaso"),
        (31, 1, "Giovanni"),

        # Febbraio
        (3, 2, "Biagio"),
        (5, 2, "Agata"),
        (10, 2, "Scolastica"),
        (14, 2, "Valentino"), (14, 2, "Valentina"),
        (22, 2, "Margherita"),

        # Marzo
        (8, 3, "Giovanni"),
        (9, 3, "Francesca"),
        (12, 3, "Gregorio"),
        (17, 3, "Patrizio"),
        (19, 3, "Giuseppe"),
        (25, 3, "Annunziata"),

        # Aprile
        (2, 4, "Francesco"),
        (4, 4, "Isidoro"),
        (11, 4, "Stanislao"),
        (21, 4, "Anselmo"),
        (23, 4, "Giorgio"),
        (25, 4, "Marco"),
        (29, 4, "Caterina"),
        (30, 4, "Pio"),

        # Maggio
        (1, 5, "Giuseppe"),
        (2, 5, "Atanasio"),
        (3, 5, "Filippo"), (3, 5, "Giacomo"),
        (10, 5, "Antonino"),
        (12, 5, "Domenico"),
        (26, 5, "Filippo"),
        (31, 5, "Petronilla"),

        # Giugno
        (1, 6, "Annibale"),
        (3, 6, "Carlo"),
        (13, 6, "Antonio"),
        (19, 6, "Romualdo"),
        (21, 6, "Luigi"),
        (24, 6, "Giovanni"),
        (29, 6, "Pietro"), (29, 6, "Paolo"),

        # Luglio
        (1, 7, "Aronne"),
        (4, 7, "Elisabetta"),
        (11, 7, "Benedetto"),
        (14, 7, "Camillo"),
        (22, 7, "Maddalena"),
        (23, 7, "Brigida"),
        (25, 7, "Giacomo"),
        (26, 7, "Anna"),
        (29, 7, "Marta"),
        (31, 7, "Ignazio"),

        # Agosto
        (1, 8, "Alfonso"),
        (4, 8, "Giovanni"),
        (7, 8, "Gaetano"),
        (8, 8, "Domenico"),
        (10, 8, "Lorenzo"),
        (11, 8, "Chiara"),
        (15, 8, "Maria"),
        (19, 8, "Ludovico"),
        (20, 8, "Bernardo"),
        (24, 8, "Bartolomeo"),
        (27, 8, "Monica"),
        (28, 8, "Agostino"),
        (29, 8, "Giovanni"),

        # Settembre
        (3, 9, "Gregorio"),
        (5, 9, "Teresa"),
        (8, 9, "Sergio"),
        (12, 9, "Maria"),
        (15, 9, "Nicomede"),
        (17, 9, "Roberto"),
        (19, 9, "Gennaro"),
        (21, 9, "Matteo"),
        (23, 9, "Pio"),
        (26, 9, "Cosma"), (26, 9, "Damiano"),
        (29, 9, "Michele"), (29, 9, "Gabriele"), (29, 9, "Raffaele"),
        (30, 9, "Girolamo"),

        # Ottobre
        (1, 10, "Teresa"),
        (2, 10, "Angelo"),
        (4, 10, "Francesco"),
        (7, 10, "Rosario"),
        (9, 10, "Dionigi"),
        (15, 10, "Teresa"),
        (16, 10, "Edvige"),
        (17, 10, "Ignazio"),
        (18, 10, "Luca"),
        (28, 10, "Simone"), (28, 10, "Giuda"),

        # Novembre
        (1, 11, "Ognissanti"),
        (4, 11, "Carlo"),
        (11, 11, "Martino"),
        (13, 11, "Diego"),
        (15, 11, "Alberto"),
        (21, 11, "Presentazione di Maria"),
        (22, 11, "Cecilia"),
        (23, 11, "Clemente"),
        (25, 11, "Caterina"),
        (30, 11, "Andrea"),

        # Dicembre
        (3, 12, "Francesco"),
        (4, 12, "Barbara"),
        (6, 12, "Nicola"), (6, 12, "Nicolò"),
        (7, 12, "Ambrogio"),
        (8, 12, "Immacolata"),
        (13, 12, "Lucia"),
        (25, 12, "Natale"),
        (26, 12, "Stefano"),
        (27, 12, "Giovanni"),
        (31, 12, "Silvestro")
    ]

    for day, month, name in name_days_data:
        cursor.execute('''
            INSERT INTO name_days (day, month, name)
            VALUES (?, ?, ?)
        ''', (day, month, name))


def populate_historical_events(cursor):
    """Populate some famous historical events"""
    events_data = [
        (12, 10, 1948, "Dichiarazione Universale dei Diritti Umani",
         "L'Assemblea Generale delle Nazioni Unite proclama la Dichiarazione Universale dei Diritti Umani.", "Storia"),

        (1, 1, 1948, "Entra in vigore la Costituzione della Repubblica Italiana",
         "La Costituzione italiana entra in vigore, fondamento della Repubblica democratica.", "Italia"),

        (25, 4, 1945, "Liberazione d'Italia",
         "Le forze partigiane liberano Milano e Torino. Fine dell'occupazione nazifascista.", "Italia"),

        (2, 6, 1946, "Referendum Repubblica",
         "Gli italiani scelgono la Repubblica con 12.717.923 voti contro 10.719.284 per la monarchia.", "Italia"),

        (12, 10, 1492, "Cristoforo Colombo scopre l'America",
         "Colombo sbarca nell'isola di San Salvador nelle Bahamas, aprendo la via al Nuovo Mondo.", "Esplorazione"),

        (14, 7, 1789, "Presa della Bastiglia",
         "Inizio della Rivoluzione Francese con l'assalto alla fortezza simbolo dell'assolutismo.", "Storia"),

        (4, 10, 1582, "Riforma del calendario gregoriano",
         "Papa Gregorio XIII introduce il calendario gregoriano, eliminando 10 giorni per correggere l'errore astronomico.", "Scienza"),

        (20, 7, 1969, "Primo uomo sulla Luna",
         "Neil Armstrong e Buzz Aldrin camminano sulla Luna con la missione Apollo 11.", "Spazio"),

        (9, 11, 1989, "Caduta del Muro di Berlino",
         "Cade il Muro di Berlino, simbolo della Guerra Fredda, riunificando la Germania.", "Storia"),

        (17, 3, 1861, "Proclamazione del Regno d'Italia",
         "Vittorio Emanuele II proclamato primo re d'Italia. Nasce lo Stato unitario italiano.", "Italia")
    ]

    for day, month, year, title, description, category in events_data:
        cursor.execute('''
            INSERT INTO historical_events (day, month, year, title, description, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (day, month, year, title, description, category))


def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)


if __name__ == '__main__':
    init_db()
