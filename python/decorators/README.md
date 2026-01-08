# Hướng dẫn Python `Decorators`

Thư mục này minh họa cách sử dụng Decorators trong Python để xây dựng một mini-framework (giống như Flask hoặc FastAPI).

## Khái niệm Decorator

Decorator là một pattern cho phép bạn thay đổi hoặc mở rộng hành vi của một hàm hoặc method mà không cần sửa đổi trực tiếp code bên trong hàm đó. Trong Python, nó thường là một hàm nhận vào một hàm khác và trả về một hàm mới.

## Các loại Decorator trong ví dụ (`main.py`)

Ví dụ này sử dụng 2 loại decorator phổ biến:

### 1. Decorator Đăng ký (Registration Decorator)

Dùng để "đánh dấu" hoặc lưu trữ hàm vào một nơi nào đó (ví dụ: router).

```python
@app.get("/items")
def read_items(): ...
```

- **Cách hoạt động**: 
    - Hàm `app.get("/items")` chạy và trả về decorator `handler`.
    - `handler` nhận hàm `read_items` và lưu nó vào dictionary `self.routes`.
    - Nó trả về `func` nguyên vẹn (hoặc đã wrap) để chương trình tiếp tục.
- **Mục đích**: Xây dựng hệ thống routing mà không cần gọi `app.add_route("/items", read_items)` thủ công.

### 2. Decorator Hành vi (Behavior Decorator)

Dùng để chèn logic trước hoặc sau khi hàm chạy (Middleware/Interceptors).

```python
@require_role("admin")
def read_admin(): ...
```

- **Cách hoạt động**:
    - `require_role("admin")` trả về hàm `decorator`.
    - `decorator` thay thế `read_admin` bằng hàm `wrapper`.
    - Khi gọi `read_admin()`, thực chất là gọi `wrapper()`.
    - `wrapper` kiểm tra logic (role có đúng không?) RỒI mới gọi hàm gốc hoặc ném lỗi.
- **Mục đích**: Tách biệt logic kiểm tra quyền (Authentication/Authorization) khỏi logic nghiệp vụ (Business Logic).

## Lưu ý quan trọng: `functools.wraps`

Khi viết decorator, luôn nhớ dùng `@wraps(func)`:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # <--- Quan trọng
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

Nếu không có `@wraps`, hàm được trang trí sẽ bị mất tên (`__name__`) và docstring (`__doc__`), biến thành tên của hàm `wrapper`, gây khó khăn khi debug.
