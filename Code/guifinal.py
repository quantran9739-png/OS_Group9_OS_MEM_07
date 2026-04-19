import customtkinter as ctk
import random
import csv
from tkinter import filedialog, messagebox
import main_logic  # Đảm bảo file main_logic.py nằm cùng thư mục

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NHÓM OS_MEM_07 - Memory Management Simulator Pro")
        self.geometry("1300x950") 
        ctk.set_appearance_mode("dark")

        self.memory_blocks = []  
        self.process_list = []   
        self.results = []
        self.sim_speed = 5

        # --- SIDEBAR (THANH ĐIỀU KHIỂN) ---
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(self.sidebar, text="OS_MEM_07", font=("Roboto", 26, "bold"), text_color="#3498db").pack(pady=20)

        ctk.CTkButton(self.sidebar, text="📥 1. Nạp Blocks CSV", command=self.load_blocks_csv).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📂 2. Nạp Process CSV", command=self.load_procs_csv).pack(pady=10, padx=20)
        
        self.algo_menu = ctk.CTkOptionMenu(self.sidebar, values=["First-Fit", "Best-Fit", "Worst-Fit"])
        self.algo_menu.pack(pady=10, padx=20)

        ctk.CTkLabel(self.sidebar, text="Tốc độ mô phỏng:").pack(pady=(10,0))
        self.speed_slider = ctk.CTkSlider(self.sidebar, from_=1, to=50, command=self.update_speed)
        self.speed_slider.set(self.sim_speed)
        self.speed_slider.pack(pady=10, padx=20)

        ctk.CTkButton(self.sidebar, text="🚀 CHẠY MÔ PHỎNG", fg_color="#28a745", command=self.run_simulation).pack(pady=20, padx=20)
        ctk.CTkButton(self.sidebar, text="📊 XUẤT KẾT QUẢ CSV", fg_color="#3498db", command=self.export_csv).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="🔄 RESET", fg_color="#e67e22", command=self.reset_app).pack(pady=10, padx=20)

        # --- MAIN VIEW (HIỂN THỊ CHÍNH) ---
        self.main_view = ctk.CTkFrame(self)
        self.main_view.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Dashboard thống kê
        self.dash_frame = ctk.CTkFrame(self.main_view, fg_color="gray15")
        self.dash_frame.pack(fill="x", padx=20, pady=10)
        self.stat_success = ctk.CTkLabel(self.dash_frame, text="✅ Allocated: 0", text_color="#2ecc71")
        self.stat_success.pack(side="left", padx=40, pady=15)
        self.stat_fail = ctk.CTkLabel(self.dash_frame, text="❌ Not Allocated: 0", text_color="#e74c3c")
        self.stat_fail.pack(side="left", padx=40, pady=15)
        self.stat_usage = ctk.CTkLabel(self.dash_frame, text="📈 Memory Usage: 0%", text_color="#3498db")
        self.stat_usage.pack(side="left", padx=40, pady=15)

        # Canvas vẽ biểu đồ bộ nhớ
        self.mem_canvas = ctk.CTkCanvas(self.main_view, height=220, bg="#111", highlightthickness=0)
        self.mem_canvas.pack(fill="x", padx=20, pady=10)

        # Bảng lịch sử cấp phát
        self.table_container = ctk.CTkScrollableFrame(self.main_view, label_text="LỊCH SỬ CẤP PHÁT CHI TIẾT")
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        self.render_table_header()

    def update_speed(self, val): 
        self.sim_speed = int(val)

    def render_table_header(self):
        self.header_frame = ctk.CTkFrame(self.table_container, fg_color="#2c3e50")
        self.header_frame.pack(fill="x", padx=5, pady=2)
        headers = ["Process", "Size", "Block", "Internal Frag.", "Status"]
        for i, text in enumerate(headers):
            ctk.CTkLabel(self.header_frame, text=text, width=160, font=("Roboto", 12, "bold")).grid(row=0, column=i, padx=10, pady=8)

    def load_blocks_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            try:
                self.memory_blocks = []
                with open(path, mode='r', encoding='utf-8-sig') as f:
                    for row in csv.DictReader(f):
                        self.memory_blocks.append({
                            "id": row['Block'], 
                            "size": int(row['Size']), 
                            "original_size": int(row['Size']), 
                            "p": None
                        })
                self.draw_blocks()
                messagebox.showinfo("Thành công", f"Đã nạp {len(self.memory_blocks)} blocks.")
            except Exception as e: 
                messagebox.showerror("Lỗi", f"File không đúng định dạng: {e}")

    def load_procs_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            try:
                self.process_list = []
                with open(path, mode='r', encoding='utf-8-sig') as f:
                    for row in csv.DictReader(f):
                        self.process_list.append({"id": row['Process'], "size": int(row['Size'])})
                messagebox.showinfo("Thành công", f"Đã nạp {len(self.process_list)} tiến trình.")
            except Exception as e: 
                messagebox.showerror("Lỗi", f"File không đúng định dạng: {e}")

    def draw_blocks(self):
        self.mem_canvas.delete("all")
        if not self.memory_blocks: return
        self.update_idletasks()
        can_w = self.mem_canvas.winfo_width() - 80
        curr_x = 40
        total_mem = sum(b['original_size'] for b in self.memory_blocks)
        for b in self.memory_blocks:
            w = (b['original_size'] / total_mem) * can_w
            self.mem_canvas.create_rectangle(curr_x, 50, curr_x + w, 160, outline="#7f8c8d", width=2)
            self.mem_canvas.create_text(curr_x + w/2, 175, text=f"{b['id']}\n({b['original_size']}MB)", fill="white")
            b['coords'] = (curr_x, 50, curr_x + w, 160)
            curr_x += w

    def animate_fill(self, p_name, p_size, block_idx, callback):
        block = self.memory_blocks[block_idx]
        start_x, start_y, end_x, end_y = block['coords']
        target_w = (end_x - start_x) * (p_size / block['original_size'])
        curr_w, color = 0, random.choice(["#3498db", "#9b59b6", "#e67e22"])
        
        def step():
            nonlocal curr_w
            self.mem_canvas.delete(f"fill_{p_name}")
            if curr_w < target_w:
                curr_w += self.sim_speed
                self.mem_canvas.create_rectangle(start_x, start_y, start_x + min(curr_w, target_w), end_y, fill=color, tags=f"fill_{p_name}")
                self.after(10, step)
            else:
                # Vẽ phần còn lại của block (nếu có)
                if target_w < (end_x - start_x):
                    self.mem_canvas.create_rectangle(start_x + target_w, start_y, end_x, end_y, fill="#2c3e50")
                self.mem_canvas.create_text(start_x + target_w/2, (start_y + end_y)/2, text=p_name, fill="white")
                callback()
        step()

    def run_simulation(self):
        if not self.process_list or not self.memory_blocks:
            messagebox.showwarning("Cảnh báo", "Vui lòng nạp đủ file Blocks và Process trước!")
            return
        
        self.reset_simulation_data()
        algo = self.algo_menu.get()
        stats = {"success": 0, "fail": 0, "used": 0}
        total_cap = sum(b['original_size'] for b in self.memory_blocks)
        
        def process_loop(idx):
            if idx >= len(self.process_list):
                pct = (stats['used'] / total_cap * 100) if total_cap > 0 else 0
                self.stat_usage.configure(text=f"📈 Memory Usage: {pct:.1f}%")
                return
            
            p = self.process_list[idx]
            target_idx = -1
            
            if algo == "First-Fit": target_idx = main_logic.find_first_fit(self.memory_blocks, p['size'])
            elif algo == "Best-Fit": target_idx = main_logic.find_best_fit(self.memory_blocks, p['size'])
            elif algo == "Worst-Fit": target_idx = main_logic.find_worst_fit(self.memory_blocks, p['size'])
                        
            if target_idx != -1:
                b = self.memory_blocks[target_idx]
                b['p'] = p['id']
                rem = b['size'] - p['size']
                b['size'] = rem # Cập nhật size còn lại của block
                
                stats['success'] += 1
                stats['used'] += p['size']
                
                self.results.append([p['id'], p['size'], b['id'], rem, "Allocated"])
                self.add_table_row(p['id'], p['size'], b['id'], rem, "Allocated")
                self.stat_success.configure(text=f"✅ Allocated: {stats['success']}")
                
                self.animate_fill(p['id'], p['size'], target_idx, lambda: process_loop(idx + 1))
            else:
                stats['fail'] += 1
                self.results.append([p['id'], p['size'], "N/A", 0, "Fail"])
                self.add_table_row(p['id'], p['size'], "N/A", 0, "Fail")
                self.stat_fail.configure(text=f"❌ Not Allocated: {stats['fail']}")
                process_loop(idx + 1)
                
        process_loop(0)

    def add_table_row(self, p, s, b, rem, status):
        row = ctk.CTkFrame(self.table_container, fg_color="transparent")
        row.pack(fill="x", padx=5, pady=1)
        color = "#2ecc71" if status == "Allocated" else "#e74c3c"
        for i, v in enumerate([p, f"{s}MB", b, f"{rem}MB", status]):
            ctk.CTkLabel(row, text=v, width=160, text_color="white" if i < 4 else color).grid(row=0, column=i, padx=10, pady=2)

    def export_csv(self):
        if not self.results:
            messagebox.showwarning("Thông báo", "Chưa có kết quả để xuất! Hãy chạy mô phỏng trước.")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            initialfile="ket_qua_mo_phong.csv", 
            filetypes=[("CSV Files", "*.csv")],
            title="Lưu kết quả mô phỏng"
        )
        
        if path:
            try:
                with open(path, mode='w', newline='', encoding='utf-8-sig') as f:
                    w = csv.writer(f)
                    w.writerow(["Process", "Size (MB)", "Block", "Internal Fragmentation", "Status"])
                    w.writerows(self.results)
                messagebox.showinfo("Thành công", f"Đã lưu tại:\n{path}")
            except Exception as e: 
                messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")

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

if __name__ == "__main__":
    app = App()
    app.mainloop()
