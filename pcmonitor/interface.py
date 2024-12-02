import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QFrame, QGroupBox
)
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from coreAdjust import CPUMonitor  # Importando a classe CPUMonitor do coreAdjust.pyx

class AdjustThread(QThread):
    """
    Thread responsável por ajustar as frequências sem bloquear a interface.
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
            # Inicia o monitoramento e ajuste de frequências
            self.cpu_monitor.params = [[self.min_freq, self.max_freq, self.cores, 1]]  # Intervalo de 1 segundo
            self.cpu_monitor.monitor()
            self.update_signal.emit()  # Emite o sinal para atualizar a interface após o ajuste
        except Exception as e:
            print(f"Erro ao ajustar frequências: {e}")


class CPUAdjusterInterface(QWidget):
    def __init__(self, cpu_monitor: CPUMonitor):
        super().__init__()
        self.cpu_monitor = cpu_monitor

        # Configurações da janela principal
        self.setWindowTitle("CPU Frequency Monitor and Adjuster")
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("background-color: #1e1e2f; color: #e0e0e0;")

        # Layout principal
        main_layout = QVBoxLayout()

        # Cabeçalho
        header_label = QLabel("CPU Frequency Monitor and Adjuster")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #00bcd4;")
        main_layout.addWidget(header_label)

        # Canvas para visualização dos núcleos
        self.canvas = CoreCanvas()
        canvas_frame = QFrame()
        canvas_layout = QVBoxLayout(canvas_frame)
        canvas_layout.addWidget(self.canvas)
        main_layout.addWidget(canvas_frame)

        # Grupo de controle de frequências
        control_group = QGroupBox("    Frequency Adjustment")
        control_group.setStyleSheet("color: #00bcd4; font-weight: bold;")
        control_layout = QVBoxLayout()

        # Campos de entrada para frequências mínima e máxima
        freq_layout = QHBoxLayout()
        self.min_freq_input = QLineEdit()
        self.max_freq_input = QLineEdit()
        freq_layout.addWidget(QLabel("Min Freq:"))
        freq_layout.addWidget(self.min_freq_input)
        freq_layout.addWidget(QLabel("Max Freq:"))
        freq_layout.addWidget(self.max_freq_input)

        # Estilo dos campos de entrada
        for widget in [self.min_freq_input, self.max_freq_input]:
            widget.setStyleSheet(
                "background-color: #333344; color: #00bcd4; border: 1px solid #00bcd4; padding: 5px;"
            )

        control_layout.addLayout(freq_layout)

        # Botão para ajustar as frequências
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

        # Configurar o layout principal
        self.setLayout(main_layout)

        # Timer para monitoramento em tempo real das frequências
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frequencies)
        self.timer.start(1000)  # Atualizar a cada 1 segundo

    def update_frequencies(self):
        """
        Atualiza as frequências dos núcleos em tempo real na interface.
        """
        try:
            current_freqs = [psutil.cpu_freq(percpu=True)[core].current for core in range(psutil.cpu_count())]

            # Atualiza o canvas com gráficos e frequências dos núcleos
            for i, freq in enumerate(current_freqs[:2]):  # Exibindo até 2 núcleos
                self.canvas.update_core(i, freq)
        except Exception as e:
            print(f"Erro ao atualizar frequências: {e}")

    def start_adjusting_frequencies(self):
        """
        Inicia o ajuste das frequências em uma thread separada.
        """
        try:
            min_freq = int(self.min_freq_input.text())
            max_freq = int(self.max_freq_input.text())
            cores = [0, 1]  # Ajustando para dois núcleos

            # Cria e inicia a thread para ajustar as frequências
            self.adjust_thread = AdjustThread(self.cpu_monitor, min_freq, max_freq, cores)
            self.adjust_thread.update_signal.connect(self.update_frequencies)  # Atualizar as frequências após o ajuste
            self.adjust_thread.start()  # Iniciar a execução da thread

        except ValueError:
            print("Por favor, insira valores válidos para as frequências.")
        except Exception as e:
            print(f"Erro ao iniciar o ajuste de frequências: {e}")


class CoreCanvas(QWidget):
    """
    Canvas personalizado para exibir representações gráficas dos núcleos.
    """
    def __init__(self):
        super().__init__()
        self.core_colors = {0: QColor("#00587a"), 1: QColor("#00587a")}
        self.core_frequencies = {0: 0, 1: 0}
        self.setMinimumHeight(200)

    def update_core(self, core, freq):
        """
        Atualiza a frequência e a cor associada ao núcleo.
        """
        self.core_frequencies[core] = freq
        self.core_colors[core] = self.get_color_for_frequency(freq)
        self.update()

    def get_color_for_frequency(self, freq):
        """
        Retorna a cor de fundo com base na frequência.
        """
        if freq < 1500:
            return QColor("#00587a")  # Frequência baixa
        elif freq < 2500:
            return QColor("#00796b")  # Frequência média
        else:
            return QColor("#c62828")  # Frequência alta

    def paintEvent(self, event):
        """
        Método de desenho do núcleo.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensões do widget
        widget_width = self.width()
        widget_height = self.height()

        # Dimensões do núcleo
        core_width = 100
        core_height = 100
        spacing = 20  # Espaço entre os núcleos

        # Calculando as posições centrais
        total_width = 2 * core_width + spacing
        start_x = (widget_width - total_width) // 2
        start_y = (widget_height - core_height) // 2

        # Coordenadas dos núcleos
        rects = [
            (start_x, start_y, core_width, core_height, 0),  # Núcleo 0
            (start_x + core_width + spacing, start_y, core_width, core_height, 1),  # Núcleo 1
        ]

        for x, y, w, h, core in rects:
            # Desenha o núcleo
            painter.setBrush(self.core_colors[core])
            painter.drawRoundedRect(x, y, w, h, 15, 15)

            # Desenha o contorno do núcleo (laranja)
            painter.setPen(QColor("#ffa726"))  # Cor da borda laranja
            painter.setBrush(Qt.transparent)  # Preenchimento transparente para apenas a borda
            painter.drawRoundedRect(x, y, w, h, 15, 15)

            # Desenha a frequência dentro do núcleo
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.drawText(
                x + w // 2 - 30, y + h // 2, f"{self.core_frequencies[core]:.0f} MHz"
            )

            # Desenha o rótulo do núcleo
            painter.setPen(QColor("#ffa726"))
            painter.drawText(
                x + w // 2 - 20, y + h + 20, f"Core {core}"
            )


if __name__ == "__main__":
    input_params = [[1000, 3000, [0, 1], 1]]

    # Cria o objeto CPUMonitor
    cpu_monitor = CPUMonitor(input_params)

    # Inicia a aplicação PyQt5
    app = QApplication(sys.argv)
    interface = CPUAdjusterInterface(cpu_monitor)
    interface.show()
    sys.exit(app.exec_())
