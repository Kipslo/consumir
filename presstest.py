from escpos.printer import Network
bar = Network("192.168.0.202")
bar.set(font="b", custom_size=True, width=2, height=2)
bar.text("1234567890123456789012345678901234567890")
bar.cut()
