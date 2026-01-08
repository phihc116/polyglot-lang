
import types

print("=== 1. CLASS LÀ OBJECT TRONG PYTHON ===")
class Robot:
    """Class Robot cơ bản"""
    population = 0  # Class attribute

    def __init__(self, name):
        self.name = name                 # Instance attribute
        Robot.population += 1
        print(f"Khởi tạo Robot: {self.name}")

    def say_hi(self):
        print(f"Xin chào, tôi là {self.name}")

# In ra 'từ điển' (namespace) của Class
print("\nNamespace của Class Robot (Robot.__dict__):")
# Chỉ in các key chính để dễ nhìn
keys = [k for k in Robot.__dict__.keys() if not k.startswith("__")]
print(keys)
# Output sẽ có: ['population', 'say_hi', ...] -> Chứng tỏ hàm và biến được lưu trong dict này.

# Tạo instance
r1 = Robot("R2D2")

print("\n=== 2. THÊM METHOD VÀO CLASS TẠI RUNTIME (MONKEY PATCHING) ===")
# Giả sử ta muốn Robot có thêm chức năng 'dance' mà không sửa code class gốc.

def dance_func(self):
    print(f"{self.name} đang nhảy múa... 💃")

# Gán function này vào Class Robot
# Python cho phép làm điều này vì Robot chỉ là một object!
Robot.dance = dance_func

print("Đã thêm method 'dance' vào Robot.")
# Gọi thử trên object r1 (được tạo TRƯỚC khi thêm hàm dance)
# Vẫn hoạt động! Vì r1 tìm 'dance' trong Robot.__dict__ tại thời điểm gọi.
r1.dance()

print("\n=== 3. THÊM METHOD VÀO MỘT INSTANCE DUY NHẤT ===")
# Đôi khi ta chỉ muốn 1 con robot cụ thể biết bay, các con khác thì không.

def fly_func(self):
    print(f"{self.name} đang bay lên trời! 🚀")

r2 = Robot("C-3PO")

# Cách SAI: r2.fly = fly_func
# Nếu làm thế này, r2.fly chỉ là function bình thường, tham số 'self' sẽ không được tự động truyền.

# Cách ĐÚNG: Dùng types.MethodType để 'bind' function vào instance
r2.fly = types.MethodType(fly_func, r2)

print(f"r2 ({r2.name}) biết bay:")
r2.fly()

print(f"Kiểm tra r1 ({r1.name}) có biết bay không?")
if hasattr(r1, 'fly'):
    r1.fly()
else:
    print("-> r1 KHÔNG biết bay (AttributeError nếu gọi).")

print("\n=== 4. THAY ĐỔI CLASS ATTRIBUTE VS INSTANCE ATTRIBUTE ===")
print(f"Class Population ban đầu: {Robot.population}")

# Thay đổi trên instance
r1.population = 999 
# Hành động này KHÔNG đổi class attribute, mà TẠO attribute mới trong r1.__dict__
print(f"r1.population: {r1.population} (Lấy từ r1.__dict__)")
print(f"Robot.population: {Robot.population} (Vẫn giữ nguyên)")

# Kiểm tra namespace để chứng minh
print(f"\nr1 namespace: {r1.__dict__}")
# Output: {'name': 'R2D2', 'population': 999}
