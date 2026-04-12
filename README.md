# TrakClub API

Esta API faz parte do desenvolvimento do MVP  Disciplina **Desenvolvimento Full Stack Básico**. O objetivo é centralizar informações de provedores, como personal trainers, academias e instrutores independentes, facilitando o cadastro e a visualização de aulas e serviços. A solução busca resolver a dificuldade atual de acesso a essas informações — que hoje dependem de interação presencial — oferecendo uma base digital simples e escalável, tanto para usuários quanto para provedores.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
