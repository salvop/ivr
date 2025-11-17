"""
Movement API Router
==================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: FastAPI router for movement-related endpoints
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module defines all API endpoints for movement management including
CRUD operations and data validation.
"""

from fastapi import APIRouter, HTTPException, Depends

from typing import List
from starlette.concurrency import run_in_threadpool


from app.services.movimenti_service import fetch_movimenti_by_pratica, create_movimento_entry
from app.models.movimenti import Movimento, MovimentoCreate
from app.config import validate_api_key, api_key_header

router = APIRouter()

@router.get(
    "/{contatore}",
    response_model=List[Movimento],
    tags=["v1 - Movimenti"],

    summary="Elenca i movimenti di una pratica",
    description=(
        "Restituisce tutti i movimenti associati alla pratica identificata dal parametro `contatore`.\n\n"
        "**Endpoint:** `GET /api/v1/movimenti/{contatore}`\n\n"
        "**Parametri:**\n"
        "- `contatore` (int): ID della pratica per cui recuperare i movimenti (deve esistere nel database)\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"
        "**Rate Limiting:**\n"
        "- 100 richieste per minuto per IP\n\n"
        "**Risposte:**\n"
        "- `200 OK`: Lista dei movimenti (può essere vuota se non ci sono movimenti)\n"
        "- `404 Not Found`: Pratica non trovata nel database\n"
        "- `401 Unauthorized`: API key mancante o non valida\n"
        "- `429 Too Many Requests`: Rate limit superato\n\n"
        "**Esempio di risposta:**\n"
        "```json\n"
        "[\n"
        "  {\n"
        '    "id": 1,\n'
        '    "data": "2024-01-15T00:00:00",\n'
        '    "ora": "14:30:00",\n'
        '    "contatore": 12345,\n'
        '    "codagenzia": "AG1",\n'
        '    "codesa": "SA1",\n'
        '    "nomeag": "Mario Rossi",\n'
        '    "esito": "Completato",\n'
        '    "descresito": "Prima visita al cliente",\n'
        '    "flagesito": true,\n'
        '    "note": "Cliente molto collaborativo",\n'
        '    "datapag": "2024-01-16T00:00:00",\n'
        '    "importopag": 1500.50,\n'
        '    "orarecall": "2024-01-17T10:00:00",\n'
        '    "tel1": "+39 333 1234567"\n'
        "  },\n"
        "  {\n"
        '    "id": 2,\n'
        '    "data": "2024-01-20T00:00:00",\n'
        '    "ora": "10:15:00",\n'
        '    "contatore": 12345,\n'
        '    "codagenzia": "AG1",\n'
        '    "codesa": "SA2",\n'
        '    "nomeag": "Mario Rossi",\n'
        '    "esito": "In corso",\n'
        '    "descresito": "Follow-up telefonico",\n'
        '    "flagesito": false,\n'
        '    "note": null,\n'
        '    "datapag": null,\n'
        '    "importopag": null,\n'
        '    "orarecall": null,\n'
        '    "tel1": null\n'
        "  }\n"
        "]\n"
        "```"
    ),
    responses={
        200: {"description": "Lista dei movimenti recuperata con successo"},
        404: {"description": "Pratica non trovata"},
        401: {"description": "API key mancante o non valida"},
        429: {"description": "Rate limit superato"}
    }
)
async def get_movimenti(
    contatore: int, 
    api_key: str = Depends(api_key_header)
):
    """
    Elenca i movimenti per la pratica specificata.
    
    Args:
        request: FastAPI request object
        contatore: ID della pratica
        api_key: Chiave API per l'autenticazione
        
    Returns:
        List[Movimento]: Lista dei movimenti associati alla pratica
        
    Raises:
        HTTPException: 404 se la pratica non esiste, 401 se API key non valida, 429 se rate limit superato
    """
    # Validate API key
    validate_api_key(api_key)
    
    movs = await run_in_threadpool(fetch_movimenti_by_pratica, contatore)
    return movs

