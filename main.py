import tkinter as tk
from tkinter import ttk
import threading
from utils import UIUtils
from basic_info_tab import BasicInfoTab
from subnet_division_tab import SubnetDivisionTab
from host_addresses_tab import HostAddressesTab
from subnet_membership_tab import SubnetMembershipTab
from eui64_conversion_tab import EUI64ConversionTab
from about_tab import AboutTab


class IPv6SubnetCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("IPv6 Address Planner (IPv6 地址规划器)")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)
        
        self.stop_flag_lock = threading.Lock()
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10), padding=5)
        style.configure('TNotebook', padding=5)
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.root.bind('<Configure>', self._on_window_resize)
        
        self.basic_info_tab = BasicInfoTab(self.notebook, self.root, self.log_status)
        self.subnet_division_tab = SubnetDivisionTab(self.notebook, self.root, self.log_status)
        self.host_addresses_tab = HostAddressesTab(self.notebook, self.root, self.log_status, self.stop_flag_lock)
        self.subnet_membership_tab = SubnetMembershipTab(self.notebook, self.root, self.log_status)
        self.eui64_conversion_tab = EUI64ConversionTab(self.notebook, self.root, self.log_status)
        self.about_tab = AboutTab(self.notebook)
        
        status_frame = tk.Frame(root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_icon = tk.Label(status_frame, text="●", font=('Arial', 12), width=3)
        self.status_icon.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.status_bar = tk.Label(status_frame, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        self._setup_shortcuts()
    
    def log_status(self, message, status_type="info"):
        icon_map = {
            "success": "✓",
            "warning": "⚠",
            "error": "✗",
            "info": "●"
        }
        icon = icon_map.get(status_type, "●")
        self.status_icon.config(text=icon, foreground=self._get_status_color(status_type))
        self.status_bar.config(text=message)
    
    def _get_status_color(self, status_type):
        color_map = {
            "success": "#009900",
            "warning": "#FF9900",
            "error": "#CC0000",
            "info": "#0066CC"
        }
        return color_map.get(status_type, "#0066CC")
    
    def _on_window_resize(self, event):
        if event.widget == self.root:
            width = event.width
            if width < 900:
                self.notebook.pack(padx=5, pady=5)
            elif width < 1100:
                self.notebook.pack(padx=10, pady=10)
            else:
                self.notebook.pack(padx=15, pady=15)
    
    def _setup_shortcuts(self):
        self.root.bind('<Control-c>', lambda e: self._copy_current_result())
        self.root.bind('<Control-s>', lambda e: self._export_current_result())
        self.root.bind('<Control-r>', lambda e: self._calculate_current_tab())
        self.root.bind('<F1>', lambda e: self._show_help())
    
    def _copy_current_result(self):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            self.basic_info_tab.copy_basic_info()
        elif current_tab == 1:
            self.subnet_division_tab.copy_subnet_division()
        elif current_tab == 2:
            self.host_addresses_tab.copy_hosts()
        elif current_tab == 3:
            self.subnet_membership_tab.copy_subnet_membership()
        elif current_tab == 4:
            self.eui64_conversion_tab.copy_eui64_result()
    
    def _export_current_result(self):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 1:
            self.subnet_division_tab.export_subnets()
        elif current_tab == 2:
            self.host_addresses_tab.export_hosts_dialog()
    
    def _calculate_current_tab(self):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            self.basic_info_tab.calculate_basic_info()
        elif current_tab == 1:
            self.subnet_division_tab.calculate_subnet_division()
        elif current_tab == 2:
            self.host_addresses_tab.generate_host_addresses()
        elif current_tab == 3:
            self.subnet_membership_tab.calculate_subnet_membership()
        elif current_tab == 4:
            self.eui64_conversion_tab.convert_eui64()
    
    def _show_help(self):
        help_text = """快捷键说明:
Ctrl+C - 复制当前结果
Ctrl+S - 导出当前结果
Ctrl+R - 重新计算当前标签页
F1 - 显示帮助信息"""
        from tkinter import messagebox
        messagebox.showinfo("快捷键帮助", help_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = IPv6SubnetCalculator(root)
    root.mainloop()