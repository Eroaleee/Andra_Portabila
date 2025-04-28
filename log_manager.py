import tkinter as tk
from tkinter import filedialog, messagebox
import datetime

class LogManager:
    def __init__(self, app, mini_log=None):
        self.log_entries = []
        self.mini_log = mini_log
        self.last_log_time = datetime.datetime.now() - datetime.timedelta(seconds=2)

    #Log
    def save_log_to_file(self, log_content):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="A fost salvat cu succes"
            )
            if filename:
                with open(filename, "w") as f:
                    f.write(log_content)
                messagebox.showinfo("Success", "A fost salvat cu succes!")
        except Exception as e:
            messagebox.showerror("Error", f"Fraiere, mai incearca... {str(e)}")
    #Log
    def clear_log(self, log_text_widget):
        if messagebox.askyesno("Sterge memoria Andrei", "Sigur vrei sa stergi????"):
            self.log_entries = []
            log_text_widget.delete("1.0", tk.END)
            # Clear mini logs if they exist
            try:
                self.mini_log.config(state="normal")
                self.mini_log.delete("1.0", tk.END)
                self.mini_log.config(state="disabled")
            except:
                pass
    #Log
    def add_to_log(self, message, highlight=False):
        # Check if 1 second has passed since last log entry
        current_time = datetime.datetime.now()
        
        # Initialize last_log_time as class attribute if it doesn't exist
        if not hasattr(self, "last_log_time"):
            self.last_log_time = current_time - datetime.timedelta(seconds=2)  # Ensure first log is recorded
        
        # Only add log entry if at least 1 second has passed
        time_diff = (current_time - self.last_log_time).total_seconds()
        if time_diff >= 1.0:
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message}"
            self.log_entries.append(log_entry)
            
            # Update the last log time
            self.last_log_time = current_time
    
            # Update mini log if it exists
            try:
                self.mini_log.config(state="normal")
    
                # Add highlighting for important entries
                if highlight:
                    self.mini_log.insert(tk.END, log_entry + "\n", "highlight")
                else:
                    self.mini_log.insert(tk.END, log_entry + "\n")
    
                self.mini_log.see(tk.END)  # Scroll to the end
                self.mini_log.config(state="disabled")
            except:
                pass