@router.post(
    "/",
    response_model=Movimento,
    status_code=201,
    tags=["v1 - Movimenti"],

    summary="Crea un nuovo movimento",
    description=(
        "Inserisce un record nella tabella `Movimenti` associato a una pratica esistente.\n\n"
        "**Endpoint:** `POST /api/v1/movimenti/`\n\n"
        "**Campi obbligatori:**\n"
        "- `data`: Data del movimento (formato YYYY-MM-DD)\n"
        "- `ora`: Ora del movimento (formato HH:MM:SS)\n"
        "- `contatore`: ID della pratica esistente (deve esistere nel database)\n"
        "- `codesa`: Codice SA (max 3 caratteri, obbligatorio)\n"
        "- `nomeag`: Nome agente\n"
        "- `esito`: Esito dell'operazione\n"
        "- `descresito`: Descrizione esito\n"
        "- `flagesito`: Flag esito (boolean)\n\n"
        "**Campi opzionali:**\n"
        "- `codagenzia`: Codice agenzia (max 3 caratteri, opzionale)\n"
        "- `note`: Note aggiuntive del movimento (opzionale)\n"
        "- `datapag`: Data del pagamento (opzionale)\n"
        "- `importopag`: Importo del pagamento (opzionale)\n"
        "- `orarecall`: Ora di recall (opzionale)\n"
        "- `tel1`: Numero di telefono 1 (opzionale, max 20 caratteri)\n\n"
        "**Nota:** Il campo `id` non deve essere incluso nella richiesta poiché viene auto-generato dal database.\n\n"
        "**Validazioni:**\n"
        "- La pratica (`contatore`) deve esistere nel database\n"
        "- Data e ora devono essere in formato valido\n"
        "- `codesa` deve essere massimo 3 caratteri (obbligatorio)\n"
        "- `codagenzia` deve essere massimo 3 caratteri (se fornito, opzionale)\n"
        "- Descrizione non può essere vuota\n"
        "- Esito non può essere vuoto\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"
        "**Rate Limiting:**\n"
        "- 10 richieste per minuto per IP\n\n"
        "**Risposte:**\n"
        "- `201 Created`: Movimento creato con successo\n"
        "- `400 Bad Request`: Dati non validi o pratica non esistente\n"
        "- `401 Unauthorized`: API key mancante o non valida\n"
        "- `429 Too Many Requests`: Rate limit superato\n\n"
        "**Esempio di richiesta:**\n"
        "```json\n"
        "{\n"
        '  "data": "2024-01-25T00:00:00",\n'
        '  "ora": "15:45:00",\n'
        '  "contatore": 12345,\n'
        '  "codagenzia": "AG1",\n'
        '  "codesa": "SA1",\n'
        '  "nomeag": "Mario Rossi",\n'
        '  "esito": "Completato",\n'
        '  "descresito": "Visita di controllo completata",\n'
        '  "flagesito": true,\n'
        '  "note": "Cliente ha confermato il pagamento",\n'
        '  "datapag": "2024-01-26T00:00:00",\n'
        '  "importopag": 2500.75,\n'
        '  "orarecall": "2024-01-27T14:30:00",\n'
        '  "tel1": "+39 333 9876543"\n'
        "}\n"
        "```"
    ),
    responses={
        201: {"description": "Movimento creato con successo"},
        400: {"description": "Dati non validi, pratica non esistente, o codici troppo lunghi"},
        401: {"description": "API key mancante o non valida"},
        429: {"description": "Rate limit superato"}
    }
)
async def post_movimento(
    mov: MovimentoCreate, 
    api_key: str = Depends(api_key_header)
):
    """
    Crea un nuovo movimento nel database.
    
    Args:
        mov: Dati del movimento da creare (senza campo ID)
        api_key: Chiave API per l'autenticazione
        
    Returns:
        Movimento: Oggetto movimento creato con ID auto-generato dal database
        
    Raises:
        HTTPException: 400 se la pratica non esiste o dati non validi, 401 se API key non valida, 429 se rate limit superato
    """
    # Validate API key
    validate_api_key(api_key)
    
    created = await run_in_threadpool(create_movimento_entry, mov)
    return created