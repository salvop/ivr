from fastapi import APIRouter, Path, Depends

from starlette.concurrency import run_in_threadpool


from app.models.email import EMailResponse, EMailCreate
from app.services.email_service import fetch_email, create_email
from app.config import validate_api_key, api_key_header

router = APIRouter(
    tags=["v1 - Email"],
    responses={404: {"description": "Not found"}}
)



@router.get(
    "/{contatore}",
    response_model=list[EMailResponse],

    summary="Elenca le email di una pratica",
    description=(
        "Restituisce tutte le email associate alla pratica identificata da `contatore`.\n\n"
        "**Endpoint:** `GET /api/v1/email/{contatore}`\n\n"
        "**Parametri:**\n"
        "- `contatore` (int): ID della pratica per cui recuperare le email\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"
        "**Rate Limiting:**\n"
        "- 100 richieste per minuto per IP\n\n"
        "**Risposte:**\n"
        "- `200 OK`: Lista delle email (può essere vuota se non ci sono email)\n"
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
        '    "destinatario": "cliente@email.com",\n'
        '    "oggetto": "Conferma appuntamento",\n'
        '    "stato": "Inviato",\n'
        '    "priorita": "Alta"\n'
        "  },\n"
        "  {\n"
        '    "id": 2,\n'
        '    "contatore": 12345,\n'
        '    "data_invio": "2024-01-20T14:15:00",\n'
        '    "destinatario": "cliente@email.com",\n'
        '    "oggetto": "Follow-up servizio",\n'
        '    "stato": "Letto",\n'
        '    "priorita": "Normale"\n'
        "  }\n"
        "]\n"
        "```"
    ),
    responses={
        200: {"description": "Lista delle email recuperata con successo"},
        404: {"description": "Pratica non trovata"},
        401: {"description": "API key mancante o non valida"},
        429: {"description": "Rate limit superato"}
    }
)
async def list_email(
    contatore: int = Path(..., description="ID della pratica (campo IdPratica)"),
    api_key: str = Depends(api_key_header)
):
    """
    Elenca le email associate alla pratica specificata.
    
    Args:
        contatore: ID della pratica
        api_key: Chiave API per l'autenticazione
        
    Returns:
        list[EMailResponse]: Lista delle email associate alla pratica
        
    Raises:
        HTTPException: 404 se la pratica non esiste, 401 se API key non valida, 429 se rate limit superato
    """
    # Validate API key
    validate_api_key(api_key)
    
    return await run_in_threadpool(fetch_email, contatore)

@router.post(
    "/",
    response_model=EMailResponse,
    status_code=201,

    summary="Crea una nuova email",
    description=(
        "Inserisce una nuova email nel database associata a una pratica esistente.\n\n"
        "**Endpoint:** `POST /api/v1/email/`\n\n"
        "**Campi obbligatori:**\n"
        "- `Agente`: Codice agente\n"
        "- `Data`: Data della email (formato YYYY-MM-DD)\n"
        "- `Ora`: Ora della email (formato HH:MM:SS)\n"
        "- `NomeMittente`: Nome del mittente\n"
        "- `Mittente`: Indirizzo email del mittente\n"
        "- `Destinatario`: Indirizzi destinatari separati da ';'\n"
        "- `Oggetto`: Oggetto dell'email (max 100 caratteri)\n"
        "- `Messaggio`: Testo del messaggio\n"
        "- `IdPratica`: ID della pratica collegata\n\n"
        "**Validazioni:**\n"
        "- La pratica deve esistere nel database\n"
        "- Email del destinatario deve essere in formato valido\n"
        "- Oggetto e corpo non possono essere vuoti\n"
        "- Priorità deve essere uno dei valori consentiti\n"
        "- Data e ora devono essere in formato valido\n\n"
        "**Autenticazione:**\n"
        "- Richiede l'header `X-API-Key` per l'autenticazione\n\n"
        "**Rate Limiting:**\n"
        "- 10 richieste per minuto per IP\n\n"
        "**Risposte:**\n"
        "- `201 Created`: Email creata con successo\n"
        "- `400 Bad Request`: Dati non validi o pratica non esistente\n"
        "- `401 Unauthorized`: API key mancante o non valida\n"
        "- `429 Too Many Requests`: Rate limit superato\n\n"
        "**Esempio di richiesta:**\n"
        "```json\n"
        "{\n"
        '  "Agente": "AG001",\n'
        '  "Data": "2024-01-15",\n'
        '  "Ora": "14:30:00",\n'
        '  "NomeMittente": "FIDES S.p.A.",\n'
        '  "Mittente": "noreply@fides.it",\n'
        '  "Destinatario": "cliente@email.com",\n'
        '  "DestinatarioCC": "supervisor@fides.it",\n'
        '  "Oggetto": "Conferma appuntamento",\n'
        '  "Messaggio": "Gentile cliente, confermiamo il suo appuntamento per il giorno 20 gennaio alle ore 10:00.",\n'
        '  "Allegati": "documento1.pdf,contratto.pdf",\n'
        '  "MailerType": "SMTP",\n'
        '  "Applicativo": "CollectFlow",\n'
        '  "IdPratica": 12345\n'
        "}\n"
        "```"
    ),
    responses={
        201: {"description": "Email creata con successo"},
        400: {"description": "Dati non validi o pratica non esistente"},
        401: {"description": "API key mancante o non valida"},
        429: {"description": "Rate limit superato"}
    }
)
async def add_email(
    m: EMailCreate, 
    api_key: str = Depends(api_key_header)
):
    """
    Crea una nuova email nel database.
    
    Args:
        m: Dati dell'email da creare
        api_key: Chiave API per l'autenticazione
        
    Returns:
        EMailResponse: Oggetto email creato con ID assegnato
        
    Raises:
        HTTPException: 400 se la pratica non esiste o dati non validi, 401 se API key non valida, 429 se rate limit superato
    """
    # Validate API key
    validate_api_key(api_key)
    
    return await run_in_threadpool(create_email, m)