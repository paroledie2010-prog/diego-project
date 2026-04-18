from pydantic import BaseModel

class FraseCrear(BaseModel):
    texto: str
    autor: str = "Anónimo"
    categoria: str = "General"
    api_key: str

class FraseRespuesta(BaseModel):
    id: int
    texto: str
    autor: str
    categoria: str

    class Config:
        from_attributes = True