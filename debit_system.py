# Creator: Sabina Smajlaj
# Module for mimicing a debit card system

class Account( object ):

    def __init__( self, initial_balance ):
	self.id = self.createUniqueID()
	self.balance = initial_balance

    def createUniqueID( self ):
	''' Create and return a unique id
	    for each account.
	'''
	import uuid
	uuid = uuid.uuid4()
	id = str( uuid )
	return id


class Hold( object ):

    def __init__( self, vendor_id, amount ):
	self.vendor_ib = vendor_id
	self.amount = amount 


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
	account = self.accounts[ account_id ]
	if vendor_id not in [ hold[ 'vendor_id' ] for hold in account.holds ]:
            return False
	hold_amt = [ hold[ 'amount' ] for hold in account.holds ]
	actual_balance = account.balance + hold_amt
	if actual_amount > actual_balance:
	    return False
	for hold in account.holds:
	    if hold[ 'vendor_id' ] == vendor_id:
		account.holds.remove( hold )
		account.balance = account.balance + hold[ 'amount' ]
	return True


import unittest
class DebitCardSystemTest( unittest.TestCase ):

    def setUp( self ):
	self.account_1 = Account( 123 )
	self.account_2 = Account( 234 )
	self.system = DebitCardSystem()

    def test_create_account( self ):
	initial_balance = 567
	account_id = self.system.create_account( initial_balance )
	self.assertIn( account_id, self.system.accounts )
	self.assertEqual( initial_balance, self.system.accounts[ account_id ] )

    def test_charge_success( self ):
        self.assertTrue( self.system.charge( self.account_1, 35 ) )

    def test_charge_fail( self ):
	self.assertFalse( self.system.charge( self.account_2, 300 ) )

    def test_hold_success( self ):
	vendor_id = 'pizza_hut'
	amount = 200
        hold1 = Hold( vendor_id, amount )
	self.assertTrue( self.system.hold( self.account_2, vendor_id, amount ) )

    def test_hold_fail( self ):
	vendor_id = 'pizza_hut'
	amount1 = 200
	amount2 = 300
	hold1 = Hold( vendor_id, amount1 )
	hold2 = Hold( vendor_id, amount2 )
	self.system.hold( self.system.hold( self.account_2, vendor_id, amount1 ) ) 
	self.assertFalse( self.system.hold( self.account_2, vendor_id, amount2 ) )

    def test_settle_hold( self ):
	pass


if '__name__' == '__main__':
    unittest.main()

	
