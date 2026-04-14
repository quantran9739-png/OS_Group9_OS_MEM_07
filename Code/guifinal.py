import customtkinter as ctk
import random
import csv
import os
from tkinter import filedialog, messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #Cấu Hình
        self.title("NHÓM OS_MEM_07 - Memory Management Simulator Pro")
        self.geometry("1300x950") 
        ctk.set_appearance_mode("dark")

        #DATA STORAGE
        self.memory_blocks = []  
        self.process_list = []   
        self.results = []
        self.sim_speed = 5 # Mặc định

        #SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="OS_MEM_07", font=("Roboto", 26, "bold"), text_color="#3498db")
        self.logo_label.pack(pady=20)

        #NÚT NẠP DỮ LIỆU
        self.btn_load_blocks = ctk.CTkButton(self.sidebar, text="📥 1. Nạp Blocks CSV", command=self.load_blocks_csv)
        self.btn_load_blocks.pack(pady=10, padx=20)

        self.btn_load_procs = ctk.CTkButton(self.sidebar, text="📂 2. Nạp Process CSV", command=self.load_procs_csv)
        self.btn_load_procs.pack(pady=10, padx=20)

        self.algo_label = ctk.CTkLabel(self.sidebar, text="Chọn thuật toán:")
        self.algo_label.pack(pady=(15,0))
        self.algo_menu = ctk.CTkOptionMenu(self.sidebar, values=["First-Fit", "Best-Fit", "Worst-Fit"])
        self.algo_menu.pack(pady=10, padx=20)

        #THANH CHỈNH TỐC ĐỘ
        self.speed_label = ctk.CTkLabel(self.sidebar, text="Tốc độ mô phỏng:")
        self.speed_label.pack(pady=(10,0))
        self.speed_slider = ctk.CTkSlider(self.sidebar, from_=1, to=50, command=self.update_speed)
        self.speed_slider.set(self.sim_speed)
        self.speed_slider.pack(pady=10, padx=20)

        self.run_btn = ctk.CTkButton(self.sidebar, text="🚀 CHẠY MÔ PHỎNG", fg_color="#28a745", hover_color="#218838", font=("Roboto", 14, "bold"), command=self.run_simulation)
        self.run_btn.pack(pady=20, padx=20)

        self.export_btn = ctk.CTkButton(self.sidebar, text="📊 XUẤT KẾT QUẢ CSV", fg_color="#3498db", command=self.export_csv)
        self.export_btn.pack(pady=10, padx=20)

        self.reset_btn = ctk.CTkButton(self.sidebar, text="🔄 RESET", fg_color="#e67e22", command=self.reset_app)
        self.reset_btn.pack(pady=10, padx=20)

        #MAIN VIEW
        self.main_view = ctk.CTkFrame(self)
        self.main_view.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        #DASHBOARD
        self.dash_frame = ctk.CTkFrame(self.main_view, fg_color="gray15", corner_radius=10)
        self.dash_frame.pack(fill="x", padx=20, pady=10)
        
        self.stat_success = ctk.CTkLabel(self.dash_frame, text="✅ Allocated: 0", text_color="#2ecc71", font=("Roboto", 16, "bold"))
        self.stat_success.pack(side="left", padx=40, pady=15)
        
        self.stat_fail = ctk.CTkLabel(self.dash_frame, text="❌ Not Allocated: 0", text_color="#e74c3c", font=("Roboto", 16, "bold"))
        self.stat_fail.pack(side="left", padx=40, pady=15)

        self.stat_usage = ctk.CTkLabel(self.dash_frame, text="📈 Memory Usage: 0%", text_color="#3498db", font=("Roboto", 16, "bold"))
        self.stat_usage.pack(side="left", padx=40, pady=15)

        #CANVAS (Memory Visualizer)
        self.mem_canvas = ctk.CTkCanvas(self.main_view, height=220, bg="#111", highlightthickness=0)
        self.mem_canvas.pack(fill="x", padx=20, pady=10)

        #BẢNG CHI TIẾT
        self.table_container = ctk.CTkScrollableFrame(self.main_view, label_text="LỊCH SỬ CẤP PHÁT CHI TIẾT", label_font=("Roboto", 14, "bold"))
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        self.render_table_header()

        self.status_label = ctk.CTkLabel(self, text="Sẵn sàng...", font=("Roboto", 12, "italic"))
        self.status_label.pack(side="bottom", fill="x", padx=20, pady=5)

    def update_speed(self, val):
        self.sim_speed = int(val)

    def render_table_header(self):
        self.header_frame = ctk.CTkFrame(self.table_container, fg_color="#2c3e50")
        self.header_frame.pack(fill="x", padx=5, pady=2)
        headers = ["Process", "Size", "Block", "Internal Frag.", "Status"]
        for i, text in enumerate(headers):
            ctk.CTkLabel(self.header_frame, text=text, font=("Roboto", 12, "bold"), width=160).grid(row=0, column=i, padx=10, pady=8)

    #INPUT UI
    def load_blocks_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            try:
                self.memory_blocks = []
                with open(path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.memory_blocks.append({
                            "id": row['Block'], 
                            "size": int(row['Size']), 
                            "original_size": int(row['Size']),
                            "p": None
                        })
                self.draw_blocks()
                self.status_label.configure(text=f"Đã nạp {len(self.memory_blocks)} Memory Blocks.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Sai định dạng file: {e}")

    def load_procs_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            try:
                self.process_list = []
                with open(path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.process_list.append({"id": row['Process'], "size": int(row['Size'])})
                self.status_label.configure(text=f"Đã nạp {len(self.process_list)} Processes.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Sai định dạng file: {e}")

    #VISUALIZER 
    def draw_blocks(self):
        self.mem_canvas.delete("all")
        if not self.memory_blocks: return
        
        self.update_idletasks()
        can_w = self.mem_canvas.winfo_width() - 80
        total_mem_size = sum(b['original_size'] for b in self.memory_blocks)
        curr_x = 40
        
        for b in self.memory_blocks:
            w = (b['original_size'] / total_mem_size) * can_w
            # Vẽ viền Block
            self.mem_canvas.create_rectangle(curr_x, 50, curr_x + w, 160, outline="#7f8c8d", width=2)
            # Text ID
            self.mem_canvas.create_text(curr_x + w/2, 175, text=f"{b['id']}\n({b['original_size']}MB)", fill="white", font=("Roboto", 10))
            b['coords'] = (curr_x, 50, curr_x + w, 160)
            curr_x += w

    def animate_fill(self, p_name, p_size, block_idx, callback):
        block = self.memory_blocks[block_idx]
        coords = block['coords']
        
        ratio = p_size / block['original_size']
        full_w = coords[2] - coords[0]
        target_w = full_w * ratio
        
        start_x, start_y, end_x, end_y = coords
        curr_w = 0
        color = random.choice(["#3498db", "#9b59b6", "#e67e22", "#1abc9c", "#f1c40f"])
        
        def step():
            nonlocal curr_w
            tag = f"fill_{p_name}"
            self.mem_canvas.delete(tag)
            if curr_w < target_w:
                curr_w += self.sim_speed 
                if curr_w > target_w: curr_w = target_w
                self.mem_canvas.create_rectangle(start_x, start_y, start_x + curr_w, end_y, fill=color, outline="white", tags=tag)
                self.after(10, step)
            else:
                # Sau khi vẽ Process, vẽ phần dư (Fragmentation) màu xám
                if target_w < full_w:
                    self.mem_canvas.create_rectangle(start_x + target_w, start_y, end_x, end_y, fill="#2c3e50", stipple="gray25")
                    self.mem_canvas.create_text(start_x + target_w + (full_w-target_w)/2, (start_y + end_y)/2, 
                                                text=f"Free", fill="#7f8c8d", font=("Roboto", 8))
                
                self.mem_canvas.create_text(start_x + target_w/2, (start_y + end_y)/2, 
                                            text=p_name, fill="white", font=("Roboto", 11, "bold"), tags=tag)
                callback()
        step()

    #CORE LOGIC
    def run_simulation(self):
        if not self.process_list or not self.memory_blocks:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nạp đầy đủ Blocks và Process!")
            return
        
        self.reset_simulation_data()
        algo = self.algo_menu.get()
        stats = {"success": 0, "fail": 0, "used_mem": 0}
        total_capacity = sum(b['original_size'] for b in self.memory_blocks)

        def process_loop(idx):
            if idx >= len(self.process_list):
                usage_pct = (stats['used_mem'] / total_capacity) * 100 if total_capacity > 0 else 0
                self.stat_usage.configure(text=f"📈 Memory Usage: {usage_pct:.1f}%")
                self.status_label.configure(text=f"Hoàn tất mô phỏng {algo}!")
                return

            p = self.process_list[idx]
            target_block_idx = -1

            # Logic thuật toán (Quân & Hảo)
            if algo == "First-Fit":
                for i, b in enumerate(self.memory_blocks):
                    if b['p'] is None and b['size'] >= p['size']:
                        target_block_idx = i
                        break
            elif algo == "Best-Fit":
                best_idx, min_diff = -1, float('inf')
                for i, b in enumerate(self.memory_blocks):
                    if b['p'] is None and b['size'] >= p['size']:
                        if (b['size'] - p['size']) < min_diff:
                            min_diff = b['size'] - p['size']; best_idx = i
                target_block_idx = best_idx
            elif algo == "Worst-Fit":
                worst_idx, max_diff = -1, -1
                for i, b in enumerate(self.memory_blocks):
                    if b['p'] is None and b['size'] >= p['size']:
                        if (b['size'] - p['size']) > max_diff:
                            max_diff = b['size'] - p['size']; worst_idx = i
                target_block_idx = worst_idx

            if target_block_idx != -1:
                b = self.memory_blocks[target_block_idx]
                b['p'] = p['id']
                rem = b['size'] - p['size']
                stats['success'] += 1; stats['used_mem'] += p['size']
                
                self.results.append([p['id'], p['size'], b['id'], rem, "Allocated"])
                self.add_table_row(p['id'], p['size'], b['id'], rem, "Allocated")
                self.stat_success.configure(text=f"✅ Allocated: {stats['success']}")
                self.animate_fill(p['id'], p['size'], target_block_idx, lambda: process_loop(idx + 1))
            else:
                stats['fail'] += 1
                self.results.append([p['id'], p['size'], "N/A", 0, "Not Allocated"])
                self.add_table_row(p['id'], p['size'], "N/A", 0, "Not Allocated")
                self.stat_fail.configure(text=f"❌ Not Allocated: {stats['fail']}")
                process_loop(idx + 1)

        process_loop(0)

    def add_table_row(self, p, s, b, rem, status):
        row = ctk.CTkFrame(self.table_container, fg_color="transparent")
        row.pack(fill="x", padx=5, pady=1)
        color = "#2ecc71" if status == "Allocated" else "#e74c3c"
        vals = [f"{p}", f"{s} MB", f"{b}", f"{rem} MB", status]
        for i, v in enumerate(vals):
            ctk.CTkLabel(row, text=v, width=160, text_color="white" if i < 4 else color).grid(row=0, column=i, padx=10, pady=2)

    def export_csv(self):
        if not self.results:
            messagebox.showwarning("Trống", "Chưa có kết quả để xuất!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if path:
            with open(path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Process", "Size", "Block", "Remaining", "Status"])
                writer.writerows(self.results)
            messagebox.showinfo("Thành công", "Đã lưu kết quả!")

    def reset_simulation_data(self):
        self.results = []
        for b in self.memory_blocks:
            b['p'] = None
            b['size'] = b['original_size']
        for child in self.table_container.winfo_children():
            if child != self.header_frame: child.destroy()
        self.draw_blocks()

    def reset_app(self):
        self.memory_blocks = []
        self.process_list = []
        self.reset_simulation_data()
        self.stat_success.configure(text="✅ Allocated: 0")
        self.stat_fail.configure(text="❌ Not Allocated: 0")
        self.stat_usage.configure(text="📈 Memory Usage: 0%")
        self.status_label.configure(text="Đã hệ thống về trạng thái ban đầu.")

if __name__ == "__main__":
    app = App()
    app.mainloop()