from googlevoice import Voice
from googlevoice.util import input

voice = Voice()
voice.login()

phoneN = 8183193707
phoneN2 = 8186120909
mess = "Reconnection successful, restarting motion..."

voice.send_sms(phoneN,mess)
voice.send_sms(phoneN2,mess)
