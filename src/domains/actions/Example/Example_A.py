from typing import List
import inject
from ...interfaces.Example import Example_Interface


class Example_action:
    @inject.autoparams()
    def __init__(self, Example_Interface: Example_Interface):
        self.__Example_Interface = Example_Interface

    def execute(self) -> None:
        self.__Example_Interface.Example()
