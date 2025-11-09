#  Bank Management System
#  Using Object Orinted Programing ,File Handling
"""
--> used for creating an new account
--> code is user-interactive-where user can enter data(nmae,account type, and transaction details)
new users creates an account and existing users can log in with their account number 

"""
import csv
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
        print(f"Account Number: {self.acc_no} \nHolder: {self.holder_name} \nBalance: {self.balance}")

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
        print(f"Added interest: {interest}.\nNew Balance: {self.balance}")

#CurrentAccount class - Inherits BankAccount(Polymorphism)
class CurrentAccount(BankAccount):
    def __init__(self, acc_no, name, balance=0, overdraft=0):
        super().__init__(acc_no, name, balance)
        self.overdraft = float(overdraft)

    def account_type(self):
        print("This is a Current Account.")


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


def load_accounts():
    accounts = {}
    try:
        with open("accounts.csv",'r') as file:
            data = csv.DictReader(file)
            for row in data:
                acc_type = row['Type']
                acc_no = row["Acc_no"]
                name = row['Name']
                balance = float(row['Balance'])
                if acc_type == 'savings':
                    accounts[acc_no] = SavingsAccount(acc_no,name,balance)
                else:
                    accounts[acc_no] = CurrentAccount(acc_no,name,balance)
    except FileNotFoundError:
        with open("accounts.csv",'w',newline="") as file:
            write = csv.writer(file)
            write.writerow(['Acc_no','Name','Type','Balance'])
    return accounts

def save_accounts(accounts):
    with open("accounts.csv",'w',newline="") as file:
        write = csv.writer(file)
        write.writerow(['Acc_no','Name','Type','Balance'])
        for acc_no, acc in accounts.items():
            acc_type = "savings" if isinstance(acc, SavingsAccount) else "current" 
            write.writerow([acc.acc_no,acc.holder_name,acc_type,acc.balance])


# executing some tests
def main():
    print("-----Welcome to the Python Bank System----- ")

    accounts = load_accounts()
    print("1.New User \n2.Existing User")
    ch = input("Enter a choice(1/2): ")

    if ch == '1':
        name = input("Enter your Name: ")
        age = int(input("Enter your age: "))
        acc_no = input("Enter Account Number: ")
        if acc_no in accounts:
            print("! Account already exists")
            return
        acc_type = input("Choose Account Type(savings/current): ").lower()
        opening_balance = float(input("Enter Opening Balance: "))

        if acc_type == "savings":
            account = SavingsAccount(acc_no,name,opening_balance)
        else:
            account = CurrentAccount(acc_no,name,opening_balance)
    
        accounts[acc_no] = account
        save_accounts(accounts)
        print("\n Account created successfully \n")
    
    elif ch == '2':
        acc_no = input("Enter your 10-digit Account Number: ")
        if acc_no not in accounts:
            print("Account not found,choose 1 for creating")
            return
        account = accounts[acc_no]
        print(f"\n Welcome {account.holder_name}")
    else:
        print("Invalid option.")
        return





    while True:
        print("\n-----MENU-------------")
        print("\n 1.Deposit \n 2.Withdraw \n 3.View Balance \n 4.Add Interest(Savings only) \n 5.Exit")
        ch = input("Enter a choice: ")

        if ch == '1':
            amount = float(input("Enter deposit amount: "))
            DepositTransaction(account,amount).process_transaction()
        elif ch == '2':
            amount = float(input("Enter withdraw amount: "))
            WithdrawTransaction(account,amount).process_transaction()
        elif ch == '3':
            account.display_info()
        elif ch == '4':
            if isinstance(account,SavingsAccount):
                account.add_interest()
            else:
                print("Interest option is only for saving account.")
        elif ch == '5':
            save_accounts(accounts)
            print("Thank you")
            break
        else:
            print("Invalid choice,Try again !!")

if __name__ == "__main__":
    main()
