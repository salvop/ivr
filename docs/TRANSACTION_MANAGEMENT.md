# Gestione delle Transazioni nel Database

**Autore:** Sistema  
**Data:** 2025-10-10  
**Versione:** 1.0.0  

## Problema Identificato

Il sistema aveva un problema critico nella gestione delle transazioni del database che causava **blocchi per giorni**:

### Cause del Problema

1. **Transazioni non chiuse automaticamente**: Il context manager `get_connection()` restituiva le connessioni al pool senza eseguire `commit()` o `rollback()`
2. **Operazioni di lettura senza commit**: Le query SELECT aprivano transazioni che rimanevano aperte indefinitamente
3. **Mancanza di rollback in caso di errore**: Le eccezioni lasciavano le transazioni aperte
4. **Connessioni riutilizzate con transazioni attive**: Il pool riusava connessioni che avevano transazioni non completate

### Impatto

- Lock di database per giorni
- Deadlock frequenti
- Performance degradate
- Impossibilità di eseguire operazioni sul database

## Soluzione Implementata

### 1. Context Manager con Gestione Automatica delle Transazioni

Il file `app/db.py` è stato modificato per gestire automaticamente commit e rollback:

```python
@contextmanager
def get_connection():
    """Get database connection with automatic transaction management"""
    pool = get_connection_pool()
    connection = None
    try:
        connection = pool.get_connection()
        yield connection
        # Commit automatico se tutto va bene
        if connection and not connection.closed:
            connection.commit()
    except Exception as e:
        # Rollback automatico in caso di errore
        if connection and not connection.closed:
            connection.rollback()
        raise
    finally:
        # Restituisce sempre la connessione al pool
        if connection:
            pool.return_connection(connection)
```

### 2. Rimozione dei Commit Espliciti

Tutti i `conn.commit()` espliciti sono stati rimossi dai service files:
- `app/services/movimenti_service.py`
- `app/services/pratiche_service.py`
- `app/services/email_service.py`
- `app/services/sms_service.py`

## Best Practices

### ✅ FARE

1. **Usare sempre il context manager**:
   ```python
   with get_connection() as conn:
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM tabella")
       # Il commit viene fatto automaticamente
   ```

2. **Non fare commit espliciti**: Il context manager gestisce tutto automaticamente

3. **Gestire le eccezioni**: Il rollback è automatico, ma gestisci le eccezioni per la logica applicativa

4. **Mantenere le transazioni brevi**: Evita operazioni lunghe dentro il blocco `with`

### ❌ NON FARE

1. **Non fare commit/rollback manuali**: 
   ```python
   # ❌ NON FARE QUESTO
   with get_connection() as conn:
       cursor.execute("INSERT ...")
       conn.commit()  # NON NECESSARIO!
   ```

2. **Non tenere connessioni aperte troppo a lungo**:
   ```python
   # ❌ NON FARE QUESTO
   with get_connection() as conn:
       # ... molte operazioni lunghe ...
       time.sleep(60)  # MAI!
   ```

3. **Non salvare la connessione fuori dal context manager**:
   ```python
   # ❌ NON FARE QUESTO
   saved_conn = None
   with get_connection() as conn:
       saved_conn = conn
   # Ora saved_conn è già stata restituita al pool!
   ```

## Compatibilità Database

Le modifiche sono implementate per **MS SQL Server** utilizzando pyodbc. Il comportamento delle transazioni segue lo standard SQL:
- `commit()` conferma le modifiche
- `rollback()` annulla le modifiche
- Gestione automatica tramite context manager

## Testing

Dopo l'implementazione, verificare:

1. **Nessun lock residuo**: 
   ```sql
   SELECT * FROM sys.dm_tran_locks WHERE request_session_id <> @@SPID
   ```

2. **Monitoraggio delle transazioni aperte**:
   ```sql
   SELECT * FROM sys.dm_tran_active_transactions
   ```

3. **Log dell'applicazione**: Verificare la presenza di messaggi:
   - "Transaction committed successfully" per operazioni completate
   - "Transaction rolled back" per errori gestiti

## Risoluzione dei Problemi

### Se il database è ancora bloccato

1. Identificare le sessioni bloccate:
   ```sql
   EXEC sp_who2
   ```

2. Uccidere le sessioni problematiche (con cautela!):
   ```sql
   KILL [session_id]
   ```

3. Riavviare l'applicazione per resettare il connection pool

### Prevenzione

- Monitorare regolarmente i lock nel database
- Configurare timeout appropriati nelle connessioni
- Implementare health checks che verificano lo stato del database
- Usare il logging per tracciare tutte le operazioni del database

## Riferimenti

- [PyODBC Transaction Management](https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#autocommit)
- [SQL Server Lock Management](https://docs.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking)
- [SQL Server Transaction Guide](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/transactions-transact-sql)

## Changelog

### 2025-10-10 - v1.0.0
- Implementata gestione automatica delle transazioni in `get_connection()`
- Rimossi tutti i commit espliciti dai service files
- Aggiunto rollback automatico in caso di errore
- Documentato il processo di gestione delle transazioni

