"""
Shared Validation Functions
==========================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: Shared validation functions for Pydantic models
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module contains common validation functions that can be reused
across different Pydantic models to reduce code duplication.
"""

import re
from typing import Any


def validate_cap(v: Any) -> str:
    """Validate CAP (Italian postal code) - 5 digits"""
    if v and not re.match(r'^\d{5}$', v):
        raise ValueError('CAP deve essere di 5 cifre')
    return v


def validate_provincia(v: Any) -> str:
    """Validate provincia - 2 uppercase letters"""
    if v and not re.match(r'^[A-Z]{2}$', v.upper()):
        raise ValueError('Provincia deve essere di 2 lettere maiuscole')
    return v.upper() if v else v


def validate_phone(v: Any) -> str:
    """Validate Italian phone number"""
    if v:
        # Remove spaces and common separators
        cleaned = re.sub(r'[\s\-\(\)\.]', '', v)
        # Check if it's a valid Italian phone number
        if not re.match(r'^(\+39|0039)?[0-9]{8,10}$', cleaned):
            raise ValueError('Numero di telefono non valido')
    return v


def validate_codes(v: Any) -> str:
    """Validate codes - uppercase letters, numbers, hyphens, underscores"""
    if v and not re.match(r'^[A-Z0-9\-_]+$', v.upper()):
        raise ValueError('Codice può contenere solo lettere maiuscole, numeri, trattini e underscore')
    return v.upper() if v else v


def validate_names(v: Any) -> str:
    """Validate names - letters, spaces, apostrophes, hyphens"""
    if v and not re.match(r'^[A-Za-zÀ-ÿ\s\'-]+$', v):
        raise ValueError('Nome e cognome possono contenere solo lettere, spazi, apostrofi e trattini')
    return v.title() if v else v


def empty_str_to_none(v: Any) -> Any:
    """Convert empty strings to None"""
    if isinstance(v, str) and not v.strip():
        return None
    return v


def validate_esito_prioritario(v: Any) -> str:
    """Validate EsitoPrioritario - 1-3 characters, not empty"""
    if not v or not v.strip():
        raise ValueError('Esito Prioritario non può essere vuoto')
    if len(v.strip()) > 3:
        raise ValueError('Esito Prioritario deve essere di massimo 3 caratteri')
    return v.strip()
