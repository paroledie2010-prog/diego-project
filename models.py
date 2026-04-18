from sqlalchemy import Column, Integer, String
from database import Base

class Frase(Base):
    __tablename__ = "frases"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, nullable=False)
    autor = Column(String, default="Anónimo")
    categoria = Column(String, default="General")
    api_key = Column(String, nullable=False)