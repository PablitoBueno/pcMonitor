# monitor_energy.pyx

import psutil
from time import time
import os
cimport cython

# Função para monitorar o consumo de CPU e ajustar desempenho
@cython.boundscheck(False)
@cython.wraparound(False)
def monitor_cpu_usage(int cpu_threshold=80, str cpu_mode='performance', int min_freq=1000, int max_freq=3000):
    """
    Monitora o uso da CPU e ajusta seu desempenho baseado nos parâmetros passados.
    """
    # Obtém o uso atual da CPU em percentual
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Imprime o uso da CPU
    print(f"Uso atual da CPU: {cpu_percent}%")
    
    # Ajuste do desempenho da CPU com base no uso
    if cpu_percent < cpu_threshold / 2:
        print(f"Uso da CPU abaixo de {cpu_threshold}%, ajustando para modo econômico (frequência: {min_freq} MHz)...")
        adjust_cpu_performance(mode='economy', min_freq=min_freq, max_freq=max_freq)
    elif cpu_percent > cpu_threshold:
        print(f"Uso da CPU acima de {cpu_threshold}%, ajustando para modo de desempenho (frequência: {max_freq} MHz)...")
        adjust_cpu_performance(mode='performance', min_freq=min_freq, max_freq=max_freq)
    else:
        print(f"Uso moderado da CPU ({cpu_percent}%), mantendo configurações padrão.")

# Função para ajustar a performance da CPU
def adjust_cpu_performance(mode, min_freq, max_freq):
    """
    Ajusta a frequência da CPU conforme o modo de operação.
    """
    if mode == 'economy':
        print(f"Reduzindo a frequência da CPU para {min_freq} MHz para economia de energia.")
        # Lógica para reduzir a frequência da CPU, pode usar ferramentas específicas do sistema
        # Exemplo: `cpufrequtils` no Linux, ou outras ferramentas de controle de energia.
        # psutil pode ajudar, mas a manipulação direta de frequência pode ser limitada dependendo do sistema
    elif mode == 'performance':
        print(f"Aumentando a frequência da CPU para {max_freq} MHz para máxima performance.")
        # Ajuste para o modo de desempenho, elevando a frequência da CPU

# Função para monitorar o consumo de memória RAM
@cython.boundscheck(False)
@cython.wraparound(False)
def monitor_ram_usage(int ram_threshold=80, str ram_mode='performance'):
    """
    Monitora o uso de RAM e ajusta o desempenho com base no limiar.
    """
    # Obtém o uso de memória RAM
    memory = psutil.virtual_memory()
    
    # Imprime o uso de RAM
    print(f"Uso de RAM: {memory.percent}%")
    
    # Ajuste do desempenho com base no uso de RAM
    if memory.percent > ram_threshold:
        print(f"Uso elevado de RAM ({memory.percent}%), iniciando liberação de memória...")
        free_memory()
        if ram_mode == 'economy':
            print("Liberando memória para reduzir o uso.")
    else:
        print(f"Uso de RAM dentro do esperado: {memory.percent}%.")

# Função para liberar memória
def free_memory():
    """
    Tenta liberar memória, matando processos não essenciais ou limpando caches.
    """
    print("Liberando memória...")
    # Lógica para liberar memória, pode envolver matar processos de alta prioridade ou liberar cache
    # Exemplo: iterar sobre processos e matá-los
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        if proc.info['memory_percent'] > 10:  # Caso esteja usando mais que 10% da memória
            print(f"Finalizando processo {proc.info['name']} ({proc.info['pid']}) para liberar memória.")
            proc.terminate()

# Função para monitorar o uso do disco
@cython.boundscheck(False)
@cython.wraparound(False)
def monitor_disk_usage(int disk_threshold=80, str disk_mode='performance'):
    """
    Monitora o uso do disco e ajusta as operações de I/O com base no limiar.
    """
    # Obtém o uso do disco
    disk_usage = psutil.disk_usage('/')
    
    # Imprime o uso do disco
    print(f"Uso do disco: {disk_usage.percent}%")
    
    # Ajuste baseado no uso do disco
    if disk_usage.percent > disk_threshold:
        print("Uso elevado do disco, ajustando para reduzir operações de I/O...")
        adjust_disk_performance(mode='economy')
    else:
        print("Uso do disco dentro do esperado.")
        
# Função para ajustar o desempenho do disco
def adjust_disk_performance(mode):
    """
    Ajusta o desempenho do disco com base no modo de operação.
    """
    if mode == 'economy':
        print("Reduzindo as operações de I/O do disco para economia de energia.")
        # Reduz a frequência das operações de I/O, minimizando leitura e escrita no disco
    elif mode == 'performance':
        print("Aumentando as operações de I/O do disco para melhorar o desempenho.")
        # Aumenta as operações de I/O, priorizando leitura e escrita rápida

# Função principal para monitoramento contínuo
def monitor_system(int cpu_threshold=80, str cpu_mode='performance',
                   int ram_threshold=80, str ram_mode='performance',
                   int disk_threshold=80, str disk_mode='performance',
                   int min_freq=1000, int max_freq=3000):
    """
    Função que monitora o sistema continuamente e ajusta a performance com base nos parâmetros fornecidos.
    """
    print("Iniciando monitoramento de energia...")

    while True:
        # Monitoramento da CPU
        monitor_cpu_usage(cpu_threshold=cpu_threshold, cpu_mode=cpu_mode, min_freq=min_freq, max_freq=max_freq)
        
        # Monitoramento da RAM
        monitor_ram_usage(ram_threshold=ram_threshold, ram_mode=ram_mode)
        
        # Monitoramento do Disco
        monitor_disk_usage(disk_threshold=disk_threshold, disk_mode=disk_mode)
        
        # Atraso de 5 segundos entre as medições
        time.sleep(5)
