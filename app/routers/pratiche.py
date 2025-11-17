"""
Practice API Router
==================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: FastAPI router for practice-related endpoints
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module defines all API endpoints for practice management including
CRUD operations, status updates, and data validation.
"""

from fastapi import APIRouter, Depends

from fastapi import HTTPException
from starlette.concurrency import run_in_threadpool


from app.services.pratiche_service import fetch_pratica, create_pratica, update_pratica_status
from app.models.pratiche import Pratica, PraticaCreate, PraticaUpdateStatus
from app.config import validate_api_key, api_key_header

router = APIRouter()

@router.get(
    "/{contatore}",
    response_model=Pratica,
    tags=["v1 - Pratiche"],

    summary="Recupera i dettagli di una pratica",
    description=(
        "Restituisce tutti i campi della pratica identificata dal parametro `contatore`.\n\n"
        "**Endpoint:** `GET /api/v1/pratiche/{contatore}`\n\n"
        "**Parametri:**\n"
        "- `contatore` (int): ID univoco della pratica nel sistema\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"

        "**Risposte:**\n"
        "- `200 OK`: Pratica trovata e restituita con successo\n"
        "- `404 Not Found`: Pratica non trovata nel database\n"
        "- `401 Unauthorized`: API key mancante o non valida\n"

        "**Esempio di risposta:**\n"
        "```json\n"
        "{\n"
        '  "contatore": 12345,\n'
        '  "codice_pratica": "PRAT-2024-001",\n'
        '  "codice_cliente": "CLI-001",\n'
        '  "vocativo": "Sig.",\n'
        '  "cognome": "Rossi",\n'
        '  "nome": "Mario",\n'
        '  "data_nascita": "1980-05-15",\n'
        '  "ragione_sociale": null,\n'
        '  "indirizzo": "Via Roma 123",\n'
        '  "cap": "20100",\n'
        '  "citta": "Milano",\n'
        '  "provincia": "MI",\n'
        '  "mandante": "Banca XYZ",\n'
        '  "intervento": "Recupero crediti",\n'
        '  "email": "mario.rossi@email.com",\n'
        '  "telefono1": "+39 333 1234567",\n'
        '  "telefono2": null,\n'
        '  "telefono3": null,\n'
        '  "telefono4": null,\n'
        '  "telefono5": null,\n'
        '  "telefono6": null,\n'
        '  "telefono7": null,\n'
        '  "telefono8": null,\n'
        '  "user_m3": 1500.50,\n'
        '  "EmailRX1": "tracking@fides.it",\n'
        '  "EsitoPrioritario": "PRO",\n'
        '  "scadenza_mandato": "2024-12-31T00:00:00",\n'
        '  "seat_importoOrig": 5000.00,\n'
        '  "posizione": "AGENTE_001",\n'
        '  "esattore": "001"\n'
        "}\n"
        "```"
    ),
    responses={
        200: {"description": "Pratica trovata con successo"},
        404: {"description": "Pratica non trovata"},
        401: {"description": "API key mancante o non valida"},
        429: {"description": "Rate limit superato"}
    }
)
async def get_pratica(
    contatore: int, 
    api_key: str = Depends(api_key_header)
):
    """
    Recupera la pratica con il contatore specificato.
    
    Args:
        contatore: ID univoco della pratica
        api_key: Chiave API per l'autenticazione
        
    Returns:
        Pratica: Oggetto pratica con tutti i dettagli
        
    Raises:
        HTTPException: 404 se la pratica non esiste, 401 se API key non valida
    """
    # Validate API key
    validate_api_key(api_key)
    
    pratica = await run_in_threadpool(fetch_pratica, contatore)
    return pratica

