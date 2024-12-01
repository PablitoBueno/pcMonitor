import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QFrame, QGroupBox
)
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from coreAdjust import CPUAdjuster  # Importing the compiled class from coreAdjust.pyx


class AdjustThread(QThread):
    """
    Thread responsible for adjusting frequencies without blocking the interface.
    """
    update_signal = pyqtSignal()

    def __init__(self, cpu_adjuster, min_freq, max_freq, cores):
        super().__init__()
        self.cpu_adjuster = cpu_adjuster
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.cores = cores

    def run(self):
        try:
            # Updates the parameters in CPUAdjuster and applies them
            self.cpu_adjuster.input_params = [[self.min_freq, self.max_freq, self.cores, 1]]  # 1-second interval
            self.cpu_adjuster.monitor_and_adjust()
            self.update_signal.emit()  # Emit signal to update the interface after adjustment
        except Exception as e:
            print(f"Error adjusting frequencies: {e}")


class CPUAdjusterInterface(QWidget):
    def __init__(self, cpu_adjuster: CPUAdjuster):
        super().__init__()
        self.cpu_adjuster = cpu_adjuster

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

        # Canvas for core visualization
        self.canvas = CoreCanvas()
        canvas_frame = QFrame()
        canvas_layout = QVBoxLayout(canvas_frame)
        canvas_layout.addWidget(self.canvas)
        main_layout.addWidget(canvas_frame)

        # Frequency control group box
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

        # Style adjustment for input fields
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

        # Configure the main layout
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

            # Update the canvas with graphics and core frequencies
            for i, freq in enumerate(current_freqs[:2]):  # Displaying up to 2 cores
                self.canvas.update_core(i, freq)
        except Exception as e:
            print(f"Error updating frequencies: {e}")

    def start_adjusting_frequencies(self):
        """
        Starts the frequency adjustment in a separate thread.
        """
        try:
            min_freq = int(self.min_freq_input.text())
            max_freq = int(self.max_freq_input.text())
            cores = [0, 1]  # Adjusting for two cores

            # Create and start the thread for adjusting frequencies
            self.adjust_thread = AdjustThread(self.cpu_adjuster, min_freq, max_freq, cores)
            self.adjust_thread.update_signal.connect(self.update_frequencies)  # Update frequencies after adjustment
            self.adjust_thread.start()  # Start thread execution

        except ValueError:
            print("Please enter valid frequency values.")
        except Exception as e:
            print(f"Error starting frequency adjustment: {e}")


class CoreCanvas(QWidget):
    """
    Custom canvas to display graphical representations of the cores.
    """
    def __init__(self):
        super().__init__()
        self.core_colors = {0: QColor("#00587a"), 1: QColor("#00587a")}
        self.core_frequencies = {0: 0, 1: 0}
        self.setMinimumHeight(200)

    def update_core(self, core, freq):
        """
        Updates the frequency and color associated with the core.
        """
        self.core_frequencies[core] = freq
        self.core_colors[core] = self.get_color_for_frequency(freq)
        self.update()

    def get_color_for_frequency(self, freq):
        """
        Returns a background color based on the frequency.
        """
        if freq < 1500:
            return QColor("#00587a")  # Low frequency
        elif freq < 2500:
            return QColor("#00796b")  # Medium frequency
        else:
            return QColor("#c62828")  # High frequency

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

        # Calculate central positions
        total_width = 2 * core_width + spacing
        start_x = (widget_width - total_width) // 2
        start_y = (widget_height - core_height) // 2

        # Core coordinates
        rects = [
            (start_x, start_y, core_width, core_height, 0),  # Core 0
            (start_x + core_width + spacing, start_y, core_width, core_height, 1),  # Core 1
        ]

        for x, y, w, h, core in rects:
            # Draw core
            painter.setBrush(self.core_colors[core])
            painter.drawRoundedRect(x, y, w, h, 15, 15)

            # Draw frequency inside the core
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.drawText(
                x + w // 2 - 30, y + h // 2, f"{self.core_frequencies[core]:.0f} MHz"
            )

            # Draw core label
            painter.setPen(QColor("#ffa726"))
            painter.drawText(
                x + w // 2 - 20, y + h + 20, f"Core {core}"
            )


if __name__ == "__main__":
    input_params = [[1000, 3000, [0, 1], 1]]

    # Create the CPUAdjuster object
    cpu_adjuster = CPUAdjuster(input_params)

    # Start the PyQt5 application
    app = QApplication(sys.argv)
    interface = CPUAdjusterInterface(cpu_adjuster)
    interface.show()
    sys.exit(app.exec_())
