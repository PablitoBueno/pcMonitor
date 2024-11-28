# distutils: language_level=3
import psutil
cimport cython
from time import time, sleep
from libc.stdio cimport printf
import os

@cython.boundscheck(False)
@cython.wraparound(False)
def monitor_cpu_usage_advanced():
    num_cores = psutil.cpu_count(logical=True)
    cpu_usage_per_core = []
    start_time = time()

    core_usages = psutil.cpu_percent(interval=1, percpu=True)
    for i in range(num_cores):
        cpu_usage_per_core.append(core_usages[i])

    end_time = time()
    elapsed_time = end_time - start_time

    return cpu_usage_per_core, elapsed_time

def monitor_total_cpu_usage():
    return psutil.cpu_percent(interval=1)

def monitor_cpu_continuous(double interval):
    """
    Exibe continuamente o uso da CPU no terminal.
    :param interval: Intervalo em segundos entre as medições.
    """
    # Declarações no início da função
    cdef double total_usage_c
    cdef double elapsed_time_c
    cdef double usage_c
    cdef int i

    try:
        while True:
            # Obtém dados detalhados de uso
            per_core_usage, elapsed_time = monitor_cpu_usage_advanced()
            total_usage = monitor_total_cpu_usage()

            # Limpa a tela para exibição contínua
            os.system('cls' if os.name == 'nt' else 'clear')

            # Converte valores para tipos compatíveis com C
            total_usage_c = <double>total_usage
            elapsed_time_c = <double>elapsed_time

            # Exibe o uso total da CPU
            printf("=== Monitoramento Contínuo da CPU ===\n")
            printf("Uso total da CPU: %.2f%%\n", total_usage_c)
            printf("Tempo para medição: %.3f segundos\n\n", elapsed_time_c)

            # Exibe o uso por núcleo
            printf("Uso por núcleo:\n")
            for i, usage in enumerate(per_core_usage):
                usage_c = <double>usage
                printf("  Núcleo %d: %.2f%%\n", i + 1, usage_c)

            printf("\nPressione Ctrl+C para sair.\n\n")

            # Aguarda o intervalo antes da próxima medição
            sleep(interval)
    except KeyboardInterrupt:
        printf("\nMonitoramento interrompido pelo usuário.\n")
