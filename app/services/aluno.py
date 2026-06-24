from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aluno import Aluno
from app.repositories.aluno import AlunoRepository
from app.schemas.aluno import AlunoAtualizar, AlunoCriar


class AlunoService:
    def __init__(self, db: AsyncSession):
        self.repo = AlunoRepository(db)

    async def listar(self) -> list[Aluno]:
        return await self.repo.listar()

    async def buscar(self, matricula: int) -> Aluno | None:
        return await self.repo.buscar_por_matricula(matricula)

    async def criar(self, dados: AlunoCriar) -> Aluno:
        existente = await self.repo.buscar_por_matricula(dados.matricula)
        if existente is not None:
            raise ValueError("Já existe um aluno com essa matrícula")

        novo_aluno = Aluno(**dados.model_dump())
        return await self.repo.criar(novo_aluno)

    async def atualizar(self, matricula: int, dados: AlunoAtualizar) -> Aluno | None:
        aluno = await self.repo.buscar_por_matricula(matricula)
        if aluno is None:
            return None

        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(aluno, campo, valor)

        return await self.repo.atualizar(aluno)

    async def deletar(self, matricula: int) -> bool:
        aluno = await self.repo.buscar_por_matricula(matricula)
        if aluno is None:
            return False

        await self.repo.deletar(aluno)
        return True
