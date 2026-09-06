from fastapi import FastAPI, HTTPException, Header, Depends
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

API_KEY = "geheimschluessel123"

def check_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Ungültiger API-Key")

def get_conn():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        dbname="blutspende",
        user="dbms10",
        password="dbms10pass"
    )

@app.get("/spender")
def list_spender():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM spender")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


from pydantic import BaseModel

class SpenderIn(BaseModel):
    vorname: str
    nachname: str
    geburtsdatum: str
    blutgruppe: str
    email: str

@app.post("/spender")
def create_spender(spender: SpenderIn, auth: None = Depends(check_api_key)):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO spender (vorname, nachname, geburtsdatum, blutgruppe, email) "
        "VALUES (%s, %s, %s, %s, %s) RETURNING *",
        (spender.vorname, spender.nachname, spender.geburtsdatum, spender.blutgruppe, spender.email)
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_row


class ZentrumIn(BaseModel):
    name: str
    adresse: str
    stadt: str

@app.post("/spendezentrum")
def create_zentrum(zentrum: ZentrumIn, auth: None = Depends(check_api_key)):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO spendezentrum (name, adresse, stadt) VALUES (%s, %s, %s) RETURNING *",
        (zentrum.name, zentrum.adresse, zentrum.stadt)
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_row

class SpendeIn(BaseModel):
    spender_id: int
    zentrum_id: int
    spende_datum: str
    menge_ml: int

@app.post("/spende")
def create_spende(spende: SpendeIn, auth: None = Depends(check_api_key)):	
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            "INSERT INTO spende (spender_id, zentrum_id, spende_datum, menge_ml) "
            "VALUES (%s, %s, %s, %s) RETURNING *",
            (spende.spender_id, spende.zentrum_id, spende.spende_datum, spende.menge_ml)
        )
        new_row = cur.fetchone()
        conn.commit()
        return new_row
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()


@app.get("/spendezentrum")
def list_zentrum():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM spendezentrum")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/spende")
def list_spende():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM spende")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

