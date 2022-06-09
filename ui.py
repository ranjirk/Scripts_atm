import tkinter as ttk
from tkinter import *
import s1
from s1 import accessing_database

class login_page:
	def __init__(self):
		self.obj_db = accessing_database()
		self.credentials = {"username":"", "password":"", "message":""}
		self.username_var, self.password_var, self.withdrawl_var, self.deposit_var = "", "", "", ""
		self.receiver_var, self.transactionAmount = "", ""
		self.top = ttk.Tk()
		self.screen_width, self.screen_height  = self.top.winfo_screenwidth(), self.top.winfo_screenheight()
		self.width, self.height  = 350, int(self.screen_height - 650)
		self.top.geometry(f"{self.width}x{self.height}")
		self.loginPageUI()
		
		self.top.mainloop()

	def loginPageUI(self):
		self.welcomeLabel = ttk.Label(self.top, text='Welcome to Bank ATM')
		self.usernameLabel = ttk.Label(self.top, text='Username')
		self.passwordLabel = ttk.Label(self.top, text='Password')
		self.usernameField = ttk.Entry(self.top, textvariable=self.username_var)
		self.passwordField = ttk.Entry(self.top, textvariable=self.password_var, show="*")
		self.loginButton = ttk.Button(self.top, text="Login", command=self.validation)

		self.welcomeLabel.grid(column=2,  row=1, columnspan=3)
		self.usernameLabel.grid(column=2, row=3)
		self.passwordLabel.grid(column=2, row=4)
		self.usernameField.grid(column=3, row=3)
		self.passwordField.grid(column=3, row=4)
		self.loginButton.grid(column=2, row=5, columnspan=2)

	def validation(self):
		self.credentials['username'] = str(self.usernameField.get())
		self.credentials['password'] = str(self.passwordField.get())
		self.login_result = self.obj_db.validate_login(self.credentials['username'], self.credentials['password'])
		self.credentials["message"] = self.login_result[1]
		self.wrongCred = ttk.Label(self.top, text=self.credentials["message"])
		if self.login_result[0]:
			self.destroyAllWidgets()
			self.firstPage()
		else:
			self.wrongCred.grid(column=2, row=6, columnspan=3)

	def firstPage(self): # Page UI after successful login
		self.destroyAllWidgets()
		self.welcomeLabel2  = ttk.Label(self.top,  text="Please select your transaction")
		self.balanceButton  = ttk.Button(self.top, text="Check Balance", command=self.displayBalancePage)
		self.withdrawButton = ttk.Button(self.top, text="Withdrawl",     command=self.withdrawMoneyPage)
		self.depositButton  = ttk.Button(self.top, text="Deposit",       command=self.depositMoneyPage)
		self.transferButton = ttk.Button(self.top, text="Transfer",      command=self.transferMoneyPage)
		self.welcomeLabel2.grid( column=2, row=1, columnspan=3)
		self.balanceButton.grid( column=2, row=2)
		self.depositButton.grid( column=2, row=3)
		self.withdrawButton.grid(column=3, row=2)
		self.transferButton.grid(column=3, row=3)
