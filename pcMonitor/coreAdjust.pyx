# distutils: language=c++
# distutils: boundscheck=False

from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string
import time  # Importing the time module directly to use sleep

cdef extern from "cpu_utils.hpp":
    void set_governor(int core_id, const char* governor)
    void adjust_freq(int core_id, int min_freq, int max_freq)

class CPUMonitor:
    def __init__(self, params):
        self.params = params

    def set_governor(self, int core_id, str governor):
        try:
            set_governor(core_id, governor.encode('utf-8'))
        except Exception as e:
            print(f"Error setting governor: {str(e)}")

    def adjust_freq(self, int min_freq, int max_freq, int core_id):
        try:
            adjust_freq(core_id, min_freq, max_freq)
        except Exception as e:
            print(f"Error adjusting frequency: {str(e)}")

    def monitor(self):
        while True:
            for min_freq, max_freq, cores, interval in self.params:
                if cores is None:
                    cores = range(4)  # Assuming 4 cores for simplicity

                for core_id in cores:
                    self.adjust_freq(min_freq, max_freq, core_id)

            time.sleep(interval)  # Using time.sleep, which is the correct approach in Cython
