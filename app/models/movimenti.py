from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class Movimento(BaseModel):
    id: Optional[int] = Field(None, description="ID auto-generato del movimento")
    data: datetime = Field(..., description="Data del movimento")
    ora: datetime = Field(..., description="Ora del movimento")
    contatore: int = Field(..., description="ID della pratica (FK)")
    codagenzia: Optional[str] = Field(None, max_length=3, description="Codice agenzia (max 3 caratteri)")
    codesa: str = Field(..., max_length=3, description="Codice SA (max 3 caratteri)")
    nomeag: str = Field(..., description="Nome dell'agente")
    esito: str = Field(..., description="Esito del movimento")
    descresito: str = Field(..., description="Descrizione dell'esito")
    flagesito: bool = Field(..., description="Flag dell'esito")
    note: Optional[str] = Field(None, description="Note aggiuntive del movimento")
    datapag: Optional[datetime] = Field(None, description="Data del pagamento")
    importopag: Optional[Decimal] = Field(None, description="Importo del pagamento")
    orarecall: Optional[datetime] = Field(None, description="Ora di recall")
    tel1: Optional[str] = Field(None, max_length=20, description="Numero di telefono 1")
    
    @field_validator('codagenzia')
    @classmethod
    def validate_codagenzia(cls, v):
        if v is not None and len(v) > 3:
            raise ValueError('codagenzia deve essere massimo 3 caratteri')
        return v
    
    @field_validator('codesa')
    @classmethod
    def validate_codesa(cls, v):
        if len(v) > 3:
            raise ValueError('codesa deve essere massimo 3 caratteri')
        return v

    model_config = {'from_attributes': True}

class MovimentoCreate(BaseModel):
    """Model for creating a new movimento (without ID field)"""
    data: datetime = Field(..., description="Data del movimento")
    ora: datetime = Field(..., description="Ora del movimento")
    contatore: int = Field(..., description="ID della pratica (FK)")
    codagenzia: Optional[str] = Field(None, max_length=3, description="Codice agenzia (max 3 caratteri)")
    codesa: str = Field(..., max_length=3, description="Codice SA (max 3 caratteri)")
    nomeag: str = Field(..., description="Nome dell'agente")
    esito: str = Field(..., description="Esito del movimento")
    descresito: str = Field(..., description="Descrizione dell'esito")
    flagesito: bool = Field(..., description="Flag dell'esito")
    note: Optional[str] = Field(None, description="Note aggiuntive del movimento")
    datapag: Optional[datetime] = Field(None, description="Data del pagamento")
    importopag: Optional[Decimal] = Field(None, description="Importo del pagamento")
    orarecall: Optional[datetime] = Field(None, description="Ora di recall")
    tel1: Optional[str] = Field(None, max_length=20, description="Numero di telefono 1")
    
    @field_validator('codagenzia')
    @classmethod
    def validate_codagenzia(cls, v):
        if v is not None and len(v) > 3:
            raise ValueError('codagenzia deve essere massimo 3 caratteri')
        return v
    
    @field_validator('codesa')
    @classmethod
    def validate_codesa(cls, v):
        if len(v) > 3:
            raise ValueError('codesa deve essere massimo 3 caratteri')
        return v
    
    model_config = {'from_attributes': True}