import mysql.connector
from datetime import datetime

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sudheer@123",
    database="bank0"
)
cursor = conn.cursor()

while True:
    print("\n--- BANKING SYSTEM MENU ---")
    print("1. Admin")
    print("2. User")
    print("3. Exit")

    choice = input("Enter your choice: ")
    admin = 'admin'
    admin_pass = 'admin_321'

    if choice == "1":
        username = input("Enter Admin Username: ")
        password = input("Enter Admin Password: ")

        if username == admin and password == admin_pass:
            print(" Successful login")
            while True:
                print("\n--- ADMIN MENU ---")
                print("1. View All Users")
                print("2. View User Transactions")
                print("3. Deposit Money into User Account")
                print("4. Delete User Account")
                print("5. Back to Main Menu")

                admin_choice = input("Enter your choice: ")

                if admin_choice == "1":
                    cursor.execute("SELECT acc_no, name, acc_type, balance FROM accounts")
                    users = cursor.fetchall()
                    if users:
                        print("All Users:")
                        for user in users:
                            print(f"Account No: {user[0]}, Name: {user[1]}, Type: {user[2]}, Balance: ₹{user[3]}")
                    else:
                        print("No users found!")

                elif admin_choice == "2":
                    acc_no = int(input("Enter Account Number: "))
                    cursor.execute("SELECT transaction_type, amount FROM transactions WHERE acc_no = %s", (acc_no,))
                    transactions = cursor.fetchall()
                    if transactions:
                        print("Transaction History:")
                        for t in transactions:
                            print(f"{t[0]} ₹{t[1]}")
                    else:
                        print("No transactions found!")

                elif admin_choice == "3":
                    acc_no = int(input("Enter Account Number: "))
                    amount = float(input("Enter Deposit Amount: "))
                    cursor.execute("SELECT balance FROM accounts WHERE acc_no = %s", (acc_no,))
                    result = cursor.fetchone()
                    if result:
                        new_balance = result[0] + amount
                        cursor.execute("UPDATE accounts SET balance = %s WHERE acc_no = %s", (new_balance, acc_no))
                        cursor.execute("INSERT INTO transactions (acc_no, transaction_type, amount) VALUES (%s, %s, %s)",
                                       (acc_no, "Deposit", amount))
                        conn.commit()
                        print(f"₹{amount} deposited into account {acc_no}.")
                    else:
                        print("Account not found!")

                elif admin_choice == "4":
                    acc_no = int(input("Enter Account Number to Delete: "))
                    cursor.execute("DELETE FROM transactions WHERE acc_no = %s", (acc_no,))
                    cursor.execute("DELETE FROM accounts WHERE acc_no = %s", (acc_no,))
                    conn.commit()
                    print(f"Account {acc_no} and all related transactions deleted.")

                elif admin_choice == "5":
                    break

                else:
                    print("Invalid admin option!")

        else:
            print("Invalid Admin Credentials!")

    elif choice == "2":
        while True:
            print("\n--- USER MENU ---")
            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Account Details")
            print("5. View Transactions")
            print("6. Change PIN")
            print("7. Back to Main Menu")

            user_choice = input("Enter your choice: ")

            if user_choice == "1":
                acc_no = int(input("Enter 9-digit Account Number: "))
                if len(str(acc_no)) != 9:
                    print("Account number must be 9 digits!")
                    continue

                name = input("Enter Name: ")
                acc_type = input("Enter Account Type (Savings/Current): ")
                balance = float(input("Enter Initial Balance: "))
                pin = int(input("Set PIN: "))
                mobile = input("Enter mobile number: ")

                if mobile[0] in '12345' and len(str(mobile))!=12345 :
                           print("Please enter a valid Indian mobile number starting with 6, 7, 8, or 9.")
                           continue  # 
                # Check if account already exists
                cursor.execute("SELECT acc_no FROM accounts WHERE acc_no = %s", (acc_no,))
                existing = cursor.fetchone()

                if existing:
                    print("Account already exists with this number!")
                else:
                    cursor.execute("INSERT INTO accounts (acc_no, name, acc_type, balance, pin, mobile) VALUES (%s, %s, %s, %s, %s, %s)",
                                   (acc_no, name, acc_type, balance, pin, mobile))
                    conn.commit()
                    print(f"Account for {name} created successfully!")



                cursor.execute("SELECT acc_no FROM accounts WHERE acc_no = %s", (acc_no,))
                existing = cursor.fetchone()
                if existing:
                    print(" Account already exists with this number!")
                else:
                    cursor.execute("INSERT INTO accounts (acc_no, name, acc_type, balance, pin, mobile) VALUES (%s, %s, %s, %s, %s, %s)",
                                   (acc_no, name, acc_type, balance, pin, mobile))
                    conn.commit()
                    print(f"Account for {name} created successfully!")

            elif user_choice == "2":
                acc_no = int(input("Enter Account Number: "))
                amount = float(input("Enter Deposit Amount: "))
                cursor.execute("SELECT balance FROM accounts WHERE acc_no = %s", (acc_no,))
                result = cursor.fetchone()
                if result:
                    new_balance = result[0] + amount
                    cursor.execute("UPDATE accounts SET balance = %s WHERE acc_no = %s", (new_balance, acc_no))
                    cursor.execute("INSERT INTO transactions (acc_no, transaction_type, amount) VALUES (%s, %s, %s)",
                                   (acc_no, "Deposit", amount))
                    conn.commit()
                    print(f"₹{amount} deposited. New balance: ₹{new_balance}")
                else:
                    print("Account not found!")

            elif user_choice == "3":
                acc_no = int(input("Enter Account Number: "))
                amount = float(input("Enter Withdrawal Amount: "))
                pin = int(input("Enter PIN: "))
                cursor.execute("SELECT balance, pin FROM accounts WHERE acc_no = %s", (acc_no,))
                result = cursor.fetchone()
                if result:
                    balance, stored_pin = result
                    if stored_pin != pin:
                        print("Incorrect PIN!")
                    elif amount > balance:
                        print("Insufficient Balance!")
                    else:
                        new_balance = balance - amount
                        cursor.execute("UPDATE accounts SET balance = %s WHERE acc_no = %s", (new_balance, acc_no))
                        cursor.execute("INSERT INTO transactions (acc_no, transaction_type, amount) VALUES (%s, %s, %s)",
                                       (acc_no, "Withdrawal", amount))
                        conn.commit()
                        print(f"₹{amount} withdrawn. New balance: ₹{new_balance}")

            elif user_choice == "4":
                acc_no = int(input("Enter Account Number: "))
                cursor.execute("SELECT acc_no, name, acc_type, balance FROM accounts WHERE acc_no = %s", (acc_no,))
                result = cursor.fetchone()
                if result:
                    print(f"Account No: {result[0]}, Name: {result[1]}, Type: {result[2]}, Balance: ₹{result[3]}")
                else:
                    print("Account not found.")

            elif user_choice == "5":
                acc_no = int(input("Enter Account Number: "))
                cursor.execute("SELECT transaction_type, amount FROM transactions WHERE acc_no = %s", (acc_no,))
                transactions = cursor.fetchall()
                if transactions:
                    print("Transaction History:")
                    for t in transactions:
                        print(f"{t[0]} ₹{t[1]}")
                else:
                    print("No transactions found.")

            elif user_choice == "6":
                acc_no = int(input("Enter Account Number: "))
                old_pin = int(input("Enter Old PIN: "))
                new_pin = int(input("Enter New PIN: "))
                cursor.execute("SELECT pin FROM accounts WHERE acc_no = %s", (acc_no,))
                result = cursor.fetchone()
                if result and result[0] == old_pin:
                    cursor.execute("UPDATE accounts SET pin = %s WHERE acc_no = %s", (new_pin, acc_no))
                    conn.commit()
                    print("PIN updated successfully!")
                else:
                    print("Incorrect old PIN or account not found!")

            elif user_choice == "7":
                break

            else:
                print("Invalid option.")

    elif choice == "3":
        print("Exiting Banking System. Goodbye!")
        break

    else:
        print("Invalid main menu option.")

conn.close()
