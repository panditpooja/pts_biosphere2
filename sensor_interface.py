import os
import pandas as pd
import glob

class SensorInterface:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.data_frames = []
        self.pointer = 0
        self.load_sensor_data()

    def load_sensor_data(self):
        print("📥 Loading sensor data from:", self.data_dir)
        all_csvs = glob.glob(os.path.join(self.data_dir, "*.csv"))
        frames = []
        for csv_path in all_csvs:
            try:
                df = pd.read_csv(csv_path)
                df["__source_file__"] = os.path.basename(csv_path)
                frames.append(df)
            except Exception as e:
                print(f"⚠️ Failed to load {csv_path}: {e}")

        if frames:
            try:
                self.data_frames = pd.concat(frames, axis=1).ffill().bfill()
                print(f"✅ Loaded sensor data with shape: {self.data_frames.shape}")
            except Exception as e:
                print("❌ Failed to merge sensor data:", e)
                self.data_frames = []
        else:
            print("❌ No valid sensor files found.")
            self.data_frames = []

    def reset(self):
        self.pointer = 0

    def get_next_sensor_frame(self):
        if isinstance(self.data_frames, pd.DataFrame) and self.pointer < len(self.data_frames):
            row = self.data_frames.iloc[self.pointer]
            self.pointer += 1
            return row.to_dict()
        return None

    def get_active_alerts(self, frame: dict, thresholds: dict):
        alerts = {}
        for key, (low, high) in thresholds.items():
            value = frame.get(key, None)
            if value is not None and (value < low or value > high):
                alerts[key] = f"{'LOW' if value < low else 'HIGH'}: {value}"
        return alerts