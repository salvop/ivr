# 🔥 HOTFIX: Gestione delle Transazioni del Database

**Data:** 2025-10-10  
**Priorità:** CRITICA  
**Tipo:** Bug Fix  
**Versione:** 1.1.0

## ⚠️ Problema Critico Risolto

Il sistema aveva un problema **CRITICO** che causava **blocchi del database per giorni**, rendendo l'applicazione inutilizzabile.

### Causa Root
Le transazioni del database non venivano mai chiuse correttamente:
- Nessun commit automatico dopo le operazioni
- Nessun rollback in caso di errore
- Connessioni riutilizzate con transazioni aperte
- Lock del database accumulati nel tempo

### Impatto
- ❌ Database bloccato per giorni
- ❌ Impossibilità di eseguire query
- ❌ Applicazione non funzionante
- ❌ Necessità di kill manuale delle sessioni

## ✅ Soluzione Implementata

### File Modificati

1. **`app/db.py`** - Context manager con gestione automatica transazioni
   - ✅ Commit automatico al successo
   - ✅ Rollback automatico in caso di errore
   - ✅ Log dettagliati di tutte le operazioni

2. **`app/services/movimenti_service.py`** - Rimosso commit manuale
3. **`app/services/pratiche_service.py`** - Rimosso commit manuale
4. **`app/services/email_service.py`** - Rimosso commit manuale
5. **`app/services/sms_service.py`** - Rimosso commit manuale

### Documentazione Creata

1. **`docs/TRANSACTION_MANAGEMENT.md`** - Guida completa sulla gestione transazioni
2. **`docs/database_lock_monitoring.sql`** - Script SQL per monitoraggio e risoluzione lock
3. **`README.md`** - Aggiornato con informazioni sulla gestione database

## 🚀 Procedura di Deployment

### 1. BACKUP (OBBLIGATORIO)
```sql
-- Backup del database MS SQL Server
BACKUP DATABASE [nome_database] TO DISK = 'C:\backup\before_hotfix.bak'
```

### 2. VERIFICA STATO ATTUALE
```bash
# Controllare se ci sono lock attivi
# Eseguire le query in docs/database_lock_monitoring.sql
```

### 3. CHIUSURA SESSIONI BLOCCATE (se necessario)
```sql
-- Identificare e uccidere sessioni bloccate se necessario
-- Vedere docs/database_lock_monitoring.sql sezione 6

-- Esempio:
-- EXEC sp_who2 'active'
-- KILL [session_id]
```

### 4. STOP APPLICAZIONE
```bash
# Fermare tutte le istanze dell'applicazione
# Systemd
sudo systemctl stop cflow-api

# PM2
pm2 stop all
```

### 5. PULL DELLE MODIFICHE
```bash
cd /path/to/cflow
git pull origin main
# oppure
git fetch origin
git checkout <commit-hash-di-questo-fix>
```

### 6. VERIFICA MODIFICHE
```bash
# Verificare che i file siano stati modificati correttamente
git log --oneline -5
git diff HEAD~1 app/db.py
```

### 7. RESTART APPLICAZIONE
```bash
# Systemd
sudo systemctl start cflow-api

# PM2
pm2 start app.main:app
```

### 8. VERIFICA FUNZIONAMENTO

#### Test Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

#### Test Operazione Database
```bash
# Test GET (lettura)
curl -H "X-API-Key: your-api-key" http://localhost:8000/pratiche/12345

# Test POST (scrittura)
curl -X POST "http://localhost:8000/movimenti/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{...}'
```

#### Verifica Log
```bash
# Controllare che ci siano messaggi di commit
tail -f logs/app.log | grep -i "commit\|rollback"

# Expected output:
# Transaction committed successfully
# (nessun messaggio di errore)
```

### 9. MONITORAGGIO POST-DEPLOYMENT

#### Verifica Lock Database (ogni 5 minuti per 1 ora)
```sql
-- Eseguire query 2 da docs/database_lock_monitoring.sql
-- Verificare che non ci siano transazioni > 30 minuti
```

