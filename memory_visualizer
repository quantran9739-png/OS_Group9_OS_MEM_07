import tkinter as tk
from tkinter import ttk, messagebox
import main_logic  # Import file thuật toán của nhóm

class MemoryVisualizer:
    def __init__(self, parent_frame):
        self.canvas = tk.Canvas(parent_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.max_height = 250
        self.box_width = 80
        self.spacing = 50

    def draw(self, initial_blocks, process_allocations):
        self.canvas.delete("all")
        if not initial_blocks: return

        block_sizes = [b.size for b in initial_blocks]
        max_block = max(block_sizes)
        scale = self.max_height / max_block if max_block > 0 else 1
        start_x, start_y = 50, 40

        for i, b_size in enumerate(block_sizes):
            b_id = initial_blocks[i].id
            x0 = start_x + i * (self.box_width + self.spacing)
            y0 = start_y
            x1 = x0 + self.box_width
            y1 = y0 + (b_size * scale)

            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#E0E0E0", outline="#333", width=2)
            self.canvas.create_text(x0 + self.box_width/2, y0 - 15, text=f"Block {b_id}\n({b_size}KB)", font=("Arial", 10, "bold"))

            current_y_bottom = y1
            allocated_size = 0

            for p in process_allocations[i]:
                p_size = p["size"]
                p_id = p["id"]
                allocated_size += p_size
                p_height = p_size * scale
                y0_process = current_y_bottom - p_height

                self.canvas.create_rectangle(x0, y0_process, x1, current_y_bottom, fill="#4CAF50", outline="black")
                self.canvas.create_text(x0 + self.box_width/2, current_y_bottom - p_height/2, 
                                        text=f"{p_id}\n({p_size}KB)", fill="white", font=("Arial", 9, "bold"))
                current_y_bottom = y0_process

            free_space = b_size - allocated_size
            if free_space > 0 and allocated_size > 0:
                self.canvas.create_text(x0 + self.box_width/2, y0 + (current_y_bottom - y0)/2, 
                                        text=f"Dư\n{free_space}KB", fill="#D32F2F", font=("Arial", 9, "bold"))
            elif allocated_size == 0:
                self.canvas.create_text(x0 + self.box_width/2, y0 + (y1 - y0)/2, 
                                        text="Trống", fill="#757575", font=("Arial", 10, "italic"))

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô Phỏng Cấp Phát Bộ Nhớ (OS_MEM_07)")
        self.root.geometry("900x700")

        input_frame = tk.Frame(root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Dữ liệu tự động nạp từ file: input.csv", fg="green", font=("Arial", 10, "italic")).grid(row=0, column=0, sticky="w", pady=5)
        
        tk.Label(input_frame, text="Thuật toán:").grid(row=1, column=0, sticky="w")
        self.algo_var = tk.StringVar(value="First-Fit")
        ttk.Combobox(input_frame, textvariable=self.algo_var, values=["First-Fit", "Best-Fit", "Worst-Fit"], state="readonly", width=15).grid(row=1, column=1, sticky="w", padx=10)

        tk.Button(input_frame, text="▶ CHẠY MÔ PHỎNG", command=self.run_simulation, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, rowspan=2, padx=40, ipadx=10, ipady=10)

        vis_frame = tk.Frame(root, bd=2, relief="groove")
        vis_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.visualizer = MemoryVisualizer(vis_frame)

        table_frame = tk.Frame(root, padx=10, pady=5)
        table_frame.pack(fill=tk.X)
        
        columns = ("Process", "Size", "Status", "Allocated Block")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill=tk.X)

    def run_simulation(self):
        # Nạp dữ liệu qua hàm của nhóm
        blocks, processes = main_logic.load_data('input.csv')
        initial_blocks, _ = main_logic.load_data('input.csv') # Lưu mảng gốc để vẽ
        
        if not blocks:
            messagebox.showerror("Lỗi", "Không tìm thấy file input.csv hoặc file bị lỗi!")
            return

        # Chạy thuật toán
        algo = self.algo_var.get()
        for p in processes:
            if algo == "First-Fit": main_logic.first_fit(blocks, p)
            elif algo == "Best-Fit": main_logic.best_fit(blocks, p)
            elif algo == "Worst-Fit": main_logic.worst_fit(blocks, p)

        # Trích xuất dữ liệu để vẽ lên Canvas
        allocations = [[] for _ in range(len(initial_blocks))]
        for p in processes:
            if p.allocated:
                base_id = p.allocated_block.split('_')[0] # Lấy tên block gốc (vd: B1)
                try:
                    idx = next(i for i, b in enumerate(initial_blocks) if b.id == base_id)
                    allocations[idx].append({"id": p.id, "size": p.size})
                except StopIteration:
                    pass
        
        self.visualizer.draw(initial_blocks, allocations)

        # Cập nhật bảng Treeview
        self.tree.delete(*self.tree.get_children())
        for p in processes:
            status = "✅ Thành công" if p.allocated else "❌ Chờ / Lỗi"
            b_id = p.allocated_block if p.allocated else "N/A"
            self.tree.insert("", "end", values=(p.id, f"{p.size} KB", status, b_id))
            
        # Xuất file result_...csv vào thư mục output giống code gốc
        export_path = main_logic.export_result(algo, processes)
        print(f"Đã xuất kết quả ra file: {export_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
