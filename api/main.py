import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Função que executa UM ping de forma assíncrona e ultra rápida
async def pingar(nome, ip):
    # -c 1 = Apenas 1 pacote
    # -W 1 = Timeout de 1 segundo (não espera uma eternidade se estiver offline)
    comando = ["ping", "-c", "1", "-W", "1", ip]
    
    processo = await asyncio.create_subprocess_exec(
        *comando,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    
    # O status agora é silencioso, mas a lógica de cor no JS continuará funcionando
    return nome, "ONLINE" if await processo.wait() == 0 else "OFFLINE"

@app.get("/status")
async def check_network():
    ativos = {
        "PE00QLAK": "192.168.1.10",
        "PE00QLAK_eth": "192.168.1.11",
        "ZENFONE": "192.168.1.12",
        "NOTE-MAE": "192.168.1.13",
        "NOTE-PAULA": "192.168.1.14",
        "NOTE-PAULA_eth": "192.168.1.15",
        "TV-MAE": "192.168.1.16",
        "TV-SALA": "192.168.1.17"
    }
    
    # Dispara os 8 pings em paralelo
    tarefas = [pingar(nome, ip) for nome, ip in ativos.items()]
    resultados = await asyncio.gather(*tarefas)
    
    return {nome: status for nome, status in resultados}