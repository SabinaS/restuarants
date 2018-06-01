# Creator: Sabina Smajlaj
# Module for mimicing a debit card system

class DebitCardSystem( object ):

    def __init__( self ):
	self.accounts = {}

    def create_account( self, initial_balance ):
	''' Create an account on the system.
	    
	    Parameters
	    ----------
	    initial_balance: double
	        The initial balance of the account 
	    
	    Returns
	    -------
	    account_id: str
	        Unique identifier for each account
	'''
	new_account = Account( initial_balance )
	self.accounts.update( { new_account.id: new_account } )
	return new_account.id

    def charge( self, account_id, amount ):
	''' Regular charge on the account of the user.
	    Automartically debit the amount from the account
            if there are sufficient funds to cover it.

	    Parameters
	    ----------
	    account_id: str
	        The unique id of the account

	    amount: double
		Monetary amount to debit from the account
	
	    Returns
	    -------
	    bool - whether the charge transction was
		successful or not 
	'''
	account = self.accounts[ account_id ]
	if account.balance < amount:
	    return False
	account.balance = account.balance - amount
	return True

    def hold( self, account_id, vendor_id, amount ):
	''' Place a hold on the account. The balance
	    should reflect this hold. Only one hold
	    per vendor_id allowed.
	'''
	account = self.accounts[ account_id ]
	if amount > account.balance:
	    return False 
	holds = account.holds
	if vendor_id in [ hold[ 'vendor_id' ] for hold in account.holds ]:
	    return False
	hold = Hold( vendor_id, amount )
	account.balance = account.balance - amount
	return True

    def settle_hold( self, account_id, vendor_id, actual_amount ):
	''' Settle the account by checking to make sure the 
	    account has sufficient balance for the actual 
	    amount to be charged.
	'''
	if vendor_id not in [ hold[ 'vendor_id' ] for hold in account.holds ]:
            return False
	account = self.accounts[ account_id ]
	hold_amt = [ hold[ 'amount' ] for hold in account.holds ]
	actual_balance = account.balance + hold_amt
	if actual_amount > actual_balance:
	    return False
	for hold in account.holds:
	    if hold[ 'vendor_id' ] == vendor_id:
		account.holds.remove( hold )
		account.balance = account.balance + hold[ 'amount' ]
	return True
	
