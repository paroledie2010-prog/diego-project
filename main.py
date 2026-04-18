from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, random

# Crea las tablas en la base de datos automáticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# API keys válidas (por ahora las ponemos aquí, después las movemos a la base de datos)
API_KEYS_VALIDAS = ["clave123", "clave456"]

def verificar_api_key(api_key: str):
    if api_key not in API_KEYS_VALIDAS:
        raise HTTPException(status_code=403, detail="API key inválida")

# ── ENDPOINTS ──────────────────────────────────────────

# Devuelve todas las frases
@app.get("/frases", response_model=list[schemas.FraseRespuesta])
def obtener_frases(db: Session = Depends(get_db)):
    return db.query(models.Frase).all()

# Devuelve una frase aleatoria
@app.get("/frases/random", response_model=schemas.FraseRespuesta)
def frase_aleatoria(db: Session = Depends(get_db)):
    frases = db.query(models.Frase).all()
    if not frases:
        raise HTTPException(status_code=404, detail="No hay frases todavía")
    return random.choice(frases)

# Devuelve frases por categoría
@app.get("/frases/categoria/{categoria}", response_model=list[schemas.FraseRespuesta])
def frases_por_categoria(categoria: str, db: Session = Depends(get_db)):
    frases = db.query(models.Frase).filter(models.Frase.categoria == categoria).all()
    if not frases:
        raise HTTPException(status_code=404, detail="No hay frases en esa categoría")
    return frases

# Agrega una frase nueva (requiere api key)
@app.post("/frases", response_model=schemas.FraseRespuesta)
def agregar_frase(frase: schemas.FraseCrear, db: Session = Depends(get_db)):
    verificar_api_key(frase.api_key)
    nueva = models.Frase(
        texto=frase.texto,
        autor=frase.autor,
        categoria=frase.categoria,
        api_key=frase.api_key
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# Elimina una frase (requiere api key)
@app.delete("/frases/{id}")
def eliminar_frase(id: int, api_key: str, db: Session = Depends(get_db)):
    verificar_api_key(api_key)
    frase = db.query(models.Frase).filter(models.Frase.id == id).first()
    if not frase:
        raise HTTPException(status_code=404, detail="Frase no encontrada")
    db.delete(frase)
    db.commit()
    return {"mensaje": "Frase eliminada"}