import tkinter as tk
from tkinter import ttk, scrolledtext

class GuiManager:
    def __init__(self, app, accent_color, highlight_color, bg_color, text_color):
        self.accent_color = accent_color
        self.highlight_color = highlight_color
        self.bg_color = bg_color
        self.text_color = text_color
        
        self.app = app

        self.is_listening = False
        self.log_entries = []

    #GUI 
    def create_main_window(self):
        # Clear existing widgets
        for widget in self.app.root.winfo_children():
            widget.destroy()
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.app.root, padding="20 20 20 20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title with decorative elements
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.pack(pady=10)
        
        # Create title label with gradient-like effect
        title_label = tk.Label(
            title_frame, 
            text="Andra Portabilă", 
            font=("Arial", 28, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Create subtitle
        subtitle = tk.Label(
            main_frame,
            text="Asistentul tău muzical personal",
            font=("Arial", 14, "italic"),
            fg=self.text_color,
            bg=self.bg_color
        )
        subtitle.pack(pady=(0, 20))
        
        # Create buttons frame
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(pady=20)
        
        # Helper function to create hover effect
        def on_enter(e, btn, original_color, hover_color):
            btn.config(bg=hover_color)
        
        def on_leave(e, btn, original_color):
            btn.config(bg=original_color)
        
        # Create custom buttons with hover effect
        live_btn = tk.Button(
            button_frame, 
            text="Andra, ce notă-i asta?", 
            font=("Arial", 14, "bold"),
            width=30,
            height=2,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.open_live_window
        )
        live_btn.pack(pady=10)
        live_btn.bind("<Enter>", lambda e: on_enter(e, live_btn, self.accent_color, self.highlight_color))
        live_btn.bind("<Leave>", lambda e: on_leave(e, live_btn, self.accent_color))
        
        # Add icon or description
        live_desc = tk.Label(
            button_frame,
            text="Detectează notele în timp real",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        live_desc.pack(pady=(0, 10))
        
        recorded_btn = tk.Button(
            button_frame, 
            text="Andra, ce acorduri sunt aici?", 
            font=("Arial", 14, "bold"),
            width=30,
            height=2,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.open_recorded_window
        )
        recorded_btn.pack(pady=10)
        recorded_btn.bind("<Enter>", lambda e: on_enter(e, recorded_btn, self.accent_color, self.highlight_color))
        recorded_btn.bind("<Leave>", lambda e: on_leave(e, recorded_btn, self.accent_color))
        
        # Add icon or description
        recorded_desc = tk.Label(
            button_frame,
            text="Analizează fișiere audio înregistrate",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        recorded_desc.pack(pady=(0, 10))
        
        log_btn = tk.Button(
            button_frame, 
            text="Yapping Andra", 
            font=("Arial", 14, "bold"),
            width=30,
            height=2,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.open_log_window
        )
        log_btn.pack(pady=10)
        log_btn.bind("<Enter>", lambda e: on_enter(e, log_btn, self.accent_color, self.highlight_color))
        log_btn.bind("<Leave>", lambda e: on_leave(e, log_btn, self.accent_color))
        
        # Add icon or description
        log_desc = tk.Label(
            button_frame,
            text="Vezi ce a fost detectat",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        log_desc.pack(pady=(0, 10))
        
        # Add decorative footer
        footer_frame = ttk.Frame(main_frame, style='TFrame')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_line = ttk.Separator(footer_frame, orient='horizontal')
        footer_line.pack(fill=tk.X, pady=5)
        
        # Add copyright text with style (centered)
        copyright_label = tk.Label(
            footer_frame, 
            text="All rights reserved to Erol Bo$$ Sefu la Bani",
            font=("Arial", 8),
            fg="gray",
            bg=self.bg_color
        )
        copyright_label.pack(fill=tk.X, pady=5)
    #GUI
    def open_live_window(self):
        # Clear existing widgets
        for widget in self.app.root.winfo_children():
            widget.destroy()
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.app.root, padding="20 20 20 20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title with decorative elements
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.pack(pady=10)
        
        # Create title label
        title_label = tk.Label(
            title_frame, 
            text="Andra, ce notă-i asta?", 
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Create description
        description = tk.Label(
            main_frame, 
            text="Apasă 'Start' ca să-ți zica Andra ce notă (si gamă/acord/progresie) se aude.",
            font=("Arial", 12),
            wraplength=550,
            bg=self.bg_color,
            fg=self.text_color
        )
        description.pack(pady=10)
        
        # Create results area with styled background
        self.result_label = tk.Label(
            main_frame, 
            text="Andra asteaptă.",
            font=("Arial", 14, "bold"),
            wraplength=350,
            bg="#e0ecf7",  # Lighter shade of our background color
            fg=self.text_color,
            width=45,
            height=4,
            relief=tk.GROOVE,
            bd=2
        )
        self.result_label.pack(pady=10)
        
        # Create log area (mini version) with styled frame
        log_frame = ttk.Frame(main_frame, style='TFrame')
        log_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        log_label = tk.Label(
            log_frame, 
            text="Ce a auzit:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        log_label.pack(anchor="w", padx=8)
        
        self.mini_log = scrolledtext.ScrolledText(
            log_frame,
            width=55,
            height=10,
            font=("Consolas", 10),
            state="disabled",
            bg="white",
            fg=self.text_color
        )
        self.mini_log.tag_configure("highlight", background="#ffff99")  # Configure highlight tag
        self.mini_log.pack(padx=10, fill=tk.BOTH, expand=True)
        self.app.log_manager.mini_log = self.mini_log

        # Create buttons frame
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(pady=10)
        
        # Create start/stop button with styling
        self.listen_btn = tk.Button(
            btn_frame, 
            text="Start", 
            font=("Arial", 14, "bold"),
            width=12,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.app.live_audio.toggle_listening
        )
        self.listen_btn.pack(side=tk.LEFT, padx=10)
        
        # Create return button
        return_btn = tk.Button(
            btn_frame, 
            text="Înapoi", 
            font=("Arial", 14, "bold"),
            width=12,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.return_to_main_window
        )
        return_btn.pack(side=tk.LEFT, padx=10)
        
        # Add decorative footer
        footer_frame = ttk.Frame(main_frame, style='TFrame')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_line = ttk.Separator(footer_frame, orient='horizontal')
        footer_line.pack(fill=tk.X, pady=5)
        
        # Add copyright text with style (centered)
        copyright_label = tk.Label(
            footer_frame, 
            text="All rights reserved to Erol Bo$$ Sefu la Bani",
            font=("Arial", 8),
            fg="gray",
            bg=self.bg_color
        )
        copyright_label.pack(fill=tk.X, pady=5)
    #GUI
    def open_recorded_window(self):
        # Clear existing widgets
        for widget in self.app.root.winfo_children():
            widget.destroy()
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.app.root, padding="20 20 20 20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title with decorative elements
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.pack(pady=10)
        
        # Create title label
        title_label = tk.Label(
            title_frame, 
            text="Andra, ce acorduri sunt aici?", 
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Create file selection frame with styling
        file_frame = ttk.Frame(main_frame, style='TFrame')
        file_frame.pack(pady=10, fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("Nu a fost ales niciun fișier")
        
        file_label = tk.Label(
            file_frame, 
            text="Fișierul Ales:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        file_label.pack(side=tk.LEFT, padx=5)
        
        file_path_label = tk.Label(
            file_frame, 
            textvariable=self.file_path_var, 
            font=("Arial", 12),
            wraplength=450,
            bg=self.bg_color,
            fg=self.text_color
        )
        file_path_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Create browse button with styling
        browse_btn = tk.Button(
            main_frame, 
            text="Alege Fișierul Audio", 
            font=("Arial", 12, "bold"),
            width=20,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.app.file_operations.browse_file
        )
        browse_btn.pack(pady=10)
        
        # Create results area with styled background
        self.file_result_label = tk.Label(
            main_frame, 
            text="Andra asteaptă.",
            font=("Arial", 14, "bold"),
            wraplength=550,
            bg="#e0ecf7",  # Lighter shade of our background color
            fg=self.text_color,
            width=45,
            height=4,
            relief=tk.GROOVE,
            bd=2
        )
        self.file_result_label.pack(pady=10)
        
        # Create log area (mini version)
        log_frame = ttk.Frame(main_frame, style='TFrame')
        log_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        log_label = tk.Label(
            log_frame, 
            text="Ce a auzit:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        log_label.pack(anchor="w", padx=10)
        
        self.mini_log = scrolledtext.ScrolledText(
            log_frame,
            width=55,
            height=8,
            font=("Consolas", 10),
            state="disabled",
            bg="white",
            fg=self.text_color
        )
        self.mini_log.tag_configure("highlight", background="#ffff99")  # Configure highlight tag
        self.mini_log.pack(padx=10, fill=tk.BOTH, expand=True)
        self.app.log_manager.mini_log = self.mini_log

        # Create buttons frame
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(pady=10)
        
        # Create analyze button with styling
        analyze_btn = tk.Button(
            btn_frame, 
            text="Start", 
            font=("Arial", 14, "bold"),
            width=12,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.app.file_operations.analyze_file
        )
        analyze_btn.pack(side=tk.LEFT, padx=10)
        
        # Create return button with styling
        return_btn = tk.Button(
            btn_frame, 
            text="Înapoi", 
            font=("Arial", 14, "bold"),
            width=12,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.return_to_main_window
        )
        return_btn.pack(side=tk.LEFT, padx=10)
        
        # Add decorative footer
        footer_frame = ttk.Frame(main_frame, style='TFrame')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_line = ttk.Separator(footer_frame, orient='horizontal')
        footer_line.pack(fill=tk.X, pady=5)
        
        # Add copyright text with style (centered)
        copyright_label = tk.Label(
            footer_frame, 
            text="All rights reserved to Erol Bo$$ Sefu la Bani",
            font=("Arial", 8),
            fg="gray",
            bg=self.bg_color
        )
        copyright_label.pack(fill=tk.X, pady=5)
    #GUI
    def open_log_window(self):
        # Clear existing widgets
        for widget in self.app.root.winfo_children():
            widget.destroy()
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.app.root, padding="20 20 20 20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title with decorative elements
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.pack(pady=10)
        
        # Create title label
        title_label = tk.Label(
            title_frame, 
            text="Yapping Andra", 
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Create log text area with styled frame
        log_frame = ttk.Frame(main_frame, style='TFrame')
        log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        log_text = scrolledtext.ScrolledText(
            log_frame,
            width=75,
            height=20,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="white",
            fg=self.text_color
        )
        log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Fill with log entries
        for entry in self.app.log_manager.log_entries:
            log_text.insert(tk.END, entry + "\n")
        
        # Create button frame with styling
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(pady=10)
        
        # Create save button with styling
        save_btn = tk.Button(
            btn_frame,
            text="Salvează Log",
            font=("Arial", 12, "bold"),
            width=12,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=lambda: self.app.log_manager.save_log_to_file(log_text.get("1.0", tk.END))
        )
        save_btn.pack(side=tk.LEFT, padx=10)
        
        # Create clear button with styling
        clear_btn = tk.Button(
            btn_frame,
            text="Șterge Log",
            font=("Arial", 12, "bold"),
            width=12,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=lambda: self.app.log_manager.clear_log(log_text)
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Create return button with styling
        return_btn = tk.Button(
            btn_frame,
            text="Înapoi",
            font=("Arial", 12, "bold"),
            width=12,
            bg=self.accent_color,
            fg="white",
            activebackground=self.highlight_color,
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=self.create_main_window
        )
        return_btn.pack(side=tk.LEFT, padx=10)
        
        # Add decorative footer
        footer_frame = ttk.Frame(main_frame, style='TFrame')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_line = ttk.Separator(footer_frame, orient='horizontal')
        footer_line.pack(fill=tk.X, pady=5)
        
        # Add copyright text with style (centered)
        copyright_label = tk.Label(
            footer_frame, 
            text="All rights reserved to Erol Bo$$ Sefu la Bani",
            font=("Arial", 8),
            fg="gray",
            bg=self.bg_color
        )
        copyright_label.pack(fill=tk.X, pady=5)
    #GUI
    def return_to_main_window(self):
        if self.app.live_audio.is_listening():
            self.app.live_audio.stop_listening()
            self.listen_btn.config(text="Start")
            self.result_label.config(text="Andra asteaptă.")
        try:  
            self.mini_log.delete("1.0", "end")
        except Exception as e:
            print(f"Failed to delete mini log: {e}")
    
        self.create_main_window()
