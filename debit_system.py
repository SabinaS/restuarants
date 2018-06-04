# Module for mimicing a debit card system

class Account( object ):

    def __init__( self, initial_balance ):
	self.id = self.createUniqueID()
	self.balance = initial_balance
	self.holds = []

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
	self.vendor_id = vendor_id
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

	    Return
	    ------
	    bool - if there is already a hold for the vendor 
	    	or if the balance is insufficient, return 
	   	False, else True. 
	'''
	account = self.accounts[ account_id ]
	if amount > account.balance:
	    return False 
	holds = account.holds
	if vendor_id in [ hold.vendor_id for hold in account.holds ]:
	    return False
	hold = Hold( vendor_id, amount )
	account.holds.append( hold )
	account.balance = account.balance - amount
	return True

    def settle_hold( self, account_id, vendor_id, actual_amount ):
	''' Settle the account by checking to make sure the 
	    account has sufficient balance for the actual 
	    amount to be charged.
	'''
	account = self.accounts[ account_id ]
	if vendor_id not in [ hold.vendor_id for hold in account.holds ]:
            return False
	hold = None
	for hold in account.holds:
	    if hold.vendor_id == vendor_id:
		hold = hold
	actual_balance = account.balance + hold.amount
	if actual_amount > actual_balance:
	    account.balance = account.balance + hold.amount
	    account.holds.remove( hold )
	    return False
	account.holds.remove( hold )
	account.balance = account.balance + hold.amount - actual_amount
	return True


import unittest
class DebitCardSystemTest( unittest.TestCase ):

    def setUp( self ):
	self.system = DebitCardSystem()
	self.account_1 = self.system.create_account( 123 )
	self.account_2 = self.system.create_account( 234 )

    def test_create_account( self ):
	initial_balance = 567
	account_id = self.system.create_account( initial_balance )
	self.assertIn( account_id, self.system.accounts )
	self.assertEqual( initial_balance, self.system.accounts[ account_id ].balance )

    def test_charge_success( self ):
        self.assertTrue( self.system.charge( self.account_1, 35 ) )

    def test_charge_fail( self ):
	self.assertFalse( self.system.charge( self.account_2, 300 ) )

    def test_hold_success( self ):
	vendor_id = 'pizza_hut'
	amount = 200
	self.assertTrue( self.system.hold( self.account_2, vendor_id, amount ) )

    def test_hold_fail( self ):
	vendor_id = 'pizza_hut'
	amount1 = 200
	amount2 = 300
	self.system.hold( self.account_2, vendor_id, amount1 ) 
	self.assertFalse( self.system.hold( self.account_2, vendor_id, amount2 ) )

    def test_settle_hold_success( self ):
	vendor_id = 'pizza_hut'
	balance = self.system.accounts[ self.account_1 ].balance 
	self.system.hold( self.account_1, vendor_id, 100 )
	actual_amount = 110
	self.assertTrue( self.system.settle_hold( self.account_1, vendor_id, actual_amount ) )
	self.assertEqual( balance - actual_amount, self.system.accounts[ self.account_1 ].balance )

    def test_settle_hold_fail( self ):
        vendor_id = 'pizza_hut'
        balance = self.system.accounts[ self.account_2 ].balance
        self.system.hold( self.account_2, vendor_id, 200 )
        actual_amount = 250
        self.assertFalse( self.system.settle_hold( self.account_2, vendor_id, actual_amount ) )
        self.assertEqual( balance, self.system.accounts[ self.account_2 ].balance )



if '__name__' == '__main__':
    unittest.main()

	
