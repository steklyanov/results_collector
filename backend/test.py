import names
import time
import datetime

new_name = names.get_full_name()
print(type(new_name))
print(new_name)
print(int(time.time()))
data = 1601382467166482691
print(datetime.datetime.fromtimestamp(data))
