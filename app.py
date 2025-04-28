import tkinter as tk
from tkinter import ttk
from gui_components import GuiManager
from log_manager import LogManager
from live_audio import LiveAudio
from audio_processing import AudioProcessor
from file_operations import FileOperations

class MusicScaleDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Andra Portabila")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.bg_color = "#e6f2fa"
        self.accent_color = "#65b7ff"
        self.highlight_color = "#9340f0"
        self.text_color = "#333333"
        self.root.configure(bg=self.bg_color)
        
        self.live_window = None
        self.recorded_window = None
        self.is_listening = False
        self.audio_thread = None
        self.selected_file = None
        self.log_entries = []
        
        self.SAMPLE_RATE = 48000
        self.BUFFER_SIZE = 4096
        self.NOISE_THRESHOLD = 0.005
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 12), background=self.accent_color, foreground='white')
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Accent.TButton', background=self.highlight_color)
        self.style.map('TButton', background=[('active', self.highlight_color)], foreground=[('active', 'white')])
        
        self.gui_components = GuiManager(self, self.accent_color, self.highlight_color, self.bg_color, self.text_color)
        self.log_manager = LogManager(self)
        self.live_audio = LiveAudio(self)
        self.audio_processing = AudioProcessor(self)
        self.file_operations = FileOperations(self)

        self.gui_components.create_main_window()
    
    # GUI methods
    def open_live_window(self):
        self.gui_components.open_live_window()

    def open_recorded_window(self):
        self.gui_components.open_recorded_window()

    def open_log_window(self):
        self.gui_components.open_log_window()

    def return_to_main_window(self):
        self.gui_components.return_to_main_window()

    # Log methods
    def save_log_to_file(self, log_content):
        self.log_manager.save_log_to_file(log_content)

    def clear_log(self, log_text_widget):
        self.log_manager.clear_log(log_text_widget)

    def add_to_log(self, message, highlight=False):
        self.log_manager.add_to_log(message, highlight)

    # Live methods
    def toggle_listening(self):
        self.live_audio_manager.toggle_listening()

    def live_audio_callback(self, indata, frames, time_info, status):
        self.live_audio_manager.live_audio_callback(indata, frames, time_info, status)

    def start_live_detection(self):
        self.live_audio_manager.start_live_detection()

    # Audio Processing methods
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        return self.live_audio_manager.butter_bandpass(lowcut, highcut, fs, order)

    def filter_audio(self, audio_buffer, lowcut=40, highcut=3000):
        return self.live_audio_manager.filter_audio(audio_buffer, lowcut, highcut)

    def frequency_to_note(self, frequency):
        return self.live_audio_manager.frequency_to_note(frequency)

    def identify_chord(self, notes, include_octave=False):
        return self.live_audio_manager.identify_chord(notes, include_octave)

    def yin_pitch(self, signal):
        return self.live_audio_manager.yin_pitch(signal)

    def process_audio(self, audio_data, sample_rate=None, is_live=True, time_position=0):
        return self.live_audio_manager.process_audio(audio_data, sample_rate, is_live, time_position)

    # File methods
    def browse_file(self):
        self.file_operations.browse_file()

    def analyze_file(self):
        self.file_operations.analyze_file()
