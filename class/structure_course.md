# Sumário do ebook - Python do básico ao avançado

01. Preparação do ambiente Python
01.1 Instalação do Python
01.2 Configuração do VS Code para Python
01.3 Extensão Python no VS Code
01.4 Debug de um Hello World
01.5 Execução de scripts pelo terminal
01.6 Organização inicial de arquivos .py

02. Como Python executa código
02.1 Interpretador Python
02.2 CPython e bytecode
02.3 Ciclo de vida de um programa Python
02.4 Script, módulo e pacote
02.5 Arquivo __init__.py
02.6 Ponto de entrada __name__ == "__main__"

03. Sintaxe essencial
03.1 Indentação e blocos
03.2 Instruções e expressões
03.3 Comentários
03.4 Docstrings
03.5 Quebra de linha
03.6 Convenções de nomes
03.7 Palavras reservadas

04. Variáveis e modelo de objetos
04.1 Nomes e referências
04.2 Tipagem dinâmica
04.3 Tipagem forte
04.4 Identidade, valor e tipo
04.5 Mutabilidade e imutabilidade
04.6 Escopo LEGB
04.7 Escopo global
04.8 Escopo nonlocal
04.9 Ciclo de vida dos objetos

05. Tipos primitivos
05.1 None
05.2 bool
05.3 int
05.4 float
05.5 complex
05.6 str
05.7 bytes
05.8 Conversão de tipos
05.9 Truthy e falsy

06. Operadores
06.1 Operadores aritméticos
06.2 Operadores de comparação
06.3 Operadores lógicos
06.4 Operadores de atribuição
06.5 Operadores de identidade
06.6 Operadores de pertencimento
06.7 Operadores bit a bit
06.8 Expressão condicional ternária
06.9 Precedência de operadores

07. Strings
07.1 Literais de string
07.2 Escape de caracteres
07.3 F-strings
07.4 Formatação de valores
07.5 Indexação de strings
07.6 Slicing de strings
07.7 Strings multilinha
07.8 Strings como objetos imutáveis

08. Estruturas de dados
08.1 list
08.2 tuple
08.3 dict
08.4 set
08.5 frozenset
08.6 Indexação de coleções
08.7 Slicing de listas
08.8 Chaves e valores em dicionários
08.9 Mutabilidade em coleções
08.10 Cópia rasa e cópia profunda

09. Desempacotamento e combinação de dados
09.1 Desempacotamento de tuplas
09.2 Desempacotamento de listas
09.3 Desempacotamento de dicionários
09.4 Operador *
09.5 Operador **
09.6 Merge de dicionários
09.7 Argumentos nomeados por dicionário

10. Comprehensions e expressões geradoras
10.1 List comprehension
10.2 Dict comprehension
10.3 Set comprehension
10.4 Generator expression
10.5 Filtros em comprehensions
10.6 Comprehensions aninhadas

11. Controle de fluxo
11.1 if
11.2 elif
11.3 else
11.4 match e case
11.5 for
11.6 while
11.7 break
11.8 continue
11.9 pass
11.10 else em loops

12. Funções
12.1 def
12.2 Parâmetros posicionais
12.3 Parâmetros nomeados
12.4 Valores padrão
12.5 Parâmetros keyword-only
12.6 Parâmetros positional-only
12.7 *args
12.8 **kwargs
12.9 return
12.10 Retorno implícito None
12.11 Funções aninhadas
12.12 Closures
12.13 Lambda
12.14 Recursão

13. Módulos, pacotes e imports
13.1 import
13.2 from import
13.3 Alias com as
13.4 Imports absolutos
13.5 Imports relativos
13.6 Imports locais
13.7 Imports circulares
13.8 Namespace de módulo
13.9 __all__

14. Exceções
14.1 try
14.2 except
14.3 except as
14.4 else em exceções
14.5 finally
14.6 raise
14.7 Repropagação de exceções
14.8 Encadeamento de exceções
14.9 Exceções customizadas
14.10 SystemExit

15. Context managers
15.1 with
15.2 as
15.3 Protocolo __enter__ e __exit__
15.4 Limpeza automática de recursos
15.5 Context managers com yield
15.6 Context managers assíncronos
15.7 async with

16. Iteráveis, iteradores e generators
16.1 Iterable
16.2 Iterator
16.3 iter
16.4 next
16.5 StopIteration
16.6 yield
16.7 yield from
16.8 Lazy evaluation
16.9 Generators infinitos

17. Decorators
17.1 Decorators de função
17.2 Decorators de classe
17.3 Decorators com parâmetros
17.4 Ordem de aplicação dos decorators
17.5 Decorators empilhados
17.6 Funções como objetos

18. Orientação a objetos
18.1 class
18.2 Objetos e instâncias
18.3 Atributos de instância
18.4 Atributos de classe
18.5 Métodos de instância
18.6 self
18.7 __init__
18.8 Encapsulamento por convenção
18.9 Herança
18.10 Composição
18.11 super
18.12 MRO
18.13 Métodos dunder
18.14 Objetos chamáveis

19. Modelagem de dados em Python
19.1 Dataclasses
19.2 field
19.3 default_factory
19.4 Defaults mutáveis
19.5 Enum
19.6 Classes abstratas
19.7 Métodos abstratos
19.8 TypedDict
19.9 Literal

20. Type hints e annotations
20.1 Anotações de variáveis
20.2 Anotações de parâmetros
20.3 Anotações de retorno
20.4 Tipos genéricos nativos
20.5 Union com |
20.6 Optional
20.7 Any
20.8 Annotated
20.9 Forward references
20.10 from __future__ import annotations
20.11 Type hints em tempo de execução
20.12 Type hints em análise estática

21. Programação assíncrona
21.1 Funções síncronas
21.2 Funções assíncronas
21.3 async def
21.4 await
21.5 Coroutine
21.6 Event loop
21.7 async for
21.8 async with
21.9 Async generators
21.10 Tratamento de exceções em código async
21.11 Cancelamento de tarefas

22. Funções built-in essenciais
22.1 print
22.2 input
22.3 len
22.4 type
22.5 isinstance
22.6 range
22.7 enumerate
22.8 zip
22.9 map
22.10 filter
22.11 sorted
22.12 sum
22.13 min e max
22.14 any e all
22.15 open

23. Arquivos e recursos
23.1 Leitura de arquivos
23.2 Escrita de arquivos
23.3 Modos de abertura
23.4 Encoding
23.5 Manipulação segura com with
23.6 Bytes e texto

24. Testes e depuração na linguagem
24.1 assert
24.2 breakpoint
24.3 Traceback
24.4 Inspeção de tipos
24.5 Erros de sintaxe
24.6 Erros de runtime

25. Tópicos avançados de Python
25.1 Descritores
25.2 property
25.3 Metaclasses
25.4 Protocolos de objetos
25.5 Data model do Python
25.6 Gerenciamento de memória
25.7 GIL
25.8 Introspection
25.9 Monkey patching
25.10 Duck typing
