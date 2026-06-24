from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.aluno import AlunoAtualizar, AlunoCriar, AlunoResposta
from app.services.aluno import AlunoService

router = APIRouter(prefix="/alunos", tags=["Alunos"])


def get_aluno_service(db: AsyncSession = Depends(get_db)) -> AlunoService:
    return AlunoService(db)


@router.get("", response_model=list[AlunoResposta])
async def listar(service: AlunoService = Depends(get_aluno_service)):
    return await service.listar()


@router.get("/{matricula}", response_model=AlunoResposta)
async def buscar(matricula: int, service: AlunoService = Depends(get_aluno_service)):
    aluno = await service.buscar(matricula)
    if aluno is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado")
    return aluno


@router.post("", response_model=AlunoResposta, status_code=status.HTTP_201_CREATED)
async def criar(dados: AlunoCriar, service: AlunoService = Depends(get_aluno_service)):
    try:
        return await service.criar(dados)
    except ValueError as erro:
        raise HTTPException(status.HTTP_409_CONFLICT, str(erro))


@router.patch("/{matricula}", response_model=AlunoResposta)
async def atualizar(
    matricula: int,
    dados: AlunoAtualizar,
    service: AlunoService = Depends(get_aluno_service),
):
    aluno = await service.atualizar(matricula, dados)
    if aluno is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado")
    return aluno


@router.delete("/{matricula}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(matricula: int, service: AlunoService = Depends(get_aluno_service)):
    if not await service.deletar(matricula):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado")
