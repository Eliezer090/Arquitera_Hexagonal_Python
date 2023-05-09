import inject
from ....interfaces import Object_Storage_Interface


class Object_Storage_Action:

    @inject.autoparams()
    def read(self, container_name: str, object_name: str, obj_storage_interface: Object_Storage_Interface) -> str:
        '''
            Lê de um caminho(container_name) o arquivo(object_name) e retorna uma string do conteudo.
        '''
        try:
            return obj_storage_interface.read(container_name, object_name)
        except Exception as e:
            raise SystemError('Error read cloud storage: '+str(e))
 