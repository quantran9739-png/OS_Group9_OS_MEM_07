import time
import random
import csv

# --- 1. LÕI THUẬT TOÁN ---
def first_fit(blocks, process_size):
    for i, b in enumerate(blocks):
        if b['p'] is None and b['size'] >= process_size: return i
    return -1

# --- 2. HÀM CHẠY STRESS TEST ---
def run_stress_test():
    print("🚀 BẮT ĐẦU STRESS TEST VÀ PERFORMANCE TEST...")
    print("-" * 50)

    # Tự động đẻ ra 10.000 Block bộ nhớ và 5.000 Tiến trình
    blocks = [{'id': f'B{i}', 'size': random.randint(50, 500), 'p': None} for i in range(10000)]
    processes = [{'id': f'P{i}', 'size': random.randint(10, 400)} for i in range(5000)]
    print(f"📦 Đã khởi tạo {len(blocks)} Memory Blocks và {len(processes)} Processes.")

    print("⏳ Đang chạy mô phỏng thuật toán First-Fit siêu tốc...")
    
    # Bắt đầu bấm giờ
    start_time = time.time()
    success, fail = 0, 0
    results = []

    # Chạy cấp phát cho 5.000 tiến trình
    for p in processes:
        idx = first_fit(blocks, p['size'])
        if idx != -1:
            b = blocks[idx]
            b['p'] = p['id']
            rem = b['size'] - p['size']
            b['size'] = rem # Cập nhật dung lượng còn lại
            success += 1
            results.append([p['id'], p['size'], b['id'], rem, "Allocated"])
        else:
            fail += 1
            results.append([p['id'], p['size'], "N/A", 0, "Fail"])

    # Kết thúc bấm giờ
    end_time = time.time()
    execution_time = end_time - start_time

    # --- 3. IN KẾT QUẢ VÀ XUẤT CSV ---
    print("\n📊 KẾT QUẢ PERFORMANCE TEST:")
    print(f"✅ Cấp phát thành công: {success}")
    print(f"❌ Cấp phát thất bại: {fail}")
    print(f"⏱️ THỜI GIAN CHẠY (Execution Time): {execution_time:.5f} giây")

    # Tự động xuất file CSV
    filename = "result_stress_test.csv"
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["Process", "Size", "Block", "Remaining", "Status"])
        writer.writerows(results)
    
    print("-" * 50)
    print(f"💾 Đã lưu chi tiết 5000 dòng kết quả vào file: {filename}")

if __name__ == "__main__":
    run_stress_test()