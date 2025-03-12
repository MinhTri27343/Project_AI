class FactoryTest:
    _registry = {}  # Dictionary chứa danh sách lớp con

    @classmethod
    def register(cls, key):
        def decorator(subclass):
            cls._registry[key] = subclass()  # Đăng ký lớp vào _registry
            return subclass
        return decorator

    @classmethod
    def getProperties(cls):
        return cls._registry  # Trả về nguyên dictionary

# Lớp cha
class Test:
    def __init__(self, pos_ghost, pos_player):
        self.pos_ghost = pos_ghost
        self.pos_player = pos_player

    def getTest(self):
        return self.pos_ghost, self.pos_player

    def signature(self):
        return self.__class__.__name__



@FactoryTest.register("Test1")
class Test1(Test):
    def __init__(self):
        super().__init__((40, 30), (540, 500))

@FactoryTest.register("Test2")
class Test2(Test):
    def __init__(self):
        super().__init__((40, 30), (40, 500))

@FactoryTest.register("Test3")
class Test3(Test):
    def __init__(self):
        super().__init__((40, 30), (540, 30))

@FactoryTest.register("Test4")
class Test4(Test):
    def __init__(self):
        super().__init__((40, 30), (290, 400))
@FactoryTest.register("Test5")
class Test5(Test):
    def __init__(self):
        super().__init__((40, 30), (290, 200))