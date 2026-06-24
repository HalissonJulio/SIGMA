import asyncio

from sqlalchemy import func, select

from app.core.database import AsyncSessionLocal, Base, engine
from app.models.aluno import Aluno

# Listas para combinar e gerar nomes variados
NOMES = [
    "Zé",
    "Mané",
    "Maria",
    "João",
    "Ana",
    "Pedro",
    "Lucas",
    "Júlia",
    "Gabriel",
    "Beatriz",
    "Rafael",
    "Larissa",
    "Bruno",
    "Camila",
    "Felipe",
    "Mariana",
    "Gustavo",
    "Letícia",
    "Mateus",
    "Carolina",
    "Thiago",
    "Amanda",
]
SOBRENOMES = [
    "Silva",
    "Souza",
    "Costa",
    "Oliveira",
    "Santos",
    "Pereira",
    "Lima",
    "Almeida",
    "Ferreira",
    "Rodrigues",
    "Gomes",
    "Martins",
    "Araújo",
    "Ribeiro",
]


def gerar_alunos(quantidade: int) -> list[Aluno]:
    alunos = []
    for i in range(quantidade):
        nome = f"{NOMES[i % len(NOMES)]} {SOBRENOMES[i % len(SOBRENOMES)]}"
        matricula = 2024001 + i
        cpf = str(10000000000 + i).zfill(11)  # 11 dígitos, sequencial
        email = f"aluno{matricula}@email.com"
        telefone = f"119{str(90000000 + i).zfill(8)}"
        alunos.append(
            Aluno(
                matricula=matricula,
                nome=nome,
                cpf=cpf,
                email=email,
                telefone_responsavel=telefone,
            )
        )
    return alunos


async def popular():
    # garante que a tabela existe
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # só popula se a tabela estiver vazia (idempotente)
        total = await db.scalar(select(func.count()).select_from(Aluno))
        if total and total > 0:
            print(f"Banco já possui {total} alunos. Nada a fazer.")
            await engine.dispose()
            return

        alunos = gerar_alunos(50)
        db.add_all(alunos)
        await db.commit()
        print(f"{len(alunos)} alunos inseridos com sucesso.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(popular())
