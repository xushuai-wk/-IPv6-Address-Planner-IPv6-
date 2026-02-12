import ipaddress
import tkinter as tk
from tkinter import ttk, messagebox
from utils import UIUtils


class SubnetMembershipTab:
    def __init__(self, notebook, root, log_status_func):
        self.notebook = notebook
        self.root = root
        self.log_status = log_status_func
        self.ipv6_entry5 = None
        self.prefix_entry5 = None
        self.result_text5 = None
        self.create_tab()
    
    def create_tab(self):
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text="所属子网")
        
        frame = ttk.Frame(tab4, padding="25")
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.ipv6_entry5 = UIUtils.create_input_row(frame, "IPv6 地址:", "2026:db8::1", 0, None, placeholder="例如: 2026:db8::1")
        self.prefix_entry5 = UIUtils.create_input_row(frame, "前缀长度:", "64", 1, None, placeholder="0-128")
        UIUtils.create_button_frame(frame, 2, [("计算", self.calculate_subnet_membership), ("复制结果", self.copy_subnet_membership)], 
                               tooltips=["计算所属子网", "复制计算结果到剪贴板"])
        self.result_text5 = UIUtils.create_result_display(frame, 3, "result_text5")
    
    def calculate_subnet_membership(self):
        try:
            ipv6_str = UIUtils.clean_ipv6_input(self.ipv6_entry5.get())
            prefix = int(self.prefix_entry5.get().strip())
            
            if not 0 <= prefix <= 128:
                raise ValueError("前缀长度必须在 0-128 之间")
            
            address = ipaddress.IPv6Address(ipv6_str)
            network = ipaddress.IPv6Network(f"{ipv6_str}/{prefix}", strict=False)
            
            self.result_text5.delete(1.0, tk.END)
            self.result_text5.insert(tk.END, "=" * 60 + "\n")
            self.result_text5.insert(tk.END, "所属子网计算\n")
            self.result_text5.insert(tk.END, "=" * 60 + "\n\n")
            self.result_text5.insert(tk.END, f"输入地址: {address.exploded}\n")
            self.result_text5.insert(tk.END, f"网络地址: {network.network_address.exploded}\n")
            self.result_text5.insert(tk.END, f"子网掩码: /{prefix}\n")
            self.result_text5.insert(tk.END, f"子网范围: {network.network_address.exploded} - {network.broadcast_address.exploded}\n")
            
            if prefix == 127:
                available_hosts = 2
            elif prefix == 128:
                available_hosts = 0
            else:
                available_hosts = network.num_addresses - 2
            self.result_text5.insert(tk.END, f"可用主机数: {available_hosts:,}\n")
            
            self.result_text5.insert(tk.END, f"主机位数: {128 - prefix} 位\n")
            self.result_text5.insert(tk.END, f"子网编号: {network.network_address.exploded}\n")
            
            address_offset = int(address) - int(network.network_address)
            address_index = address_offset + 1
            self.result_text5.insert(tk.END, f"\n该地址在子网中的序号: 第 {address_index:,} 个地址\n")
            
            self.log_status("计算完成", "success")
            
        except (ipaddress.AddressValueError, ValueError) as e:
            UIUtils.highlight_error(self.ipv6_entry5)
            messagebox.showerror("错误", f"输入无效: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
        except Exception as e:
            UIUtils.highlight_error(self.ipv6_entry5)
            messagebox.showerror("错误", f"计算失败: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
    
    def copy_subnet_membership(self):
        try:
            content = self.result_text5.get(1.0, tk.END)
            if not content.strip():
                self.log_status("没有可复制的内容")
                return
            
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.log_status("已复制计算结果", "success")
        except Exception as e:
            self.log_status(f"复制失败: {str(e)}")