# ___________________________________ First page button actions ___________________________________
	def displayBalancePage(self):
		self.balanceAmount = self.obj_db.check_balance(self.credentials['username'])
		self.balanceLabel = ttk.Label(self.top, text=f'Balance is : {str(self.balanceAmount)} rupees')
		self.balanceLabel.grid(column=2, row=5, columnspan=4)
		print("Displaying Funds")
	def withdrawMoneyPage(self):
		self.destroyAllWidgets()
		self.withdrawBackButton = ttk.Button(self.top, text='Back', command=self.firstPage)
		self.withdrawlAmountLabel = ttk.Label(self.top, text="Enter the amount you want to withdraw")
		self.withdrawlAmountField = ttk.Entry(self.top, textvariable=self.withdrawl_var)
		self.withdrawlPageButton = ttk.Button(self.top, text='Withdraw Funds', command=self.withdrawAction)
		self.withdrawBackButton.grid(column=1, row=1)
		self.withdrawlAmountLabel.grid(column=2, row=2, columnspan=3)
		self.withdrawlAmountField.grid(column=5, row=2)
		self.withdrawlPageButton.grid(column=2, row=3)
		print("Withdrawing Funds")
	def depositMoneyPage(self):
		self.destroyAllWidgets()
		self.depositBackButton  = ttk.Button(self.top, text='Back', command=self.firstPage)
		self.depositAmountLabel = ttk.Label(self.top, text="Enter the amount you want to deposit")
		self.depositAmountField = ttk.Entry(self.top, textvariable=self.deposit_var)
		self.depositPageButton  = ttk.Button(self.top, text='Deposit funds', command=self.depositAction)
		self.depositBackButton.grid(column=1, row=1)
		self.depositAmountLabel.grid(column=2, row=2, columnspan=3)
		self.depositAmountField.grid(column=5, row=2)
		self.depositPageButton.grid(column=2, row=3)
		print("Depositing Funds")
	def transferMoneyPage(self):
		self.destroyAllWidgets()
		self.transferBackButton     = ttk.Button(self.top, text='Back', command=self.firstPage)
		self.receiverAccountLabel   = ttk.Label(self.top,  text='Receiver Account number')
		self.receiverAccountField   = ttk.Entry(self.top,  textvariable=self.receiver_var)
		self.transactionAmountLabel = ttk.Label(self.top,  text='Enter transaction amount')
		self.transactionAmountField = ttk.Entry(self.top,  textvariable=self.transactionAmount)
		self.transferButton     = ttk.Button(self.top, text='Transfer', command=self.transferAction)
		self.transferBackButton.grid(column=1, row=1)
		self.receiverAccountLabel.grid(column=1, row=2, columnspan=3)
		self.receiverAccountField.grid(column=4, row=2)
		self.transactionAmountLabel.grid(column=1, row=3, columnspan=3)
		self.transactionAmountField.grid(column=4, row=3)
		self.transferButton.grid(column=2, row=4)
		print("Transferring Funds")
# _________________________________________________________________________________________________
	def withdrawAction(self):
		self.amount = int(self.withdrawlAmountField.get())
		self.current_balance = int(self.obj_db.check_balance(self.credentials['username']))
		if self.current_balance < self.amount :
			self.lowBalancePage()
		else :
			self.obj_db.withdrawl_money(self.amount, self.credentials['username'])
			self.successMessageLabel = ttk.Label(self.top, text="Funds withdrawn successfully")
			self.successMessageLabel.grid(column=3,row=5, columnspan=2)
	def lowBalancePage(self):
		print("Insufficient funds")
		self.destroyAllWidgets()
		self.lowBalanceLabel = ttk.Label(self.top, text="Insufficient funds")
		self.lowBalanceLabel.grid(column=4, row=4)
		self.withdrawBackButton2 = ttk.Button(self.top, text='Back', command=self.withdrawMoneyPage)
		self.withdrawBackButton2.grid(column=1, row=1)
	def depositAction(self):
		self.amount = int(self.depositAmountField.get())
		self.obj_db.deposit_money(self.amount, self.credentials['username'])
		self.successMessageLabel = ttk.Label(self.top, text="Funds deposited successfully")
		self.successMessageLabel.grid(column=3,row=5, columnspan=2)
	def transferAction(self):
		self.transactionAmount = int(self.transactionAmountField.get())
		self.toAccountNo = int(self.receiverAccountField.get())
		self.balance = int(self.obj_db.check_balance(self.credentials['username']))
		if self.balance < self.transactionAmount :
			self.lowBalancePage()
		else:
			self.transactionResult = self.obj_db.transfer_fund( self.transactionAmount, self.balance, \
																self.credentials['username'], self.toAccountNo)
			self.successMessageLabel = ttk.Label(self.top, text=self.transactionResult[1])
			self.successMessageLabel.grid(column=3,row=5, columnspan=2)

	def destroyAllWidgets(self):
		for wid in self.top.winfo_children():
			wid.destroy()

obj = login_page()