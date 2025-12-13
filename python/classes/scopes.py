module_counter = 0

def outer():
    enclosed = 0
    
    def inner_local():
        local_var = "I am local"
        print("[inner_local] local_var =", local_var)

        # tạo biến cục bộ 'enclosed' trong inner_local, không trỏ tới outer().enclosed        
        enclosed = "shadowed"  
        print("[inner_local] shadowed enclosed =", enclosed)
        
        module_counter = "counter"
        print("[inner_local] module_counter counter =", module_counter)
        
    def inner_nonlocal():
        # nonlocal: sửa biến "enclosed" của outer()
        nonlocal enclosed
        enclosed += 1         
        print("[inner_nonlocal] incremented enclosed to", enclosed)
        
    def inner_global():
        # global: sửa biến module_counter ở cấp module
        global module_counter 
        module_counter += 1
        print("[inner_global] incremented module_counter to", module_counter)        
        
    print(">> Before inner_local, enclosed =", enclosed)
    inner_local()
    print(">> After inner_local, enclosed =", enclosed)
    
    print(">> Before inner_nonlocal, enclosed =", enclosed)
    inner_nonlocal()
    print(">> After inner_nonlocal, enclosed =", enclosed)
    
    print(">> Before inner_global, module_counter =", module_counter)
    inner_global()
    print(">> After inner_global, module_counter =", module_counter)        
    
if __name__ == "__main__":
    print("=== Running scopes_demo.py ===")
    print("Initial module_counter =", module_counter)
    outer()
    print("Final module_counter =", module_counter)                
