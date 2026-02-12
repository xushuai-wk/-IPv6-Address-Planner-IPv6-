import ipaddress
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils import UIUtils


class SubnetDivisionTab:
    def __init__(self, notebook, root, log_status_func):
        self.notebook = notebook
        self.root = root
        self.log_status = log_status_func
        self.ipv6_entry2 = None
        self.current_prefix_entry = None
        self.subnet_count_entry = None
        self.result_text2 = None
        self.create_tab()
    
    def create_tab(self):
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="子网划分")
        
        frame = ttk.Frame(tab2, padding="25")
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.ipv6_entry2 = UIUtils.create_input_row(frame, "IPv6 地址:", "2026:db8::", 0, None, placeholder="例如: 2026:db8::")
        self.current_prefix_entry = UIUtils.create_input_row(frame, "当前前缀:", "64", 1, None, placeholder="0-128")
        self.subnet_count_entry = UIUtils.create_input_row(frame, "目标划分网段数量:", "8", 2, None, placeholder="例如: 8")
        UIUtils.create_button_frame(frame, 3, [
            ("计算", self.calculate_subnet_division),
            ("复制结果", self.copy_subnet_division),
            ("导出完整列表", self.export_subnets)
        ], tooltips=["计算子网划分", "复制计算结果到剪贴板", "导出所有子网到文件"])
        self.result_text2 = UIUtils.create_result_display(frame, 4, "result_text2")
    
    def calculate_subnet_division(self):
        try:
            ipv6_str = UIUtils.clean_ipv6_input(self.ipv6_entry2.get())
            current_prefix = int(self.current_prefix_entry.get().strip())
            subnet_count = int(self.subnet_count_entry.get().strip())
            
            if not 0 <= current_prefix <= 128:
                raise ValueError("前缀长度必须在 0-128 之间")
            if subnet_count <= 0:
                raise ValueError("划分网段数量必须大于 0")
            
            network = ipaddress.IPv6Network(f"{ipv6_str}/{current_prefix}", strict=False)
            
            new_prefix = current_prefix
            max_subnets = 1
            while max_subnets < subnet_count and new_prefix < 128:
                new_prefix += 1
                max_subnets = 2 ** (new_prefix - current_prefix)
            
            if new_prefix == 128 and max_subnets < subnet_count:
                raise ValueError("无法划分这么多子网，已达到最大前缀长度 /128")
            
            subnets_iterator = network.subnets(new_prefix=new_prefix)
            first_100_subnets = []
            for i, subnet in enumerate(subnets_iterator):
                if i < 100:
                    first_100_subnets.append(subnet)
                else:
                    break
            
            self.result_text2.delete(1.0, tk.END)
            self.result_text2.insert(tk.END, "=" * 60 + "\n")
            self.result_text2.insert(tk.END, "计算\n")
            self.result_text2.insert(tk.END, "=" * 60 + "\n\n")
            self.result_text2.insert(tk.END, f"原网络: {network.exploded}\n")
            self.result_text2.insert(tk.END, f"原前缀: /{current_prefix}\n")
            self.result_text2.insert(tk.END, "新前缀: ")
            self.result_text2.insert(tk.END, f"/{new_prefix}\n", "highlight")
            self.result_text2.insert(tk.END, f"可划分子网总数: {max_subnets:,}\n")
            self.result_text2.insert(tk.END, f"请求划分数量: {subnet_count}\n\n")
            self.result_text2.insert(tk.END, "-" * 60 + "\n")
            self.result_text2.insert(tk.END, "前 100 个子网段:\n")
            self.result_text2.insert(tk.END, "-" * 60 + "\n\n")
            
            for i, subnet in enumerate(first_100_subnets):
                self.result_text2.insert(tk.END, f"{i+1}. ")
                self.result_text2.insert(tk.END, f"{subnet.exploded}\n", "subnet")
            
            self.result_text2.tag_config("highlight", foreground="#0066CC", font=('Arial', 10, 'bold'))
            self.result_text2.tag_config("subnet", foreground="#009900")
            
            if max_subnets > 100:
                self.result_text2.insert(tk.END, f"\n... 还有 {max_subnets - 100:,} 个子网未显示\n")
                self.result_text2.insert(tk.END, f"点击\"导出完整列表\"按钮可导出所有 {max_subnets:,} 个子网\n")
            
            self.log_status(f"计算完成，共 {max_subnets:,} 个子网", "success")
            
        except (ipaddress.AddressValueError, ValueError) as e:
            UIUtils.highlight_error(self.ipv6_entry2)
            messagebox.showerror("错误", f"输入无效: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
        except Exception as e:
            UIUtils.highlight_error(self.ipv6_entry2)
            messagebox.showerror("错误", f"计算失败: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
    
    def export_subnets(self):
        try:
            ipv6_str = UIUtils.clean_ipv6_input(self.ipv6_entry2.get())
            current_prefix = int(self.current_prefix_entry.get().strip())
            subnet_count = int(self.subnet_count_entry.get().strip())
            
            if not 0 <= current_prefix <= 128:
                raise ValueError("前缀长度必须在 0-128 之间")
            if subnet_count <= 0:
                raise ValueError("划分网段数量必须大于 0")
            
            network = ipaddress.IPv6Network(f"{ipv6_str}/{current_prefix}", strict=False)
            
            new_prefix = current_prefix
            max_subnets = 1
            while max_subnets < subnet_count and new_prefix < 128:
                new_prefix += 1
                max_subnets = 2 ** (new_prefix - current_prefix)
            
            if new_prefix == 128 and max_subnets < subnet_count:
                raise ValueError("无法划分这么多子网，已达到最大前缀长度 /128")
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV 文件", "*.csv"), ("文本文件", "*.txt"), ("所有文件", "*.*")],
                title="保存子网列表"
            )
            
            if not file_path:
                return
            
            self._export_subnets_preview(network, new_prefix, max_subnets, file_path)
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            self.log_status(f"导出失败: {str(e)}", "error")
    
    def _export_subnets_preview(self, network, new_prefix, max_subnets, file_path):
        preview_dialog = tk.Toplevel(self.root)
        preview_dialog.title("导出预览")
        preview_dialog.geometry("600x400")
        preview_dialog.transient(self.root)
        preview_dialog.grab_set()
        
        main_frame = ttk.Frame(preview_dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text=f"即将导出 {max_subnets:,} 个子网", font=('Arial', 10, 'bold')).pack(pady=5)
        
        preview_text = tk.Text(main_frame, height=12, wrap=tk.WORD, font=('Arial', 9))
        preview_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(preview_text, orient=tk.VERTICAL, command=preview_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        preview_text.config(yscrollcommand=scrollbar.set)
        
        for i, subnet in enumerate(network.subnets(new_prefix=new_prefix), 1):
            if i > 10:
                preview_text.insert(tk.END, f"\n... 还有 {max_subnets - 10:,} 个子网 ...\n")
                break
            preview_text.insert(tk.END, f"{i}. {subnet.exploded}\n")
        
        preview_text.config(state=tk.DISABLED)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def do_export():
            preview_dialog.destroy()
            self._do_export_subnets(network, new_prefix, max_subnets, file_path)
        
        def cancel_export():
            preview_dialog.destroy()
        
        ttk.Button(button_frame, text="确认导出", command=do_export).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=cancel_export).pack(side=tk.LEFT, padx=5)
    
    def _do_export_subnets(self, network, new_prefix, max_subnets, file_path):
        try:
            self.log_status("正在导出，请稍候...")
            self.root.update()
            
            if file_path.endswith('.csv'):
                import csv
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['序号', '网络地址', '前缀长度', '子网结束地址', '完整表示'])
                    
                    for i, subnet in enumerate(network.subnets(new_prefix=new_prefix), 1):
                        writer.writerow([
                            i,
                            str(subnet.network_address),
                            subnet.prefixlen,
                            str(subnet.broadcast_address),
                            str(subnet)
                        ])
                        
                        if i % 100000 == 0:
                            self.log_status(f"已导出 {i:,} 个子网...")
                            self.root.update()
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for i, subnet in enumerate(network.subnets(new_prefix=new_prefix), 1):
                        f.write(f"{i}. {subnet.exploded}\n")
                        
                        if i % 100000 == 0:
                            self.log_status(f"已导出 {i:,} 个子网...")
                            self.root.update()
            
            messagebox.showinfo("成功", f"已导出 {max_subnets:,} 个子网到:\n{file_path}")
            self.log_status(f"导出成功: {file_path}", "success")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            self.log_status(f"导出失败: {str(e)}", "error")
    
    def copy_subnet_division(self):
        try:
            content = self.result_text2.get(1.0, tk.END)
            if not content.strip():
                self.log_status("没有可复制的内容")
                return
            
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.log_status("已复制计算结果", "success")
        except Exception as e:
            self.log_status(f"复制失败: {str(e)}")