import threading
import time
import sounddevice as sd
import numpy as np
from tkinter import messagebox

class LiveAudio:
    def __init__(self, app, sample_rate=44100, buffer_size=1024):
        self.SAMPLE_RATE = sample_rate
        self.BUFFER_SIZE = buffer_size
        self._stop_event = threading.Event()
        self.audio_thread = None
        self.app = app

    def toggle_listening(self):
        if not self.is_listening():
            self._stop_event.clear()
            self.app.gui_components.listen_btn.config(text="Stop")
            self.app.gui_components.result_label.config(text="Listening...")

            self.audio_thread = threading.Thread(target=self.start_live_detection)
            self.audio_thread.daemon = True
            self.audio_thread.start()
        else:
            self.stop_listening()

    def is_listening(self):
        return not self._stop_event.is_set()

    def stop_listening(self):
        self._stop_event.set()
        self.app.gui_components.listen_btn.config(text="Start")
        self.app.gui_components.result_label.config(text="Andra asteaptă.")

    def live_audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status)
            return

        audio_buffer = indata[:, 0]  # mono
        self.app.audio_processing.process_audio(audio_buffer, is_live=True)

    def start_live_detection(self):
        try:
            with sd.InputStream(callback=self.live_audio_callback, samplerate=self.SAMPLE_RATE, 
                                channels=1, blocksize=self.BUFFER_SIZE):
                while not self._stop_event.is_set():
                    time.sleep(0.1)
        except Exception as e:
            messagebox.showerror("Error", f"Audio input error: {str(e)}")
            self._stop_event.set()
            self.app.root.after(0, lambda: self.app.gui_components.listen_btn.config(text="Start"))
