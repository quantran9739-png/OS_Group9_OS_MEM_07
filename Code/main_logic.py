# main_logic.py
# Module xử lý các thuật toán cấp phát bộ nhớ

def find_first_fit(blocks, process_size):
    """Tìm khối đầu tiên đủ lớn (First-Fit)"""
    for i, b in enumerate(blocks):
        if b['p'] is None and b['size'] >= process_size:
            return i
    return -1

def find_best_fit(blocks, process_size):
    """Tìm khối nhỏ nhất nhưng vẫn đủ chứa (Best-Fit)"""
    target_idx = -1
    min_d = float('inf')
    for i, b in enumerate(blocks):
        if b['p'] is None and b['size'] >= process_size:
            diff = b['size'] - process_size
            if diff < min_d:
                min_d = diff
                target_idx = i
    return target_idx

def find_worst_fit(blocks, process_size):
    """Tìm khối lớn nhất để cấp phát (Worst-Fit)"""
    target_idx = -1
    max_d = -1
    for i, b in enumerate(blocks):
        if b['p'] is None and b['size'] >= process_size:
            diff = b['size'] - process_size
            if diff > max_d:
                max_d = diff
                target_idx = i
    return target_idx
