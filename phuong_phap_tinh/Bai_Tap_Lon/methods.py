# methods.py
import numpy as np

# --- Phương trình Kepler & Đạo hàm ---
def kepler_func(E, e, M):
    return E - e * np.sin(E) - M

def kepler_func_prime(E, e):
    return 1.0 - e * np.cos(E)

# --- Các phương pháp tìm nghiệm xấp xỉ ---

def newton_method(e, M, E0, tol=1e-8, max_iter=100):
    """
    Phương pháp Newton:
    Công thức lặp: 
    - E_{n+1} = E_n - f(E_n) / f'(E_n)

    Return: (E_final, history, final_error, iterations) or (None, history, None, iterations)
    History format: list of [iteration, E_value, error_metric]
    """
    E = E0 # Khởi tạo E
    history = [] # Lưu trữ lịch sử lặp
    iterations = 0
    last_E = E # Lưu giá trị E trước đó để tính độ thay đổi

    for i in range(max_iter):
        iterations = i + 1
        f_E = kepler_func(E, e, M)
        f_prime_E = kepler_func_prime(E, e)

        # Sử dụng giá trị tuyệt đối của f(E) để kiểm tra hội tụ
        # Lưu ý: f(E) có thể âm hoặc dương, nên cần giá trị tuyệt đối
        error_f_E = abs(f_E)
        delta_step = abs(E - last_E) # Tính độ thay đổi giữa các lần lặp

        history.append([iterations, E, error_f_E])

        if abs(f_prime_E) < 1e-14:
            print("Warning (Newton): Derivative close to zero.")
            # Trả về E nếu f(E) đã hội tụ
            if error_f_E < tol:
                 return E, history, error_f_E, iterations
            # Nếu không hội tụ, trả về None
            return None, history, None, iterations

        delta_E = f_E / f_prime_E
        E_new = E - delta_E
        last_E = E # Lưu giá trị E trước đó để tính độ thay đổi
        E = E_new

        # Kiểm tra hội tụ dựa trên độ thay đổi giữa các lần lặp
        if delta_step < tol and i > 0 : # Kiểm tra delta_step và i > 0 để tránh trường hợp đầu tiên
             history.append([iterations + 1, E, abs(kepler_func(E, e, M))]) # Lưu giá trị cuối cùng
             return E, history, abs(kepler_func(E, e, M)), iterations

    print(f"Warning (Newton): Failed to converge within {max_iter} iterations.")
    return None, history, None, iterations # Trả về None nếu không hội tụ


def secant_method(e, M, E0, E1, tol=1e-8, max_iter=100):
    """
    Phương pháp dây cung.
    Yêu cầu hai giá trị khởi tạo E0, E1.
    Trả về: (E_final, history, final_error, iterations) hoặc (None, history, None, iterations)
    Định dạng lịch sử: danh sách các [iteration, E_value, error_metric]
    """
    En_minus_1 = E0
    En = E1
    f_En_minus_1 = kepler_func(En_minus_1, e, M)
    history = [[0, E0, abs(f_En_minus_1)], [1, E1, abs(kepler_func(En, e, M))]] # Bắt đầu lưu lịch sử
    iterations = 0

    for i in range(max_iter):
        iterations = i + 1 # Tương ứng với việc tính toán E_next
        f_En = kepler_func(En, e, M)

        denominator = f_En - f_En_minus_1
        if abs(denominator) < 1e-14:
            print("Cảnh báo (Secant): Mẫu số gần bằng 0.")
            if abs(f_En) < tol: # Kiểm tra nếu En hiện tại đủ tốt
                return En, history, abs(f_En), iterations
            return None, history, None, iterations

        # Tính giá trị ước lượng tiếp theo
        E_next = En - f_En * (En - En_minus_1) / denominator

        # Tính các chỉ số lỗi
        error_f_E = abs(kepler_func(E_next, e, M))
        delta_step = abs(E_next - En)

        # Lưu lịch sử (số lần lặp là i+2 vì bắt đầu từ 0 và 1)
        history.append([i + 2, E_next, error_f_E])

        # Kiểm tra hội tụ dựa trên sự thay đổi của E
        if delta_step < tol:
            return E_next, history, error_f_E, iterations + 1 # +1 vì số lần lặp là cho bước tính toán

        # Cập nhật cho lần lặp tiếp theo
        En_minus_1 = En
        f_En_minus_1 = f_En
        En = E_next


    print(f"Cảnh báo (Secant): Không hội tụ trong {max_iter} lần lặp.")
    return None, history, None, iterations + 1


def bisection_method(e, M, a, b, tol=1e-8, max_iter=100):
    """
    Phương pháp Chia đổi
    Yêu cầu khoảng [a, b] sao cho f(a) và f(b) có dấu trái ngược.
    Return: (E_final, history, final_error, iterations) hoặc (None, history, None, iterations)
    History[]: danh sách các [iteration, E_value (midpoint), error_metric (độ rộng khoảng)]
    """
    f_a = kepler_func(a, e, M)
    f_b = kepler_func(b, e, M)
    history = []
    iterations = 0

    # Exception: Kiểm tra dấu của f(a) và f(b)
    # Nếu không có dấu trái ngược, không thể áp dụng phương pháp chia đổi
    if np.sign(f_a) == np.sign(f_b):
        print(f"Lỗi (Bisection): f(a) và f(b) phải có dấu trái ngược.")
        print(f"  f({a:.4f}) = {f_a:.4e}, f({b:.4f}) = {f_b:.4e}")
        return None, history, None, iterations

    for i in range(max_iter):
        iterations = i + 1
        interval_width = abs(b - a)
        c = a + interval_width / 2.0 # Tính trung điểm an toàn hơn
        f_c = kepler_func(c, e, M)

        # Sử dụng độ rộng khoảng làm chỉ số lỗi
        history.append([iterations, c, interval_width])

        # Kiểm tra hội tụ dựa trên độ rộng khoảng HOẶC f(c) gần bằng 0
        if interval_width < tol or abs(f_c) < tol :
            final_error = abs(f_c) # Chỉ số lỗi trực tiếp hơn
            return c, history, final_error, iterations

        if np.sign(f_c) == 0: # Tìm thấy nghiệm chính xác (hiếm khi xảy ra với số thực)
             return c, history, 0.0, iterations

        # Cập nhật khoảng [a, b] dựa trên dấu của f(c)
        if np.sign(f_c) == np.sign(f_a): # f(c) và f(a) cùng dấu
            a = c
            f_a = f_c 
        else: # f(c) và f(b) cùng dấu
            b = c
            f_b = f_c

    print(f"Cảnh báo (Bisection): Không hội tụ trong {max_iter} lần lặp.")
    final_error = abs(kepler_func(c, e, M))
    return c, history, final_error, iterations # Trả về ước lượng tốt nhất ngay cả khi không hội tụ