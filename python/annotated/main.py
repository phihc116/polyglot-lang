from typing import Annotated, get_type_hints

class Field:
    def __init__(self, gt=None, lt=None):
        self.gt = gt
        self.lt = lt
    
def get_metadata(cls):
    hints = get_type_hints(cls, include_extras=True) 
    metadata = {}
    for field, annotated in hints.items(): 
        origin = getattr(annotated, "__origin__", None)
        metas = getattr(annotated, "__metadata__", [])
        metadata[field] = metas  
    return metadata

class BaseModel:
    def __init__(self, **kwargs): 
        self.__meta = get_metadata(self.__class__)

        for key, value in kwargs.items():
            self.validate(key, value)
            setattr(self, key, value)

    def validate(self, key, value): 
        metas = self.__meta.get(key, [])
        for m in metas:
            if isinstance(m, Field):
                if m.gt is not None and not (value > m.gt):
                    raise ValueError(f"{key} must be > {m.gt}")
                if m.lt is not None and not (value < m.lt):
                    raise ValueError(f"{key} must be < {m.lt}")

class User(BaseModel):
    name: str
    age: Annotated[int, Field(gt=0, lt=120)]

u1 = User(name="Alice", age=18)  
u2 = User(name="Bob", age=-5)      
