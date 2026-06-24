from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Aluno(Base):
    __tablename__ = "aluno"

    matricula: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str | None] = mapped_column(String)
    cpf: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String)
    telefone_responsavel: Mapped[str | None] = mapped_column(String)
