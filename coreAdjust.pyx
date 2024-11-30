import psutil
import subprocess
import os
from libc.stdio cimport printf
from cython.parallel import prange
import time

class CPUAdjuster:
    """
    Class to monitor and dynamically adjust the CPU core frequencies.
    """
    def __init__(self, list input_params):
        """
        Initializes the CPU adjuster with the provided parameters.

        Parameters:
        - input_params: A list of lists, where each list contains:
            [min_freq, max_freq, cores, interval]
        """
        self.input_params = input_params

    def check_permissions(self):
        """
        Checks if the script has the necessary permissions to make changes to the CPU.
        """
        if os.geteuid() != 0:
            raise PermissionError("Insufficient permissions! This script needs to be run as root.")
        if subprocess.run("which cpupower", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
            raise FileNotFoundError("cpupower not found! Please ensure it is installed.")

    def adjust_frequency_to_limits(self, int min_freq, int max_freq, int core_id):
        """
        Adjusts the frequency of a core to the specified limits.

        Parameters:
        - min_freq: Minimum allowed frequency (in MHz).
        - max_freq: Maximum allowed frequency (in MHz).
        - core_id: The core ID to be adjusted.
        """
        try:
            self.check_permissions()
        except Exception as e:
            print(f"Error: {str(e)}")
            return

        # Get the current frequency of the core
        current_freq = psutil.cpu_freq(percpu=True)[core_id].current

        # Adjust the frequency to the specified limits
        if current_freq < min_freq:
            subprocess.run(f"cpupower -c {core_id} frequency-set -d {min_freq}MHz -u {min_freq}MHz", shell=True)
        elif current_freq > max_freq:
            subprocess.run(f"cpupower -c {core_id} frequency-set -d {max_freq}MHz -u {max_freq}MHz", shell=True)

    def monitor_and_adjust(self):
        """
        Monitors and dynamically adjusts the cores based on the provided parameters.
        """
        while True:
            for param_set in self.input_params:
                min_freq, max_freq, cores, interval = param_set

                # If cores is None, adjust all cores
                if cores is None:
                    cores = range(psutil.cpu_count())  # Adjust all cores

                # Adjust each specified core
                for core_id in cores:
                    self.adjust_frequency_to_limits(min_freq, max_freq, core_id)

            # Wait for the specified interval before making the next adjustment
            time.sleep(interval)
