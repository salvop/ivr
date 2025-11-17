# CollectFlowAPI - HTTP Messages Summary

## ** Overview**

This document provides a comprehensive summary of all HTTP messages, status codes, request/response formats, and error handling for each endpoint in the CollectFlowAPI.

---

## ** Authentication**

### **Required Header**
```
X-API-Key: your_api_key_here
```

### **Authentication Error Response**
```json
{
  "detail": "API key mancante o non valida"
}
```
- **Status Code**: `401 Unauthorized`
- **Trigger**: Missing or invalid API key

---

## **⚡ Rate Limiting**

### **Rate Limit Exceeded Response**
```json
{
  "detail": "Rate limit exceeded: 100 per 1 minute"
}
```
- **Status Code**: `429 Too Many Requests`
- **GET Endpoints**: 100 requests per minute per IP
- **POST Endpoints**: 10 requests per minute per IP

---

## ** Endpoint Summary**

| Module | Method | Endpoint | Rate Limit | Status Codes |
|--------|--------|----------|------------|--------------|
| **Pratiche** | GET | `/{contatore}` | 100/min | 200, 401, 404, 429 |
| **Pratiche** | POST | `/` | 10/min | 201, 400, 401, 429 |
| **Movimenti** | GET | `/{contatore}` | 100/min | 200, 401, 404, 429 |
| **Movimenti** | POST | `/` | 10/min | 201, 400, 401, 429 |
| **Email** | GET | `/{contatore}` | 100/min | 200, 401, 404, 429 |
| **Email** | POST | `/` | 10/min | 201, 400, 401, 429 |
| **SMS** | GET | `/{contatore}` | 100/min | 200, 401, 404, 429 |
| **SMS** | POST | `/` | 10/min | 201, 400, 401, 429 |

---

## ** Pratiche Module**

### **GET /pratiche/{contatore}**

#### **Request**
```http
GET /pratiche/12345
X-API-Key: your_api_key_here
```

#### **Success Response (200 OK)**
```json
{
  "contatore": 12345,
  "ragione_sociale": "Azienda Example SRL",
  "indirizzo": "Via Roma 123",
  "cap": "00100",
  "citta": "Roma",
  "provincia": "RM",
  "telefono1": "+393331234567",
  "telefono2": "+393339876543",
  "email": "info@azienda.com",
  "partita_iva": "12345678901",
  "codice_fiscale": "RSSMRA80A01H501U",
  "stato": "Attivo",
  "data_creazione": "2024-01-15T10:30:00",
  "note": "Cliente premium"
}
```

#### **Error Responses**

**404 Not Found**
```json
{
  "detail": "Pratica non trovata"
}
```

**401 Unauthorized**
```json
{
  "detail": "API key mancante o non valida"
}
```

**429 Too Many Requests**
```json
{
  "detail": "Rate limit exceeded: 100 per 1 minute"
}
```

### **POST /pratiche/**

#### **Request**
```http
POST /pratiche/
X-API-Key: your_api_key_here
Content-Type: application/json

{
  "ragione_sociale": "Nuova Azienda SRL",
  "indirizzo": "Via Milano 456",
  "cap": "20100",
  "citta": "Milano",
  "provincia": "MI",
  "telefono1": "+393331234567",
  "email": "info@nuovaazienda.com",
  "partita_iva": "98765432109",
  "codice_fiscale": "NVSRL80A01H501U",
  "stato": "Attivo",
  "note": "Nuovo cliente"
}
```

#### **Success Response (201 Created)**
```json
{
  "contatore": 12346,
  "ragione_sociale": "Nuova Azienda SRL",
  "indirizzo": "Via Milano 456",
  "cap": "20100",
  "citta": "Milano",
  "provincia": "MI",
  "telefono1": "+393331234567",
  "telefono2": null,
  "email": "info@nuovaazienda.com",
  "partita_iva": "98765432109",
  "codice_fiscale": "NVSRL80A01H501U",
  "stato": "Attivo",
  "data_creazione": "2024-01-25T15:30:00",
  "note": "Nuovo cliente"
}
```