@router.post(
    "/",
    response_model=Pratica,
    status_code=201,
    tags=["v1 - Pratiche"],

    summary="Crea una nuova pratica",
    description=(
        "Crea una nuova riga nella tabella `tabella pratiche` con i dati forniti.\n\n"
        "**Endpoint:** `POST /api/v1/pratiche/`\n\n"
        "**Campi obbligatori:**\n"
        "- `codice_pratica`: Codice univoco della pratica (1-50 caratteri, solo lettere maiuscole, numeri, trattini e underscore)\n"
        "- `codice_cliente`: Codice del cliente (1-50 caratteri, solo lettere maiuscole, numeri, trattini e underscore)\n\n"
        "**Validazioni:**\n"
        "- Email deve essere in formato valido\n"
        "- CAP deve essere di 5 cifre\n"
        "- Provincia deve essere di 2 caratteri\n"
        "- `user_m3` deve essere >= 0\n"
        "- Numeri di telefono devono essere validi\n"
        "- Nomi e cognomi solo lettere valide\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"

        "**Risposte:**\n"
        "- `201 Created`: Pratica creata con successo\n"
        "- `400 Bad Request`: Dati non validi o codice pratica duplicato\n"
        "- `401 Unauthorized`: API key mancante o non valida\n"

        "**Esempio di richiesta:**\n"
        "```json\n"
        "{\n"
        '  "codice_pratica": "PRAT-2024-002",\n'
        '  "codice_cliente": "CLI-002",\n'
        '  "vocativo": "Sig.ra",\n'
        '  "cognome": "Bianchi",\n'
        '  "nome": "Anna",\n'
        '  "data_nascita": "1975-03-20",\n'
        '  "ragione_sociale": null,\n'
        '  "indirizzo": "Via Garibaldi 45",\n'
        '  "cap": "20121",\n'
        '  "citta": "Milano",\n'
        '  "provincia": "MI",\n'
        '  "mandante": "Banca ABC",\n'
        '  "intervento": "Gestione debiti",\n'
        '  "email": "anna.bianchi@email.com",\n'
        '  "telefono1": "+39 333 1234567",\n'
        '  "telefono2": "+39 02 1234567",\n'
        '  "user_m3": 2500.75,\n'
        '  "EmailRX1": "tracking@fides.it",\n'
        '  "scadenza_mandato": "2024-12-31T00:00:00",\n'
        '  "seat_importoOrig": 7500.25,\n'
        '  "posizione": "AGENTE_002",\n'
        '  "esattore": "002"\n'
        "}\n"
        "```"
    ),
    responses={
        201: {"description": "Pratica creata con successo"},
        400: {"description": "Dati non validi o codice pratica duplicato"},
        401: {"description": "API key mancante o non valida"},
        429: {"description": "Rate limit superato"}
    }
)
async def post_pratica(
    pratica: PraticaCreate, 
    api_key: str = Depends(api_key_header)
):
    """
    Crea una nuova pratica nel database.
    
    Args:
        pratica: Dati della pratica da creare
        api_key: Chiave API per l'autenticazione
        
    Returns:
        Pratica: Oggetto pratica creato con ID assegnato
        
    Raises:
        HTTPException: 400 se codice pratica duplicato o dati non validi, 401 se API key non valida
    """
    # Validate API key
    validate_api_key(api_key)
    
    created = await run_in_threadpool(create_pratica, pratica)
    return created


@router.patch(
    "/{contatore}/status",
    response_model=Pratica,
    tags=["v1 - Pratiche"],

    summary="Aggiorna lo status di una pratica",
    description=(
        "Aggiorna il campo `EsitoPrioritario` (API) che mappa sul campo `EsitoFonia` (database) di una pratica esistente.\n\n"
        "**Endpoint:** `PATCH /api/v1/pratiche/{contatore}/status`\n\n"
        "**Parametri:**\n"
        "- `contatore` (int): ID univoco della pratica nel sistema\n\n"
        "**Campi obbligatori:**\n"
        "- `EsitoPrioritario` (string): Esito Prioritario (1-3 caratteri, non vuoto)\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"

        "**Risposte:**\n"
        "- `200 OK`: Status aggiornato con successo\n"
        "- `404 Not Found`: Pratica non trovata nel database\n"
        "- `400 Bad Request`: Dati non validi\n"
        "- `401 Unauthorized`: API key mancante o non valida\n"

        "**Esempio di richiesta:**\n"
        "```json\n"
        "{\n"
        '  "EsitoPrioritario": "PRO"\n'
        "}\n"
        "```\n\n"
        "**Esempi di valori validi:**\n"
        "- `\"PRO\"` - Promessa Pagamento\n"
        "- `\"210\"` - Già Pagato\n"

    ),
    responses={
        200: {"description": "Status aggiornato con successo"},
        404: {"description": "Pratica non trovata"},
        400: {"description": "Dati non validi"},
        401: {"description": "API key mancante o non valida"}
    }
)
async def patch_pratica_status(
    contatore: int,
    status_update: PraticaUpdateStatus,
    api_key: str = Depends(api_key_header)
):
    """
    Aggiorna lo status di una pratica.
    
    Args:
        contatore: ID univoco della pratica
        status_update: Dati per l'aggiornamento dello status
        api_key: Chiave API per l'autenticazione
        
    Returns:
        Pratica: Oggetto pratica aggiornato
        
    Raises:
        HTTPException: 404 se la pratica non esiste, 400 se dati non validi, 401 se API key non valida
    """
    # Validate API key
    validate_api_key(api_key)
    
    updated = await run_in_threadpool(update_pratica_status, contatore, status_update.EsitoPrioritario)
    return updated