import tkinter as tk
from tkinter import ttk
import re


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
    
    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#FFFFE0", relief=tk.SOLID, borderwidth=1,
                      font=("Arial", 9))
        label.pack(ipadx=1)
    
    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class UIUtils:
    @staticmethod
    def clean_ipv6_input(input_str):
        cleaned = input_str.strip()
        
        bracket_match = re.search(r'\[([0-9a-fA-F:%]+)\]', cleaned)
        if bracket_match:
            cleaned = bracket_match.group(1)
        
        cleaned = cleaned.split('/', 1)[0]
        
        return cleaned
    
    @staticmethod
    def add_placeholder(entry, default_value, placeholder):
        entry.insert(0, default_value)
        
        def on_focus_in(event):
            if entry.get() == default_value:
                entry.delete(0, tk.END)
        
        def on_focus_out(event):
            if not entry.get().strip():
                entry.insert(0, default_value)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
    
    @staticmethod
    def highlight_error(entry):
        style = ttk.Style()
        style.configure('Error.TEntry', fieldbackground='#FFCCCC')
        entry.configure(style='Error.TEntry')
        entry.after(2000, lambda: entry.configure(style='TEntry'))
    
    @staticmethod
    def clear_error_highlight(entry):
        entry.configure(style='TEntry')
    
    @staticmethod
    def create_input_row(parent, label_text, default_value, row, entry_name, entry_width=50, placeholder=None):
        ttk.Label(parent, text=label_text, font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=8)
        entry = ttk.Entry(parent, width=entry_width)
        entry.grid(row=row, column=1, pady=8, padx=8, sticky=tk.W)
        
        if placeholder:
            UIUtils.add_placeholder(entry, default_value, placeholder)
        else:
            entry.insert(0, default_value)
        
        return entry
    
    @staticmethod
    def create_button_frame(parent, row, buttons, tooltips=None):
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        for i, (button_text, button_command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=button_text, command=button_command)
            btn.pack(side=tk.LEFT, padx=5)
            if tooltips and i < len(tooltips):
                ToolTip(btn, tooltips[i])
        return button_frame
    
    @staticmethod
    def create_result_display(parent, row, text_name, height=18, width=80):
        result_text = tk.Text(parent, height=height, width=width, wrap=tk.WORD, font=('Arial', 10))
        result_text.grid(row=row, column=0, columnspan=2, pady=10)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=result_text.yview)
        scrollbar.grid(row=row, column=2, sticky=tk.NS)
        result_text.config(yscrollcommand=scrollbar.set)
        setattr(parent, text_name, result_text)
        return result_text
    
    @staticmethod
    def add_tooltip(widget, text):
        ToolTip(widget, text)
