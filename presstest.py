from escpos.printer import Network
bar = Network("192.168.0.202")

bar.set(custom_size=True, width=2, height=2)
print(bar.textln("oioioioioi"))

print(bar.text("oiiiiiii/niiiiiiiiiiiiiiiiin/iiiiiiiiiiiiiiiiiiiiiiin/iiiiiiiiiiin/iiiiiiiiiiii"))
bar.cut()
