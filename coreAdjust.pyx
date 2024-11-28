import psutil
import subprocess
import os
from libc.stdio cimport printf
from cython.parallel import prange
import time

class CPUAdjuster:
    """
    Classe para monitorar e ajustar dinamicamente a frequência dos núcleos da CPU.
    """
    def __init__(self, list input_params):
        """
        Inicializa o ajustador de CPU com os parâmetros fornecidos.

        Parâmetros:
        - input_params: Lista de listas, onde cada lista contém:
            [min_freq, max_freq, cores, interval]
        """
        self.input_params = input_params

    def check_permissions(self):
        """
        Verifica se o script tem permissões necessárias para executar alterações na CPU.
        """
        if os.geteuid() != 0:
            raise PermissionError("Permissões insuficientes! Este script precisa ser executado como root.")
        if subprocess.run("which cpupower", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
            raise FileNotFoundError("cpupower não encontrado! Certifique-se de que ele está instalado.")

    def adjust_frequency_to_limits(self, int min_freq, int max_freq, int core_id):
        """
        Ajusta a frequência de um núcleo para dentro dos limites especificados.

        Parâmetros:
        - min_freq: Frequência mínima permitida (em MHz).
        - max_freq: Frequência máxima permitida (em MHz).
        - core_id: ID do núcleo a ser ajustado.
        """
        try:
            self.check_permissions()
        except Exception as e:
            print(f"Erro: {str(e)}")
            return

        # Obter a frequência atual do núcleo
        current_freq = psutil.cpu_freq(percpu=True)[core_id].current

        # Ajustar a frequência para os limites especificados
        if current_freq < min_freq:
            subprocess.run(f"cpupower -c {core_id} frequency-set -d {min_freq}MHz -u {min_freq}MHz", shell=True)
        elif current_freq > max_freq:
            subprocess.run(f"cpupower -c {core_id} frequency-set -d {max_freq}MHz -u {max_freq}MHz", shell=True)

    def monitor_and_adjust(self):
        """
        Monitora e ajusta dinamicamente os núcleos com base nos parâmetros fornecidos.
        """
        while True:
            for param_set in self.input_params:
                min_freq, max_freq, cores, interval = param_set

                # Se cores for None, ajusta todos os núcleos
                if cores is None:
                    cores = range(psutil.cpu_count())  # Ajusta todos os núcleos

                # Ajusta cada núcleo especificado
                for core_id in cores:
                    self.adjust_frequency_to_limits(min_freq, max_freq, core_id)

            # Aguarda o intervalo antes de realizar a próxima verificação
            time.sleep(interval)
