from pydantic import BaseModel, ConfigDict, EmailStr


class AlunoBase(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
    telefone_responsavel: str


class AlunoCriar(AlunoBase):
    matricula: int


class AlunoResposta(AlunoBase):
    matricula: int
    model_config = ConfigDict(from_attributes=True)


class AlunoAtualizar(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    email: EmailStr | None = None
    telefone_responsavel: str | None = None
