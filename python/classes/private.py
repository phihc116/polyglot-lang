class User:
    def __init__(self):
        self._role = "admin"
        self._permissions = self._load_permissions()

    def _load_permissions(self):
        return {"read", "write"}

    def can_write(self):
        return "write" in self._permissions

class Guest(User):
    def __init__(self):
        self._role = "guest"
        self._permissions = set()   # phá invariant

g = Guest()
print(g.can_write())   # False

#### _attribute không ngăn sub class phá nội bộ ####
#### khi đó __name (name mangling) sẽ có giá trị

class Account:
    def __init__(self):
        self.__features = self.__init_features()

    def __init_features(self):
        return {"download", "upload"}

    def can_upload(self):
        return "upload" in self.__features

class TrialAccount(Account):
    def __init__(self):
        super().__init__() 
        self.__features = set()   # KHÔNG đụng Account.__features

acc = TrialAccount()
print(acc.__dict__)
print(acc._Account__features) 
print(acc.can_upload())
