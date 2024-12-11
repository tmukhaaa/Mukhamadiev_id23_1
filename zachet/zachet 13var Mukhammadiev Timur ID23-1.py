import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, \
    QSpinBox, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor


class ElevatorSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Симулятор лифта")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()
        self.reset_simulation()

    def init_ui(self):
        layout = QVBoxLayout()

        # Элементы управления
        controls_layout = QVBoxLayout()

        # Количество этажей
        floor_layout = QHBoxLayout()
        self.floor_label = QLabel("Количество этажей:")
        self.floor_spinbox = QSpinBox()
        self.floor_spinbox.setRange(2, 100)
        self.floor_spinbox.setValue(10)
        floor_layout.addWidget(self.floor_label)
        floor_layout.addWidget(self.floor_spinbox)
        controls_layout.addLayout(floor_layout)

        # Мощность двигателя
        power_layout = QHBoxLayout()
        self.power_label = QLabel("Мощность двигателя (P):")
        self.power_slider = QSlider()
        self.power_slider.setOrientation(1)  # Вертикальное расположение
        self.power_slider.setRange(1, 100)
        self.power_slider.setValue(50)
        power_layout.addWidget(self.power_label)
        power_layout.addWidget(self.power_slider)
        controls_layout.addLayout(power_layout)

        #груз
        weight_layout = QHBoxLayout()
        self.weight_label = QLabel("Вес груза (M):")
        self.weight_spinbox = QSpinBox()
        self.weight_spinbox.setRange(1, 5000)
        self.weight_spinbox.setValue(100)
        weight_layout.addWidget(self.weight_label)
        weight_layout.addWidget(self.weight_spinbox)
        controls_layout.addLayout(weight_layout)

        layout.addLayout(controls_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Начать анимацию")
        self.reset_button = QPushButton("Сбросить лифт")
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.reset_button)
        layout.addLayout(buttons_layout)

        # Отображение лифта
        self.elevator_display = ElevatorDisplay()
        layout.addWidget(self.elevator_display)

        self.central_widget.setLayout(layout)

        # Подключение кнопок
        self.start_button.clicked.connect(self.start_animation)
        self.reset_button.clicked.connect(self.reset_simulation)

    def reset_simulation(self):
        self.elevator_display.reset()

    def start_animation(self):
        num_floors = self.floor_spinbox.value()
        power = self.power_slider.value()
        weight = self.weight_spinbox.value()

        if weight == 0:
            speed = 0
        else:
            speed = power / weight

        self.elevator_display.start_moving(num_floors, speed)


class ElevatorDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.elevator_y = 0
        self.current_floor = 0
        self.direction = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.speed = 1
        self.num_floors = 10
        self.floor_height = 50
        self.stop_delay = 500  # Время остановки на каждом этаже (в миллисекундах)
        self.setFixedSize(200, 600)

    def reset(self):
        self.timer.stop()
        self.elevator_y = 0
        self.current_floor = 0
        self.direction = 1
        self.update()

    def start_moving(self, num_floors, speed):
        self.num_floors = num_floors
        self.speed = speed
        self.floor_height = self.height() / self.num_floors
        self.timer.start(50)

    def update_position(self):
        target_y = self.current_floor * self.floor_height

        if abs(self.elevator_y - target_y) < self.speed:
            self.elevator_y = target_y
            self.update()

            # Остановиться на этаже на короткое время
            self.timer.stop()
            QTimer.singleShot(self.stop_delay, self.move_to_next_floor)
        else:
            self.elevator_y += self.direction * self.speed
            self.update()

    def move_to_next_floor(self):
        if self.direction == 1 and self.current_floor < self.num_floors - 1:
            self.current_floor += 1
        elif self.direction == -1 and self.current_floor > 0:
            self.current_floor -= 1
        else:
            self.direction *= -1  # Изменить направление на верхнем или нижнем этаже
            self.current_floor += self.direction

        self.timer.start(50)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Рисуем шахту лифта
        painter.drawRect(50, 0, 100, self.height())

        # Рисуем этажи
        for i in range(self.num_floors):
            y = int(i * self.floor_height)
            painter.drawLine(50, y, 150, y)

        # Рисуем лифт
        elevator_rect = (50, int(self.elevator_y), 100, int(self.floor_height))

        # Устанавливаем красный цвет для лифта
        painter.setBrush(QColor(255, 0, 0))  # Красный цвет
        painter.drawRect(*elevator_rect)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulator = ElevatorSimulator()
    simulator.show()
    sys.exit(app.exec_())
