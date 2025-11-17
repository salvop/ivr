# CollectFlowAPI

API FastAPI per la gestione di pratiche, movimenti, email e SMS.

## 🚀 Features

- **Gestione Pratiche**: CRUD operations per le pratiche
- **Gestione Movimenti**: Tracking dei movimenti associati alle pratiche
- **Gestione Email**: Invio e tracking delle email
- **Gestione SMS**: Invio e tracking degli SMS
- **Autenticazione**: API Key authentication
- **CORS Support**: Cross-origin resource sharing
- **Health Check**: Endpoint per il monitoraggio dello stato
- **Documentazione**: Swagger UI e ReDoc automatici

## 📋 Endpoints

### Root & Health
- `GET /` - Informazioni sull'API
- `GET /health` - Health check

### Pratiche
- `GET /pratiche/{contatore}` - Recupera pratica per ID
- `POST /pratiche/` - Crea nuova pratica

### Movimenti
- `GET /movimenti/{contatore}` - Lista movimenti per pratica
- `POST /movimenti/` - Crea nuovo movimento

### Email
- `GET /email/{contatore}` - Lista email per pratica
- `POST /email/` - Crea nuova email

### SMS
- `GET /sms/{contatore}` - Lista SMS per pratica
- `POST /sms/` - Crea nuovo SMS

## 🔧 Setup

### Prerequisiti
- Python 3.8+
- SQL Server database
- Virtual environment

### Installazione

1. **Clona il repository**
```bash
git clone <repository-url>
cd project1
```

2. **Crea virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows
```

3. **Installa dipendenze**
```bash
pip install -r requirements.txt
```

4. **Configura variabili d'ambiente**
Crea un file `.env` nella root del progetto:
```env
SQLSERVER_DSN=Driver={ODBC Driver 17 for SQL Server};Server=your_server;Database=your_db;UID=your_user;PWD=your_password
API_KEYS=your-api-key-1,your-api-key-2
```

5. **Avvia l'applicazione**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

##  Autenticazione

Tutti gli endpoint richiedono l'header `X-API-Key` per l'autenticazione.

**Esempio:**
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/pratiche/12345
```

## 📚 Documentazione

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **[Gestione delle Transazioni](docs/TRANSACTION_MANAGEMENT.md)**: Guida completa sulla gestione delle transazioni del database
- **[Standard API](docs/API_STANDARDS.md)**: Standard per lo sviluppo delle API
- **[Checklist Produzione](docs/PRODUCTION_CHECKLIST.md)**: Checklist per il deployment in produzione

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Esempio di creazione pratica
```bash
curl -X POST "http://localhost:8000/pratiche/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "codice_pratica": "PRAT-2024-001",
    "codice_cliente": "CLI-001",
    "cognome": "Rossi",
    "nome": "Mario",
    "email": "mario.rossi@email.com",
    "cap": "12345",
    "provincia": "MI"
  }'
```

## 🏗️ Architettura

```
app/
├── main.py              # Entry point dell'applicazione
├── config.py            # Configurazione e validazione API key
├── db.py                # Connessione database
├── middleware.py        # Middleware personalizzati
├── models/              # Modelli Pydantic
│   ├── pratiche.py
│   ├── movimenti.py
│   ├── email.py
│   └── sms.py
├── routers/             # Endpoint API
│   ├── pratiche.py
│   ├── movimenti.py
│   ├── email.py
│   └── sms.py
└── services/            # Logica di business
    ├── pratiche_service.py
    ├── movimenti_service.py
    ├── email_service.py
    └── sms_service.py
```

## 🗄️ Gestione Database

### Connection Pooling
L'applicazione implementa un connection pool personalizzato per gestire efficientemente le connessioni al database:
- Pool configurabile (default: 10 connessioni)
- Gestione automatica delle transazioni
- Commit automatico per operazioni riuscite
- Rollback automatico in caso di errori

### Gestione Transazioni
Tutte le operazioni del database utilizzano un context manager che garantisce:
- **Commit automatico**: Le transazioni vengono committate automaticamente al termine dell'operazione
- **Rollback automatico**: In caso di errore, viene eseguito il rollback per mantenere la consistenza dei dati
- **Prevenzione dei lock**: Le connessioni e transazioni vengono sempre chiuse correttamente

⚠️ **Importante**: Non usare mai `conn.commit()` o `conn.rollback()` manualmente. La gestione è automatica.

Per maggiori dettagli, consultare la [Documentazione sulla Gestione delle Transazioni](docs/TRANSACTION_MANAGEMENT.md).

## 🔍 Logging

L'applicazione utilizza logging configurato con:
- Rotazione giornaliera dei file di log
- Retention di 7 giorni
- Output su console e file `app.log`
- Log dettagliati per commit/rollback delle transazioni

## 🚨 Note di Sicurezza

- **CORS**: Configurato per permettere tutte le origini (`*`). Configurare appropriatamente per la produzione.
- **API Keys**: Gestire le chiavi API in modo sicuro e non committarle nel codice.
- **Database**: Utilizzare connessioni sicure e credenziali appropriate.

## 📝 TODO

- [x] Implementare connection pooling per il database ✅
- [x] Gestione automatica delle transazioni ✅
- [ ] Aggiungere caching per le query frequenti
- [ ] Implementare rate limiting avanzato
- [ ] Aggiungere test unitari e di integrazione
- [ ] Aggiungere paginazione per gli endpoint di lista
- [ ] Implementare validazione più robusta dei dati
- [ ] Monitoraggio e alerting per lock del database

## 🤝 Contributing

1. Fork il progetto
2. Crea un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.
