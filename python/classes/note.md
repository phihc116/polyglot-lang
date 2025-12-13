# Python Classes - Tài liệu Học tập

## Mục lục
1. [Giới thiệu về Class](#giới-thiệu-về-class)
2. [Class Object](#class-object)
3. [Instance Object](#instance-object)
4. [Attribute Lookup](#attribute-lookup)
5. [Inheritance (Kế thừa)](#inheritance-kế-thừa)
6. [Private Variables](#private-variables)
7. [Random Remarks](#random-remarks)

---

## Giới thiệu về Class

**Điểm quan trọng:** Lớp trong Python chỉ được tạo ra khi dòng `class ...` được thực thi. 

- Class có thể đặt ở bất kỳ đâu: trong hàm, trong `if`, hoặc bất kỳ nơi nào
- Class chỉ tồn tại khi chương trình chạy đến dòng định nghĩa đó
- **Class chạy lúc runtime, không phải compile time**

---

## Class Object

### Cách Python tạo Class

Khi viết code:

```python
class A:
    x = 1
    
    def f(self):
        return self
    
    def greet(self):
        return "hello"
```

Python thực hiện **4 bước**:

1. **Tạo namespace tạm** cho class (giống dictionary)
2. **Chạy tất cả code** trong class A và điền vào namespace:
   ```python
   dict["x"] = 1
   dict["f"] = <function f>
   dict["greet"] = <function greet>
   ```
3. **Tạo class object** bằng `type("A", bases, namespace)`
4. **Gán class object** vào namespace của module với tên `A`

### Class Namespace

Class namespace là **độc lập** và giữ các thành phần:

- Class attributes
- Method functions
- Docstrings
- Special methods (`__init__`, `__str__`, v.v.)
- Static methods, class methods

### Thao tác với Class Object

Class object có thể:

- ✅ Truy cập thuộc tính: `A.x`, `A.f`
- ✅ Thay đổi thuộc tính: `A.x = 100`
- ✅ Tạo instance: `a = A()`

---

## Instance Object

### Khái niệm

Instance là một **đối tượng mới, riêng biệt** được tạo từ class.

### Quá trình tạo Instance

Khi gọi:

```python
a = A()
```

Python thực hiện:

1. **Tạo instance trống**
2. **Gọi `__init__`** nếu có: `A.__init__(a, ...)`
3. **Trả về instance**

### Instance Namespace

- Instance có **namespace riêng** lưu các attribute riêng của nó
- Kiểm tra: `a.__dict__` (khác với `A.__dict__`)

### Instance Attributes

**Đặc điểm quan trọng:** Instance attributes tự sinh khi gán, không cần khai báo trước!

```python
a.counter = 10  # Tự động tạo attribute
```

Python thực tế làm:

```python
a.__dict__["counter"] = 10
```

> ⚠️ **Khác với Java, C#, C++:** Không cần định nghĩa trước

### Hai loại Instance Attributes

1. **Data attributes** - Dữ liệu thuộc instance
2. **Method attributes** - Hàm gắn với instance

### Method vs Function

- **Method** = function thuộc về instance, được Python **"bind"** thêm `self`
- `MyClass.f` → function object
- `x.f` → method object (đã bind với x)

---

## Attribute Lookup

### Trình tự tìm kiếm Attribute

Khi gọi `a.something`, Python tìm theo thứ tự:

```
1. a.__dict__           → instance attributes
2. A.__dict__           → class attributes  
3. Base classes         → các lớp cha
4. Built-in fallback    → hành vi mặc định
```

> 💡 **Lưu ý:** Instance attributes được ưu tiên trước class attributes!

---

## Inheritance (Kế thừa)

### Các khái niệm chính

- **Đa kế thừa** (Multiple Inheritance)
- **MRO** (Method Resolution Order)
- **Super** - Truy cập phương thức của lớp cha

### Hàm kiểm tra

| Hàm                      | Dùng cho   | Câu hỏi nó trả lời                                  |
| ------------------------ | ---------- | --------------------------------------------------- |
| `isinstance(obj, Class)` | **object** | *Object này có thuộc Class (hoặc class con) không?* |
| `issubclass(Sub, Base)`  | **class**  | *Class Sub có kế thừa từ Base không?*               |

**Ví dụ:**

```python
class Animal:
    pass

class Dog(Animal):
    pass

d = Dog()
isinstance(d, Dog)      # True
isinstance(d, Animal)   # True
issubclass(Dog, Animal) # True
```

---

## Private Variables

### Quy ước đặt tên

- **Single underscore** `_variable`: Private theo quy ước (không ép buộc)
- **Double underscore** `__variable`: Name mangling (Python tự động đổi tên)

### Name Mangling

```python
class MyClass:
    def __init__(self):
        self.__private = 42  # Trở thành _MyClass__private
```

Python tự động đổi tên `__private` thành `_MyClass__private` để tránh xung đột với các lớp con.

> ⚠️ **Chú ý:** Vẫn có thể truy cập qua `obj._MyClass__private`, nhưng không nên!

### Best Practices

- Dùng single underscore `_var` cho private attributes
- Tránh dùng double underscore trừ khi thực sự cần name mangling
- Tôn trọng quy ước: "We are all consenting adults here"

---

## Random Remarks

### Các ghi chú quan trọng

- 🔹 Bất kỳ **function object** nào nằm trong namespace của class sẽ trở thành **method** khi được truy cập qua instance

- 🔹 Function **không cần** được định nghĩa bên trong class; chỉ cần gán vào class là thành method:
  ```python
  def external_func(self):
      return "I'm external!"
  
  MyClass.new_method = external_func  # Gán từ bên ngoài
  ```

- 🔹 **Global scope** của method chính là module nơi function được định nghĩa

- 🔹 Mọi object đều có thuộc tính `obj.__class__`, cho biết class (type) của object

---

## Tài liệu tham khảo

- [Python Official Documentation - Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)

---

*Cập nhật lần cuối: 2025-12-13*
