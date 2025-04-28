# __init__.py

from file_operations import FileOperations
from audio_processing import AudioProcessor
from live_audio import LiveAudio
from log_manager import LogManager
import tkinter as tk

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Andra Portabila")
        self.root.geometry("600x400")
        
        # Initialize the components
        self.file_operations = FileOperations(self)
        self.audio_processing = AudioProcessor(self)
        self.live_audio = LiveAudio(self)
        self.log_operations = LogManager(self)

        # Create UI elements
        self.create_ui()

    def create_ui(self):
        """Create the main UI components"""
        
        # Create buttons for file operations
        self.browse_button = tk.Button(self.root, text="Browse File", command=self.file_operations.browse_file)
        self.browse_button.pack(pady=10)

        self.analyze_button = tk.Button(self.root, text="Analyze File", command=self.file_operations.analyze_file)
        self.analyze_button.pack(pady=10)

        # Label for displaying results
        self.file_result_label = tk.Label(self.root, text="File Analysis Result")
        self.file_result_label.pack(pady=10)

        # Create buttons for live audio operations
        self.listen_button = tk.Button(self.root, text="Start", command=self.live_audio.toggle_listening)
        self.listen_button.pack(pady=10)

        # Label for live audio results
        self.live_result_label = tk.Label(self.root, text="Live Audio Result")
        self.live_result_label.pack(pady=10)

        # Log text area
        self.log_text_widget = tk.Text(self.root, height=10, width=50)
        self.log_text_widget.pack(pady=10)

        # Create log management buttons
        self.save_log_button = tk.Button(self.root, text="Save Log", command=lambda: self.log_operations.save_log_to_file(self.log_text_widget.get("1.0", tk.END)))
        self.save_log_button.pack(pady=5)

        self.clear_log_button = tk.Button(self.root, text="Clear Log", command=lambda: self.log_operations.clear_log(self.log_text_widget))
        self.clear_log_button.pack(pady=5)
    
    def run(self):
        """Start the tkinter event loop"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.run()
