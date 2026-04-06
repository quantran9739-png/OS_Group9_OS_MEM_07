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
        self.allocated_block = "None"

# --- 2. CÁC THUẬT TOÁN ---
def first_fit(blocks, p):
    for i, b in enumerate(blocks):
        if b.proc == "None" and b.size >= p.size:
            # Tách phần bộ nhớ dư ra thành một block mới
            if b.size > p.size:
                leftover_size = b.size - p.size
                new_block = Block(f"{b.id}_new", leftover_size)
                blocks.insert(i + 1, new_block)
            
            # Gắn tiến trình vào block hiện tại
            b.size = p.size
            b.proc = p.id
            p.allocated = True
            p.allocated_block = b.id
            return True
    return False

def best_fit(blocks, p):
    best_idx = -1
    # Tìm ô nhớ trống NHỎ NHẤT nhưng vẫn ĐỦ LỚN để chứa tiến trình
    for i, b in enumerate(blocks):
        if b.proc == "None" and b.size >= p.size:
            if best_idx == -1 or b.size < blocks[best_idx].size:
                best_idx = i
                
    if best_idx != -1:
        b = blocks[best_idx]
        # Tách phần bộ nhớ dư ra thành một block mới
        if b.size > p.size:
            leftover_size = b.size - p.size
            new_block = Block(f"{b.id}_new", leftover_size)
            blocks.insert(best_idx + 1, new_block)
            
        # Cập nhật block hiện tại cho tiến trình
        b.size = p.size
        b.proc = p.id
        p.allocated = True
        p.allocated_block = b.id
        return True
        
    return False

def worst_fit(blocks, p):
    worst_idx = -1
    # Tìm ô nhớ trống LỚN NHẤT để chứa tiến trình
    for i, b in enumerate(blocks):
        if b.proc == "None" and b.size >= p.size:
            if worst_idx == -1 or b.size > blocks[worst_idx].size:
                worst_idx = i
                
    if worst_idx != -1:
        b = blocks[worst_idx]
        # Tách phần bộ nhớ dư ra thành một block mới
        if b.size > p.size:
            leftover_size = b.size - p.size
            new_block = Block(f"{b.id}_new", leftover_size)
            blocks.insert(worst_idx + 1, new_block)
            
        # Cập nhật block hiện tại cho tiến trình
        b.size = p.size
        b.proc = p.id
        p.allocated = True
        p.allocated_block = b.id
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
        # Thêm cột Block_ID vào tiêu đề
        writer.writerow(['ProcessID', 'Size', 'Status', 'Block_ID']) 
        for p in processes:
            status = "Allocated" if p.allocated else "Failed"
            # Xuất thêm thông tin block
            writer.writerow([p.id, p.size, status, p.allocated_block]) 
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
    print("\n[HOÀN TẤT BƯỚC 1] - Đã có dữ liệu so sánh 3 thuật toán