#### **Error Responses**

**400 Bad Request - Validation Errors**
```json
{
  "detail": [
    {
      "loc": ["body", "telefono1"],
      "msg": "Numero di telefono non valido",
      "type": "value_error"
    },
    {
      "loc": ["body", "cap"],
      "msg": "CAP deve essere di 5 cifre",
      "type": "value_error"
    },
    {
      "loc": ["body", "provincia"],
      "msg": "Provincia deve essere di 2 lettere maiuscole",
      "type": "value_error"
    }
  ]
}
```

**400 Bad Request - Business Logic Error**
```json
{
  "detail": "Partita IVA già esistente nel database"
}
```

---

## **📋 Movimenti Module**

### **GET /movimenti/{contatore}**

#### **Request**
```http
GET /movimenti/12345
X-API-Key: your_api_key_here
```

#### **Success Response (200 OK)**
```json
[
  {
    "id": 1,
    "contatore": 12345,
    "data": "2024-01-15",
    "ora": "14:30:00",
    "esito": "Completato",
    "descrizione": "Prima visita al cliente",
    "flag": true
  },
  {
    "id": 2,
    "contatore": 12345,
    "data": "2024-01-20",
    "ora": "10:15:00",
    "esito": "In corso",
    "descrizione": "Follow-up telefonico",
    "flag": false
  }
]
```

#### **Empty Response (200 OK)**
```json
[]
```

### **POST /movimenti/**

#### **Request**
```http
POST /movimenti/
X-API-Key: your_api_key_here
Content-Type: application/json

{
  "contatore": 12345,
  "data": "2024-01-25",
  "ora": "15:45:00",
  "esito": "Completato",
  "descrizione": "Visita di controllo completata",
  "flag": true
}
```

#### **Success Response (201 Created)**
```json
{
  "id": 3,
  "contatore": 12345,
  "data": "2024-01-25",
  "ora": "15:45:00",
  "esito": "Completato",
  "descrizione": "Visita di controllo completata",
  "flag": true
}
```

#### **Error Response (400 Bad Request)**
```json
{
  "detail": "Pratica non trovata nel database"
}
```

---

## **📧 Email Module**

### **GET /email/{contatore}**

#### **Request**
```http
GET /email/12345
X-API-Key: your_api_key_here
```

#### **Success Response (200 OK)**
```json
[
  {
    "id": 1,
    "contatore": 12345,
    "data_invio": "2024-01-15T10:30:00",
    "destinatario": "cliente@email.com",
    "oggetto": "Conferma appuntamento",
    "corpo": "Gentile cliente, confermiamo il suo appuntamento...",
    "stato": "Inviato",
    "priorita": "Alta",
    "allegati": ["documento1.pdf"]
  },
  {
    "id": 2,
    "contatore": 12345,
    "data_invio": "2024-01-20T14:15:00",
    "destinatario": "cliente@email.com",
    "oggetto": "Follow-up servizio",
    "corpo": "Gentile cliente, ecco il follow-up...",
    "stato": "Letto",
    "priorita": "Normale",
    "allegati": []
  }
]
```

### **POST /email/**

#### **Request**
```http
POST /email/
X-API-Key: your_api_key_here
Content-Type: application/json

{
  "contatore": 12345,
  "destinatario": "cliente@email.com",
  "oggetto": "Conferma appuntamento",
  "corpo": "Gentile cliente, confermiamo il suo appuntamento per domani alle 15:00",
  "priorita": "Alta",
  "allegati": ["documento1.pdf"]
}
```

#### **Success Response (201 Created)**
```json
{
  "id": 3,
  "contatore": 12345,
  "data_invio": "2024-01-25T16:00:00",
  "destinatario": "cliente@email.com",
  "oggetto": "Conferma appuntamento",
  "corpo": "Gentile cliente, confermiamo il suo appuntamento per domani alle 15:00",
  "stato": "In attesa",
  "priorita": "Alta",
  "allegati": ["documento1.pdf"]
}
```

