import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QFrame, QGroupBox
)
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from coreAdjust import CPUMonitor  # Importing the CPUMonitor class from coreAdjust.pyx

class AdjustThread(QThread):
    """
    Thread responsible for adjusting frequencies without blocking the interface.
    """
    update_signal = pyqtSignal()

    def __init__(self, cpu_monitor, min_freq, max_freq, cores):
        super().__init__()
        self.cpu_monitor = cpu_monitor
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.cores = cores

    def run(self):
        try:
            # Start monitoring and adjusting frequencies
            self.cpu_monitor.params = [[self.min_freq, self.max_freq, self.cores, 1]]  # Interval of 1 second
            self.cpu_monitor.monitor()
            self.update_signal.emit()  # Emit signal to update the interface after adjustment
        except Exception as e:
            print(f"Error adjusting frequencies: {e}")


class CPUAdjusterInterface(QWidget):
    def __init__(self, cpu_monitor: CPUMonitor):
        super().__init__()
        self.cpu_monitor = cpu_monitor

        # Main window settings
        self.setWindowTitle("CPU Frequency Monitor and Adjuster")
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("background-color: #1e1e2f; color: #e0e0e0;")

        # Main layout
        main_layout = QVBoxLayout()

        # Header
        header_label = QLabel("CPU Frequency Monitor and Adjuster")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #00bcd4;")
        main_layout.addWidget(header_label)

        # Canvas for displaying core visuals
        self.canvas = CoreCanvas()
        canvas_frame = QFrame()
        canvas_layout = QVBoxLayout(canvas_frame)
        canvas_layout.addWidget(self.canvas)
        main_layout.addWidget(canvas_frame)

        # Frequency adjustment control group
        control_group = QGroupBox("    Frequency Adjustment")
        control_group.setStyleSheet("color: #00bcd4; font-weight: bold;")
        control_layout = QVBoxLayout()

        # Input fields for minimum and maximum frequencies
        freq_layout = QHBoxLayout()
        self.min_freq_input = QLineEdit()
        self.max_freq_input = QLineEdit()
        freq_layout.addWidget(QLabel("Min Freq:"))
        freq_layout.addWidget(self.min_freq_input)
        freq_layout.addWidget(QLabel("Max Freq:"))
        freq_layout.addWidget(self.max_freq_input)

        # Styling for input fields
        for widget in [self.min_freq_input, self.max_freq_input]:
            widget.setStyleSheet(
                "background-color: #333344; color: #00bcd4; border: 1px solid #00bcd4; padding: 5px;"
            )

        control_layout.addLayout(freq_layout)

        # Button to adjust frequencies
        self.adjust_button = QPushButton("Adjust Frequency")
        self.adjust_button.setStyleSheet("""
            QPushButton {
                background-color: #00bcd4;
                color: #1e1e2f;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0288d1;
            }
        """)
        self.adjust_button.clicked.connect(self.start_adjusting_frequencies)
        control_layout.addWidget(self.adjust_button)

        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

        # Set the main layout
        self.setLayout(main_layout)

        # Timer for real-time frequency monitoring
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frequencies)
        self.timer.start(1000)  # Update every 1 second

    def update_frequencies(self):
        """
        Updates the core frequencies in real-time on the interface.
        """
        try:
            current_freqs = [psutil.cpu_freq(percpu=True)[core].current for core in range(psutil.cpu_count())]

            # Update the canvas with core frequency visuals
            for i, freq in enumerate(current_freqs[:2]):  # Displaying up to 2 cores
                self.canvas.update_core(i, freq)
        except Exception as e:
            print(f"Error updating frequencies: {e}")

    def start_adjusting_frequencies(self):
        """
        Starts adjusting the frequencies in a separate thread.
        """
        try:
            min_freq = int(self.min_freq_input.text())
            max_freq = int(self.max_freq_input.text())
            cores = [0, 1]  # Adjusting for two cores

            # Create and start the thread to adjust frequencies
            self.adjust_thread = AdjustThread(self.cpu_monitor, min_freq, max_freq, cores)
            self.adjust_thread.update_signal.connect(self.update_frequencies)  # Update frequencies after adjustment
            self.adjust_thread.start()  # Start the thread execution

        except ValueError:
            print("Please enter valid frequency values.")
        except Exception as e:
            print(f"Error starting frequency adjustment: {e}")


