from pydantic import BaseModel, constr, Field, model_validator
from datetime import date, time, datetime
from typing import Optional

class EMailBase(BaseModel):
    """
    Schema di base per una email.
    """
    Agente: constr(min_length=1) = Field(..., description="Codice agente")
    Data: date = Field(..., description="Data della email")
    Ora: time = Field(..., description="Ora della email")
    NomeMittente: constr(min_length=1) = Field(..., description="Nome del mittente")
    Mittente: constr(min_length=1) = Field(..., description="Indirizzo email del mittente")
    Destinatario: constr(min_length=1) = Field(..., description="Indirizzi destinatari separati da ';'")
    DestinatarioCC: Optional[constr(min_length=1)] = Field(None, description="Indirizzi CC separati da ';' (opzionale)")
    Oggetto: constr(min_length=1, max_length=100) = Field(..., description="Oggetto della email, max 100 caratteri")
    Messaggio: constr(min_length=1) = Field(..., description="Testo del messaggio")
    Allegati: Optional[constr(min_length=1)] = Field(None, description="Nomi degli allegati, separati da virgola")
    MailerType: Optional[constr(min_length=1)] = Field(None, description="Tipo di mailer utilizzato")
    IdMessage: Optional[constr(min_length=1)] = Field(None, description="ID del messaggio esterno")
    IdResponse: Optional[str] = Field(None, description="ID della risposta esterna")
    Response: Optional[str] = Field(None, description="Risposta del server esterno")
    Error: Optional[str] = Field(None, description="Messaggio di errore, se presente")
    Applicativo: Optional[constr(min_length=1)] = Field(None, description="Applicativo che ha generato la email")
    IdPratica: int = Field(..., description="ID della pratica collegata")

    @model_validator(mode='before')
    def parse_timestamps(cls, values):
        # parse Data
        raw_data = values.get('Data')
        if isinstance(raw_data, str):
            try:
                dt = datetime.fromisoformat(raw_data.rstrip('Z'))
                values['Data'] = dt.date()
            except (ValueError, TypeError):
                raise ValueError('invalid datetime format for Data')
        # parse Ora
        raw_ora = values.get('Ora')
        if isinstance(raw_ora, str):
            try:
                dt = datetime.fromisoformat(raw_ora.rstrip('Z'))
                values['Ora'] = dt.time()
            except (ValueError, TypeError):
                raise ValueError('invalid datetime format for Ora')
        return values

class EMailCreate(EMailBase):
    """Payload per creare una nuova email"""
    pass

class EMailResponse(EMailBase):
    """Schema di risposta includendo l'ID generato dal DB"""
    IdEMail: int = Field(..., description="Chiave primaria generata dal DB")
    model_config = { 'from_attributes': True }
