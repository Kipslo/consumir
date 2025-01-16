from escpos.printer import Network
import time
bar = Network("192.168.0.202")

print(bar.text("oioioioioi"))
print(bar.ln())
print(bar.text("oioioioi"))
print(bar.cut())

cost = [0,1,2,3,4,5,6,7,8,9]

for i in cost:
    print(i)
    time.sleep(3)