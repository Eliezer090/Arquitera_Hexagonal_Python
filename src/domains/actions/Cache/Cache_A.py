
import inject
from ...interfaces import Cache_Interface


class Cache_Action:

    @inject.autoparams()
    def getkey(self, key: str, cache_interface: Cache_Interface) -> str:
        '''
            Pega o valor de uma chave do Redis
        '''
        return cache_interface.getkey(key)

    @inject.autoparams()
    def setKey(self, key: str, content: str, cache_interface: Cache_Interface) -> bool:
        '''
            Seta valor para uma chave do Redis
        '''
        return cache_interface.setKey(key, content)

    @inject.autoparams()
    def getkey_DataBase(self, key: str, cache_interface: Cache_Interface) -> str:
        '''
            Pega valor de uma chave do Redis, caso nao encontre o valor no redis pesquisa no banco de dados!
        '''
        return cache_interface.getkey_DataBase(key)
