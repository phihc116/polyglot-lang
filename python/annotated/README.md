# Hướng dẫn Python `Annotated`

Thư mục này chứa ví dụ về cách sử dụng `typing.Annotated` trong Python để thêm metadata vào type hint, tạo nền tảng cho việc validation dữ liệu (tương tự như cách thư viện **Pydantic** hoạt động).

## `typing.Annotated` là gì?

`Annotated` cho phép bạn gắn thêm thông tin bổ sung (metadata) vào một type mà không làm thay đổi bản chất của type đó.

Cú pháp: `Annotated[T, x]`
- `T`: Kiểu dữ liệu gốc (ví dụ: `int`, `str`).
- `x`: Metadata (có thể là bất cứ thứ gì: string, object, list...).

Ví dụ:
```python
age: Annotated[int, "Phải lớn hơn 0"]
```
Với Python, biến `age` vẫn là `int`. Python bỏ qua phần metadata ở runtime trừ khi bạn chủ động đọc nó.

## Cách hoạt động của Ví dụ (`main.py`)

Trong file `main.py`, chúng ta xây dựng một hệ thống validation mini:

1.  **`Field` Class**: Đây là class dùng để chứa luật validation (metadata).
    ```python
    class Field:
        def __init__(self, gt=None, lt=None): ...
    ```

2.  **`get_metadata` Function**: Sử dụng `typing.get_type_hints` với `include_extras=True` để lấy ra cả type lẫn metadata từ class.
    - `__origin__`: Lấy kiểu gốc (ví dụ `int`).
    - `__metadata__`: Lấy danh sách các object đi kèm trong `Annotated`.

3.  **`BaseModel` Class**:
    - Khi khởi tạo (`__init__`), nó tự động quét metadata của class con (`self.__class__`).
    - Kiểm tra giá trị đầu vào (`kwargs`) có thỏa mãn các điều kiện trong `Field` metadata không.
    - Nếu vi phạm (ví dụ `value <= gt`), ném lỗi `ValueError`.

## Minh họa

```python
class User(BaseModel):
    # age là int, NHƯNG đi kèm luật: phải > 0 và < 120
    age: Annotated[int, Field(gt=0, lt=120)]

# Hợp lệ
u = User(name="Tý", age=18)

# Lỗi ngay lập tức vì -5 không > 0
u = User(name="Tèo", age=-5) 
```

## Tại sao điều này hữu ích?

Cách tiếp cận này (Declarative Programming) giúp code:
- **Rõ ràng**: Luật validation nằm ngay cạnh khai báo biến.
- **Tái sử dụng**: Logic validation nằm trong `BaseModel`, không cần viết lại `if/else` trong mỗi hàm `__init__`.
- **Mạnh mẽ**: Đây là cơ sở của các framework hiện đại như FastAPI, Pydantic, SQLModel.
