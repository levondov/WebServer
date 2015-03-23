from googlevoice import Voice
from googlevoice.util import input

voice = Voice()
voice.login()

phoneN = 8183193707
mess = "New Camera motion detected, check your email in a few minutes!"

voice.send_sms(phoneN,mess)
