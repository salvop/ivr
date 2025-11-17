"""
Practice Data Models
===================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: Pydantic models for practice data validation and serialization
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module contains Pydantic models for practice-related data structures,
including validation rules and business logic for practice management.
"""

import re
from pydantic import BaseModel, EmailStr, Field, confloat, field_validator
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from .validators import (
    validate_cap, validate_provincia, validate_phone, validate_codes, 
    validate_names, empty_str_to_none, validate_esito_prioritario
)


class Pratica(BaseModel):
    contatore: int = Field(..., description="ID univoco della pratica (auto-generato)")
    codice_pratica: Optional[str] = Field(None, description="Codice della pratica")
    codice_cliente: Optional[str] = Field(None, description="Codice del cliente")
    vocativo: Optional[str] = Field(None, max_length=10, description="Vocativo (es. Sig., Sig.ra)")
    cognome: Optional[str] = Field(None, max_length=50, description="Cognome del cliente")
    nome: Optional[str] = Field(None, max_length=50, description="Nome del cliente")
    data_nascita: Optional[date] = Field(None, description="Data di nascita del cliente")
    ragione_sociale: Optional[str] = Field(None, max_length=100, description="Ragione sociale (per aziende)")
    indirizzo: Optional[str] = Field(None, max_length=200, description="Indirizzo completo")
    cap: Optional[str] = Field(None, description="Codice postale (5 cifre)")
    citta: Optional[str] = Field(None, max_length=50, description="Città")
    provincia: Optional[str] = Field(None, description="Provincia (2 lettere maiuscole)")
    mandante: Optional[str] = Field(None, description="Ente mandante")
    intervento: Optional[str] = Field(None, description="Tipo di intervento")
    email: Optional[EmailStr] = Field(
        None,
        max_length=100,
        description="Email valida del cliente (es. nome@dominio.it)"
    )
    telefono1: Optional[str] = Field(None, description="Numero di telefono principale")
    telefono2: Optional[str] = Field(None, description="Numero di telefono secondario")
    telefono3: Optional[str] = Field(None, description="Numero di telefono alternativo 1")
    telefono4: Optional[str] = Field(None, description="Numero di telefono alternativo 2")
    telefono5: Optional[str] = Field(None, description="Numero di telefono alternativo 3")
    telefono6: Optional[str] = Field(None, description="Numero di telefono alternativo 4")
    telefono7: Optional[str] = Field(None, description="Numero di telefono alternativo 5")
    telefono8: Optional[str] = Field(None, description="Numero di telefono alternativo 6")
    user_m3: Optional[confloat(ge=0)] = Field(
        None,
        description="Valore numerico (float) di user_m3, deve essere >= 0"
    )
    EmailRX1: Optional[EmailStr] = Field(
        None,
        description="Indirizzo email di rintraccio (opzionale)"
    )
    EsitoPrioritario: Optional[str] = Field(
        None,
        max_length=3,
        description="Esito Prioritario (3 caratteri) - Maps to database field 'EsitoFonia'"
    )
    scadenza_mandato: Optional[datetime] = Field(None, description="Data di scadenza del mandato")
    seat_importoOrig: Optional[Decimal] = Field(None, description="Importo originale SEAT")
    posizione: Optional[str] = Field(None, max_length=25, description="Posizione della pratica")
    esattore: Optional[str] = Field(None, max_length=3, description="Codice esattore")
    
    @field_validator('email', 'EmailRX1', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v
    
    @field_validator('cap')
    @classmethod
    def validate_cap(cls, v):
        if v and not re.match(r'^\d{5}$', v):
            raise ValueError('CAP deve essere di 5 cifre')
        return v
    
    @field_validator('provincia')
    @classmethod
    def validate_provincia(cls, v):
        if v and not re.match(r'^[A-Z]{2}$', v.upper()):
            raise ValueError('Provincia deve essere di 2 lettere maiuscole')
        return v.upper() if v else v
    
    @field_validator('telefono1', 'telefono2', 'telefono3', 'telefono4', 
               'telefono5', 'telefono6', 'telefono7', 'telefono8')
    @classmethod
    def validate_phone(cls, v):
        if v:
            # Remove spaces and common separators
            cleaned = re.sub(r'[\s\-\(\)\.]', '', v)
            # Check if it's a valid Italian phone number
            if not re.match(r'^(\+39|0039)?[0-9]{8,10}$', cleaned):
                raise ValueError('Numero di telefono non valido')
        return v

    model_config = {'from_attributes': True}

class PraticaCreate(BaseModel):
    """
    Modello di Input per POST /pratiche:
    - contatore NON va inserito (identity autogenerato)
    - tutti gli altri campi sono opzionali tranne quelli che vuoi rendere obbligatori
    """
    codice_pratica: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Codice pratica obbligatorio, 1–50 caratteri"
    )
    codice_cliente: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Codice cliente obbligatorio, 1–50 caratteri"
    )
    vocativo: Optional[str] = Field(None, max_length=10)
    cognome: Optional[str] = Field(None, max_length=50)
    nome: Optional[str] = Field(None, max_length=50)
    data_nascita: Optional[date] = Field(None, description="Data di nascita del cliente")
    ragione_sociale: Optional[str] = Field(None, max_length=100)
    indirizzo: Optional[str] = Field(None, max_length=200)
    cap: Optional[str] = Field(None, pattern=r"^\d{5}$", description="CAP a 5 cifre")
    citta: Optional[str] = Field(None, max_length=50)
    provincia: Optional[str] = Field(None, min_length=2, max_length=2)
    mandante: Optional[str]
    intervento: Optional[str]
    email: Optional[EmailStr] = Field(
        None,
        max_length=100,
        description="Email valida del cliente (es. nome@dominio.it)"
    )
    telefono1: Optional[str]
    telefono2: Optional[str]
    telefono3: Optional[str]
    telefono4: Optional[str]
    telefono5: Optional[str]
    telefono6: Optional[str]
    telefono7: Optional[str]
    telefono8: Optional[str]
    user_m3: Optional[confloat(ge=0)] = Field(
        None,
        description="Valore numerico (float) di user_m3, deve essere >= 0"
        )
    EmailRX1: Optional[EmailStr] = Field(
        None,
        description="Indirizzo email secondario (opzionale)"
        )
    scadenza_mandato: Optional[datetime] = Field(None, description="Data di scadenza del mandato")
    seat_importoOrig: Optional[Decimal] = Field(None, description="Importo originale SEAT")
    posizione: Optional[str] = Field(None, max_length=25, description="Posizione della pratica")
    esattore: Optional[str] = Field(None, max_length=3, description="Codice esattore")
    
    @field_validator('email', 'EmailRX1', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v
    
    @field_validator('cap')
    @classmethod
    def validate_cap(cls, v):
        if v and not re.match(r'^\d{5}$', v):
            raise ValueError('CAP deve essere di 5 cifre')
        return v
    
    @field_validator('provincia')
    @classmethod
    def validate_provincia(cls, v):
        if v and not re.match(r'^[A-Z]{2}$', v.upper()):
            raise ValueError('Provincia deve essere di 2 lettere maiuscole')
        return v.upper() if v else v
    
    @field_validator('telefono1', 'telefono2', 'telefono3', 'telefono4', 
               'telefono5', 'telefono6', 'telefono7', 'telefono8')
    @classmethod
    def validate_phone(cls, v):
        if v:
            # Remove spaces and common separators
            cleaned = re.sub(r'[\s\-\(\)\.]', '', v)
            # Check if it's a valid Italian phone number
            if not re.match(r'^(\+39|0039)?[0-9]{8,10}$', cleaned):
                raise ValueError('Numero di telefono non valido')
        return v
    
    @field_validator('codice_pratica', 'codice_cliente')
    @classmethod
    def validate_codes(cls, v):
        if v and not re.match(r'^[A-Z0-9\-_]+$', v.upper()):
            raise ValueError('Codice può contenere solo lettere maiuscole, numeri, trattini e underscore')
        return v.upper() if v else v
    
    @field_validator('cognome', 'nome')
    @classmethod
    def validate_names(cls, v):
        if v and not re.match(r'^[A-Za-zÀ-ÿ\s\'-]+$', v):
            raise ValueError('Nome e cognome possono contenere solo lettere, spazi, apostrofi e trattini')
        return v.title() if v else v

    model_config = {'from_attributes': True}


class PraticaUpdateStatus(BaseModel):
    """
    Modello per PATCH /pratiche/{contatore}/status:
    - Aggiorna solo il campo EsitoPrioritario (API) che mappa su EsitoFonia (database)
    """
    EsitoPrioritario: str = Field(
        ...,
        min_length=1,
        max_length=3,
        description="Esito Prioritario (obbligatorio, 1-3 caratteri) - Maps to database field 'EsitoFonia'"
    )
    
    @field_validator('EsitoPrioritario')
    @classmethod
    def validate_esito_prioritario(cls, v):
        if not v or not v.strip():
            raise ValueError('Esito Prioritario non può essere vuoto')
        if len(v.strip()) > 3:
            raise ValueError('Esito Prioritario deve essere di massimo 3 caratteri')
        return v.strip()

    model_config = {'from_attributes': True}