import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, \
    QWidget
from PyQt5.QtCore import QTimer
from app_tracker import AppTracker


class AppTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tracker = AppTracker()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("App Usage Tracker")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Application", "Time (s)"])
        layout.addWidget(self.table)

        self.start_button = QPushButton("Start Tracking")
        self.start_button.clicked.connect(self.start_tracking)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Tracking")
        self.stop_button.clicked.connect(self.stop_tracking)
        layout.addWidget(self.stop_button)

        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)

        self.total_time_label = QLabel("Total Time: 0 s")
        layout.addWidget(self.total_time_label)

        self.avg_time_label = QLabel("Avg Time per Session: 0 s")
        layout.addWidget(self.avg_time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)

    def start_tracking(self):
        self.tracker.start_tracking()
        self.timer.start(1000)

    def stop_tracking(self):
        self.tracker.stop_tracking()
        self.timer.stop()

    def save_data(self):
        self.tracker.save_data()

    def load_data(self):
        self.tracker.load_data()
        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        usage = self.tracker.get_usage()
        for app, duration in usage.items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(app))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(duration)))
        self.update_statistics()

    def update_statistics(self):
        total_time = self.tracker.get_total_usage_time()
        avg_time = self.tracker.get_average_time_per_session()
        self.total_time_label.setText(f"Total Time: {total_time} s")
        self.avg_time_label.setText(f"Avg Time per Session: {avg_time:.2f} s")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = AppTrackerGUI()
    gui.show()
    sys.exit(app.exec_())
