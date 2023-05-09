from typing import List
import inject
from ...interfaces.Database import DatabaseInterface
from ...entities.User import User


class Database_Action:

    @inject.autoparams()
    def get_all_Users(self, data_base_interface: DatabaseInterface) -> List[User]:
        '''
            Pega todos os usuários do banco de dados, e retorna uma lista deles.
        '''
        try:
            return data_base_interface.get_all_Usersdb()
        except Exception as e:
            raise SystemError('Error search all users: '+str(e))

    @inject.autoparams()
    def getkey_DataBase(self, key: str, data_base_interface: DatabaseInterface) -> str:
        '''
            Pega uma chave do banco de dados e retorna o conteudo desta chave.
        '''
        try:
            return data_base_interface.getkey_DataBase(key)
        except Exception as e:
            raise SystemError('Error get key database: '+str(e))
        
