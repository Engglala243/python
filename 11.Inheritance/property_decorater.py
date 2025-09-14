class Emp:
    a = 1

    @classmethod # class decorator
    def show(cls):
        print(cls.a)

    @property # property decorator
    def name(self):
        return f"{self.__fname} and {self.__lname}"

    @name.setter # setter decorator
    def name(self, value):
        self.__fname = value.split(" ")[0]
        self.__lname = value.split(" ")[1]
        
e = Emp()
e.name = "Aje Raj"

print(e.name)

e.show()
