import datetime
from app.db import get_connection
from app.models.email import EMailCreate
from fastapi import HTTPException

import logging
logger = logging.getLogger("app.services.email")

def fetch_email(contatore: int):
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
            SELECT IdEMail, Agente, Data, Ora, NomeMittente, Mittente,
                   Destinatario, DestinatarioCC, Oggetto, Messaggio, Allegati,
                   MailerType, IdMessage, IdResponse, Response, Error,
                   Applicativo, IdPratica
              FROM dbo.tblEMail
             WHERE IdPratica = ?
        """, (contatore,))
        rows = cursor.fetchall()
        
        logger.info(f"[fetch_email] contatore={contatore}, righe raw={len(rows)}")
        for r in rows:
            logger.debug(r)

        # mappatura come prima…
        result = []
        for (
            idem, agente, data_sql, ora_sql, nome_mitt, mitt, dest, destcc,
            oggetto, mess, allegati, mailertype, idmsg, idresp,
            response, error, applic, idpr
        ) in rows:
            result.append({
                "IdEMail": idem,
                "Agente": agente,
                "Data": data_sql,
                "Ora": ora_sql,
                "NomeMittente": nome_mitt,
                "Mittente": mitt,
                "Destinatario": dest,
                "DestinatarioCC": destcc or None,
                "Oggetto": oggetto,
                "Messaggio": mess,
                "Allegati": allegati,
                "MailerType": mailertype,
                "IdMessage": idmsg,
                "IdResponse": idresp,
                "Response": response,
                "Error": error,
                "Applicativo": applic,
                "IdPratica": idpr
            })
        return result

def create_email(m: EMailCreate):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dbo.tblEMail (
                Agente, Data, Ora, NomeMittente, Mittente,
                Destinatario, DestinatarioCC, Oggetto, Messaggio, Allegati,
                MailerType, IdMessage, IdResponse, Response, Error,
                Applicativo, IdPratica
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, 
        m.Agente, m.Data, m.Ora, m.NomeMittente, m.Mittente,
        m.Destinatario, m.DestinatarioCC, m.Oggetto, m.Messaggio, m.Allegati,
        m.MailerType, m.IdMessage, m.IdResponse, m.Response, m.Error,
        m.Applicativo, m.IdPratica)
        
        cursor.execute("SELECT @@IDENTITY")
        new_id = cursor.fetchone()[0]
        return {**m.model_dump(), "IdEMail": new_id}