---

## **📱 SMS Module**

### **GET /sms/{contatore}**

#### **Request**
```http
GET /sms/12345
X-API-Key: your_api_key_here
```

#### **Success Response (200 OK)**
```json
[
  {
    "id": 1,
    "contatore": 12345,
    "data_invio": "2024-01-15T10:30:00",
    "numero_destinatario": "+393331234567",
    "messaggio": "Conferma appuntamento alle 15:00",
    "stato": "Inviato",
    "priorita": "Alta"
  },
  {
    "id": 2,
    "contatore": 12345,
    "data_invio": "2024-01-20T14:15:00",
    "numero_destinatario": "+393331234567",
    "messaggio": "Promemoria: appuntamento domani",
    "stato": "Consegnato",
    "priorita": "Normale"
  }
]
```

### **POST /sms/**

#### **Request**
```http
POST /sms/
X-API-Key: your_api_key_here
Content-Type: application/json

{
  "contatore": 12345,
  "numero_destinatario": "+393331234567",
  "messaggio": "Gentile cliente, confermiamo il suo appuntamento per domani alle 15:00",
  "priorita": "Alta",
  "scheduled_time": "2024-01-25T10:00:00"
}
```

#### **Success Response (201 Created)**
```json
{
  "id": 3,
  "contatore": 12345,
  "data_invio": "2024-01-25T10:00:00",
  "numero_destinatario": "+393331234567",
  "messaggio": "Gentile cliente, confermiamo il suo appuntamento per domani alle 15:00",
  "stato": "In attesa",
  "priorita": "Alta"
}
```

---

## **🚨 Common Error Responses**

### **Validation Errors (400 Bad Request)**
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Error message in Italian",
      "type": "value_error"
    }
  ]
}
```

### **Not Found (404 Not Found)**
```json
{
  "detail": "Risorsa non trovata"
}
```

### **Internal Server Error (500 Internal Server Error)**
```json
{
  "detail": "Errore interno del server"
}
```

---

## **📈 Response Headers**

### **Standard Headers**
```
Content-Type: application/json
X-Request-ID: unique-request-id
X-Rate-Limit-Remaining: 99
X-Rate-Limit-Reset: 1643123456
```

### **Rate Limiting Headers**
- `X-Rate-Limit-Remaining`: Number of requests remaining
- `X-Rate-Limit-Reset`: Timestamp when rate limit resets
- `X-Rate-Limit-Limit`: Maximum requests per time window

---

## **🔍 Request Validation**

### **Path Parameters**
- `contatore` (int): Must be a positive integer

### **Query Parameters**
- Currently no query parameters implemented

### **Body Validation**
- All required fields must be present
- Data types must match expected formats
- Business rules validation (e.g., phone numbers, CAP codes)

---

## **📝 Logging Information**

### **Request Logs**
```
[2024-01-25 15:30:00] INFO - GET /pratiche/12345 - Client: 192.168.1.100 - User-Agent: Mozilla/5.0 - API-Key: *** - Status: 200 - Duration: 45ms
```

### **Error Logs**
```
[2024-01-25 15:30:00] ERROR - POST /pratiche/ - Client: 192.168.1.100 - Validation Error: Numero di telefono non valido - Status: 400
```

---

## **🎯 Best Practices**

### **Client Implementation**
1. **Always include API key** in `X-API-Key` header
2. **Handle rate limiting** by checking `429` responses
3. **Implement retry logic** for transient errors
4. **Validate responses** before processing
5. **Log request/response** for debugging

### **Error Handling**
1. **Check status codes** before processing response body
2. **Handle validation errors** by displaying field-specific messages
3. **Implement exponential backoff** for rate limit errors
4. **Log all errors** for troubleshooting

This comprehensive HTTP messages summary ensures consistent API usage and proper error handling across all endpoints! 🚀

