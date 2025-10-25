# Object Orinted Programing 
"""Bank Management System"""

from abc import ABC, abstractmethod

# Parent class - inherited by BankAccount
class Customer:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Customer Name: {self.name}, Age: {self.age}")

# BankAccount class - Inherits customer + encapsulation
class BankAccount:
    def __init__(self, acc_no, holder_name,balance=0):
        # Simple account that stores owner name and numeric balance
        self.acc_no = acc_no
        self.holder_name = holder_name
        self.balance = float(balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: {amount}. New Balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew: {amount}. New Balance: {self.balance}")
        else:
            print("Insufficient balance or invalid withdrawal amount.")

    def display_info(self):
        print(f"Account Number: {self.acc_no}, Holder: {self.holder_name}, Balance: {self.balance}")

#SavingsAccount class - Inherits BankAccount
class SavingsAccount(BankAccount):
    def __init__(self, acc_no, name, balance=0, rate=5.0):
        super().__init__(acc_no, name, balance)
        self.rate = float(rate)

    def account_type(self):
        print("This is a Savings Account.")

    def interest_rate(self):
        print(f"Interest rate is: {self.rate}%")

    def add_interest(self):
        interest = (self.balance * self.rate) / 100
        self.balance += interest
        print(f"Added interest: {interest}. New Balance: {self.balance}")

#CurrentAccount class - Inherits BankAccount(Polymorphism)
class CurrentAccount(BankAccount):
    def __init__(self, acc_no, name, balance=0, overdraft=0):
        super().__init__(acc_no, name, balance)
        self.overdraft = float(overdraft)

    def account_type(self):
        print("This is a Current Account.")

    def overdraft_limit(self, limit):
        self.overdraft = float(limit)
        print(f"Overdraft limit is set to: {self.overdraft}")

#Transaction class - Abstract Base Class
class Transaction(ABC):
    @abstractmethod
    def process_transaction(self):
        raise NotImplementedError

class DepositTransaction(Transaction):
    def __init__(self, account: BankAccount, amount: float):
        self.account = account
        self.amount = amount

    def process_transaction(self):
        self.account.deposit(self.amount)


class WithdrawTransaction(Transaction):
    def __init__(self, account: BankAccount, amount: float):
        self.account = account
        self.amount = amount

    def process_transaction(self):
        self.account.withdraw(self.amount)


# executing some tests
if __name__ == '__main__':
    customer1 = Customer("Alice", 30)
    customer1.display_info()

    account1 = SavingsAccount("SA123", "Alice", 1000)
    account1.display_info()
    account1.deposit(500)
    account1.withdraw(200)
    account1.add_interest()
    account1.display_info()

    account2 = CurrentAccount("CA456", "Bob", 2000)
    account2.display_info()
    account2.deposit(1000)
    account2.withdraw(500)
    account2.overdraft_limit(1000)
    account2.display_info()

    transaction1 = DepositTransaction(account1, 300)
    transaction1.process_transaction()
    transaction2 = WithdrawTransaction(account2, 400)
    transaction2.process_transaction()

    print("Done tests.")


