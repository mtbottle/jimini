import re

matchers = [amazon_giftcard_matcher]

def amazon_giftcard_matcher(s):
	''' This function maps amazon digital order coupon codes exactly. This
		will match the coupon code and generate and return the url for an
		Amazon.com purchase. '''
	coupon_code =  re.search(re.search('payment\?code=(?P<coupon>[^>]+)', str(message))
	if coupon_code:
		return 'https://www.amazon.com/gp/css/gc/payment?code=%s' % coupon_code
	return

##############################################################################
def get_url(s):
	''' Iterate through all the matchers and return the first match for
		the code of the string order s '''
	for matcher in matchers:
		order_url = matcher(s)
		if order_url:
			return order_url