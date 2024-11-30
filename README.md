CPU Frequency Monitor and Adjuster

This is a Python application built using PyQt5 to monitor and dynamically adjust the CPU core frequencies. The application provides an intuitive interface for adjusting the minimum and maximum frequency limits for specific CPU cores, offering real-time monitoring of CPU performance.
Features

Real-time Monitoring: View the current frequencies of up to two CPU cores.
Dynamic Adjustment: Adjust the minimum and maximum frequencies of selected cores.
CPU Frequency Visualization: Visual representation of CPU cores with color-coded frequency ranges.
Multi-Core Support: Ability to adjust multiple CPU cores simultaneously.

Requirements

Python 3.x
PyQt5: For the graphical user interface.
psutil: For gathering system information (e.g., CPU frequencies).
cpupower: A utility for adjusting CPU frequencies (needs to be installed on the system).

Installation

Clone the repository:

git clone https://github.com/PablitoBueno/coreAdjust.git
cd cpu-frequency-adjuster

Install the required Python libraries:

pip install psutil PyQt5

Ensure that cpupower is installed on your system. You can install it using your package manager:

On Ubuntu/Debian-based systems:

sudo apt-get install linux-tools-common linux-tools-$(uname -r)

Run the application:

python cpu_adjuster_interface.py

Usage
Adjusting Frequencies

The application will display a graphical interface with options to set the minimum and maximum frequencies for the CPU cores.
Enter the desired minimum and maximum frequency (in MHz) for the cores you want to adjust.
Press the "Adjust Frequency" button to apply the changes.

Real-time Monitoring

The application updates the frequency of each core in real time and provides a visual representation of the frequency using color-coded indicators:

Low frequency: Blue
Medium frequency: Green
High frequency: Red

How It Works

CPUAdjuster Class: This class monitors and dynamically adjusts the CPU core frequencies based on the provided parameters (minimum and maximum frequencies, cores, and interval).
AdjustThread Class: Runs the adjustment process in a separate thread to prevent freezing the user interface.
CoreCanvas Class: Displays a graphical representation of CPU cores and their frequencies.

Contributing

Feel free to fork the repository, create issues, or send pull requests. Any improvements or bug fixes are welcome!
License
