from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from entidade_receita import Receita
from banco_receitas import MiniBancoCSV
import csv
import io
import zipfile
import hashlib

# ----------------------------------------------------------
# Inicialização da API e do banco de dados
# ----------------------------------------------------------
app = FastAPI(title="API de Receitas Culinárias")

banco = MiniBancoCSV(
    "receitas.csv",
    "receitas.seq",
    ["nome", "ingredientes", "modo_preparo", "tempo_preparo", "dificuldade", "categoria"]
)

# ----------------------------------------------------------
# F1 — Inserir nova receita
# ----------------------------------------------------------
@app.post("/receitas")
def inserir_receita(receita: Receita):
    try:
        novo_id = banco.insert(receita.to_dict())
        return {"mensagem": "Receita inserida com sucesso!", "id": novo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------------
# F2 — Listar receitas com paginação
# ----------------------------------------------------------
@app.get("/receitas")
def listar_receitas(pagina: int = Query(1, ge=1), tamanho: int = Query(10, ge=1)):
    receitas = banco.get()
    inicio = (pagina - 1) * tamanho
    fim = inicio + tamanho
    return receitas[inicio:fim]


# ----------------------------------------------------------
# F5 — Exportar banco de dados em ZIP via streaming
# ----------------------------------------------------------
@app.get("/receitas/exportar-zip")
def exportar_receitas():
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=banco.fields)
        writer.writeheader()
        for row in banco.get(incluir_deletados=True):
            writer.writerow(row)
        zipf.writestr("receitas.csv", csv_buffer.getvalue().encode("utf-8"))

    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=receitas.zip"}
    )


# ----------------------------------------------------------
# F4 — Contagem de receitas
# ----------------------------------------------------------
@app.get("/receitas/count")
def contar_receitas():
    return {"quantidade": banco.count()}


# ----------------------------------------------------------
# F3 — CRUD completo
# ----------------------------------------------------------
@app.get("/receitas/{id}")
def obter_receita(id: int):
    registros = banco.get({"id": id})
    if not registros:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    return registros[0]


@app.put("/receitas/{id}")
def atualizar_receita(id: int, dados: Receita):
    if not banco.update(id, dados.to_dict()):
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    return {"mensagem": "Receita atualizada com sucesso!"}


@app.delete("/receitas/{id}")
def deletar_receita(id: int):
    if not banco.delete(id):
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    return {"mensagem": "Receita deletada (soft delete) com sucesso!"}


# ----------------------------------------------------------
# F6 — Gerar hash (MD5, SHA1, SHA256)
# ----------------------------------------------------------
@app.post("/hash")
def gerar_hash(dados: dict):
    """
    Gera o hash criptográfico (MD5, SHA1 ou SHA256) de um texto fornecido.
    Espera um JSON com as chaves 'texto' e 'metodo'.
    Exemplo: 
    {
    "texto": "string",
    "metodo": "md5"
    }
    """
    # Garante que 'texto' é uma string vazia se não for fornecido
    texto = dados.get("texto", "") 
    
    # Pega o método, usando 'md5' como padrão
    metodo = dados.get("metodo", "md5").lower() 

    if metodo not in ["md5", "sha1", "sha256"]:
        raise HTTPException(status_code=400, detail="Método de hash inválido. Use md5, sha1 ou sha256.")

    funcoes = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256
    }

    # Calcula o hash: 
    # 1. texto.encode(): Converte o texto para bytes
    # 2. funcoes[metodo](...): Chama a função de hash e processa os bytes
    # 3. .hexdigest(): Converte o resultado em uma string hexadecimal
    resultado = funcoes[metodo](texto.encode()).hexdigest()
    
    return {"metodo": metodo, "hash": resultado}



# ----------------------------------------------------------
# F7 — Executar Vacuum
# ----------------------------------------------------------
@app.post("/receitas/vacuum")
def executar_vacuum():
    
    banco.vacuum()
    return {"mensagem": "Operação de vacuum concluída. Registros deletados permanentemente removidos."}