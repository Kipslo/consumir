from escpos.printer import Network
bar = Network("192.168.0.202")

bar.text("CAMARÃO, camarão".replace("ã", "a").replace("Ã", "A"))
bar.cut()

