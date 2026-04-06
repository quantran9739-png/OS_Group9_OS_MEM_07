import csv
import os

# --- 1. CẤU TRÚC DỮ LIỆU ---
class Block:
    def __init__(self, id, size):
        self.id = id
        self.size = size             # Kích thước trống hiện tại
        self.original_size = size    # Kích thước ban đầu
        self.proc = "None"           # Tên tiến trình đang chiếm (nếu có)

class Process:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.allocated = False

# --- 2. CÁC THUẬT TOÁN ---
def first_fit(blocks, p):
    for b in blocks:
        if b.proc == "None" and b.size >= p.size:
            b.proc, b.size, p.allocated = p.id, b.size - p.size, True
            return True
    return False

def best_fit(blocks, p):
    best_idx = -1
    for i, b in enumerate(blocks):
        if b.proc == "None" and b.size >= p.size:
            if best_idx == -1 or b.size < blocks[best_idx].size:
                best_idx = i
    if best_idx != -1:
        blocks[best_idx].proc, blocks[best_idx].size = p.id, blocks[best_idx].size - p.size
        p.allocated = True
        return True
    return False

def worst_fit(blocks, p):
    worst_idx = -1
    for i, b in enumerate(blocks):
        if b.proc == "None" and b.size >= p.size:
            if worst_idx == -1 or b.size > blocks[worst_idx].size:
                worst_idx = i
    if worst_idx != -1:
        blocks[worst_idx].proc, blocks[worst_idx].size = p.id, blocks[worst_idx].size - p.size
        p.allocated = True
        return True
    return False

# --- 3. XỬ LÝ CSV ---
def load_data(file_path):
    blocks, processes = [], []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t, i, s = row['Type'].strip(), row['ID'].strip(), int(row['Size'])
                if t == 'Block': blocks.append(Block(i, s))
                else: processes.append(Process(i, s))
        return blocks, processes
    except Exception as e:
        print(f"Lỗi đọc file CSV: {e}")
        return [], []

def export_result(algo_name, processes):
    if not os.path.exists('output'): os.makedirs('output')
    path = f'output/result_{algo_name.lower()}.csv'
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ProcessID', 'Size', 'Status'])
        for p in processes:
            writer.writerow([p.id, p.size, "Allocated" if p.allocated else "Failed"])
    return path

# --- 4. HÀM CHẠY CHÍNH ---
def run_all():
    algorithms = ["First-Fit", "Best-Fit", "Worst-Fit"]
    
    for algo in algorithms:
        # Load lại dữ liệu sạch cho mỗi thuật toán
        blocks, processes = load_data('input.csv')
        if not blocks: break
        
        print(f"\n" + "="*30)
        print(f" CHẠY MÔ PHỎNG: {algo.upper()} ")
        print("="*30)
        
        for p in processes:
            if algo == "First-Fit": first_fit(blocks, p)
            elif algo == "Best-Fit": best_fit(blocks, p)
            else: worst_fit(blocks, p)
            
            res = "✅ OK" if p.allocated else "❌ FAIL"
            print(f"Tiến trình {p.id:4} ({p.size:4}KB) -> {res}")
        
        path = export_result(algo, processes)
        print(f"--> Kết quả lưu tại: {path}")

if __name__ == "__main__":
    run_all()
    print("\n[HOÀN TẤT BƯỚC 1] - Đã có dữ liệu so sánh 3 thuật toán.")
