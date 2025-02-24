# CPU Frequency Monitor and Adjuster

This Python application, developed with **PyQt5**, is designed to monitor and dynamically adjust CPU core frequencies in real-time. Tested on Linux systems with a dual-core processor, it demonstrates how to optimize performance even in resource-limited environments while providing a modern and intuitive interface.

## Features

- **Real-time Monitoring:**  
  Displays the current frequencies of up to 2 CPU cores, allowing dynamic performance tracking.

- **Dynamic Adjustment:**  
  Configure the minimum and maximum frequency limits for selected CPU cores, adapting performance to system conditions.

- **Graphical Visualization:**  
  Represents core frequencies with color-coded indicators:
  - **Blue:** Low frequency
  - **Green:** Medium frequency
  - **Red:** High frequency

- **Multi-Core Support (Modular):**  
  While tested on a dual-core processor, the code structure allows scalability for systems with more cores.

## Requirements

- **Python 3.x**
- **PyQt5:** Graphical user interface.
- **psutil:** System information gathering, such as CPU frequency monitoring.
- **cpupower:** A utility for adjusting CPU frequencies.  
  *Ensure that cpupower is installed on your system.*

## Installation and Execution

### 1. Clone the Repository

Clone the GitHub repository to your machine:

```bash
git clone https://github.com/PablitoBueno/coreAdjust.git
cd cpu-frequency-adjuster
```

### 2. Install Python Dependencies

Install the required libraries using pip:

```bash
pip install psutil PyQt5
```

### 3. Install cpupower

For Ubuntu/Debian-based systems, install cpupower using:

```bash
sudo apt-get install linux-tools-common linux-tools-$(uname -r)
```

### 4. Run the Application

Launch the application with:

```bash
python cpu_adjuster_interface.py
```

## Usage

### Adjusting Frequencies

1. **Intuitive Interface:**  
   Upon launching, the graphical interface displays options to set frequency limits.

2. **Configuring Values:**  
   Enter the desired minimum and maximum frequency values (in MHz) for the selected CPU cores.

3. **Applying Changes:**  
   Click the **"Adjust Frequency"** button to update CPU core frequencies in real time.

### Real-time Monitoring

- **Continuous Updates:**  
  The application constantly updates displayed frequencies for each core.
  
- **Visualization with CoreCanvas:**  
  The visualization panel uses a color-coded system to indicate frequency states:
  - **Blue:** Low frequency
  - **Green:** Medium frequency
  - **Red:** High frequency

## Internal Functionality

- **CPUAdjuster Class:**  
  Responsible for monitoring and adjusting core frequencies based on user-defined parameters (minimum and maximum limits, selected cores, and update interval). Even on a dual-core processor, this class efficiently manages resources.

- **AdjustThread Class:**  
  Runs the adjustment process in a separate thread, ensuring that the user interface remains responsive during frequency modifications.

- **CoreCanvas Class:**  
  Handles graphical rendering of CPU cores and their frequencies, using color indicators for clear performance visualization.

## Considerations on System Limitations

- **Linux Environment:**  
  Developed and tested specifically for Linux systems, the application relies on native tools like cpupower for frequency adjustments.

- **Dual-Core Processor:**  
  Despite hardware limitations, the application offers:
  - **Precise Monitoring:** Real-time tracking of the dual-core CPU frequency.
  - **Efficient Adjustments:** Smooth frequency management even with limited resources.
  - **Simple and Modern UI:** A practical solution that can be expanded for multi-core systems, showcasing the scalability of the design.
