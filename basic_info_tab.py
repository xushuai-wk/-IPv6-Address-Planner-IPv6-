import ipaddress
import tkinter as tk
from tkinter import ttk, messagebox
from utils import UIUtils


class BasicInfoTab:
    def __init__(self, notebook, root, log_status_func):
        self.notebook = notebook
        self.root = root
        self.log_status = log_status_func
        self.ipv6_entry1 = None
        self.prefix_entry1 = None
        self.result_text1 = None
        self.create_tab()
    
    def create_tab(self):
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="基础子网信息")
        
        frame = ttk.Frame(tab1, padding="25")
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.ipv6_entry1 = UIUtils.create_input_row(frame, "IPv6 地址:", "2026:db8::", 0, None, placeholder="例如: 2026:db8::")
        self.prefix_entry1 = UIUtils.create_input_row(frame, "前缀长度:", "64", 1, None, placeholder="0-128")
        UIUtils.create_button_frame(frame, 2, [("计算", self.calculate_basic_info), ("复制结果", self.copy_basic_info)], 
                               tooltips=["计算基础子网信息", "复制计算结果到剪贴板"])
        self.result_text1 = UIUtils.create_result_display(frame, 3, "result_text1")
    
    def calculate_basic_info(self):
        try:
            ipv6_str = UIUtils.clean_ipv6_input(self.ipv6_entry1.get())
            prefix = int(self.prefix_entry1.get().strip())
            
            if not 0 <= prefix <= 128:
                raise ValueError("前缀长度必须在 0-128 之间")
            
            network = ipaddress.IPv6Network(f"{ipv6_str}/{prefix}", strict=False)
            input_address = ipaddress.IPv6Address(ipv6_str)
            
            network_address = network.network_address
            broadcast_address = network.broadcast_address
            total_addresses = network.num_addresses
            
            self.result_text1.delete(1.0, tk.END)
            self.result_text1.insert(tk.END, "=" * 60 + "\n")
            self.result_text1.insert(tk.END, "计算\n")
            self.result_text1.insert(tk.END, "=" * 60 + "\n\n")
            self.result_text1.insert(tk.END, f"输入地址全写: {input_address.exploded}\n\n")
            self.result_text1.insert(tk.END, "网络地址: ")
            self.result_text1.insert(tk.END, f"{network_address.exploded}\n", "network")
            self.result_text1.insert(tk.END, f"网络范围: {network_address.exploded} - {broadcast_address.exploded}\n\n")
            self.result_text1.insert(tk.END, f"前缀长度: /{prefix}\n")
            self.result_text1.insert(tk.END, f"可用地址总数: {total_addresses:,}\n")
            
            self.result_text1.tag_config("network", foreground="#0066CC", font=('Arial', 10, 'bold'))
            
            self.log_status("计算完成", "success")
            
        except (ipaddress.AddressValueError, ValueError) as e:
            UIUtils.highlight_error(self.ipv6_entry1)
            messagebox.showerror("错误", f"输入无效: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
        except Exception as e:
            UIUtils.highlight_error(self.ipv6_entry1)
            messagebox.showerror("错误", f"计算失败: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
    
    def copy_basic_info(self):
        try:
            content = self.result_text1.get(1.0, tk.END)
            if not content.strip():
                self.log_status("没有可复制的内容")
                return
            
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.log_status("已复制计算结果", "success")
        except Exception as e:
            self.log_status(f"复制失败: {str(e)}")