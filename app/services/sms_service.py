from datetime import datetime
from app.db import get_connection
from app.models.sms import SMSCreate
from fastapi import HTTPException

def fetch_sms(contatore: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verifica che la pratica esista
        cursor.execute(
            "SELECT 1 FROM [tabella pratiche] WHERE contatore = ?",
            (contatore,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail=f"Pratica con contatore={contatore} non trovata"
            )
        
        cursor.execute("""
            SELECT Id, Data, Ora, CodAg, Mittente, Destinatario,
                   NrTel, Testo, IdSpedizione, Stato, FlagAuto, IdPratica,
                   FlagDaSpedire, DataSpedizione, Fornitore, Applicazione,
                   Interno, IdTestoSMS,
                   NrSMS
              FROM dbo.sms
             WHERE IdPratica = ?
        """, (contatore,))
        rows = cursor.fetchall()
        cols = ["Id","Data","Ora","CodAg","Mittente","Destinatario",
                "NrTel","Testo","IdSpedizione","Stato","FlagAuto","IdPratica",
                "FlagDaSpedire","DataSpedizione","Fornitore","Applicazione",
                "Interno","IdTestoSMS","NrSMS"]
        return [dict(zip(cols, row)) for row in rows]

def create_sms(s: SMSCreate):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dbo.sms (
                Data, Ora, CodAg, Mittente, Destinatario,
                NrTel, Testo, IdSpedizione, Stato, FlagAuto,
                IdPratica, FlagDaSpedire, DataSpedizione, Fornitore,
                Applicazione, Interno, IdTestoSMS
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        s.Data, s.Ora, s.CodAg, s.Mittente, s.Destinatario,
        s.NrTel, s.Testo, s.IdSpedizione, s.Stato, s.FlagAuto,
        s.IdPratica, s.FlagDaSpedire, s.DataSpedizione, s.Fornitore,
        s.Applicazione, s.Interno, s.IdTestoSMS)
        
        cursor.execute("SELECT @@IDENTITY")
        new_id = cursor.fetchone()[0]
        # NrSMS è calcolato in DB
        cursor.execute("SELECT NrSMS FROM dbo.sms WHERE Id = ?", new_id)
        nr_sms = cursor.fetchone()[0]
        result = s.model_dump()
        result.update({"Id": new_id, "NrSMS": nr_sms})
        return result
