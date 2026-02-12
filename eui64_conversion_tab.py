import ipaddress
import tkinter as tk
from tkinter import ttk, messagebox
import re
from utils import UIUtils


class EUI64ConversionTab:
    def __init__(self, notebook, root, log_status_func):
        self.notebook = notebook
        self.root = root
        self.log_status = log_status_func
        self.mac_entry = None
        self.prefix_entry = None
        self.result_text6 = None
        self.create_tab()
    
    def create_tab(self):
        tab5 = ttk.Frame(self.notebook)
        self.notebook.add(tab5, text="EUI-64 转换")
        
        frame = ttk.Frame(tab5, padding="25")
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.mac_entry = UIUtils.create_input_row(frame, "MAC 地址 (格式: XX:XX:XX:XX:XX:XX):", "00:11:22:33:44:55", 0, None, placeholder="例如: 00:11:22:33:44:55")
        self.prefix_entry = UIUtils.create_input_row(frame, "IPv6 前缀 (格式: 2026:db8::/64):", "2026:db8::/64", 1, None, placeholder="例如: 2026:db8::/64")
        UIUtils.create_button_frame(frame, 2, [("转换", self.convert_eui64), ("复制结果", self.copy_eui64_result)], 
                               tooltips=["MAC地址转换为EUI-64", "复制转换结果到剪贴板"])
        self.result_text6 = UIUtils.create_result_display(frame, 3, "result_text6")
    
    def convert_eui64(self):
        try:
            mac_input = self.mac_entry.get().strip()
            
            mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$')
            if not mac_pattern.match(mac_input):
                raise ValueError("MAC 地址格式无效，请使用 XX:XX:XX:XX:XX:XX 或 XX-XX-XX-XX-XX-XX 格式")
            
            mac_str = mac_input.replace(":", "").replace("-", "")
            if len(mac_str) != 12:
                raise ValueError("MAC 地址必须是12位十六进制数字 (例如: 001122334455)")
            
            eui64 = mac_str[:6] + "FFFE" + mac_str[6:]
            
            mac_bytes = bytes.fromhex(eui64)
            mac_bytes = bytearray(mac_bytes)
            mac_bytes[0] = mac_bytes[0] ^ 0x02
            eui64 = mac_bytes.hex()
            
            eui64_formatted = ":".join([eui64[i:i+4] for i in range(0, len(eui64), 4)])
            
            prefix = self.prefix_entry.get().strip()
            if not prefix.endswith("/64"):
                raise ValueError("前缀必须包含 /64 例如: 2026:db8::/64")
            
            prefix_without_len = prefix.split("/")[0]
            
            if prefix_without_len.endswith("::"):
                ipv6_address = prefix_without_len + eui64_formatted
            else:
                ipv6_address = prefix_without_len + "::" + eui64_formatted
            
            ipv6_full_address = ipaddress.IPv6Address(ipv6_address)
            
            self.result_text6.delete(1.0, tk.END)
            self.result_text6.insert(tk.END, "=" * 60 + "\n")
            self.result_text6.insert(tk.END, "EUI-64 转换结果\n")
            self.result_text6.insert(tk.END, "=" * 60 + "\n\n")
            self.result_text6.insert(tk.END, f"原始 MAC 地址: {self.mac_entry.get()}\n")
            self.result_text6.insert(tk.END, f"转换后的 EUI-64: {eui64_formatted}\n")
            self.result_text6.insert(tk.END, f"完整 IPv6 地址: {ipv6_full_address.exploded}\n")
            self.result_text6.insert(tk.END, f"网络前缀: {prefix_without_len}\n")
            
            self.result_text6.insert(tk.END, "\n地址结构:\n")
            self.result_text6.insert(tk.END, f"网络前缀: {prefix_without_len}\n")
            self.result_text6.insert(tk.END, f"接口标识: {eui64_formatted}\n")
            self.result_text6.insert(tk.END, f"完整地址: {ipv6_full_address.exploded}\n")
            
            self.log_status("转换完成", "success")
            
        except (ValueError, ipaddress.AddressValueError) as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
    
    def copy_eui64_result(self):
        try:
            content = self.result_text6.get(1.0, tk.END)
            if not content.strip():
                self.log_status("没有可复制的内容")
                return
            
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.log_status("已复制转换结果", "success")
        except Exception as e:
            self.log_status(f"复制失败: {str(e)}")