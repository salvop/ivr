"""
Practice Business Logic Service
==============================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: Business logic and database operations for practice management
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module contains all business logic for practice operations including
CRUD operations, validation, and database interactions.
"""

from fastapi import HTTPException
from app.db import get_connection
from app.models.pratiche import Pratica, PraticaCreate

def fetch_pratica(contatore: int) -> Pratica:
    """
    Recupera la pratica dal DB e la mappa in un modello Pydantic.
    Se non esiste, solleva 404.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                contatore,
                [codice pratica],
                [codice cliente],
                vocativo,
                cognome,
                nome,
                [data nascita],
                [ragione sociale],
                indirizzo,
                cap,
                citta,
                provincia,
                [tipo mandato],
                [tipo intervento],
                email,
                telefono1,
                telefono2,
                telefono3,
                telefono4,
                telefono5,
                telefono6,
                telefono7,
                telefono8,
                User_M3,
                EmailRX1,
                EsitoFonia,
                [scadenza mandato],
                [seat_importoOrig],
                posizione,
                [codice esattore]
        FROM [tabella pratiche]
            WHERE contatore = ?
        """, (contatore,))
        row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Pratica non trovata")

    return Pratica(
        contatore=row[0],
        codice_pratica=row[1],
        codice_cliente=row[2],
        vocativo=row[3],
        cognome=row[4],
        nome=row[5],
        data_nascita=row[6],
        ragione_sociale=row[7],
        indirizzo=row[8],
        cap=row[9],
        citta=row[10],
        provincia=row[11],
        mandante=row[12],
        intervento=row[13],
        email=row[14],
        telefono1=row[15],
        telefono2=row[16],
        telefono3=row[17],
        telefono4=row[18],
        telefono5=row[19],
        telefono6=row[20],
        telefono7=row[21],
        telefono8=row[22],
        user_m3=row[23],
        EmailRX1=row[24],
        EsitoPrioritario=row[25],  # Maps to database field EsitoFonia
        scadenza_mandato=row[26],
        seat_importoOrig=row[27],
        posizione=row[28],
        esattore=row[29],
    )
    
def create_pratica(data: PraticaCreate) -> Pratica:
    """
    Inserisce una nuova pratica nella tabella [tabella pratiche].
    Verifica eventuali vincoli di business (ad es. unicità), poi fa l'INSERT.
    Restituisce il modello Pratica con 'contatore' valorizzato.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # Esempio di validazione di business: controllo unicità codice_pratica
        cursor.execute(
            "SELECT COUNT(*) FROM [tabella pratiche] WHERE [codice pratica] = ?",
            (data.codice_pratica,)
        )
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="codice_pratica già esistente")

        # Esempio di validazione di business: controllo città non nulla se indirizzo è settato
        if data.indirizzo and not data.citta:
            raise HTTPException(status_code=400, detail="Se indirizzo è valorizzato, citta è obbligatoria")

        # Esegui l'INSERT (includendo tutti i campi)
        cursor.execute(f"""
            INSERT INTO [tabella pratiche]
                ([codice pratica], [codice cliente], vocativo, cognome, nome, [data nascita],
                 [ragione sociale], indirizzo, cap, citta, provincia, [tipo mandato], [tipo intervento], email,
                 telefono1, telefono2, telefono3, telefono4, telefono5, telefono6, telefono7, telefono8, User_M3, EmailRX1, [scadenza mandato], [seat_importoOrig], posizione, [codice esattore])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.codice_pratica,
            data.codice_cliente,
            data.vocativo,
            data.cognome,
            data.nome,
            data.data_nascita,
            data.ragione_sociale,
            data.indirizzo,
            data.cap,
            data.citta,
            data.provincia,
            data.mandante,
            data.intervento,
            data.email,
            data.telefono1,
            data.telefono2,
            data.telefono3,
            data.telefono4,
            data.telefono5,
            data.telefono6,
            data.telefono7,
            data.telefono8,
            data.user_m3,
            data.EmailRX1,
            data.scadenza_mandato,
            data.seat_importoOrig,
            data.posizione,
            data.esattore,
        ))
        
        # Recupera l'ID generato
        new_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

    # Ricostruisci e restituisci il modello completo
    return Pratica(
        contatore=new_id,
        codice_pratica=data.codice_pratica,
        codice_cliente=data.codice_cliente,
        vocativo=data.vocativo,
        cognome=data.cognome,
        nome=data.nome,
        data_nascita=data.data_nascita,
        ragione_sociale=data.ragione_sociale,
        indirizzo=data.indirizzo,
        cap=data.cap,
        citta=data.citta,
        provincia=data.provincia,
        mandante=data.mandante,
        intervento=data.intervento,
        email=data.email,
        telefono1=data.telefono1,
        telefono2=data.telefono2,
        telefono3=data.telefono3,
        telefono4=data.telefono4,
        telefono5=data.telefono5,
        telefono6=data.telefono6,
        telefono7=data.telefono7,
        telefono8=data.telefono8,
        user_m3=data.user_m3,
        EmailRX1=data.EmailRX1,
        scadenza_mandato=data.scadenza_mandato,
        seat_importoOrig=data.seat_importoOrig,
        posizione=data.posizione,
        esattore=data.esattore,
    )


def update_pratica_status(contatore: int, esito_prioritario: str) -> Pratica:
    """
    Aggiorna il campo EsitoFonia (database) con il valore EsitoPrioritario (API).
    
    Args:
        contatore: ID univoco della pratica
        esito_prioritario: Nuovo valore per EsitoPrioritario (1-3 caratteri)
        
    Returns:
        Pratica: Oggetto pratica aggiornato
        
    Raises:
        HTTPException: 404 se la pratica non esiste
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # Verifica che la pratica esista
        cursor.execute(
            "SELECT COUNT(*) FROM [tabella pratiche] WHERE contatore = ?",
            (contatore,)
        )
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="Pratica non trovata")

        # Aggiorna il campo EsitoFonia (database) con il valore EsitoPrioritario (API)
        cursor.execute(
            "UPDATE [tabella pratiche] SET EsitoFonia = ? WHERE contatore = ?",
            (esito_prioritario, contatore)
        )
        
    # Restituisce la pratica aggiornata
    return fetch_pratica(contatore)