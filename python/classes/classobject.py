# Khi Python chạy đến dòng class MyClass:
# 1. Python tạo một namespace tạm (giống dict rỗng)
# 2. Chạy toàn bộ code trong class body vào namespace này
# 3. Tạo class object từ namespace đó
# 4. Gán class object vào module namespace dưới tên MyClass

class MyClass:
    """A simple example class"""

    # Đây là class attribute (thuộc tính của class object)
    i = 12345

    # Hàm được định nghĩa trong class, đi vào class namespace như một function object
    def __init__(self, value):
        # Đây là instance attribute (được gán vào instance.__dict__)
        self.data = value

    def f(self):
        # Method luôn nhận self (instance) trước
        return f"hello, my data = {self.data}"

    # Code trong class body chạy ngay thời điểm định nghĩa class
    print("Class body is executing: namespace of class is being populated")

# =============================
# Sau khi kết thúc class body:
# - MyClass đã trở thành một CLASS OBJECT thật sự
# - Ta kiểm tra:
# =============================

print("\n--- Class Object Info ---")
print(MyClass)                # class object
print(type(MyClass))          # <class 'type'> → class object được tạo bằng metaclass 'type'
print(MyClass.__doc__)        # docstring của class

# __dict__ chứa toàn bộ namespace của class
print("\nClass namespace:", MyClass.__dict__)

# =============================
# Khởi tạo instance (instantiation)
# Gọi MyClass(...) giống như gọi một function → trả về một instance object
# =============================

obj = MyClass(99)

print("\n--- Instance Info ---")
print(obj)                    # instance object
print(obj.__dict__)           # namespace riêng của instance
print("obj.data =", obj.data) # instance attribute
print("obj.i =", obj.i)       # truy cập class attribute (fallback từ class)

# =============================
# Method binding: obj.f -> bound method
# Python tự truyền self = obj khi gọi
# =============================

print("\n--- Method Binding ---")
print(obj.f())                # tương đương MyClass.f(obj)
print(MyClass.f(obj))         # gọi thủ công để xem rõ self

# =============================
# Sửa class attribute → mọi instance nhìn thấy thay đổi
# =============================

print("\n--- Class attribute mutation ---")
MyClass.i = 777
print("MyClass.i =", MyClass.i)
print("obj.i =", obj.i)       # instance không có attr i nên lấy từ class

# =============================
# Gán thêm attribute cho instance → không ảnh hưởng instance khác
# =============================

obj.new_attr = "I belong only to this object"
print("\nobj.new_attr =", obj.new_attr)

# Tạo instance mới để chứng minh new_attr không dùng chung
obj2 = MyClass(50)
print("Does obj2 have new_attr?", hasattr(obj2, "new_attr"))