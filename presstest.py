from escpos.printer import Network
bar = Network("192.168.0.202")

bar.image("imgs\person.png", )
bar.cut()
