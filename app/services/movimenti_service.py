from app.db import get_connection
from app.models.movimenti import Movimento, MovimentoCreate
from fastapi import HTTPException

def fetch_movimenti_by_pratica(idpratica: int) -> list[Movimento]:
    """
    Recupera tutti i movimenti associati a una pratica e restituisce una lista di modelli.
    Se la pratica non esiste, solleva 404.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verifica che la pratica esista
        cursor.execute(
            "SELECT 1 FROM [tabella pratiche] WHERE contatore = ?",
            (idpratica,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail=f"Pratica con contatore={idpratica} non trovata"
            )
        
        # Recupera i movimenti
        cursor.execute("""
            SELECT
                ID,
                Data,
                Ora,
                IdPratica,
                CodAgenzia,
                CodEsa,
                NomeAg,
                Esito,
                DescrEsito,
                FlagEsito,
                Note,
                DataPag,
                ImportoPag,
                OraRecall,
                Tel1
            FROM [Movimenti]
            WHERE IdPratica = ?
        """, (idpratica,))
        rows = cursor.fetchall()

        movimenti = []
        for row in rows:
            movimenti.append(
                Movimento(
                    id=int(row[0]),   
                    data=row[1],
                    ora=row[2],
                    contatore=row[3],
                    codagenzia=row[4],
                    codesa=row[5],
                    nomeag=row[6],
                    esito=row[7],
                    descresito=row[8],
                    flagesito=row[9],
                    note=row[10],
                    datapag=row[11],
                    importopag=row[12],
                    orarecall=row[13],
                    tel1=row[14],
                )
            )
        return movimenti

def create_movimento_entry(mov: MovimentoCreate) -> Movimento:
    """
    Inserisce un nuovo movimento:
      - Verifica che la pratica esista (contatore valido)
      - Esegue l'INSERT
      - Restituisce il Movimento con l'ID generato
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1) Verifica esistenza della pratica
        cursor.execute(
            "SELECT 1 FROM [tabella pratiche] WHERE contatore = ?",
            (mov.contatore,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=400,
                detail=f"Pratica con contatore={mov.contatore} non trovata"
            )

        # 2) Inserimento del movimento
        cursor.execute("""
            INSERT INTO [Movimenti]
              (Data, Ora, IdPratica, CodAgenzia, CodEsa, NomeAg, Esito, DescrEsito, FlagEsito, Note, DataPag, ImportoPag, OraRecall, Tel1)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mov.data,
            mov.ora,
            mov.contatore,
            mov.codagenzia,
            mov.codesa,
            mov.nomeag,
            mov.esito,
            mov.descresito,
            mov.flagesito,
            mov.note,
            mov.datapag,
            mov.importopag,
            mov.orarecall,
            mov.tel1
        ))
        
        # Recupera l'ID generato
        new_id_decimal = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
        new_id = int(new_id_decimal)   # <-- cast esplicito a int

        # Crea e restituisci il Movimento completo con l'ID
        return Movimento(
            id=new_id,
            data=mov.data,
            ora=mov.ora,
            contatore=mov.contatore,
            codagenzia=mov.codagenzia,
            codesa=mov.codesa,
            nomeag=mov.nomeag,
            esito=mov.esito,
            descresito=mov.descresito,
            flagesito=mov.flagesito,
            note=mov.note,
            datapag=mov.datapag,
            importopag=mov.importopag,
            orarecall=mov.orarecall,
            tel1=mov.tel1
        )
