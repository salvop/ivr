from pydantic import BaseModel, constr, Field, model_validator
from datetime import date, time, datetime
from typing import Optional

class SMSBase(BaseModel):
    """
    Schema di base per un SMS. Contiene tutti i campi condivisi tra input e output.
    """
    Data: date = Field(..., description="Data dell'SMS")
    Ora: time = Field(..., description="Ora dell'SMS")
    CodAg: Optional[constr(min_length=1, max_length=3)] = Field(None, description="Codice agente (fino a 3 caratteri)")
    Mittente: Optional[constr(min_length=1)] = Field(None, description="Mittente dello SMS")
    Destinatario: Optional[constr(min_length=1)] = Field(None, description="Destinatario dello SMS")
    NrTel: Optional[constr(min_length=1)] = Field(None, description="Numero di telefono")
    Testo: constr(min_length=1) = Field(..., description="Testo del messaggio")
    IdSpedizione: Optional[constr(min_length=1)] = Field(None, description="ID di spedizione esterno")
    Stato: Optional[constr(min_length=1)] = Field(None, description="Stato di spedizione")
    FlagAuto: Optional[bool] = Field(None)
    IdPratica: int = Field(..., description="ID della pratica collegata")
    FlagDaSpedire: Optional[bool] = Field(None)
    DataSpedizione: Optional[date] = Field(None, description="Data di spedizione programmata")
    Fornitore: Optional[constr(min_length=1)] = Field(None)
    Applicazione: Optional[constr(min_length=1)] = Field(None)
    Interno: Optional[bool] = Field(None)
    IdTestoSMS: Optional[int] = Field(None)

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
        # parse DataSpedizione if present
        raw_ds = values.get('DataSpedizione')
        if isinstance(raw_ds, str):
            try:
                dt = datetime.fromisoformat(raw_ds.rstrip('Z'))
                values['DataSpedizione'] = dt.date()
            except (ValueError, TypeError):
                raise ValueError('invalid datetime format for DataSpedizione')
        return values

class SMSCreate(SMSBase):
    """
    Schema per creazione dell'SMS.
    """
    pass

class SMSResponse(SMSBase):
    """
    Schema di risposta per un SMS: include ID generato e numero di segmenti.
    """
    Id: int = Field(..., description="Chiave primaria generata dal DB")
    NrSMS: int = Field(..., description="Numero di segmenti SMS")

    model_config = { 'from_attributes': True }
