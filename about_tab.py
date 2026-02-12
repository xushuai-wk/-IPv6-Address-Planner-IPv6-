import tkinter as tk
from tkinter import ttk
import webbrowser


class AboutTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.create_tab()
    
    def create_tab(self):
        tab6 = ttk.Frame(self.notebook)
        self.notebook.add(tab6, text="关于")
        
        main_frame = ttk.Frame(tab6)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(main_frame, padding="20")
        header_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(header_frame, text="IPv6 Address Planner", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 3))
        
        subtitle_label = ttk.Label(header_frame, text="IPv6 地址规划器", font=('Arial', 11), foreground="#666666")
        subtitle_label.pack(pady=(0, 8))
        
        version_label = ttk.Label(header_frame, text="版本: v1.0.7", font=('Arial', 10))
        version_label.pack(pady=2)
        
        date_label = ttk.Label(header_frame, text="发布日期: 2026年2月11日", font=('Arial', 9), foreground="#666666")
        date_label.pack(pady=2)
        
        ttk.Separator(header_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)
        
        prefix_frame = ttk.Frame(header_frame)
        prefix_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(prefix_frame, text="IPv6 地址前缀使用建议", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 6))
        
        prefix_info = [
            "/48: 建议给单个站点的网段",
            "/56: 建议给中小型客户的网段",
            "/64: 建议给单个 LAN 的网段 (SLAAC 必须使用 /64)",
            "/127: 建议用于路由器之间的点对点链路"
        ]
        
        for info in prefix_info:
            ttk.Label(prefix_frame, text=info, font=('Arial', 9)).pack(anchor=tk.W, pady=1)
        
        ttk.Separator(header_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)
        
        rfc_frame = ttk.Frame(header_frame)
        rfc_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(rfc_frame, text="参考标准", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 6))
        
        ttk.Button(rfc_frame, text="RFC 4291 - IPv6 地址架构", 
                  command=lambda: self.open_url("https://datatracker.ietf.org/doc/html/rfc4291")).pack(pady=2, anchor=tk.W)
        ttk.Button(rfc_frame, text="RFC 6164 - 使用 /127 的点对点链路", 
                  command=lambda: self.open_url("https://datatracker.ietf.org/doc/html/rfc6164")).pack(pady=2, anchor=tk.W)
        
        ttk.Separator(header_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)
        
        disclaimer_frame = ttk.Frame(header_frame)
        disclaimer_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(disclaimer_frame, text="免责声明", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 6))
        
        disclaimer_text = "使用者应自行验证所有计算结果的准确性，对于因使用本软件计算结果而导致的任何直接或间接损失，开发者不承担任何责任。"
        
        ttk.Label(disclaimer_frame, text=disclaimer_text, font=('Arial', 8), 
                 wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, pady=3)
        
        ttk.Separator(header_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)
        
        copyright_frame = ttk.Frame(header_frame)
        copyright_frame.pack(fill=tk.X, pady=10)
        
        copyright_label = ttk.Label(copyright_frame, text="基于 MIT 协议开源", font=('Arial', 9), 
                                 foreground="#0066CC", cursor="hand2")
        copyright_label.pack(pady=5)
        copyright_label.bind("<Button-1>", lambda e: self.open_url("https://gitee.com/xushuai-wk/ipv6-address-planner"))
    
    def open_url(self, url):
        webbrowser.open(url)