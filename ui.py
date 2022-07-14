import tkinter as ttk
from tkinter import *
import s1, audio_accessibility
from s1 import accessing_database
from audio_accessibility import haudio
import time, logging

class login_page :
	def __init__(self):
		logging.basicConfig(filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
		self.obj_db = accessing_database()
		self.credentials = {"username":"", "password":"", "message":""}
		self.username_var, self.password_var, self.withdrawl_var, self.deposit_var = "", "", "", ""
		self.receiver_var, self.transactionAmount = "", ""
		self.top = ttk.Tk()
		self.screen_width, self.screen_height  = self.top.winfo_screenwidth(), self.top.winfo_screenheight()
		self.width, self.height  = 350, int(self.screen_height - 650)
		self.top.geometry(f"{self.width}x{self.height}")
		self.firstPageDict = {"balance" : self.displayBalancePage, "withdrawl" : self.withdrawMoneyPage, 
							  "deposit" : self.depositMoneyPage,   "transfer"  : self.transferMoneyPage}
		self.loginPageUI()
		self.top.mainloop()

	def loginPageUI(self):
		self.welcomeLabel  = ttk.Label( self.top, text='Welcome to Bank ATM')
		self.usernameLabel = ttk.Label( self.top, text='Username')
		self.passwordLabel = ttk.Label( self.top, text='Password')
		self.usernameField = ttk.Entry( self.top, textvariable=self.username_var)
		self.passwordField = ttk.Entry( self.top, textvariable=self.password_var, show="*")
		self.loginButton   = ttk.Button(self.top, text="Login", command=self.validation)

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
			logging.debug(f"Successfull login by {self.credentials['username']}")
			self.destroyAllWidgets()
			self.firstPage()
		else:
			logging.debug(f"Unsuccessfull login by {self.credentials['username']}")
			self.wrongCred.grid(column=2, row=6, columnspan=3)

	def firstPage(self): # Page UI after successful login
		self.destroyAllWidgets()
		self.welcomeLabel2  = ttk.Label(self.top,  text="Please select your transaction")
		self.audioLabel1    = ttk.Label(self.top,  text="Voice input")
		self.balanceButton  = ttk.Button(self.top, text="Check Balance", command=self.displayBalancePage)
		self.withdrawButton = ttk.Button(self.top, text="Withdrawl",     command=self.withdrawMoneyPage)
		self.depositButton  = ttk.Button(self.top, text="Deposit",       command=self.depositMoneyPage)
		self.transferButton = ttk.Button(self.top, text="Transfer",      command=self.transferMoneyPage)
		self.recordButton   = ttk.Button(self.top, text="Record",        command= \
			lambda: self.recordStart( ["balance", "withdrawl", "deposit", "transfer"] ))
		self.welcomeLabel2.grid( column=2, row=1, columnspan=3)
		self.balanceButton.grid( column=2, row=2)
		self.depositButton.grid( column=2, row=3)
		self.withdrawButton.grid(column=3, row=2)
		self.transferButton.grid(column=3, row=3)
		self.audioLabel1.grid(column=1, row=5, columnspan=3)
		self.recordButton.grid(column=2, row=6)
# ___________________________________ First page button actions ___________________________________
	def displayBalancePage(self):
		self.balanceAmount = self.obj_db.check_balance(self.credentials['username'])
		self.balanceLabel = ttk.Label(self.top, text=f'Balance is : {str(self.balanceAmount)} rupees')
		self.balanceLabel.grid(column=2, row=5, columnspan=4)
		logging.debug("Selected Check Balance option")
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
		logging.debug("Selected Withdraw option")
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
		logging.debug("Selected Deposit option")
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
		logging.debug("Selected Fund Transfer option")
	def recordStart(self, options):
		logging.debug("Selected Audio input option")
		self.options = options
		self.speakLabel = ttk.Label(self.top, text="Read out the option you want to choose...")
		self.speakLabel.grid(column=2, row=7)
		self.audioObj = haudio()
		self.recordResult = self.audioObj.record_Audio()
		self.speakLabel.destroy()
		if self.recordResult :
			logging.debug("Audio recording successful")
			self.wordResult, self.words = self.audioObj.speech2Words()
			if self.wordResult :
				logging.debug("Transcription successfull")
				self.selResult, self.selWord = self.audioObj.matchIt(self.words, self.options)
				if self.selResult :
					logging.debug("Audio to option successful")
					self.firstPageDict[self.selWord]()
			else :
				logging.warning("No words could be transcribed from audio")
				self.transError = ttk.Label(self.top, text="Error in recognizing words, \
					please choose options by clicking their respective button or retry recording")
				self.transError.grid(column=2, row=9)
				time.sleep(3)
				self.transError.destroy()
		else:
			logging.warning("Unable to record audio")
			self.audioErrorLabel = ttk.Label(self.top, text="Error in recording audio, \
				please choose options by clicking their respective button or retry recording")
			self.audioErrorLabel.grid(column=2, row=8)
			time.sleep(3)
			self.audioErrorLabel.destroy()
# _________________________________________________________________________________________________
	def withdrawAction(self):
		self.amount = int(self.withdrawlAmountField.get())
		self.current_balance = int(self.obj_db.check_balance(self.credentials['username']))
		if self.current_balance < self.amount :
			logging.debug("No balance to withdraw")
			self.lowBalancePage()
		else :
			self.resultWith = self.obj_db.withdrawl_money(self.amount, self.credentials['username'])
			if self.resultWith:
				logging.debug("Successfull withdrawn of money")
				self.successMessageLabel = ttk.Label(self.top, text="Funds withdrawn successfully")
				self.successMessageLabel.grid(column=3,row=5, columnspan=2)
			else :
				logging.warning("Unsuccessfull withdrawl of money")
	def lowBalancePage(self):
		self.destroyAllWidgets()
		self.lowBalanceLabel = ttk.Label(self.top, text="Insufficient funds")
		self.lowBalanceLabel.grid(column=4, row=4)
		self.withdrawBackButton2 = ttk.Button(self.top, text='Back', command=self.withdrawMoneyPage)
		self.withdrawBackButton2.grid(column=1, row=1)
		logging.debug("Low Balance page loaded")
	def depositAction(self):
		self.amount = int(self.depositAmountField.get())
		self.resultDep = self.obj_db.deposit_money(self.amount, self.credentials['username'])
		if self.resultDep:
			logging.debug("Successfull Deposit made")
			self.successMessageLabel = ttk.Label(self.top, text="Funds deposited successfully")
			self.successMessageLabel.grid(column=3,row=5, columnspan=2)
		else:
			logging.warning("Unsuccessfull deposit made")
	def transferAction(self):
		self.transactionAmount = int(self.transactionAmountField.get())
		self.toAccountNo = int(self.receiverAccountField.get())
		self.balance = int(self.obj_db.check_balance(self.credentials['username']))
		if self.balance < self.transactionAmount :
			logging.warning("Low balance triggered")
			self.lowBalancePage()
		else:
			self.resultTrans = self.obj_db.transfer_fund( self.transactionAmount, self.balance, \
																self.credentials['username'], self.toAccountNo)
			if self.resultTrans:
				logging.debug("Successfull transfer of funds")
				self.transactionMessageLabel = ttk.Label(self.top, text="Funds transferred")
			else :
				logging.warning("Unsuccessfull transfer of funds")
				self.transactionMessageLabel = ttk.Label(self.top, text="Funds could not be transferred")				
			self.transactionMessageLabel.grid(column=3,row=5, columnspan=2)	
# ____________________________________________________
	def destroyAllWidgets(self):
		for self.wid in self.top.winfo_children():
			self.wid.destroy()
# ____________________________________________________

obj = login_page()