class CompanyCar():
    def __init__(self,name):
        self.name = name

    def get_name(self) -> str:
        print(self.name)
        return self.name
    
    def set_name(self,name) -> str:
        self.name = name
        print(self.name)
        return name
    

class Car(CompanyCar):
    def __init__(self,name,roda,company):
        super().__init__(name) 
        self.company = company
        self.name = name
        self.roda = roda

    def get_name(self) -> str:
        print("car : ",self.name, "company",self.company)
        return self.name
    
    def set_name(self,name) -> str:
        self.name = name
        print(self.name)
        return name
