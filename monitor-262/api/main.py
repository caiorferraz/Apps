import asyncio
import re
import time
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# --- CONFIGURAÇÕES FIXAS --- 
COUNT = "1"
TIMEOUT = "0.9" # Se não responder em 900ms, cancela para dar tempo do ciclo
INTERVAL = "0.1"

async def pingar(nome, ip):
    comando = ["ping", "-c", COUNT, "-W", TIMEOUT, ip]
    processo = await asyncio.create_subprocess_exec(
        *comando,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )
    stdout, _ = await processo.communicate()
    saida = stdout.decode()
    
    status = "ONLINE" if processo.returncode == 0 else "OFFLINE"
    tempos = re.findall(r'time=(\d+\.?\d*)', saida)
    
    # Arredondamento
    if tempos:
        val = float(tempos[0])
        latencia = round(val, 2) if val < 1 else int(round(val))
    else:
        latencia = None

    return nome, {"ip": ip, "status": status, "latencia": latencia}

@app.get("/status")
async def check_network():

    inicio_ciclo = time.time()

    ativos = {
        "DNS CLOUDFLARE": "1.1.1.1",
        "DNS GOOGLE": "8.8.8.8",
        "MODEM": "187.3.32.117",
        "ROTEADOR": "192.168.1.1",
        "ACCESS POINT": "192.168.1.3",
        "PE00QLAK": "192.168.1.10",        
        "ZENFONE": "192.168.1.12",
        "PE00QLAK_eth": "192.168.1.11",
        "REDMI10": "192.168.1.18",
        "TV32": "192.168.1.16",
        "NOTE-LENOVO": "192.168.1.13",
        "TV65": "192.168.1.17",
        "NOTE-ASUS": "192.168.1.14",
        "REDMI13": "192.168.1.20",
        "NOTE-ASUS_eth": "192.168.1.15",
        "PLAYSTATION": "192.168.1.19"
    }

    # Dispara todos os pings em paralelo
    tarefas = [pingar(nome, ip) for nome, ip in ativos.items()]
    resultados = await asyncio.gather(*tarefas)
    
    dados_finais = {nome: info for nome, info in resultados}

    # Calcula quanto tempo o processamento levou (ex: 0.1s ou 0.8s)
    tempo_gasto = time.time() - inicio_ciclo
    
    # O SEGREDO: Calcula quanto falta para completar 1.0 segundo
    tempo_de_espera = max(0, 1.0 - tempo_gasto)

    # Segura a resposta até completar o 1 segundo cravado
    await asyncio.sleep(tempo_de_espera)

    return dados_finais
