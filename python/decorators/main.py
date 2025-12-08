from typing import Callable
from functools import wraps

class MiniRouter:
    def __init__(self):
        self.routes: dict[str, Callable] = {}
        
    def get(self, path: str):
        def handler(func: Callable):
            print(f"Registering path '{path}' for handler: {func.__name__}") 
            self.routes[path] = func
            return func
        return handler
    
    def run(self, path: str, current_role: str = "guest"): 
        print(f"\nRequest: {path} | Role: {current_role}")
        
        if path in self.routes:
            handler_function = self.routes[path]
            try:
                result = handler_function(current_role=current_role)
                print(f"200 OK: {result}")
            except PermissionError as e:
                print(f"403 Forbidden: {e}")
        else:
            print("404 Not Found")    

def require_role(role: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current = kwargs.get("current_role", "guest")
            
            if current != role:
                raise PermissionError(f"You need '{role}' to access!")
            
            if "current_role" in kwargs:
                del kwargs["current_role"]
            return func(*args, **kwargs)
        return wrapper
    return decorator

app = MiniRouter()

@app.get("/")
def read_root(current_role=None):
    return {"message": "Hello World"}

@app.get("/items")
def read_items(current_role=None):
    return ["Item 1", "Item 2"]

@app.get("/admin")
@require_role("admin")
def read_admin():
    return "Private: Revenue = 999,999 USD"
 
if __name__ == "__main__":
    print("\n---MINI SERVER STARTING ---")

    app.run("/")                     
    app.run("/items", "user")          
    app.run("/admin", "guest")          
    app.run("/admin", "admin")        
    app.run("/unknown-page")            
