# Sistema bancário descentralizado - PBL Redes 02

O seguinte documento possui como principal propósito, abordar acerca do projeto construído neste repositório. Tal projeto, seria uma API para sistemas bancários que funcionam cooperativamente de maneira descentralizada. Diferentemente, dos sistemas bancários atuais, que possuem um banco central para gerenciar as transações e movimentações financeiras.

## 🚀 Overview do projeto

Para o desenvolvimento deste produto, foi escolhida uma arquitetura organizacional do código, além de um algoritmo para evitar o acontecimento de conflitos e concorrência. A arquitetura utilizada foi semelhante ao MVC, utilizando Models e Controllers para separar as camadas da API. Como algoritmo para lidar com a concorrência de transações, foi usado o Token Ring.

## 📋 Pré-requisitos

Para garantir o bom funcionamento do projeto em seu ambiente, é necessário que haja algumas ferramentas instaladas:

```
Python 3.10.5
```

## 🔧 Instalação

Esta seção irá explicar como rodar este projeto em sua máquina local. 

### 📦 Como baixar projeto:

1) Baixe o projeto como ZIP em sua máquina, ou clone o repositório:

```
git clone https://github.com/PeuTrindade/PBL_BANK_BACKEND.git
```

2) Acesse pelo terminal o projeto `PBL_BANK_BACKEND`.
   
3) Execute o programa:
   
```
python3 index.py
```

## Desenvolvimento do projeto

É válido realizar uma melhor explanação a respeito do produto desenvolvido. Para a sua construção, foi utilizada a linguagem de programação Python, juntamente com a biblioteca Flask para facilitar a criação das rotas da API.

Buscando atingir um maior nível de organização e otimização, foi utilizada a arquitetura MVC, porém sem a camada visual, já que a API será testada pelo software Postman. Ela funciona da seguinte forma, os models armazenam em si as classes responsáveis pelo gerenciamento dos dados na lista de informações (simulação de um banco de dados). Ou seja, eles apenas inserem, modificam, atualizam ou excluem dados de forma direta, sem realizar validações prévias.

Os controllers, por sua vez, realizam a parte de validações e possuem em si a regra de negócio. Eles ditam como os dados devem ser processados, como devem ser recebidos e para onde vão. Além disso, retornam as mensagens de erro ou de sucesso para as rotas.

Dessa forma, o fluxo dos dados seguindo a arquitetura seria da seguinte maneira. As rotas são chamadas através do Postman, sendo enviados os dados esperados. Após isso, a rota recebe os dados e os envia para o controller responsável, então eles serão validados e processados pela regra de negócio. Caso as informações enviadas forem corretas e válidas, serão enviadas ao model responsável, e caso não estejam, será retornada uma mensagem de erro para a rota e passada ao cliente. Segue abaixo um diagrama representando esse fluxo.

![Figura 1](https://github.com/PeuTrindade/PBL_BANK_BACKEND/assets/84353169/25acd6ca-a45d-4c3c-bf04-c66bc4024811)

Por conta da descentralização dos sistemas bancários, não havendo um banco que gerencia todas as transações e movimentações, é possível que ocorra concorrências e conflitos, como por exemplo, transações sendo realizadas ao mesmo tempo. Esse fator pode gerar problemas nas contas bancárias, pois algum cliente pode ter seu dinheiro perdido em meio a tantas transações, ou outros receberem dinheiro de forma indevida. Para lidar com esse problema, foi necessária a utilização de um algoritmo.

Existem diversos algoritmos que possuem como finalidade resolver essa situação indesejada, porém, para este projeto foi escolhido o algoritmo Token Ring devido a sua simplicidade. A teoria funciona da seguinte maneira, um token deve ser enviado para um banco inicialmente, e após um tempo determinado ele será passado para o próximo banco. Existe uma fila contendo o endereço de cada banco pertencente ao sistema.

O token serve como uma permissão para que o banco possa realizar suas transações. Dessa forma, apenas o banco que possui momentaneamente o Token pode operar, e após um determinado tempo, ele deve enviar para outro. Segue abaixo um diagrama representando esse funcionamento.

![Figura 2](https://github.com/PeuTrindade/PBL_BANK_BACKEND/assets/84353169/60eec6ed-5ba9-410d-bcba-f315438dbe57)

É possível que ocorram erros durante a transmissão do Token. Como por exemplo, o banco que deve recebê-lo em seguida pode estar offline por motivos internos, logo, o banco remetente irá tentar novamente até que o envio seja bem sucedido. Foi-se considerado que um banco não cairia por completo, apenas teriam pequenas quedas de conexões, então, não seria necessário ignorar o banco destinatário.

Enquanto um banco não possui o token, as transações recebidas são armazenadas em uma lista. A partir do momento que o token é recebido, as transações são realizadas uma a uma. É válido ressaltar que se caso o tempo determinado para enviar o token acabe, ele só será enviado caso nenhuma transação esteja em andamento.

Após o entendimento do algoritmo utilizado, e como ocorre a lógica dos bancos, é necessário compreender as estruturas utilizadas para garantir o bom funcionamento do projeto. Foram utilizadas threads para garantir o funcionamento adequado em sincronia. Threads são sequências de instruções que ocorrem de forma paralela a outro processo em andamento.

Assim, existem três threads em funcionamento constante no programa. A primeira delas é a camada da API, responsável por receber as chamadas nas rotas a todo instante. As outras duas, são as threads responsáveis pelo gerenciamento do Token e da execução das transações. Com o uso desses três recursos, o sistema funciona sem bloquear nenhuma execução. Segue abaixo um diagrama contendo essa representação.

![Figura 3](https://github.com/PeuTrindade/PBL_BANK_BACKEND/assets/84353169/25e0a074-0e76-4434-9cea-46d09f9b608d)
