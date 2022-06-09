import sqlite3

class accessing_database:
	def __init__(self):
		self.conn = sqlite3.connect('test.db')

	def validate_login(self, username, password):
		self.conn = sqlite3.connect('test.db')
		self.username, self.password = username, password
		# ____________________________ empty value check ____________________________
		if len(self.username)==0 :
			self.conn.commit()
			self.conn.close()
			return False, "Please enter username"
		elif len(self.password)==0 :
			self.conn.commit()
			self.conn.close()
			return False, "Please enter password"
		# _____________________________ username check ______________________________
		self.check_username = self.conn.execute(f"SELECT USER_ID FROM ACCOUNT WHERE USER_ID='{self.username}'").fetchall()
		if not self.check_username :
			self.conn.commit()
			self.conn.close()
			print("Username does not exist")
			return False, "Username does not exist"
		# ___________________________________________________________________________
		else:
			self.cred_password = self.conn.execute(f"SELECT PASSWORD from ACCOUNT WHERE USER_ID='{self.username}'").fetchone()
			self.conn.commit()
			self.conn.close()
			if str(self.cred_password[0]) == str(self.password) :
				return True, "Validation success"
			else :
				return False, "Wrong password"
		# ___________________________________________________________________________
	def check_balance(self, username):
		self.conn = sqlite3.connect('test.db')
		self.username = username
		self.balance_amount = self.conn.execute(f"SELECT BALANCE FROM ACCOUNT WHERE USER_ID='{self.username}'").fetchone()
		self.conn.commit()
		self.conn.close()
		return self.balance_amount[0]


	def withdrawl_money(self, amount, username):
		self.conn = sqlite3.connect('test.db')
		self.amount, self.username = amount, username
		self.balance = self.conn.execute(f"SELECT BALANCE FROM ACCOUNT WHERE USER_ID='{self.username}'").fetchone()
		self.new_balance = int(self.balance[0]) - int(self.amount)
		self.conn.execute(f"UPDATE ACCOUNT SET BALANCE='{self.new_balance}' WHERE USER_ID='{self.username}'")
		self.conn.commit()
		self.conn.close()

	def deposit_money(self, amount, username):
		self.conn = sqlite3.connect('test.db')
		self.amount, self.username = amount, username
		self.balance = self.conn.execute(f"SELECT BALANCE FROM ACCOUNT WHERE USER_ID='{self.username}'").fetchone()
		print("___________________________________________________________________________")
		print("Old balance : ", self.balance[0])
		print("amount : ", self.amount)
		print("___________________________________________________________________________")
		self.new_balance = int(self.balance[0]) + int(self.amount)
		self.conn.execute(f"UPDATE ACCOUNT SET BALANCE='{self.new_balance}' WHERE USER_ID='{self.username}'")
		self.conn.commit()
		self.conn.close()

	def transfer_fund(self, amount, balance, username, to_acc_no):
		self.conn = sqlite3.connect('test.db')
		self.amount, self.username, self.to_acc_no = amount, username, to_acc_no

		self.balance_from = self.conn.execute(f"SELECT BALANCE FROM ACCOUNT WHERE USER_ID='{self.username}'").fetchone()
		self.balance_to   = self.conn.execute(f"SELECT BALANCE FROM ACCOUNT WHERE ACCOUNT_NO='{self.to_acc_no}'").fetchone()

		self.new_balance_from = self.balance_from[0] - self.amount
		self.new_balance_to   = self.balance_to[0] + self.amount
		print("sender new balance" , self.new_balance_from)
		print("receiver new balance", self.new_balance_to)

		self.conn.execute(f"UPDATE ACCOUNT SET BALANCE='{self.new_balance_from}' WHERE USER_ID='{self.username}'")
		self.conn.execute(f"UPDATE ACCOUNT SET BALANCE='{self.new_balance_to}' WHERE ACCOUNT_NO='{self.to_acc_no}'")

		self.conn.commit()
		self.conn.close()

		return True, "Funds transferred successfully"




