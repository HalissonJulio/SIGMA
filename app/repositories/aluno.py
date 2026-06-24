from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aluno import Aluno


class AlunoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def listar(self) -> list[Aluno]:
        resultado = await self.db.execute(select(Aluno))
        return list(resultado.scalars().all())

    async def buscar_por_matricula(self, matricula: int) -> Aluno | None:
        resultado = await self.db.execute(
            select(Aluno).where(Aluno.matricula == matricula)
        )
        return resultado.scalar_one_or_none()

    async def criar(self, aluno: Aluno) -> Aluno:
        self.db.add(aluno)
        await self.db.commit()
        await self.db.refresh(aluno)
        return aluno

    async def atualizar(self, aluno: Aluno) -> Aluno:
        await self.db.commit()
        await self.db.refresh(aluno)
        return aluno

    async def deletar(self, aluno: Aluno) -> None:
        await self.db.delete(aluno)
        await self.db.commit()