#### Verifica Connessioni Pool
```bash
# Nei log dovrebbero apparire:
tail -f logs/app.log | grep -i "pool"

# Expected:
# "Connection returned to pool. Pool size: X"
# "Reusing connection from pool"
```

#### Verifica Performance
```bash
# Test di carico rapido
for i in {1..10}; do
  curl -H "X-API-Key: your-api-key" http://localhost:8000/pratiche/12345 &
done
wait

# Tutte le richieste dovrebbero completarsi senza errori
```

## 📊 Metriche da Monitorare

### Prima Ora
- ✅ Nessun lock > 1 minuto
- ✅ Tutte le transazioni committate entro 10 secondi
- ✅ Nessun errore nei log
- ✅ Response time < 500ms

### Primo Giorno
- ✅ Nessun lock > 5 minuti
- ✅ Pool connections stabili
- ✅ Nessun accumulo di transazioni
- ✅ Nessun deadlock

### Prima Settimana
- ✅ Zero incidenti di lock prolungati
- ✅ Performance stabili
- ✅ Log senza anomalie

## 🔍 Risoluzione Problemi

### Problema: Ancora lock dopo il deployment

**Possibile causa:** Sessioni vecchie ancora attive

**Soluzione:**
```sql
-- 1. Identificare sessioni vecchie
-- Eseguire query 4 da docs/database_lock_monitoring.sql

-- 2. Uccidere sessioni con IdleMinutes > 5
KILL [session_id];

-- 3. Riavviare applicazione
```

### Problema: Errori "Connection pool exhausted"

**Possibile causa:** Troppe connessioni concorrenti

**Soluzione:**
```python
# In app/config.py, aumentare DB_POOL_SIZE
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))  # da 10 a 20
```

### Problema: Transazioni che impiegano troppo tempo

**Possibile causa:** Query lente

**Soluzione:**
```bash
# Abilitare log dettagliati
# In app/main.py, impostare log level a DEBUG
logging.basicConfig(level=logging.DEBUG)

# Analizzare i log per identificare query lente
tail -f logs/app.log | grep -i "duration"
```

## 📞 Contatti di Emergenza

In caso di problemi critici durante il deployment:

1. **Rollback immediato:**
   ```bash
   git checkout HEAD~1
   # Restart con systemd
   sudo systemctl restart cflow-api
   # oppure con PM2
   pm2 restart app.main:app
   ```

2. **Ripristino database:**
   ```bash
   # Ripristinare il backup fatto al punto 1
   ```

3. **Contattare il team di sviluppo**

## ✅ Checklist Finale

Prima di considerare il deployment completato:

- [ ] Backup del database eseguito
- [ ] Lock esistenti identificati e risolti
- [ ] Applicazione fermata
- [ ] Codice aggiornato
- [ ] Applicazione riavviata
- [ ] Health check OK
- [ ] Test lettura OK
- [ ] Test scrittura OK
- [ ] Log mostrano commit/rollback corretti
- [ ] Nessun lock > 1 minuto nel database
- [ ] Connessioni pool funzionanti
- [ ] Performance accettabili
- [ ] Monitoraggio attivo per 1 ora
- [ ] Documentazione letta dal team
- [ ] Alert configurati per lock > 5 minuti

## 📚 Documentazione di Riferimento

- [docs/TRANSACTION_MANAGEMENT.md](docs/TRANSACTION_MANAGEMENT.md) - Guida completa
- [docs/database_lock_monitoring.sql](docs/database_lock_monitoring.sql) - Script monitoraggio
- [README.md](README.md) - Documentazione generale aggiornata

## 🎯 Risultati Attesi

Dopo questo hotfix:
- ✅ Zero lock > 5 minuti
- ✅ Tutte le transazioni completate correttamente
- ✅ Nessun intervento manuale necessario
- ✅ Sistema stabile e performante
- ✅ Database sempre accessibile

---

**IMPORTANTE:** Questo è un fix critico che risolve un problema di stabilità del sistema. Il deployment deve essere eseguito al più presto, preferibilmente in una finestra di manutenzione.