class CoreCanvas(QWidget):
    """
    Custom canvas to display graphical representations of cores.
    """
    def __init__(self):
        super().__init__()
        self.core_colors = {0: QColor("#00587a"), 1: QColor("#00587a")}
        self.core_frequencies = {0: 0, 1: 0}
        self.core_temperatures = {0: 0, 1: 0}
        self.setMinimumHeight(200)

    def update_core(self, core, freq):
        """
        Updates the frequency and temperature associated with the core.
        """
        self.core_frequencies[core] = freq
        self.core_colors[core] = self.get_color_for_frequency(freq)
        self.core_temperatures[core] = self.get_temperature_for_core(core)
        self.update()

    def get_color_for_frequency(self, freq):
        """
        Returns the background color based on the frequency, with a broader range of colors.
        """
        if freq < 1000:
            return QColor("#003d5c")  # Very low frequency (Dark Blue)
        elif freq < 1200:
            return QColor("#00587a")  # Low frequency (Blue)
        elif freq < 1500:
            return QColor("#00796b")  # Low to medium frequency (Dark Green)
        elif freq < 1800:
            return QColor("#4caf50")  # Medium frequency (Green)
        elif freq < 2000:
            return QColor("#8bc34a")  # Medium-high frequency (Light Green)
        elif freq < 2200:
            return QColor("#fdd835")  # High frequency (Yellow)
        elif freq < 2500:
            return QColor("#ff9800")  # Very high frequency (Orange)
        elif freq < 2800:
            return QColor("#f44336")  # Extremely high frequency (Red)
        else:
            return QColor("#c62828")  # Critical frequency (Dark Red)

    def get_temperature_for_core(self, core):
        """
        Returns the temperature for the specified core.
        """
        try:
            temps = psutil.sensors_temperatures().get('coretemp', [])
            if temps:
                # Finding the temperature for the specific core
                return temps[core].current
            else:
                return 0
        except (IndexError, KeyError):
            return 0

    def paintEvent(self, event):
        """
        Core drawing method.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Widget dimensions
        widget_width = self.width()
        widget_height = self.height()

        # Core dimensions
        core_width = 100
        core_height = 100
        spacing = 20  # Space between cores

        # Calculating central positions
        total_width = 2 * core_width + spacing
        start_x = (widget_width - total_width) // 2
        start_y = (widget_height - core_height) // 2

        # Core coordinates
        rects = [
            (start_x, start_y, core_width, core_height, 0),  # Core 0
            (start_x + core_width + spacing, start_y, core_width, core_height, 1),  # Core 1
        ]

        for x, y, w, h, core in rects:
            # Drawing the core
            painter.setBrush(self.core_colors[core])
            painter.drawRoundedRect(x, y, w, h, 15, 15)

            # Drawing the core border (orange)
            painter.setPen(QColor("#ffa726"))  # Border color (Orange)
            painter.setBrush(Qt.transparent)  # Transparent fill for the border
            painter.drawRoundedRect(x, y, w, h, 15, 15)

            # Drawing the frequency inside the core
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.drawText(
                x + w // 2 - 30, y + h // 2, f"{self.core_frequencies[core]:.0f} MHz"
            )

            # Drawing the temperature inside the core
            painter.setPen(QColor("#ff7043"))
            painter.drawText(
                x + w // 2 - 30, y + h // 2 + 20, f"    {self.core_temperatures[core]:.0f}°C"
            )

            # Drawing the core label
            painter.setPen(QColor("#ffa726"))
            painter.drawText(
                x + w // 2 - 20, y + h + 20, f"Core {core}"
            )


if __name__ == "__main__":
    input_params = [[1000, 3000, [0, 1], 1]]  # Set frequency parameters

    # Create the CPUMonitor object
    cpu_monitor = CPUMonitor(input_params)

    # Start the PyQt5 application
    app = QApplication(sys.argv)
    interface = CPUAdjusterInterface(cpu_monitor)
    interface.show()
    sys.exit(app.exec_())
