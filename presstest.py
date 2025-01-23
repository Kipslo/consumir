from escpos.printer import Network
bar = Network("192.168.0.202")

bar.image("imgs\person.png", fragment_height=50)
bar.cut()
