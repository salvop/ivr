# CollectFlowAPI - Complete Documentation

**Author:** Salvatore Privitera  
**Company:** FIDES S.p.A.  
**Version:** 1.0.0  
**License:** Proprietary - FIDES S.p.A.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL & Endpoints](#base-url--endpoints)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [API Endpoints](#api-endpoints)
   - [Pratiche (Practices)](#pratiche-practices)
   - [Movimenti (Movements)](#movimenti-movements)
   - [Email](#email)
   - [SMS](#sms)
7. [Data Models](#data-models)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

CollectFlowAPI is a comprehensive REST API for managing debt collection practices, including movements, email communications, and SMS notifications. The API provides secure, scalable endpoints for all aspects of practice management.

### Key Features
- **Secure Authentication**: API key-based authentication
- **Comprehensive CRUD Operations**: Full lifecycle management
- **Real-time Validation**: Input validation and business rule enforcement
- **Performance Monitoring**: Built-in request/response logging
- **Scalable Architecture**: Connection pooling and efficient resource management

---

## 🔐 Authentication

All API endpoints require authentication using an API key.

### Header
```
X-API-Key: your_api_key_here
```

### Authentication Flow
1. Include your API key in the `X-API-Key` header
2. The API validates the key against configured valid keys
3. If valid, the request proceeds; if invalid, returns `401 Unauthorized`

### Error Responses
- `401 Unauthorized`: Missing or invalid API key
- `401 Unauthorized`: API keys not configured (server error)

---

## 🌐 Base URL & Endpoints

### Base URL
```
http://localhost:8000
```

### API Versioning
All endpoints are versioned under `/api/v1/`:
- Current version: `v1`
- All endpoints: `/api/v1/{resource}`

### Available Resources
- **Pratiche**: `/api/v1/pratiche`
- **Movimenti**: `/api/v1/movimenti`
- **Email**: `/api/v1/email`
- **SMS**: `/api/v1/sms`

---

## ⚠️ Error Handling

### Standard Error Response Format
```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Common Error Scenarios
- **Invalid API Key**: `401 Unauthorized`
- **Missing Required Fields**: `400 Bad Request`
- **Pratica Not Found**: `404 Not Found`
- **Validation Errors**: `400 Bad Request`
- **Rate Limit Exceeded**: `429 Too Many Requests`

---

## 🚦 Rate Limiting

### Limits
- **Default**: 100 requests per minute per IP
- **POST Operations**: 10 requests per minute per IP

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

### Rate Limit Exceeded Response
```json
{
  "detail": "Rate limit exceeded: 100 per 1 minute"
}
```

---

## 📚 API Endpoints

### Pratiche (Practices)

Practice management endpoints for debt collection cases.

#### GET `/api/v1/pratiche/{contatore}`

Retrieve a specific practice by its unique identifier.

**Parameters:**
- `contatore` (integer, required): Unique practice identifier

**Response:**
```json
{
  "contatore": 12345,
  "codice_pratica": "PRAT-2024-001",
  "codice_cliente": "CLI-001",
  "vocativo": "Sig.",
  "cognome": "Rossi",
  "nome": "Mario",
  "ragione_sociale": null,
  "indirizzo": "Via Roma 123",
  "cap": "20100",
  "citta": "Milano",
  "provincia": "MI",
  "mandante": "Banca XYZ",
  "intervento": "Recupero crediti",
  "email": "mario.rossi@email.com",
  "telefono1": "+39 333 1234567",
  "telefono2": null,
  "telefono3": null,
  "telefono4": null,
  "telefono5": null,
  "telefono6": null,
  "telefono7": null,
  "telefono8": null,
  "user_m3": 1500.50,
  "EmailRX1": "tracking@fides.it",
  "EsitoPrioritario": "PRO"
}
```

**Error Responses:**
- `404 Not Found`: Practice not found
- `401 Unauthorized`: Invalid API key

---

#### POST `/api/v1/pratiche/`

Create a new practice.

**Request Body:**
```json
{
  "codice_pratica": "PRAT-2024-002",
  "codice_cliente": "CLI-002",
  "vocativo": "Sig.ra",
  "cognome": "Bianchi",
  "nome": "Anna",
  "ragione_sociale": null,
  "indirizzo": "Via Milano 456",
  "cap": "20123",
  "citta": "Milano",
  "provincia": "MI",
  "mandante": "Banca ABC",
  "intervento": "Recupero crediti",
  "email": "anna.bianchi@email.com",
  "telefono1": "+39 333 9876543",
  "user_m3": 2500.00,
  "EmailRX1": "tracking@fides.it"
}
```

**Required Fields:**
- `codice_pratica`: Practice code (1-50 characters)
- `codice_cliente`: Client code (1-50 characters)

**Validation Rules:**
- `codice_pratica` and `codice_cliente`: Only uppercase letters, numbers, hyphens, underscores
- `cap`: Exactly 5 digits
- `provincia`: Exactly 2 uppercase letters
- `email`: Valid email format
- `telefono1-8`: Valid Italian phone number format
- `user_m3`: Non-negative number

**Response:**
```json
{
  "contatore": 12346,
  "codice_pratica": "PRAT-2024-002",
  "codice_cliente": "CLI-002",
  "vocativo": "Sig.ra",
  "cognome": "Bianchi",
  "nome": "Anna",
  "ragione_sociale": null,
  "indirizzo": "Via Milano 456",
  "cap": "20123",
  "citta": "Milano",
  "provincia": "MI",
  "mandante": "Banca ABC",
  "intervento": "Recupero crediti",
  "email": "anna.bianchi@email.com",
  "telefono1": "+39 333 9876543",
  "telefono2": null,
  "telefono3": null,
  "telefono4": null,
  "telefono5": null,
  "telefono6": null,
  "telefono7": null,
  "telefono8": null,
  "user_m3": 2500.00,
  "EmailRX1": "tracking@fides.it",
  "EsitoPrioritario": null
}
```

**Error Responses:**
- `400 Bad Request`: Validation errors or duplicate practice code
- `401 Unauthorized`: Invalid API key

---

#### PATCH `/api/v1/pratiche/{contatore}/status`

Update the priority outcome status of a practice.

**Parameters:**
- `contatore` (integer, required): Unique practice identifier

**Request Body:**
```json
{
  "EsitoPrioritario": "PRO"
}
```

**Validation Rules:**
- `EsitoPrioritario`: 1-3 characters, not empty
- Valid values: "PRO", "210", "220", etc.

**Response:**
```json
{
  "contatore": 12345,
  "codice_pratica": "PRAT-2024-001",
  "codice_cliente": "CLI-001",
  "vocativo": "Sig.",
  "cognome": "Rossi",
  "nome": "Mario",
  "ragione_sociale": null,
  "indirizzo": "Via Roma 123",
  "cap": "20100",
  "citta": "Milano",
  "provincia": "MI",
  "mandante": "Banca XYZ",
  "intervento": "Recupero crediti",
  "email": "mario.rossi@email.com",
  "telefono1": "+39 333 1234567",
  "telefono2": null,
  "telefono3": null,
  "telefono4": null,
  "telefono5": null,
  "telefono6": null,
  "telefono7": null,
  "telefono8": null,
  "user_m3": 1500.50,
  "EmailRX1": "tracking@fides.it",
  "EsitoPrioritario": "PRO"
}
```

**Error Responses:**
- `404 Not Found`: Practice not found
- `400 Bad Request`: Invalid status value
- `401 Unauthorized`: Invalid API key

---

### Movimenti (Movements)

Movement tracking endpoints for practice activities.

#### GET `/api/v1/movimenti/{contatore}`

Retrieve all movements for a specific practice.

**Parameters:**
- `contatore` (integer, required): Practice identifier (must exist)

**Response:**
```json
[
  {
    "id": 1,
    "data": "2024-01-15T00:00:00",
    "ora": "14:30:00",
    "contatore": 12345,
    "codagenzia": "AG1",
    "codesa": "SA1",
    "nomeag": "Mario Rossi",
    "esito": "Completato",
    "descresito": "Prima visita al cliente",
    "flagesito": true
  },
  {
    "id": 2,
    "data": "2024-01-20T00:00:00",
    "ora": "10:15:00",
    "contatore": 12345,
    "codagenzia": "AG1",
    "codesa": "SA2",
    "nomeag": "Mario Rossi",
    "esito": "In corso",
    "descresito": "Follow-up telefonico",
    "flagesito": false
  }
]
```

**Error Responses:**
- `404 Not Found`: Practice not found
- `401 Unauthorized`: Invalid API key

---

#### POST `/api/v1/movimenti/`

Create a new movement for a practice.

**Request Body:**
```json
{
  "data": "2024-01-25T00:00:00",
  "ora": "15:45:00",
  "contatore": 12345,
  "codagenzia": "AG1",
  "codesa": "SA1",
  "nomeag": "Mario Rossi",
  "esito": "Completato",
  "descresito": "Visita di controllo completata",
  "flagesito": true
}
```

**Required Fields:**
- `data`: Movement date (YYYY-MM-DD format)
- `ora`: Movement time (HH:MM:SS format)
- `contatore`: Practice ID (must exist)
- `codesa`: SA code (max 3 characters)
- `nomeag`: Agent name
- `esito`: Outcome
- `descresito`: Outcome description
- `flagesito`: Outcome flag (boolean)

**Optional Fields:**
- `codagenzia`: Agency code (max 3 characters)

**Validation Rules:**
- `codesa`: Maximum 3 characters (required)
- `codagenzia`: Maximum 3 characters (optional)
- `contatore`: Must reference existing practice
- `data` and `ora`: Valid date/time format

**Response:**
```json
{
  "id": 3,
  "data": "2024-01-25T00:00:00",
  "ora": "15:45:00",
  "contatore": 12345,
  "codagenzia": "AG1",
  "codesa": "SA1",
  "nomeag": "Mario Rossi",
  "esito": "Completato",
  "descresito": "Visita di controllo completata",
  "flagesito": true
}
```

**Error Responses:**
- `400 Bad Request`: Validation errors or practice not found
- `401 Unauthorized`: Invalid API key

---

### Email

Email communication management endpoints.

#### GET `/api/v1/email/{contatore}`

Retrieve all emails for a specific practice.

**Parameters:**
- `contatore` (integer, required): Practice identifier (must exist)

**Response:**
```json
[
  {
    "IdEMail": 1,
    "Agente": "AG001",
    "Data": "2024-01-15",
    "Ora": "10:30:00",
    "NomeMittente": "FIDES S.p.A.",
    "Mittente": "noreply@fides.it",
    "Destinatario": "cliente@email.com",
    "DestinatarioCC": null,
    "Oggetto": "Conferma appuntamento",
    "Messaggio": "Gentile cliente, confermiamo l'appuntamento...",
    "Allegati": null,
    "MailerType": "SMTP",
    "IdMessage": "MSG001",
    "IdResponse": null,
    "Response": null,
    "Error": null,
    "Applicativo": "CollectFlow",
    "IdPratica": 12345
  }
]
```

**Error Responses:**
- `404 Not Found`: Practice not found
- `401 Unauthorized`: Invalid API key

---

#### POST `/api/v1/email/`

Create a new email record.

**Request Body:**
```json
{
  "Agente": "AG001",
  "Data": "2024-01-25",
  "Ora": "14:15:00",
  "NomeMittente": "FIDES S.p.A.",
  "Mittente": "noreply@fides.it",
  "Destinatario": "cliente@email.com",
  "DestinatarioCC": "supervisor@fides.it",
  "Oggetto": "Promemoria pagamento",
  "Messaggio": "Gentile cliente, le ricordiamo il pagamento...",
  "Allegati": "documento.pdf,ricevuta.pdf",
  "MailerType": "SMTP",
  "IdMessage": "MSG002",
  "IdResponse": null,
  "Response": null,
  "Error": null,
  "Applicativo": "CollectFlow",
  "IdPratica": 12345
}
```

**Required Fields:**
- `Agente`: Agent code
- `Data`: Email date (YYYY-MM-DD format)
- `Ora`: Email time (HH:MM:SS format)
- `NomeMittente`: Sender name
- `Mittente`: Sender email
- `Destinatario`: Recipient email(s) (separated by ';')
- `Oggetto`: Email subject (max 100 characters)
- `Messaggio`: Email content
- `IdPratica`: Practice ID

**Optional Fields:**
- `DestinatarioCC`: CC recipients (separated by ';')
- `Allegati`: Attachment names (separated by comma)
- `MailerType`: Email system type
- `IdMessage`: External message ID
- `IdResponse`: External response ID
- `Response`: Server response
- `Error`: Error message
- `Applicativo`: Application name

**Response:**
```json
{
  "IdEMail": 2,
  "Agente": "AG001",
  "Data": "2024-01-25",
  "Ora": "14:15:00",
  "NomeMittente": "FIDES S.p.A.",
  "Mittente": "noreply@fides.it",
  "Destinatario": "cliente@email.com",
  "DestinatarioCC": "supervisor@fides.it",
  "Oggetto": "Promemoria pagamento",
  "Messaggio": "Gentile cliente, le ricordiamo il pagamento...",
  "Allegati": "documento.pdf,ricevuta.pdf",
  "MailerType": "SMTP",
  "IdMessage": "MSG002",
  "IdResponse": null,
  "Response": null,
  "Error": null,
  "Applicativo": "CollectFlow",
  "IdPratica": 12345
}
```

**Error Responses:**
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Invalid API key

---

### SMS

SMS communication management endpoints.

#### GET `/api/v1/sms/{contatore}`

Retrieve all SMS messages for a specific practice.

**Parameters:**
- `contatore` (integer, required): Practice identifier (must exist)

**Response:**
```json
[
  {
    "Id": 1,
    "Data": "2024-01-15",
    "Ora": "10:30:00",
    "CodAg": "AG1",
    "Mittente": "FIDES",
    "Destinatario": "Cliente",
    "NrTel": "+393331234567",
    "Testo": "Gentile cliente, confermiamo l'appuntamento alle 15:00",
    "IdSpedizione": "SMS001",
    "Stato": "Inviato",
    "FlagAuto": true,
    "IdPratica": 12345,
    "FlagDaSpedire": false,
    "DataSpedizione": "2024-01-15",
    "Fornitore": "Twilio",
    "Applicazione": "CollectFlow",
    "Interno": false,
    "IdTestoSMS": 1,
    "NrSMS": 1
  }
]
```

**Error Responses:**
- `404 Not Found`: Practice not found
- `401 Unauthorized`: Invalid API key

---

#### POST `/api/v1/sms/`

Create a new SMS record.

**Request Body:**
```json
{
  "Data": "2024-01-25",
  "Ora": "14:15:00",
  "CodAg": "AG1",
  "Mittente": "FIDES",
  "Destinatario": "Cliente",
  "NrTel": "+393331234567",
  "Testo": "Gentile cliente, le ricordiamo il pagamento scaduto",
  "IdSpedizione": "SMS002",
  "Stato": "Da inviare",
  "FlagAuto": false,
  "IdPratica": 12345,
  "FlagDaSpedire": true,
  "DataSpedizione": "2024-01-25",
  "Fornitore": "Twilio",
  "Applicazione": "CollectFlow",
  "Interno": false,
  "IdTestoSMS": 2
}
```

**Required Fields:**
- `Data`: SMS date (YYYY-MM-DD format)
- `Ora`: SMS time (HH:MM:SS format)
- `Testo`: SMS message content
- `IdPratica`: Practice ID

**Optional Fields:**
- `CodAg`: Agent code (max 3 characters)
- `Mittente`: Sender name
- `Destinatario`: Recipient name
- `NrTel`: Phone number
- `IdSpedizione`: External shipment ID
- `Stato`: SMS status
- `FlagAuto`: Automatic flag (boolean)
- `FlagDaSpedire`: To be sent flag (boolean)
- `DataSpedizione`: Scheduled date
- `Fornitore`: SMS provider
- `Applicazione`: Application name
- `Interno`: Internal flag (boolean)
- `IdTestoSMS`: SMS template ID

**Response:**
```json
{
  "Id": 2,
  "Data": "2024-01-25",
  "Ora": "14:15:00",
  "CodAg": "AG1",
  "Mittente": "FIDES",
  "Destinatario": "Cliente",
  "NrTel": "+393331234567",
  "Testo": "Gentile cliente, le ricordiamo il pagamento scaduto",
  "IdSpedizione": "SMS002",
  "Stato": "Da inviare",
  "FlagAuto": false,
  "IdPratica": 12345,
  "FlagDaSpedire": true,
  "DataSpedizione": "2024-01-25",
  "Fornitore": "Twilio",
  "Applicazione": "CollectFlow",
  "Interno": false,
  "IdTestoSMS": 2,
  "NrSMS": 1
}
```

**Error Responses:**
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Invalid API key

---

## 📊 Data Models

### Pratica (Practice)
```json
{
  "contatore": "integer (auto-generated)",
  "codice_pratica": "string (1-50 chars, required)",
  "codice_cliente": "string (1-50 chars, required)",
  "vocativo": "string (max 10 chars, optional)",
  "cognome": "string (max 50 chars, optional)",
  "nome": "string (max 50 chars, optional)",
  "ragione_sociale": "string (max 100 chars, optional)",
  "indirizzo": "string (max 200 chars, optional)",
  "cap": "string (5 digits, optional)",
  "citta": "string (max 50 chars, optional)",
  "provincia": "string (2 uppercase letters, optional)",
  "mandante": "string (optional)",
  "intervento": "string (optional)",
  "email": "email (max 100 chars, optional)",
  "telefono1-8": "string (Italian phone format, optional)",
  "user_m3": "float (>= 0, optional)",
  "EmailRX1": "email (optional)",
  "EsitoPrioritario": "string (max 3 chars, optional)"
}
```

### Movimento (Movement)
```json
{
  "id": "integer (auto-generated)",
  "data": "datetime (required)",
  "ora": "datetime (required)",
  "contatore": "integer (required, FK to pratica)",
  "codagenzia": "string (max 3 chars, optional)",
  "codesa": "string (max 3 chars, required)",
  "nomeag": "string (required)",
  "esito": "string (required)",
  "descresito": "string (required)",
  "flagesito": "boolean (required)"
}
```

### Email
```json
{
  "IdEMail": "integer (auto-generated)",
  "Agente": "string (required)",
  "Data": "date (required)",
  "Ora": "time (required)",
  "NomeMittente": "string (required)",
  "Mittente": "string (required)",
  "Destinatario": "string (required, semicolon-separated)",
  "DestinatarioCC": "string (optional, semicolon-separated)",
  "Oggetto": "string (max 100 chars, required)",
  "Messaggio": "string (required)",
  "Allegati": "string (optional, comma-separated)",
  "MailerType": "string (optional)",
  "IdMessage": "string (optional)",
  "IdResponse": "string (optional)",
  "Response": "string (optional)",
  "Error": "string (optional)",
  "Applicativo": "string (optional)",
  "IdPratica": "integer (required, FK to pratica)"
}
```

### SMS
```json
{
  "Id": "integer (auto-generated)",
  "Data": "date (required)",
  "Ora": "time (required)",
  "CodAg": "string (max 3 chars, optional)",
  "Mittente": "string (optional)",
  "Destinatario": "string (optional)",
  "NrTel": "string (optional)",
  "Testo": "string (required)",
  "IdSpedizione": "string (optional)",
  "Stato": "string (optional)",
  "FlagAuto": "boolean (optional)",
  "IdPratica": "integer (required, FK to pratica)",
  "FlagDaSpedire": "boolean (optional)",
  "DataSpedizione": "date (optional)",
  "Fornitore": "string (optional)",
  "Applicazione": "string (optional)",
  "Interno": "boolean (optional)",
  "IdTestoSMS": "integer (optional)",
  "NrSMS": "integer (auto-calculated)"
}
```

---

## 💡 Examples

### Complete Workflow Example

#### 1. Create a Practice
```bash
curl -X POST "http://localhost:8000/api/v1/pratiche/" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "codice_pratica": "PRAT-2024-003",
    "codice_cliente": "CLI-003",
    "vocativo": "Sig.",
    "cognome": "Verdi",
    "nome": "Giuseppe",
    "indirizzo": "Via Napoli 789",
    "cap": "80100",
    "citta": "Napoli",
    "provincia": "NA",
    "mandante": "Banca XYZ",
    "intervento": "Recupero crediti",
    "email": "giuseppe.verdi@email.com",
    "telefono1": "+39 333 5555555",
    "user_m3": 3000.00,
    "EmailRX1": "tracking@fides.it"
  }'
```

#### 2. Add a Movement
```bash
curl -X POST "http://localhost:8000/api/v1/movimenti/" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "data": "2024-01-26T00:00:00",
    "ora": "09:30:00",
    "contatore": 12347,
    "codagenzia": "AG1",
    "codesa": "SA1",
    "nomeag": "Mario Rossi",
    "esito": "Primo contatto",
    "descresito": "Telefonata di presentazione",
    "flagesito": true
  }'
```

#### 3. Send an Email
```bash
curl -X POST "http://localhost:8000/api/v1/email/" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "Agente": "AG001",
    "Data": "2024-01-26",
    "Ora": "10:00:00",
    "NomeMittente": "FIDES S.p.A.",
    "Mittente": "noreply@fides.it",
    "Destinatario": "giuseppe.verdi@email.com",
    "Oggetto": "Benvenuto",
    "Messaggio": "Gentile Sig. Verdi, benvenuto nel nostro servizio...",
    "IdPratica": 12347
  }'
```

#### 4. Send an SMS
```bash
curl -X POST "http://localhost:8000/api/v1/sms/" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "Data": "2024-01-26",
    "Ora": "11:00:00",
    "CodAg": "AG1",
    "Mittente": "FIDES",
    "Destinatario": "Sig. Verdi",
    "NrTel": "+393335555555",
    "Testo": "Gentile Sig. Verdi, confermiamo la ricezione della sua pratica.",
    "IdPratica": 12347
  }'
```

#### 5. Update Practice Status
```bash
curl -X PATCH "http://localhost:8000/api/v1/pratiche/12347/status" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "EsitoPrioritario": "PRO"
  }'
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Authentication Errors
**Problem:** `401 Unauthorized`
**Solutions:**
- Verify API key is correct
- Ensure `X-API-Key` header is included
- Check API key is not expired or revoked

#### 2. Validation Errors
**Problem:** `400 Bad Request`
**Solutions:**
- Check required fields are provided
- Verify data formats (dates, emails, phone numbers)
- Ensure field length limits are respected

#### 3. Resource Not Found
**Problem:** `404 Not Found`
**Solutions:**
- Verify the resource ID exists
- Check the endpoint URL is correct
- Ensure the practice exists before creating related records

#### 4. Rate Limiting
**Problem:** `429 Too Many Requests`
**Solutions:**
- Reduce request frequency
- Implement exponential backoff
- Consider batch operations for multiple records

### Debug Information

#### Request Headers
```bash
curl -v -H "X-API-Key: your_api_key" \
  "http://localhost:8000/api/v1/pratiche/12345"
```

#### Response Headers
```
X-Process-Time: 0.045
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

### Log Analysis

#### Check Application Logs
```bash
# View recent logs
tail -f app.log

# Search for errors
grep "ERROR" app.log

# Search for specific practice
grep "12345" app.log

# Check API key usage
grep "API key" app.log
```

#### Performance Monitoring
```bash
# Find slow requests (>1 second)
grep "Response:" app.log | awk '$NF > 1.000'

# Count requests by endpoint
grep "Request:" app.log | awk '{print $5}' | sort | uniq -c
```

---

## 📞 Support

For technical support or questions about the API:

- **Email:** support@fides.it
- **Phone:** +39 02 1234567
- **Documentation:** https://docs.fides.it/api
- **Status Page:** https://status.fides.it

---

**© 2024 FIDES S.p.A. - All rights reserved**
