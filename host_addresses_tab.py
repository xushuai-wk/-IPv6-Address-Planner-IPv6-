import ipaddress
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from utils import UIUtils


class HostAddressesTab:
    def __init__(self, notebook, root, log_status_func, stop_flag_lock):
        self.notebook = notebook
        self.root = root
        self.log_status = log_status_func
        self.stop_flag_lock = stop_flag_lock
        self.ipv6_entry3 = None
        self.prefix_entry3 = None
        self.result_text3 = None
        self.current_network = None
        self.is_calculating = False
        self.is_exporting = False
        self.calculate_lock = threading.Lock()
        self.export_lock = threading.Lock()
        self.create_tab()
    
    def create_tab(self):
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="可用主机地址")
        
        frame = ttk.Frame(tab3, padding="25")
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.ipv6_entry3 = UIUtils.create_input_row(frame, "IPv6 地址:", "2026:db8::", 0, None, placeholder="例如: 2026:db8::")
        self.prefix_entry3 = UIUtils.create_input_row(frame, "前缀长度:", "64", 1, None, placeholder="0-128")
        UIUtils.create_button_frame(frame, 2, [
            ("计算地址", self.generate_host_addresses),
            ("复制结果", self.copy_hosts),
            ("导出地址", self.export_hosts_dialog)
        ], tooltips=["生成可用主机地址", "复制地址列表到剪贴板", "导出地址到文件"])
        self.result_text3 = UIUtils.create_result_display(frame, 3, "result_text3")
    
    def _set_stop_flag(self, flag_name, value):
        with self.stop_flag_lock:
            setattr(self, flag_name, value)
    
    def _get_stop_flag(self, flag_name):
        with self.stop_flag_lock:
            return getattr(self, flag_name)
    
    def generate_host_addresses(self):
        try:
            if self.is_calculating:
                self.log_status("正在计算中，请稍候...", "info")
                return
            
            ipv6_str = UIUtils.clean_ipv6_input(self.ipv6_entry3.get())
            prefix = int(self.prefix_entry3.get().strip())
            
            if not 0 <= prefix <= 128:
                raise ValueError("前缀长度必须在 0-128 之间")
            
            def generate_thread():
                try:
                    self._set_stop_flag("stop_generate", False)
                    with self.calculate_lock:
                        self.is_calculating = True
                        try:
                            network = ipaddress.IPv6Network(f"{ipv6_str}/{prefix}", strict=False)
                            self.current_network = network
                            
                            total_hosts = network.num_addresses - 2 if network.num_addresses > 2 else 0
                            
                            if prefix == 127:
                                total_hosts = 2
                            elif prefix == 128:
                                total_hosts = 1
                            
                            first_100_hosts = []
                            
                            if prefix == 127:
                                first_100_hosts = [
                                    network.network_address + 1,
                                    network.network_address + 2
                                ]
                            elif prefix == 128:
                                first_100_hosts = [network.network_address]
                            else:
                                hosts_iterator = network.hosts()
                                for i, host in enumerate(hosts_iterator):
                                    if self._get_stop_flag("stop_generate"):
                                        break
                                    if i < 100:
                                        first_100_hosts.append(host)
                                    else:
                                        break
                            
                            if not self._get_stop_flag("stop_generate"):
                                self.root.after(0, lambda: self._display_hosts(network, total_hosts, first_100_hosts, prefix))
                            else:
                                self.root.after(0, lambda: self.log_status("已停止生成", "info"))
                        finally:
                            self.is_calculating = False
                            
                except Exception as e:
                    self.root.after(0, lambda: self._show_error(f"输入无效: {str(e)}"))
                    self.is_calculating = False
            
            self.log_status("正在生成地址...")
            thread = threading.Thread(target=generate_thread, daemon=True)
            thread.start()
            
        except (ipaddress.AddressValueError, ValueError) as e:
            UIUtils.highlight_error(self.ipv6_entry3)
            messagebox.showerror("错误", f"输入无效: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
        except Exception as e:
            UIUtils.highlight_error(self.ipv6_entry3)
            messagebox.showerror("错误", f"计算失败: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
    
    def _display_hosts(self, network, total_hosts, hosts_list, prefix):
        self.result_text3.delete(1.0, tk.END)
        self.result_text3.insert(tk.END, "=" * 60 + "\n")
        self.result_text3.insert(tk.END, "可用主机地址\n")
        self.result_text3.insert(tk.END, "=" * 60 + "\n\n")
        self.result_text3.insert(tk.END, f"网络: {network.exploded}\n")
        self.result_text3.insert(tk.END, f"可用主机总数: {total_hosts:,}\n\n")
        
        if prefix == 127:
            self.result_text3.insert(tk.END, "RFC 6164 说明: /127 网络用于点对点链路，两个有效地址为:\n")
            self.result_text3.insert(tk.END, f"  1. ")
            self.result_text3.insert(tk.END, f"{(network.network_address + 1).exploded}\n", "host")
            self.result_text3.insert(tk.END, f"  2. ")
            self.result_text3.insert(tk.END, f"{(network.network_address + 2).exploded}\n\n", "host")
        elif prefix == 128:
            self.result_text3.insert(tk.END, "RFC 4291 说明: /128 网络表示单个主机地址\n\n")
        
        self.result_text3.insert(tk.END, "-" * 60 + "\n")
        if prefix == 127:
            self.result_text3.insert(tk.END, "可用主机地址:\n")
        elif prefix == 128:
            self.result_text3.insert(tk.END, "主机地址:\n")
        else:
            self.result_text3.insert(tk.END, "前 100 个可用主机地址:\n")
        self.result_text3.insert(tk.END, "-" * 60 + "\n\n")
        
        for i, host in enumerate(hosts_list):
            if prefix == 127:
                self.result_text3.insert(tk.END, f"{i+1}. ")
                self.result_text3.insert(tk.END, f"{host.exploded}\n", "host")
            elif prefix == 128:
                self.result_text3.insert(tk.END, f"{host.exploded}\n", "host")
            else:
                self.result_text3.insert(tk.END, f"{i+1}. ")
                self.result_text3.insert(tk.END, f"{host.exploded}\n", "host")
        
        self.result_text3.tag_config("host", foreground="#009900")
        
        if prefix not in [127, 128] and total_hosts > 100:
            self.result_text3.insert(tk.END, f"\n... 还有 {total_hosts - 100:,} 个地址未显示\n")
            self.result_text3.insert(tk.END, f"点击\"导出地址\"按钮可导出更多地址\n")
        
        self.log_status(f"生成完成，共 {total_hosts:,} 个可用地址", "success")
    
    def _show_error(self, error_msg):
        messagebox.showerror("错误", error_msg)
        self.log_status(f"错误: {error_msg}", "error")
    
    def copy_hosts(self):
        try:
            if not self.current_network:
                self.log_status("请先生成主机地址", "warning")
                return
            
            content = self.result_text3.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.log_status("已复制计算结果", "success")
            
        except Exception as e:
            self.log_status(f"复制失败: {str(e)}")
    
    def export_hosts_dialog(self):
        try:
            if not self.current_network:
                messagebox.showwarning("警告", "请先生成主机地址")
                return
            
            dialog = tk.Toplevel(self.root)
            dialog.title("导出地址")
            dialog.geometry("500x650")
            dialog.transient(self.root)
            dialog.grab_set()
            
            network = self.current_network
            prefix = network.prefixlen
            total_hosts = network.num_addresses - 2 if network.num_addresses > 2 else 0
            
            if prefix == 127:
                total_hosts = 2
            elif prefix == 128:
                total_hosts = 1
            
            main_frame = ttk.Frame(dialog)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            ttk.Label(main_frame, text=f"网络: {network.exploded}", font=('Arial', 10, 'bold')).pack(pady=5)
            ttk.Label(main_frame, text=f"可用主机总数: {total_hosts:,}").pack(pady=5)
            
            if total_hosts > 1000000:
                warning_frame = ttk.Frame(main_frame)
                warning_frame.pack(fill=tk.X, pady=10)
                warning_label = tk.Label(warning_frame, text=f"⚠️ 警告: 地址数量 {total_hosts:,} 超过 100 万", 
                                       fg="red", font=('Arial', 10, 'bold'))
                warning_label.pack(pady=2)
                estimated_size = total_hosts * 50 / 1024 / 1024
                size_str = f"{estimated_size:.1f} MB" if estimated_size < 1024 else f"{estimated_size/1024:.1f} GB"
                size_label = tk.Label(warning_frame, text=f"预估文件大小: {size_str}", 
                                     fg="red", font=('Arial', 9))
                size_label.pack(pady=2)
            
            ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
            
            ttk.Label(main_frame, text="选择导出方式:", font=('Arial', 10, 'bold')).pack(pady=5)
            
            export_var = tk.StringVar(value="all")
            
            ttk.Radiobutton(main_frame, text="导出全部地址", variable=export_var, value="all").pack(anchor=tk.W, pady=2)
            
            ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
            
            ttk.Radiobutton(main_frame, text="导出前 N 个地址", variable=export_var, value="first_n").pack(anchor=tk.W, pady=2)
            
            first_n_frame = ttk.Frame(main_frame)
            first_n_frame.pack(anchor=tk.W, pady=5, padx=20)
            ttk.Label(first_n_frame, text="N = ").pack(side=tk.LEFT)
            first_n_entry = ttk.Entry(first_n_frame, width=15)
            first_n_entry.insert(0, "1000")
            first_n_entry.pack(side=tk.LEFT)
            
            ttk.Radiobutton(main_frame, text="导出后 N 个地址", variable=export_var, value="last_n").pack(anchor=tk.W, pady=2)
            
            last_n_frame = ttk.Frame(main_frame)
            last_n_frame.pack(anchor=tk.W, pady=5, padx=20)
            ttk.Label(last_n_frame, text="N = ").pack(side=tk.LEFT)
            last_n_entry = ttk.Entry(last_n_frame, width=15)
            last_n_entry.insert(0, "1000")
            last_n_entry.pack(side=tk.LEFT)
            
            ttk.Radiobutton(main_frame, text="从第 N 个地址到第 N 个地址", variable=export_var, value="range").pack(anchor=tk.W, pady=2)
            
            range_frame = ttk.Frame(main_frame)
            range_frame.pack(anchor=tk.W, pady=5, padx=20)
            ttk.Label(range_frame, text="从第 ").pack(side=tk.LEFT)
            range_start_entry = ttk.Entry(range_frame, width=10)
            range_start_entry.insert(0, "1")
            range_start_entry.pack(side=tk.LEFT, padx=2)
            ttk.Label(range_frame, text=" 个到第 ").pack(side=tk.LEFT, padx=2)
            range_end_entry = ttk.Entry(range_frame, width=10)
            range_end_entry.insert(0, "1000")
            range_end_entry.pack(side=tk.LEFT, padx=2)
            ttk.Label(range_frame, text=" 个").pack(side=tk.LEFT)
            
            ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
            
            def on_export():
                export_type = export_var.get()
                
                if export_type == "all":
                    if total_hosts > 1000000:
                        estimated_size = total_hosts * 50 / 1024 / 1024
                        size_str = f"{estimated_size:.1f} MB" if estimated_size < 1024 else f"{estimated_size/1024:.1f} GB"
                        confirm = messagebox.askyesno(
                            "⚠️ 警告：超大网络导出",
                            f"您即将导出全部 {total_hosts:,} 个地址。\n\n"
                            f"⚠️ 注意事项：\n"
                            f"• 预估文件大小: {size_str}\n"
                            f"• 导出可能需要很长时间\n"
                            f"• 将占用大量磁盘空间\n"
                            f"• 可能导致程序响应变慢\n\n"
                            f"建议：考虑使用\"前N个\"或\"指定范围\"选项\n\n"
                            f"是否仍要导出？",
                            icon=messagebox.WARNING
                        )
                        if not confirm:
                            return
                    elif total_hosts > 10000:
                        confirm = messagebox.askyesno(
                            "确认导出",
                            f"您即将导出全部 {total_hosts:,} 个地址。\n\n"
                            f"地址数量较多，导出可能需要较长时间。\n\n"
                            f"是否继续导出？",
                            icon=messagebox.WARNING
                        )
                        if not confirm:
                            return
                    start_index = 1
                    end_index = total_hosts
                    count = total_hosts
                elif export_type == "first_n":
                    try:
                        count = int(first_n_entry.get().strip())
                        if count <= 0:
                            messagebox.showerror("错误", "请输入大于 0 的数字")
                            return
                        count = min(count, total_hosts)
                        start_index = 1
                        end_index = count
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的数字")
                        return
                elif export_type == "last_n":
                    try:
                        count = int(last_n_entry.get().strip())
                        if count <= 0:
                            messagebox.showerror("错误", "请输入大于 0 的数字")
                            return
                        count = min(count, total_hosts)
                        start_index = max(1, total_hosts - count + 1)
                        end_index = total_hosts
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的数字")
                        return
                elif export_type == "range":
                    try:
                        start_index = int(range_start_entry.get().strip())
                        end_index = int(range_end_entry.get().strip())
                        if start_index <= 0 or end_index <= 0:
                            messagebox.showerror("错误", "请输入大于 0 的数字")
                            return
                        if start_index > end_index:
                            messagebox.showerror("错误", "起始地址不能大于结束地址")
                            return
                        if end_index > total_hosts:
                            messagebox.showerror("错误", f"结束地址不能超过可用地址总数 {total_hosts:,}")
                            return
                        count = end_index - start_index + 1
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的数字")
                        return
                else:
                    return
                
                dialog.destroy()
                self.export_hosts(export_type, start_index, end_index, count, total_hosts)
            
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(pady=15)
            ttk.Button(button_frame, text="导出", command=on_export).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("错误", f"打开导出对话框失败: {str(e)}")
            self.log_status(f"错误: {str(e)}", "error")
    
    def export_hosts(self, export_type, start_index, end_index, count, total_hosts):
        try:
            if self.is_exporting:
                messagebox.showwarning("警告", "正在导出中，请稍候...")
                return
            
            if not self.current_network:
                messagebox.showwarning("警告", "请先生成主机地址")
                return
            
            network = self.current_network
            prefix = network.prefixlen
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
                title="保存主机地址列表"
            )
            
            if not file_path:
                return
            
            progress_dialog = tk.Toplevel(self.root)
            progress_dialog.title("导出进度")
            progress_dialog.geometry("450x250")
            progress_dialog.transient(self.root)
            progress_dialog.grab_set()
            
            frame = ttk.Frame(progress_dialog, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="正在导出地址...", font=('Arial', 10, 'bold')).pack(pady=10)
            
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100, length=380)
            progress_bar.pack(pady=10)
            
            progress_label = ttk.Label(frame, text="准备中...")
            progress_label.pack(pady=5)
            
            stats_label = ttk.Label(frame, text="")
            stats_label.pack(pady=5)
            
            def on_stop():
                self._set_stop_flag("stop_export", True)
            
            ttk.Button(frame, text="停止导出", command=on_stop).pack(pady=10)
            
            progress_dialog.update()
            
            def export_thread():
                try:
                    self._set_stop_flag("stop_export", False)
                    with self.export_lock:
                        self.is_exporting = True
                        try:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(f"网络: {network.exploded}\n")
                                f.write(f"可用主机总数: {total_hosts:,}\n")
                                f.write(f"导出范围: 第 {start_index:,} 个到第 {end_index:,} 个\n")
                                f.write(f"导出数量: {count:,}\n")
                                f.write("=" * 60 + "\n\n")
                                
                                if prefix == 127:
                                    f.write(f"1. {(network.network_address + 1).exploded}\n")
                                    f.write(f"2. {(network.network_address + 2).exploded}\n")
                                    current_index = 2
                                elif prefix == 128:
                                    f.write(f"{network.network_address.exploded}\n")
                                    current_index = 1
                                else:
                                    current_index = 0
                                    start_time = time.time()
                                    
                                    network_int = int(network.network_address)
                                    
                                    for i in range(start_index, end_index + 1):
                                        if self._get_stop_flag("stop_export"):
                                            break
                                        
                                        address_int = network_int + i
                                        address = ipaddress.IPv6Address(address_int)
                                        
                                        current_index += 1
                                        f.write(f"{i}. {address.exploded}\n")
                                        
                                        if current_index % 100000 == 0 or current_index == count:
                                            percent = (current_index / count) * 100
                                            progress_var.set(percent)
                                            
                                            elapsed = time.time() - start_time
                                            if current_index > 0:
                                                rate = current_index / elapsed
                                                remaining = (count - current_index) / rate if rate > 0 else 0
                                                remaining_str = f"{int(remaining)}秒" if remaining < 60 else f"{int(remaining/60)}分{int(remaining%60)}秒"
                                                stats_label.config(text=f"速率: {rate:.0f} 地址/秒 | 剩余: {remaining_str}")
                                            
                                            progress_label.config(text=f"已导出 {current_index:,} / {count:,} ({percent:.1f}%)")
                                            progress_dialog.update()
                            
                            progress_dialog.after(0, lambda: progress_dialog.destroy())
                            
                            if self._get_stop_flag("stop_export"):
                                self.root.after(0, lambda: messagebox.showinfo("已停止", f"导出已停止，已导出部分地址到:\n{file_path}"))
                                self.root.after(0, lambda: self.log_status("导出已停止"))
                            else:
                                self.root.after(0, lambda: messagebox.showinfo("成功", f"已导出 {count:,} 个主机地址到:\n{file_path}"))
                                self.root.after(0, lambda: self.log_status(f"导出成功: {file_path}"))
                        finally:
                            self.is_exporting = False
                            
                except Exception as e:
                    progress_dialog.after(0, lambda: progress_dialog.destroy())
                    self.root.after(0, lambda: messagebox.showerror("错误", f"导出失败: {str(e)}"))
                    self.root.after(0, lambda: self.log_status(f"导出失败: {str(e)}"))
                    self.is_exporting = False
            
            thread = threading.Thread(target=export_thread, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            self.log_status(f"导出失败: {str(e)}")