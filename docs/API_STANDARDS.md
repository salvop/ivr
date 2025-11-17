# CollectFlowAPI - Standardized Patterns & Rules

## **📋 Standardized Endpoint Patterns**

All endpoints in the CollectFlowAPI follow the same programming rules and patterns for consistency, security, and maintainability.

## **🔐 Authentication Standards**

### **API Key Authentication**
- **Header**: `X-API-Key` required on all endpoints
- **Validation**: All endpoints validate API keys using `validate_api_key()`
- **Error**: Returns `401 Unauthorized` for invalid/missing API keys

```python
# Standard pattern in all endpoints
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def endpoint_function(request: Request, api_key: str = Depends(api_key_header)):
    # Validate API key
    validate_api_key(api_key)
    # ... rest of function
```

## **⚡ Rate Limiting Standards**

### **Rate Limits by Endpoint Type**
- **GET endpoints**: 100 requests per minute per IP
- **POST endpoints**: 10 requests per minute per IP (more restrictive)

```python
# Standard rate limiting pattern
limiter = request.app.state.limiter

# GET endpoints
await limiter.rate_limit("100/minute", key_func=get_remote_address)(request)

# POST endpoints  
await limiter.rate_limit("10/minute", key_func=get_remote_address)(request)
```

## **📝 Documentation Standards**

### **Required Documentation Elements**
All endpoints include:

1. **Summary**: Brief description of endpoint purpose
2. **Description**: Detailed explanation with sections:
   - **Parametri**: Input parameters
   - **Autenticazione**: Authentication requirements
   - **Rate Limiting**: Rate limit information
   - **Risposte**: All possible response codes
   - **Esempio di risposta/richiesta**: JSON examples

3. **Responses**: All HTTP status codes with descriptions
4. **Function docstring**: Args, Returns, Raises documentation

### **Standard Response Codes**
- `200 OK`: Successful GET operations
- `201 Created`: Successful POST operations
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: API key issues
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded

## **🔍 Validation Standards**

### **Input Validation**
- **Pydantic models**: All inputs validated through Pydantic
- **Custom validators**: Enhanced validation for business rules
- **Error messages**: Clear, Italian error messages

### **Enhanced Validation Rules**
```python
# Phone number validation
@validator('telefono1', 'telefono2', ...)
def validate_phone(cls, v):
    if v:
        cleaned = re.sub(r'[\s\-\(\)\.]', '', v)
        if not re.match(r'^(\+39|0039)?[0-9]{8,10}$', cleaned):
            raise ValueError('Numero di telefono non valido')

# CAP validation
@validator('cap')
def validate_cap(cls, v):
    if v and not re.match(r'^\d{5}$', v):
        raise ValueError('CAP deve essere di 5 cifre')

# Province validation
@validator('provincia')
def validate_provincia(cls, v):
    if v and not re.match(r'^[A-Z]{2}$', v.upper()):
        raise ValueError('Provincia deve essere di 2 lettere maiuscole')
    return v.upper() if v else v
```

## **🔄 Function Signature Standards**

### **Standard Parameters**
```python
async def endpoint_function(
    request: Request,                    # Required for rate limiting
    path_param: int,                     # Path parameters
    body_param: ModelType,               # Body parameters
    api_key: str = Depends(api_key_header)  # Authentication
):
```

### **Standard Function Structure**
```python
async def endpoint_function(...):
    """
    Function description.
    
    Args:
        request: FastAPI request object
        param: Parameter description
        api_key: Chiave API per l'autenticazione
        
    Returns:
        ModelType: Return description
        
    Raises:
        HTTPException: Error conditions
    """
    # 1. Rate limiting
    limiter = request.app.state.limiter
    await limiter.rate_limit("X/minute", key_func=get_remote_address)(request)
    
    # 2. API key validation
    validate_api_key(api_key)
    
    # 3. Business logic
    result = await run_in_threadpool(business_function, params)
    
    # 4. Return response
    return result
```

## **📊 Endpoint Summary**

| Module | GET Endpoint | POST Endpoint | Rate Limit GET | Rate Limit POST |
|--------|--------------|---------------|----------------|-----------------|
| **Pratiche** | `/{contatore}` | `/` | 100/min | 10/min |
| **Movimenti** | `/{contatore}` | `/` | 100/min | 10/min |
| **Email** | `/{contatore}` | `/` | 100/min | 10/min |
| **SMS** | `/{contatore}` | `/` | 100/min | 10/min |

## **🛡️ Security Standards**

### **Authentication**
- ✅ API key required on all endpoints
- ✅ API key validation function
- ✅ Configurable via environment variables

### **Rate Limiting**
- ✅ IP-based rate limiting
- ✅ Different limits for GET vs POST
- ✅ Automatic blocking with 429 responses

### **Input Validation**
- ✅ Pydantic model validation
- ✅ Custom business rule validation
- ✅ SQL injection protection via parameterized queries

### **Error Handling**
- ✅ Global exception handlers
- ✅ Consistent error response format
- ✅ Detailed logging of all errors

## **📈 Performance Standards**

### **Database Operations**
- ✅ Thread pool for blocking operations
- ✅ Proper connection handling
- ✅ Error handling for database failures

### **Logging**
- ✅ Request/response timing
- ✅ Client IP and user agent logging
- ✅ Error logging with stack traces

## **🎯 Consistency Benefits**

### **Developer Experience**
- ✅ Predictable API behavior
- ✅ Consistent error messages
- ✅ Standardized documentation

### **Maintenance**
- ✅ Easy to add new endpoints
- ✅ Consistent code patterns
- ✅ Centralized configuration

### **Security**
- ✅ Uniform authentication
- ✅ Consistent rate limiting
- ✅ Standardized validation

## **📋 Implementation Checklist**

When adding new endpoints, ensure:

- [ ] API key authentication implemented
- [ ] Rate limiting configured
- [ ] Input validation added
- [ ] Documentation complete
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Tests written (future)

This standardization ensures your API is secure, maintainable, and provides a consistent developer experience! 🚀

