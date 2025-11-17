# CollectFlowAPI - Production Deployment Checklist
# ===============================================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

## 🚨 CRITICAL PRE-DEPLOYMENT CHECKS

### ✅ Environment Configuration
- [ ] Create `.env` file from `env.template`
- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Configure `SQLSERVER_DSN` with production database
- [ ] Set strong `API_KEYS` (comma-separated)
- [ ] Set appropriate `DB_POOL_SIZE` (recommended: 20-50)

### ✅ Security Configuration
- [ ] Remove debug logging from production
- [ ] Ensure API keys are not logged
- [ ] Verify CORS settings for production domains
- [ ] Check rate limiting is enabled
- [ ] Validate all endpoints require authentication

### ✅ Database Configuration
- [ ] Test database connection with production credentials
- [ ] Verify connection pooling works correctly
- [ ] Check database permissions for application user
- [ ] Ensure proper indexes exist on tables

### ✅ Application Health
- [ ] Test all endpoints with valid API keys
- [ ] Verify error handling works correctly
- [ ] Check logging configuration
- [ ] Test health check endpoint (`/health`)
- [ ] Verify version info endpoint (`/api/versions`)

## 🔧 PRODUCTION DEPLOYMENT STEPS

### 1. Environment Setup
```bash
# Copy environment template
cp env.template .env

# Edit .env with production values
nano .env
```

### 2. Dependencies Installation
```bash
# Install production dependencies
pip install -r requirements.txt

# Verify all packages installed
pip list
```

### 3. Application Testing
```bash
# Test application import
python -c "from app.main import app; print('✅ Application ready')"

# Test with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Production Server Configuration
```bash
# Recommended production command
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info \
  --access-log
```

## 📋 ENDPOINT VERIFICATION

### Core Endpoints
- [ ] `GET /` - Root endpoint
- [ ] `GET /health` - Health check
- [ ] `GET /api/versions` - Version info
- [ ] `GET /docs` - API documentation

### API v1 Endpoints
- [ ] `GET /api/v1/pratiche/{contatore}` - Get practice
- [ ] `POST /api/v1/pratiche/` - Create practice
- [ ] `PATCH /api/v1/pratiche/{contatore}/status` - Update status
- [ ] `GET /api/v1/movimenti/{contatore}` - Get movements
- [ ] `POST /api/v1/movimenti/` - Create movement
- [ ] `GET /api/v1/email/{contatore}` - Get emails
- [ ] `POST /api/v1/email/` - Create email
- [ ] `GET /api/v1/sms/{contatore}` - Get SMS
- [ ] `POST /api/v1/sms/` - Create SMS

## 🔒 SECURITY VERIFICATION

### Authentication
- [ ] All endpoints require `X-API-Key` header
- [ ] Invalid API keys return 401
- [ ] Missing API keys return 401
- [ ] API keys are not logged in production

### Rate Limiting
- [ ] GET endpoints: 100 requests/minute
- [ ] POST endpoints: 10 requests/minute
- [ ] PATCH endpoints: 50 requests/minute
- [ ] Rate limit exceeded returns 429

### Error Handling
- [ ] Validation errors return 422
- [ ] Not found errors return 404
- [ ] Server errors return 500
- [ ] All errors include proper JSON response

## 📊 MONITORING & LOGGING

### Logging Configuration
- [ ] File logging to `app.log`
- [ ] Console logging enabled
- [ ] Log rotation (7 days retention)
- [ ] No sensitive data in logs

### Health Monitoring
- [ ] Health check endpoint responds correctly
- [ ] Database connectivity verified
- [ ] Application startup logs recorded
- [ ] Error logs captured properly

## 🚀 DEPLOYMENT COMMANDS

### Development Testing
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment (if applicable)
```bash
docker build -t collectflow-api .
docker run -p 8000:8000 collectflow-api
```

## 📞 SUPPORT CONTACTS

- **Developer**: Salvatore Privitera
- **Company**: FIDES S.p.A.
- **Emergency Contact**: [Add emergency contact]

## ✅ FINAL VERIFICATION

Before going live:
- [ ] All tests pass
- [ ] Documentation is complete
- [ ] Security review completed
- [ ] Performance testing done
- [ ] Backup procedures in place
- [ ] Monitoring configured
- [ ] Rollback plan ready

---
**Last Updated**: 2025-08-19
**Version**: 1.0.0
