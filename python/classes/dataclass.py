from dataclasses import dataclass

# Đôi khi rất hữu ích khi có một kiểu dữ liệu giống như struct, 
# dùng để gom một vài dữ liệu có tên lại với nhau. 
# Cách làm theo chuẩn Python (idiomatic) cho mục đích này là dùng dataclasses.
@dataclass
class User:
    age: int
    name: str
    
user = User(18, "Hello")
print(user.age)