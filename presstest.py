from escpos.printer import Network
bar = Network("192.168.0.202")

print(bar.text("oioioioioi"))
print(bar.ln())
print(bar.text("oiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"))
bar.cut()
bar.set()
