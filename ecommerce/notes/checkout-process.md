# checkout process

1. cart -> checkout view
	- lingin/register or enter an email as guest
	- shipping address
	- billing info
	  - billing address
	  - credit card / payment

2. billing app/component
	- billing profile
		- user or email (guest email)
		- generate payment processor token (stripe or braintree)

3. order / invoices component
	- connecting the billing profile
	- shipping / billing address
	- cart 
	- status -- shipped? cancelled?