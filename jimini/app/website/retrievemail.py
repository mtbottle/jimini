import poplib
from email import parser
import re


pop_conn = poplib.POP3_SSL('jiminico.domain.com')
pop_conn.user('cricket@jimini.co')
pop_conn.pass_('Cricket@SW2012')
# Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
# Parse message intom an email object:
messages = [parser.Parser().parsestr(mssg) for mssg in messages]

for message in messages:
    print message["to"]
    print message["from"]

    parsedLine = re.search('payment\?code=(?P<coupon>[^>]+)',str(message))
    if parsedLine:
        coupon = parsedLine.group("coupon")
        print coupon

    # we actually only need the to address and the coupon code for the next steps

    # https://www.amazon.com/gp/css/gc/payment?code=NS3KJRN3ELEJ6B
for i in range(1, len(pop_conn.list()[1]) + 1):
    pop_conn.dele(i)
    
pop_conn.quit()
