#minimum balance class

class OpenAccount:
    def __init__(self,starting_balance):
        self.current = starting_balance
        

    def deposit(self,amount):
        self.amount=amount
        self.current += self.amount
        return self.current

    def withdraw(self,amount):
        self.amount = amount
        try:
            self.current -=self.amount
            if self.current < 0:
                raise LessThanZero
        except LessThanZero:
            self.current +=self.amount
            print"you cant withdraw the amount ",self.current

        else:
            return self.current
        
class LessThanZero(Exception):
    pass
a = OpenAccount(5000)
b = OpenAccount(3000)
a.withdraw(2000)
a.withdraw(2000)
a.withdraw(2000)
            
        
        
