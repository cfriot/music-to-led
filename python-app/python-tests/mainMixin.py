from viz.extraMethodsMixin import ExtraMethodsMixin
from viz.otherViz import OtherViz

class MainClass(ExtraMethodsMixin, OtherViz):

    def __init__(self):
        self.name = "thibaud"
        print("titi")

main = MainClass()

main.extra_1()
main.extra_2()
