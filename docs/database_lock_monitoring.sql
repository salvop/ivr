-- =====================================================================
-- Script per Monitoraggio e Risoluzione Lock del Database
-- =====================================================================
-- Autore: Sistema
-- Data: 2025-10-10
-- Versione: 1.0.0
-- Database: MS SQL Server
-- =====================================================================

-- 1. VERIFICA LOCK ATTIVI
-- Mostra tutte le risorse bloccate e le sessioni coinvolte
SELECT 
    request_session_id AS SessionID,
    resource_type AS ResourceType,
    resource_database_id AS DatabaseID,
    resource_description AS ResourceDescription,
    request_mode AS LockMode,
    request_status AS Status
FROM sys.dm_tran_locks
WHERE request_session_id <> @@SPID
ORDER BY request_session_id;

-- 2. VERIFICA TRANSAZIONI ATTIVE
-- Mostra tutte le transazioni attualmente attive
SELECT 
    transaction_id AS TransactionID,
    name AS TransactionName,
    transaction_begin_time AS BeginTime,
    DATEDIFF(MINUTE, transaction_begin_time, GETDATE()) AS DurationMinutes,
    transaction_type AS Type,
    transaction_state AS State
FROM sys.dm_tran_active_transactions
ORDER BY transaction_begin_time;

-- 3. IDENTIFICA SESSIONI BLOCCATE E BLOCCANTI
-- Mostra quale sessione sta bloccando quale altra
SELECT 
    blocking.session_id AS BlockingSessionID,
    blocked.session_id AS BlockedSessionID,
    blocked.wait_type AS WaitType,
    blocked.wait_time AS WaitTimeMs,
    blocking_sql.text AS BlockingQuery,
    blocked_sql.text AS BlockedQuery,
    blocking.login_name AS BlockingUser,
    blocked.login_name AS BlockedUser,
    blocking.host_name AS BlockingHost,
    blocked.host_name AS BlockedHost,
    blocking.program_name AS BlockingProgram
FROM sys.dm_exec_requests blocked
INNER JOIN sys.dm_exec_sessions blocking 
    ON blocked.blocking_session_id = blocking.session_id
OUTER APPLY sys.dm_exec_sql_text(blocking.sql_handle) AS blocking_sql
OUTER APPLY sys.dm_exec_sql_text(blocked.sql_handle) AS blocked_sql
WHERE blocked.blocking_session_id <> 0;

-- 4. VERIFICA CONNESSIONI ATTIVE PER APPLICAZIONE
-- Mostra tutte le connessioni aperte dalla tua applicazione
SELECT 
    session_id AS SessionID,
    login_name AS User,
    host_name AS Host,
    program_name AS Program,
    status AS Status,
    open_transaction_count AS OpenTransactions,
    DATEDIFF(MINUTE, last_request_start_time, GETDATE()) AS IdleMinutes,
    last_request_start_time AS LastRequestTime
FROM sys.dm_exec_sessions
WHERE program_name LIKE '%python%' 
   OR program_name LIKE '%fastapi%'
   OR host_name = HOST_NAME()
ORDER BY open_transaction_count DESC, IdleMinutes DESC;

-- 5. DETTAGLI SU UNA SESSIONE SPECIFICA
-- Sostituire @SessionID con l'ID della sessione da analizzare
DECLARE @SessionID INT = 52; -- MODIFICARE CON L'ID DELLA SESSIONE

SELECT 
    s.session_id,
    s.login_name,
    s.host_name,
    s.program_name,
    s.status,
    s.cpu_time,
    s.memory_usage,
    s.open_transaction_count,
    r.command,
    r.wait_type,
    r.wait_time,
    t.text AS CurrentQuery
FROM sys.dm_exec_sessions s
LEFT JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE s.session_id = @SessionID;

-- 6. UCCIDERE UNA SESSIONE BLOCCATA (CON CAUTELA!)
-- Sostituire @SessionID con l'ID della sessione da terminare
-- ⚠️ USARE SOLO SE ASSOLUTAMENTE NECESSARIO
-- DECLARE @SessionID INT = 52; -- MODIFICARE CON L'ID DELLA SESSIONE
-- KILL @SessionID;

-- 7. STATISTICHE LOCK PER OGGETTO
-- Mostra quali tabelle hanno più lock
SELECT 
    OBJECT_NAME(p.object_id, p.database_id) AS TableName,
    resource_type AS ResourceType,
    request_mode AS LockMode,
    COUNT(*) AS LockCount
FROM sys.dm_tran_locks l
INNER JOIN sys.partitions p ON l.resource_associated_entity_id = p.hobt_id
WHERE resource_database_id = DB_ID()
GROUP BY OBJECT_NAME(p.object_id, p.database_id), resource_type, request_mode
ORDER BY LockCount DESC;

-- =====================================================================
-- PROCEDURE DI EMERGENZA
-- =====================================================================

-- STEP 1: Identificare le sessioni problematiche
-- Eseguire le query 1, 2, 3, 4 per identificare le sessioni che stanno
-- causando lock per molto tempo (> 30 minuti)

-- STEP 2: Tentare di risolvere naturalmente
-- Se possibile, aspettare che l'applicazione rilasci i lock
-- Verificare nei log dell'applicazione se ci sono errori

-- STEP 3: Uccidere le sessioni solo se necessario
-- Usare le query 6 (SQL Server) o 5 (Oracle) per terminare le sessioni
-- ⚠️ Questo può causare perdita di dati se la transazione era importante

-- STEP 4: Riavviare l'applicazione
-- Dopo aver risolto il problema, riavviare l'applicazione per:
-- - Resettare il connection pool
-- - Chiudere eventuali connessioni residue
-- - Applicare le nuove modifiche alla gestione delle transazioni

-- STEP 5: Monitorare
-- Continuare a monitorare per assicurarsi che il problema non si ripresenti
-- Controllare i log dell'applicazione per messaggi di commit/rollback

-- =====================================================================
-- NOTE IMPORTANTI
-- =====================================================================

-- 1. I lock di breve durata (< 1 minuto) sono normali
-- 2. Lock > 5 minuti indicano un potenziale problema
-- 3. Lock > 30 minuti richiedono intervento immediato
-- 4. Salvare sempre i risultati delle query prima di uccidere sessioni
-- 5. Comunicare con il team prima di terminare sessioni in produzione
-- 6. Verificare sempre che la gestione delle transazioni sia corretta nel codice

-- =====================================================================
-- ESEMPI DI USO
-- =====================================================================

-- Scenario 1: Verificare se ci sono lock attivi
-- Eseguire le query 1 e 3

-- Scenario 2: Identificare una sessione che blocca da ore
-- Eseguire la query 3 e cercare sessioni con WaitTimeMs molto alto
-- Verificare chi è l'utente bloccante e cosa sta facendo

-- Scenario 3: L'applicazione è bloccata completamente
-- 1. Eseguire query 4 per vedere tutte le connessioni dell'app
-- 2. Eseguire query 2 per vedere transazioni aperte da molto tempo
-- 3. Identificare e terminare le sessioni problematiche
-- 4. Riavviare l'applicazione

-- Scenario 4: Monitoraggio preventivo
-- Programmare l'esecuzione della query 2 ogni 5 minuti
-- Impostare un alert se ci sono transazioni > 30 minuti

