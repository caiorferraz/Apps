import numpy as np
import scipy.fftpack
import time
import socket

# Configurações de áudio de alta precisão
SAMPLE_RATE = 44100  # Padrão de CD (ou 48000 se sua interface suportar)
BUFFER_SIZE = 4096   # Tamanho da janela para análise (maior = mais precisão, mas mais latência)

def analisar_harmonics(onda_sonora):
    """Disseca a onda para encontrar a fundamental e seus harmônicos"""
    # 1. Aplica a Transformada Rápida de Fourier (FFT)
    fft_result = scipy.fftpack.fft(onda_sonora)
    frequencies = scipy.fftpack.fftfreq(len(fft_result)) * SAMPLE_RATE
    
    # Pega apenas a parte positiva e a magnitude
    magnitudes = np.abs(fft_result)
    pos_mask = (frequencies > 0) & (frequencies < 2000) # Filtra até 2kHz (guitarra)
    
    final_freqs = frequencies[pos_mask]
    final_mags = magnitudes[pos_mask]
    
    # 2. Encontra os Picos de Frequência (Harmônicos)
    # Aqui não pegamos apenas o maior pico, pegamos os TOP 5
    peak_indices = np.argsort(final_mags)[-5:] # Índices dos 5 maiores picos
    picos = []
    
    for idx in peak_indices:
        picos.append({
            "freq": round(final_freqs[idx], 2),
            "mag": round(final_mags[idx], 4)
        })
    
    # Ordena os picos por frequência para identificar Fundamental, 2º, 3º...
    picos = sorted(picos, key=lambda x: x['freq'])
    
    fundamental = picos[0]['freq'] if picos else 0
    
    return {
        "fundamental": fundamental,
        "harmonics": picos,
        "timbre_signature": final_mags # Isso define o timbre da sua guitarra
    }

def analisar_sustain(mags_historico):
    """Analisa como a energia da fundamental cai ao longo do tempo ( Decay )"""
    if len(mags_historico) < 10: return 0
    
    # Cálculo de inclinação de reta (Regressão Linear Simples) no decay
    x = np.arange(len(mags_historico))
    y = np.array(mags_historico)
    
    # Quanto mais negativo o 'slope', mais rápido o sustain morre
    slope, intercept = np.polyfit(x, y, 1)
    return slope

# --- LOOP PRINCIPAL DO ANALISTA ---
def main():
    # Setup de rede para ouvir o Windows (via UDP)
    sock = socket.socket(socket.socket.AF_INET, socket.socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 12345)) # Ouve na porta do Docker
    
    mags_fundamental = [] # Para medir sustain
    last_print = time.time()
    
    print(f"✅ Analista de Áudio Operacional. Ouvindo stream UDP na porta 12345...")

    while True:
        # 1. Recebe o áudio bruto do Windows via Rede
        data, addr = sock.recvfrom(BUFFER_SIZE * 2) # *2 pq são shorts (16bit)
        onda_sonora = np.frombuffer(data, dtype=np.int16)
        
        # 2. Executa a análise de Harmônicos
        dados = analisar_harmonics(onda_sonora)
        
        # Guarda a magnitude da fundamental para cálculo de sustain
        if dados['harmonics']:
            mags_fundamental.append(dados['harmonics'][0]['mag'])
            if len(mags_fundamental) > 50: mags_fundamental.pop(0)
            
        # 3. Executa análise de Sustain (a cada 0.5s)
        if time.time() - last_print > 0.5:
            sustain_rate = analisar_sustain(mags_fundamental)
            
            # Print de debug no terminal do WSL
            if dados['fundamental'] > 50: # Se houver som
                print(f"--- ANÁLISE DE CORDA ---")
                print(f"🎵 Nota (Fundamental): {dados['fundamental']:.2f} Hz")
                print(f"📊 Harmônicos Detectados (Filtro < 2kHz):")
                for h in dados['harmonics']:
                    print(f"  > Freq: {h['freq']} Hz | Mag: {h['mag']}")
                print(f"⏳ Sustain (Decay Rate): {sustain_rate:.5f}")
                print(f"------------------------\n")
            
            last_print = time.time()

