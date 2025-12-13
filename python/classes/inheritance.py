class A:
    def process(self):
        print("A")
    
class B(A):
    def process(self):
        print("B")
        
class C(A):
    def process(self):
        print("C")
        
class D(C, B):
    def process(self):
        super().process()
        print("D")
     
d = D()        
print(D.__mro__)
print(d.process())

# Output này vì super nó chỉ in lớp gần kề theo MRO
# (<class '__main__.D'>, <class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
# C
# D
# None