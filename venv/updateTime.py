import ntplib
from datetime import  datetime
from time import ctime

c = ntplib.NTPClient()

response = c.request('europe.pool.ntp.org', version=3)
t = datetime.fromtimestamp(response.tx_time)
print(t.minute)
print(t.hour)
print(t.second)

