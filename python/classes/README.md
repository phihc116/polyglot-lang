# Python Classes - Tài liệu Học tập Chi tiết

Tài liệu này tổng hợp các kiến thức cốt lõi về Object-Oriented Programming (OOP) trong Python. Khác với Java hay C++, Python xử lý Classes rất động (dynamic) và linh hoạt.

## Mục lục
1. [Giới thiệu về Class](#giới-thiệu-về-class)
2. [Class Object (Lớp đối tượng)](#class-object)
3. [Instance Object (Đối tượng thể hiện)](#instance-object)
4. [Attribute Lookup (Cơ chế tìm kiếm thuộc tính)](#attribute-lookup)
5. [Inheritance (Cơ chế kế thừa)](#inheritance-kế-thừa)
6. [Private Variables & Name Mangling](#private-variables--name-mangling)
7. [Các Lưu ý Khác (Random Remarks)](#random-remarks)

---

## 1. Giới thiệu về Class

Trong Python, **Class không chỉ là bản thiết kế (blueprint), nó còn là một object thực sự**.

- **Thời điểm khởi tạo**: Class được tạo ra khi trình thông dịch (interpreter) chạy qua dòng lệnh `class ...`.
- **Phạm vi (Scope)**: Class có thể được định nghĩa ở bất cứ đâu: top-level, trong một hàm, hoặc thậm chí trong một câu lệnh `if`.
- **Runtime**: Không giống C++/Java (class được define lúc compile), Python define class lúc **runtime** (khi chương trình đang chạy).

---

## 2. Class Object

### Cách Python "dựng" một Class

Khi bạn viết:
```python
class A:
    x = 1             # Class Attribute
    
    def greet(self):  # Method
        return "hello"
```

Python thực hiện một quy trình gồm 4 bước ngầm bên dưới:

1.  **Tạo Namespace**: Tạo một dictionary rỗng để chứa các biến/hàm của class.
2.  **Thực thi code**: Chạy toàn bộ code bên trong khối `class A`, và lưu kết quả vào dictionary trên.
    - `dict["x"] = 1`
    - `dict["greet"] = <function object greet>`
3.  **Tạo Class Object**: Gọi `type("A", bases, dict)` để tạo ra object đại diện cho class `A`.
4.  **Gán tên**: Gán object vừa tạo vào biến tên là `A` trong module hiện tại.

### Thao tác với Class Object
Vì `A` là một object, bạn có thể tương tác với nó ngay lập tức mà chưa cần tạo instance nào cả:
- `A.x` (Truy cập attribute) -> trả về `1`
- `A.x = 100` (Sửa attribute trực tiếp trên class) -> Tất cả instance sau này sẽ thấy giá trị mới này (nếu chưa bị override).

---

## 3. Instance Object

Instance là một "bản sao" cụ thể được tạo ra từ Class.

### Quá trình tạo Instance (`a = A()`)
1.  **Tạo vỏ rỗng**: Python tạo một object mới chưa có dữ liệu gì.
2.  **Khởi tạo (`__init__`)**: Nếu class có `__init__`, Python gọi nó và truyền instance mới vào tham số `self`.
    ```python
    A.__init__(new_instance, ...)
    ```
3.  **Trả về**: Trả về instance đã được setup.

### Instance Metadata (`__dict__`)
Mỗi instance `a` có một dictionary riêng tên là `__dict__` để lưu trữ dữ liệu của CÁ NHÂN nó.
- `a.__dict__` lưu các attributes như `name`, `age` mà bạn gán qua `self.name = ...`.
- **Quan trọng**: `a.__dict__` KHÔNG chứa các method (`greet`) hay class attribute (`x`). Chúng nằm ở `A.__dict__`.

### `self` là gì?
- `self` không phải từ khóa, chỉ là quy ước đặt tên (nhưng BẮT BUỘC phải tuân theo để code dễ đọc).
- Khi bạn gọi `a.greet()`, Python tự động chuyển thành: `A.greet(a)`.
- Tham số đầu tiên của method luôn nhận chính object đang gọi method đó.

---

## 4. Attribute Lookup

Điều gì xảy ra khi bạn gõ `a.x`? Python đi tìm `x` ở đâu?

Quy trình tìm kiếm (The Lookup Chain):
1.  **Instance**: Tìm trong `a.__dict__` trước. (Có `x` riêng của `a` không?)
2.  **Class**: Nếu không thấy, tìm trong `A.__dict__`. (Class `A` có biến `x` chung không?)
3.  **Base Class**: Nếu không thấy, tìm tiếp lên các class cha (theo thứ tự MRO).
4.  **Lỗi**: Nếu tìm hết không thấy -> `AttributeError`.

**Ví dụ minh họa sự khác biệt:**
```python
class DongVat:
    loai = "Thú"       # Class Attribute (Dùng chung)

meo = DongVat()
cho = DongVat()

# Read lookup
print(meo.loai)  # "Thú" (Tìm ở meo ko thấy -> tìm ở DongVat thấy)

# Write (Coi chừng nhầm lẫn!)
meo.loai = "Mèo" # TẠO attribute mới "loai" trong meo.__dict__
                 # KHÔNG sửa DongVat.loai

print(cho.loai)  # Vẫn là "Thú"
print(meo.loai)  # Là "Mèo"
```

---

## 5. Inheritance (Kế thừa)

Python hỗ trợ **Đa kế thừa (Multiple Inheritance)**.

### Hàm (Functions) hữu ích
- `isinstance(obj, Class)`: Kiểm tra `obj` có được sinh ra từ `Class` (hoặc con của nó) không.
- `issubclass(Sub, Parent)`: Kiểm tra quan hệ cha-con giữa 2 class.

### MRO (Method Resolution Order)
Khi một class kế thừa từ nhiều class cha, Python dùng thuật toán C3 Linearization để quyết định thứ tự tìm kiếm method. Bạn có thể xem thứ tự này bằng:
`print(ClassTen.__mro__)`

---

## 6. Private Variables & Name Mangling

Python **KHÔNG** có biến private thực sự (như `private` trong Java). Mọi thứ đều có thể truy cập nếu bạn cố tình.

### Quy ước (Convention)
- `_variable` (1 gạch dưới): "Làm ơn đừng đụng vào, đây là nội bộ". (Vẫn truy cập được bình thường).
- `__variable` (2 gạch dưới): Kích hoạt cơ chế **Name Mangling**.

### Name Mangling là gì?
Để tránh các class con vô tình đặt tên trùng làm hỏng biến của class cha, Python tự động đổi tên các biến bắt đầu bằng `__`.
- Bạn viết: `self.__bi_mat` bên trong class `A`.
- Python đổi thành: `_A__bi_mat`.

-> Giúp tránh xung đột tên (name clashes), nhưng không phải để bảo mật tuyệt đối.

---

## 7. Random Remarks (Ghi chú nhỏ)

1.  **Method vs Function**: 
    - Bên trong class, nó là `function`.
    - Khi truy cập qua instance (`a.f`), nó biến thành `method` (bound method) - tức là function đã được "gắn" sẵn `self` vào.

2.  **Thêm method từ bên ngoài**:
    Do class là object, bạn có thể gắn thêm hàm cho nó BẤT CỨ LÚC NÀO.
    ```python
    def bark(self):
        print("Gâu gâu")
    
    Dog.bark = bark  # Gắn hàm bark vào class Dog
    d = Dog()
    d.bark()         # Hoạt động bình thường!
    ```

3.  **Empty Class**:
    Đôi khi ta cần một class rỗng chỉ để chứa dữ liệu (giống Struct trong C).
    ```python
    class Data: pass
    d = Data()
    d.name = "John"
    d.salary = 1000
    ```

---
*Tài liệu này được biên soạn để giúp bạn nắm bắt cơ chế "dưới nắp capo" của Python OOP.*

--- 
