import sys
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QWidget


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def do_work(self):
        for i in range(1, 101):
            self.progress.emit(i)
            QThread.msleep(100)  # Simulate long-running task
        self.finished.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Threading Example")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Progress")
        layout.addWidget(self.label)

        self.button = QPushButton("Start Task")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.start_task)

        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.do_work)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

    def start_task(self):
        self.worker_thread.start()

    def update_progress(self, value):
        self.label.setText(f"Progress: {value}%")
        if value == 100:
            self.label.setText("Task Completed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
