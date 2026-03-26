import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Função que executa UM ping de forma assíncrona e ultra rápida
async def pingar(nome, ip):
    # -c 2 = Envia 2 pacotes
    # -W 0.9 = Timeout  
    # -i 1 = Intervalo entre pings 
    comando = ["ping", "-c", "2", "-i", "1", "-W", "0.9", ip]
    
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
        "ROUTER": "192.168.1.1",
        "ACCESS POINT": "192.168.1.3",
        "PE00QLAK": "192.168.1.10",
        "PE00QLAK_eth": "192.168.1.11",
        "ZENFONE": "192.168.1.12",
        "NOTE-MAE": "192.168.1.13",
        "NOTE-PAULA": "192.168.1.14",
        "NOTE-PAULA_eth": "192.168.1.15",
        "TV-MAE": "192.168.1.16",
        "TV-SALA": "192.168.1.17",
        "CEL-MAE": "192.168.1.18",
        "PLAYSTATION": "192.168.1.19"
    }
    
    # Dispara os 8 pings em paralelo
    tarefas = [pingar(nome, ip) for nome, ip in ativos.items()]
    resultados = await asyncio.gather(*tarefas)
    
    return {nome: status for nome, status in resultados}