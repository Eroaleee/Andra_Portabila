import threading
import time
import sounddevice as sd
import numpy as np
from tkinter import messagebox

class LiveAudio:
    def __init__(self, app, sample_rate=44100, buffer_size=1024):
        self.SAMPLE_RATE = sample_rate
        self.BUFFER_SIZE = buffer_size
        self.is_listening = False
        self.audio_thread = None
        self.app = app

#Live
    def toggle_listening(self):
        if not self.is_listening:
            # Start listening
            self.is_listening = True
            self.app.gui_components.listen_btn.config(text="Stop")
            self.app.gui_components.result_label.config(text="Listening...")
            
            # Start audio processing in a separate thread
            self.audio_thread = threading.Thread(target=self.start_live_detection)
            self.audio_thread.daemon = True
            self.audio_thread.start()
        else:
            # Stop listening
            self.is_listening = False
            self.app.gui_components.listen_btn.config(text="Start")
            self.app.gui_components.result_label.config(text="Andra asteaptă.")
            
    #Live
    def live_audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status)
            return
        
        # Process the live audio buffer
        audio_buffer = indata[:, 0]  # Convert to mono
        self.app.audio_processing.process_audio(audio_buffer, is_live=True)
    #Live
    def start_live_detection(self):
        try:
            with sd.InputStream(callback=self.live_audio_callback, samplerate=self.SAMPLE_RATE, 
                              channels=1, blocksize=self.BUFFER_SIZE):
                while self.is_listening:
                    time.sleep(0.5)
        except Exception as e:
            messagebox.showerror("Error", f"Audio input error: {str(e)}")
            self.is_listening = False
            self.app.root.after(0, lambda: self.app.gui_components.listen_btn.config(text="Start"))
