from escpos.printer import Network
bar = Network("192.168.0.202")

print(bar.textln("oioioioioi"))

print(bar.text("oiiiiiii/niiiiiiiiiiiiiiiiin/iiiiiiiiiiiiiiiiiiiiiiin/iiiiiiiiiiin/iiiiiiiiiiii"))
bar.cut()
bar.set()
