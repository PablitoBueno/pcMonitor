# distutils: language=c++
# distutils: boundscheck=False

from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string
import time  # Importando o módulo time diretamente para usar sleep

cdef extern from "cpu_utils.hpp":
    void set_governor(int core_id, const char* governor)
    void adjust_freq(int core_id, int min_freq, int max_freq)
    cdef vector[pair[string, float]] get_temperatures()  # Correção aqui

class CPUMonitor:
    def __init__(self, params):
        self.params = params

    def set_governor(self, int core_id, str governor):
        try:
            set_governor(core_id, governor.encode('utf-8'))
        except Exception as e:
            print(f"Erro ao definir governador: {str(e)}")

    def adjust_freq(self, int min_freq, int max_freq, int core_id):
        try:
            adjust_freq(core_id, min_freq, max_freq)
        except Exception as e:
            print(f"Erro ao ajustar frequência: {str(e)}")

    def get_temp(self):
        cdef vector[pair[string, float]] temps
        cdef dict result = {}

        try:
            temps = get_temperatures()
            for i in range(len(temps)):
                result[temps[i].first] = temps[i].second
            return result
        except Exception as e:
            print(f"Erro ao obter temperaturas: {str(e)}")
            return None

    def monitor(self):
        while True:
            for min_freq, max_freq, cores, interval in self.params:
                if cores is None:
                    cores = range(4)  # Assumindo 4 núcleos para simplificação

                for core_id in cores:
                    self.adjust_freq(min_freq, max_freq, core_id)

            temps = self.get_temp()
            if temps:
                print(f"Temperaturas dos núcleos: {temps}")

            time.sleep(interval)  # Usando time.sleep, que é a maneira correta no Cython
