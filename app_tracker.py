import time
import psutil
import win32gui
import win32process
import threading
import json
import os


class AppTracker:
    def __init__(self, data_file="app_usage.json"):
        self.app_usage = {}
        self.tracking = False
        self.lock = threading.Lock()
        self.data_file = data_file
        self.load_data()

    def get_active_window(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['pid'] == pid:
                    return proc.info['name']
        except Exception as e:
            print(f"Error getting active window: {e}")
        return None

    def start_tracking(self):
        self.tracking = True
        threading.Thread(target=self.track_usage).start()

    def stop_tracking(self):
        self.tracking = False

    def track_usage(self):
        while self.tracking:
            active_app = self.get_active_window()
            if active_app:
                with self.lock:
                    if active_app not in self.app_usage:
                        self.app_usage[active_app] = 0
                    self.app_usage[active_app] += 1
            time.sleep(1)

    def get_usage(self):
        with self.lock:
            return dict(self.app_usage)

    def save_data(self):
        with self.lock:
            try:
                with open(self.data_file, 'w') as f:
                    json.dump(self.app_usage, f)
            except Exception as e:
                print(f"Error saving data: {e}")

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.app_usage = json.load(f)
            except Exception as e:
                print(f"Error loading data: {e}")

    def get_total_usage_time(self):
        with self.lock:
            return sum(self.app_usage.values())

    def get_average_time_per_session(self):
        with self.lock:
            if len(self.app_usage) == 0:
                return 0
            return sum(self.app_usage.values()) / len(self.app_usage)