if __name__ == "__main__":
    main()import numpy as np
    import scipy.fftpack
    import time
    import socket
    
    # Configurações de áudio de alta precisão
    SAMPLE_RATE = 44100  # Padrão de CD (ou 48000 se sua interface suportar)
    BUFFER_SIZE = 4096   # Tamanho da janela para análise (maior = mais precisão, mas mais latência)
    
    def analisar_harmonics(onda_sonora):
        """Disseca a onda para encontrar a fundamental e seus harmônicos"""
        # 1. Aplica a Transformada Rápida de Fourier (FFT)
        fft_result = scipy.fftpack.fft(onda_sonora)
        frequencies = scipy.fftpack.fftfreq(len(fft_result)) * SAMPLE_RATE
        
        # Pega apenas a parte positiva e a magnitude
        magnitudes = np.abs(fft_result)
        pos_mask = (frequencies > 0) & (frequencies < 2000) # Filtra até 2kHz (guitarra)
        
        final_freqs = frequencies[pos_mask]
        final_mags = magnitudes[pos_mask]
        
        # 2. Encontra os Picos de Frequência (Harmônicos)
        # Aqui não pegamos apenas o maior pico, pegamos os TOP 5
        peak_indices = np.argsort(final_mags)[-5:] # Índices dos 5 maiores picos
        picos = []
        
        for idx in peak_indices:
            picos.append({
                "freq": round(final_freqs[idx], 2),
                "mag": round(final_mags[idx], 4)
            })
        
        # Ordena os picos por frequência para identificar Fundamental, 2º, 3º...
        picos = sorted(picos, key=lambda x: x['freq'])
        
        fundamental = picos[0]['freq'] if picos else 0
        
        return {
            "fundamental": fundamental,
            "harmonics": picos,
            "timbre_signature": final_mags # Isso define o timbre da sua guitarra
        }
    
    def analisar_sustain(mags_historico):
        """Analisa como a energia da fundamental cai ao longo do tempo ( Decay )"""
        if len(mags_historico) < 10: return 0
        
        # Cálculo de inclinação de reta (Regressão Linear Simples) no decay
        x = np.arange(len(mags_historico))
        y = np.array(mags_historico)
        
        # Quanto mais negativo o 'slope', mais rápido o sustain morre
        slope, intercept = np.polyfit(x, y, 1)
        return slope
    
    # --- LOOP PRINCIPAL DO ANALISTA ---
    def main():
        # Setup de rede para ouvir o Windows (via UDP)
        sock = socket.socket(socket.socket.AF_INET, socket.socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 12345)) # Ouve na porta do Docker
        
        mags_fundamental = [] # Para medir sustain
        last_print = time.time()
        
        print(f"✅ Analista de Áudio Operacional. Ouvindo stream UDP na porta 12345...")
    
        while True:
            # 1. Recebe o áudio bruto do Windows via Rede
            data, addr = sock.recvfrom(BUFFER_SIZE * 2) # *2 pq são shorts (16bit)
            onda_sonora = np.frombuffer(data, dtype=np.int16)
            
            # 2. Executa a análise de Harmônicos
            dados = analisar_harmonics(onda_sonora)
            
            # Guarda a magnitude da fundamental para cálculo de sustain
            if dados['harmonics']:
                mags_fundamental.append(dados['harmonics'][0]['mag'])
                if len(mags_fundamental) > 50: mags_fundamental.pop(0)
                
            # 3. Executa análise de Sustain (a cada 0.5s)
            if time.time() - last_print > 0.5:
                sustain_rate = analisar_sustain(mags_fundamental)
                
                # Print de debug no terminal do WSL
                if dados['fundamental'] > 50: # Se houver som
                    print(f"--- ANÁLISE DE CORDA ---")
                    print(f"🎵 Nota (Fundamental): {dados['fundamental']:.2f} Hz")
                    print(f"📊 Harmônicos Detectados (Filtro < 2kHz):")
                    for h in dados['harmonics']:
                        print(f"  > Freq: {h['freq']} Hz | Mag: {h['mag']}")
                    print(f"⏳ Sustain (Decay Rate): {sustain_rate:.5f}")
                    print(f"------------------------\n")
                
                last_print = time.time()
    
    if __name__ == "__main__":
        main()
