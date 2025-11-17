"""
SMS API Router
=============

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: FastAPI router for SMS-related endpoints
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module defines all API endpoints for SMS management including
CRUD operations and data validation.
"""

from fastapi import APIRouter, Path, Depends

from starlette.concurrency import run_in_threadpool


from app.models.sms import SMSResponse, SMSCreate
from app.services.sms_service import fetch_sms, create_sms
from app.config import validate_api_key, api_key_header

router = APIRouter(
    tags=["v1 - SMS"],
    responses={404: {"description": "Not found"}}
)



@router.get(
    "/{contatore}",
    response_model=list[SMSResponse],

    summary="Elenca gli SMS di una pratica",
    description=(
        "Restituisce tutti gli SMS associati alla pratica identificata da `contatore`.\n\n"
        "**Endpoint:** `GET /api/v1/sms/{contatore}`\n\n"
        "**Parametri:**\n"
        "- `contatore` (int): ID della pratica per cui recuperare gli SMS\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"
        "**Rate Limiting:**\n"
        "- 100 richieste per minuto per IP\n\n"
        "**Risposte:**\n"
        "- `200 OK`: Lista degli SMS (può essere vuota se non ci sono SMS)\n"
        "- `404 Not Found`: Pratica non trovata nel database\n"
        "- `401 Unauthorized`: API key mancante o non valida\n"
        "- `429 Too Many Requests`: Rate limit superato\n\n"
        "**Esempio di risposta:**\n"
        "```json\n"
        "[\n"
        "  {\n"
        '    "id": 1,\n'
        '    "contatore": 12345,\n'
        '    "data_invio": "2024-01-15T10:30:00",\n'
        '    "numero_destinatario": "+393331234567",\n'
        '    "messaggio": "Conferma appuntamento alle 15:00",\n'
        '    "stato": "Inviato",\n'
        '    "priorita": "Alta"\n'
        "  },\n"
        "  {\n"
        '    "id": 2,\n'
        '    "contatore": 12345,\n'
        '    "data_invio": "2024-01-20T14:15:00",\n'
        '    "numero_destinatario": "+393331234567",\n'
        '    "messaggio": "Promemoria: appuntamento domani",\n'
        '    "stato": "Consegnato",\n'
        '    "priorita": "Normale"\n'
        "  }\n"
        "]\n"
        "```"
    ),
    responses={
        200: {"description": "Lista degli SMS recuperata con successo"},
        404: {"description": "Pratica non trovata"},
        401: {"description": "API key mancante o non valida"},
        429: {"description": "Rate limit superato"}
    }
)
async def list_sms(
    contatore: int = Path(..., description="ID della pratica (campo IdPratica)"),
    api_key: str = Depends(api_key_header)
):
    """
    Elenca gli SMS associati alla pratica specificata.
    
    Args:
        request: FastAPI request object
        contatore: ID della pratica
        api_key: Chiave API per l'autenticazione
        
    Returns:
        list[SMSResponse]: Lista degli SMS associati alla pratica
        
    Raises:
        HTTPException: 404 se la pratica non esiste, 401 se API key non valida, 429 se rate limit superato
    """
    # Validate API key
    validate_api_key(api_key)
    
    return await run_in_threadpool(fetch_sms, contatore)

@router.post(
    "/",
    response_model=SMSResponse,
    status_code=201,

    summary="Crea un nuovo SMS",
    description=(
        "Inserisce un nuovo SMS nel database associato a una pratica esistente.\n\n"
        "**Endpoint:** `POST /api/v1/sms/`\n\n"
        "**Campi obbligatori:**\n"
        "- `Data`: Data dell'SMS (formato YYYY-MM-DD)\n"
        "- `Ora`: Ora dell'SMS (formato HH:MM:SS)\n"
        "- `Testo`: Testo del messaggio SMS\n"
        "- `IdPratica`: ID della pratica collegata\n\n"
        "**Validazioni:**\n"
        "- La pratica deve esistere nel database\n"
        "- Numero di telefono deve essere in formato valido\n"
        "- Messaggio non può essere vuoto e deve rispettare i limiti di lunghezza\n"
        "- Priorità deve essere uno dei valori consentiti\n"
        "- Data e ora devono essere in formato valido\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"
        "**Rate Limiting:**\n"
        "- 10 richieste per minuto per IP\n\n"
        "**Risposte:**\n"
        "- `201 Created`: SMS creato con successo\n"
        "- `400 Bad Request`: Dati non validi o pratica non esistente\n"
        "- `401 Unauthorized`: API key mancante o non valida\n"
        "- `429 Too Many Requests`: Rate limit superato\n\n"
        "**Esempio di richiesta:**\n"
        "```json\n"
        "{\n"
        '  "Data": "2024-01-15",\n'
        '  "Ora": "14:30:00",\n'
        '  "CodAg": "AG1",\n'
        '  "Mittente": "FIDES",\n'
        '  "Destinatario": "Mario Rossi",\n'
        '  "NrTel": "+39 333 1234567",\n'
        '  "Testo": "Gentile cliente, le ricordiamo l\'appuntamento di domani alle 10:00.",\n'
        '  "IdSpedizione": "SMS001",\n'
        '  "Stato": "Inviato",\n'
        '  "FlagAuto": false,\n'
        '  "IdPratica": 12345,\n'
        '  "FlagDaSpedire": false,\n'
        '  "DataSpedizione": "2024-01-15",\n'
        '  "Fornitore": "TIM",\n'
        '  "Applicazione": "CollectFlow",\n'
        '  "Interno": false\n'
        "}\n"
        "```"
    ),
    responses={
        201: {"description": "SMS creato con successo"},
        400: {"description": "Dati non validi o pratica non esistente"},
        401: {"description": "API key mancante o non valida"},
        429: {"description": "Rate limit superato"}
    }
)
async def add_sms(
    s: SMSCreate, 
    api_key: str = Depends(api_key_header)
):
    """
    Crea un nuovo SMS nel database.
    
    Args:
        request: FastAPI request object
        s: Dati dell'SMS da creare
        api_key: Chiave API per l'autenticazione
        
    Returns:
        SMSResponse: Oggetto SMS creato con ID assegnato
        
    Raises:
        HTTPException: 400 se la pratica non esiste o dati non validi, 401 se API key non valida, 429 se rate limit superato
    """
    # Validate API key
    validate_api_key(api_key)
    
    return await run_in_threadpool(create_sms, s)