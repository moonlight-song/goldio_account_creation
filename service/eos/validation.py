from re import fullmatch


def validate_account_name(account_name):
	if not (type(account_name) == str and fullmatch("^[1-5a-z]{12}$", account_name)):
		raise TypeError("Invalid EOS account name")


def validate_public_key(public_key):
	if not (type(public_key) == str and fullmatch("^EOS[0-9a-zA-Z]{50}$", public_key)):
		raise TypeError("Invalid EOS public key")


def validate_private_key(private_key):
	if not (type(private_key) == str and fullmatch("^5[HJK][0-9a-zA-Z]{49}$", private_key)):
		raise TypeError("Invalid EOS private key")