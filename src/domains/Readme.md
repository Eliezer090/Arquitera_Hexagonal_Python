# DOMAINS
- Nesta parte é considerado uma das partes mais importantes da Aplicação, pois é onde estão definidos os objetos que são denomidos o corração do sistema.
- Temos 3 divisões aqui:
    - actions: Dentro das actions deve ser definido toda a lógica de comunicação entre as camadas, geralmente é o que vai definir para onde e o que vai fazer dependendo da ação.
    - interfaces: Interfaces são as interfaces de comunicação entre as camadas, aqui deve conter tanto as classes com a definição da extrutura dos dados quanto os metodos abstractos que são utilizados para realizar a comunicação entre as camadas.
    - usecase: É o corração do sistema de fato, aqui são definido toda a regra de negócio, tratamentos, etc. É a parte que diz o que será feito e como será feito.
    - Entities: É a implemetação de entidades que geralmente são utilizadas no banco de dados, mas o por que fazer aqui, pois na camada de domínio é mais independente da infraestrutura(adapters) e permite que a entidade seja utilizada em diferentes contextos, sem depender de um framework específico de banco de dados. Isso pode tornar a aplicação mais flexível e modular.