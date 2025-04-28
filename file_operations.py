# file_operations.py

import os
import traceback
from collections import Counter
from tkinter import filedialog, messagebox
import librosa

class FileOperations:
    def __init__(self, app):
        self.SAMPLE_RATE = 44100
        self.selected_file = None
        self.app = app

    def analyze_file(self):
        """Analyze an audio file for notes and chords"""
        if not self.selected_file:
            messagebox.showinfo("Info", "Please select an audio file first.")
            return
        
        self.app.gui_components.file_result_label.config(text="Analyzing...")
        self.app.root.update()
        
        try:
            # Load the audio file
            y, sr = librosa.load(self.selected_file, sr=self.SAMPLE_RATE)
            
            # Initialize results storage
            chunk_results = []
            
            # Break into small chunks and analyze each
            chunk_length = 1  # seconds
            chunk_samples = chunk_length * sr
            overlap = 0.5  # 50% overlap for smoother analysis
            overlap_samples = int(overlap * chunk_samples)
            
            # Process chunks with overlap
            for i in range(0, len(y) - chunk_samples, overlap_samples):
                chunk = y[i:i + chunk_samples]
                if len(chunk) < sr * 0.5:  # Skip very short chunks
                    continue
                
                time_position = i / sr
                result = self.app.audio_processing.process_audio(chunk, sample_rate=sr, is_live=False, time_position=time_position)
                
                if result["notes"]:  # Only keep chunks with detected notes
                    chunk_results.append(result)
            
            if chunk_results:
                # Analyze all detected notes and chords
                all_detected_notes = set()
                chord_counts = Counter()
                
                # Process all chunk results
                for result in chunk_results:
                    all_detected_notes.update(result["notes"])
                    if result["chord"] != "No chord detected" and result["chord"] != "Error":
                        chord_counts[result["chord"]] += 1
                
                # Get the most common chords (more than 5% of occurrences)
                total_chunks = len(chunk_results)
                significant_chords = [chord for chord, count in chord_counts.items() 
                                    if count / total_chunks > 0.05]
                
                # If too many chords, take the most frequent ones
                if len(significant_chords) > 8:
                    significant_chords = [chord for chord, _ in chord_counts.most_common(8)]
                
                # Update UI with detected chord information
                result_text = f"Detected Notes: {', '.join(sorted(all_detected_notes))}\n" 
                result_text += f"Detected Chords: {', '.join(significant_chords)}"
                
                self.app.gui_components.file_result_label.config(text=result_text)
    
                # Add to log
                filename = os.path.basename(self.selected_file)
                self.app.log_manager.add_to_log(f"File Analysis: {filename} - Notes: {', '.join(sorted(all_detected_notes))} - Chords: {', '.join(significant_chords)}")
            else:
                self.app.gui_components.file_result_label.config(text="Could not detect any chords in this audio file.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Analysis error: {str(e)}")
            self.app.gui_components.file_result_label.config(text="Analysis failed")
            print(f"Detailed error: {traceback.format_exc()}")

    def browse_file(self):
        filetypes = (
            ('Audio files', '*.mp3 *.wav *.flac *.ogg'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Open an audio file',
            initialdir='/',
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.app.gui_components.file_path_var.set(os.path.basename(filename))
