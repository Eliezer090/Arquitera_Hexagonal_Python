from abc import ABC, abstractmethod


class Example_Interface(ABC):
    '''
        Interface para exportar documetnos utilizado para binder entre route e usecase
    '''
    @abstractmethod
    def Example(self):
        pass
