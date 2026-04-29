# Ebook Python do Básico ao Avançado

Cada capítulo do sumário foi expandido para que **cada subtopic numerado** tenha sua própria explicação, seu exemplo de código curto e seu passo a passo. O domínio dos exemplos é análise de crédito (renda, parcela, LTV, score), para manter o contexto consistente.

Formato de cada subtopic:
- **O que é:** explicação curta do conceito.
- **Exemplo:** trecho de código pronto para rodar.
- **Passo a passo:** o que acontece linha a linha.
- **Código explicado:** resumo final.

---

## 00. Conhecendo o VS Code

Antes de escrever uma linha de código, vale entender a ferramenta onde você vai passar a maior parte do tempo. Esta seção apresenta o VS Code de ponta a ponta.

### 00.1 O que é o VS Code

**O que é:** o Visual Studio Code (VS Code) é um **editor de código gratuito e de código aberto** criado pela Microsoft. Ele roda em Linux, macOS e Windows. Não é a mesma coisa que o Visual Studio (IDE pesada para C#/.NET) — o VS Code é leve, rápido e extensível.

Ele não é um IDE completo por padrão, mas com extensões se torna tão poderoso quanto um. A ideia é: você instala só o que precisa para o seu projeto.

**Principais características:**
- Suporte a centenas de linguagens (Python, JavaScript, Java, Go, Rust etc.)
- Terminal integrado (não precisa sair do editor para rodar comandos)
- Debugger embutido
- Integração nativa com Git
- Milhares de extensões disponíveis no marketplace
- Gratuito e open source

---

### 00.2 Onde o VS Code é instalado

Quando você instala o VS Code, os arquivos vão para locais diferentes dependendo do sistema operacional:

| SO | Caminho da instalação | Como instalar |
|---|---|---|
| **Linux** (Debian/Ubuntu) | `/usr/share/code/` | `sudo apt install code` ou baixe o `.deb` em code.visualstudio.com |
| **Linux** (Snap) | `/snap/code/` | `sudo snap install code --classic` |
| **macOS** | `/Applications/Visual Studio Code.app/` | Baixe o `.zip` em code.visualstudio.com e arraste para Applications |
| **Windows** | `C:\Users\<usuario>\AppData\Local\Programs\Microsoft VS Code\` (instalação por usuário) | Baixe o instalador `.exe` em code.visualstudio.com |

> **Dica:** no terminal, o comando para abrir o VS Code é `code`. Para abrir uma pasta: `code meu_projeto/`. Para abrir o diretório atual: `code .`.

---

### 00.3 Estrutura da interface — o que é cada parte

Ao abrir o VS Code, você vê estas áreas:

```
┌─────────────────────────────────────────────────────────────┐
│  Barra de Título                                            │
├──────┬──────────────────────────────────────┬───────────────┤
│      │                                      │               │
│  B   │                                      │   Barra       │
│  a   │        Área do Editor                │   Lateral     │
│  r   │      (onde o código aparece)         │   Direita     │
│  r   │                                      │  (secundária) │
│  a   │                                      │               │
│      ├──────────────────────────────────────┤               │
│  L   │                                      │               │
│  a   │        Painel Inferior               │               │
│  t   │   (Terminal, Problemas, Output)      │               │
│  e   │                                      │               │
│  r   │                                      │               │
│  a   │                                      │               │
│  l   │                                      │               │
├──────┴──────────────────────────────────────┴───────────────┤
│  Barra de Status (inferior)                                 │
└─────────────────────────────────────────────────────────────┘
```

---

#### Barra Lateral Esquerda (Activity Bar + Side Bar)

A coluna de ícones no canto esquerdo é a **Activity Bar**. Cada ícone abre uma visão diferente na **Side Bar** ao lado:

| Ícone | Nome | Atalho | O que faz |
|---|---|---|---|
| 📄 | Explorer | `Ctrl+Shift+E` (`Cmd+Shift+E` no macOS) | Navega pelos arquivos e pastas do projeto |
| 🔍 | Search | `Ctrl+Shift+F` (`Cmd+Shift+F`) | Busca texto em todos os arquivos do projeto |
| 🔀 | Source Control | `Ctrl+Shift+G` (`Cmd+Shift+G`) | Integração com Git (commits, branches, diffs) |
| 🐛 | Run and Debug | `Ctrl+Shift+D` (`Cmd+Shift+D`) | Configurar e rodar o debugger |
| 🧩 | Extensions | `Ctrl+Shift+X` (`Cmd+Shift+X`) | Instalar e gerenciar extensões |

> Você pode arrastar ícones para reordenar ou clicar com botão direito para ocultar os que não usa.

#### Barra Lateral Direita (Secondary Side Bar)

Desde a versão 1.64, o VS Code tem uma **segunda barra lateral** no lado direito. Para abrir: `View > Secondary Side Bar` ou `Ctrl+Alt+B` (`Cmd+Alt+B` no macOS).

Uso comum: mover o Explorer ou o Outline para a direita, deixando a esquerda livre para Git ou busca. Você arrasta as views entre as barras.

#### Área do Editor

A parte central onde os arquivos abertos aparecem em **abas** (tabs). Você pode:
- Dividir em colunas: `Ctrl+\` (`Cmd+\`) para ver dois arquivos lado a lado.
- Abrir uma prévia: clique simples no Explorer abre em modo preview (itálico na aba); clique duplo abre permanente.

#### Painel Inferior

Abra com `` Ctrl+` `` ou `View > Terminal`. Contém abas para:

| Aba | O que mostra |
|---|---|
| **Terminal** | Shell integrado (bash, zsh, PowerShell) — você roda comandos sem sair do editor |
| **Problems** | Erros e warnings detectados por linters e extensões |
| **Output** | Logs das extensões e do VS Code |
| **Debug Console** | Interação com o debugger durante execução |

#### Barra de Status (inferior)

A barra fina na parte de baixo mostra informações do contexto atual:

| Posição | O que mostra | Exemplo |
|---|---|---|
| Esquerda | Branch do Git atual | `main` |
| Esquerda | Erros e warnings do projeto | `0 ⚠ 2 ✕` |
| Direita | Linha e coluna do cursor | `Ln 42, Col 8` |
| Direita | Encoding do arquivo | `UTF-8` |
| Direita | Tipo de fim de linha | `LF` (Linux/macOS) ou `CRLF` (Windows) |
| Direita | Linguagem detectada | `Python` |
| Direita | **Interpretador Python** selecionado | `Python 3.12.0 ('.venv')` |

> **Dica:** clique em qualquer item da barra de status para alterar. Clique no nome da linguagem para trocar, clique no interpretador Python para selecionar outro.

---

### 00.4 Paleta de Comandos — o controle central

**O que é:** a paleta de comandos é o **atalho mais importante** do VS Code. Ela dá acesso a praticamente qualquer ação sem precisar navegar por menus.

**Atalho:** `Ctrl+Shift+P` (Linux/Windows) ou `Cmd+Shift+P` (macOS).

Ao abrir, aparece um campo de texto com `>` no início. Você digita palavras-chave e o VS Code filtra os comandos disponíveis:

```
> Python: Select Interpreter
> Preferences: Open User Settings (JSON)
> Git: Clone
> View: Toggle Terminal
> File: New File
```

**Variações da paleta:**

| Atalho | Prefixo | O que faz |
|---|---|---|
| `Ctrl+Shift+P` / `Cmd+Shift+P` | `>` | Busca **comandos** |
| `Ctrl+P` / `Cmd+P` | (nenhum) | Busca **arquivos** pelo nome — muito mais rápido que navegar no Explorer |
| `Ctrl+P` depois `@` | `@` | Busca **símbolos** (funções, classes) no arquivo atual |
| `Ctrl+P` depois `#` | `#` | Busca **símbolos** no workspace inteiro |
| `Ctrl+P` depois `:` | `:` | Vai para uma **linha** específica |

**Exemplo prático:**
1. Pressione `Ctrl+Shift+P`.
2. Digite `terminal`.
3. Selecione `View: Toggle Terminal` para abrir/fechar o terminal integrado.

> **Dica:** você não precisa decorar menus. Se quer fazer algo no VS Code, abra a paleta e descreva o que quer. É a forma mais rápida de fazer qualquer coisa.

---

### 00.5 Workspace — o conceito de área de trabalho

**O que é:** quando você abre uma pasta no VS Code com `File > Open Folder`, essa pasta vira o **workspace**. Tudo que o VS Code faz (busca, Git, terminal, configurações) é relativo a essa pasta.

**Tipos de workspace:**

| Tipo | Como abrir | Quando usar |
|---|---|---|
| **Pasta única** | `File > Open Folder` | O mais comum — um projeto por janela |
| **Multi-root** | `File > Add Folder to Workspace` | Vários projetos na mesma janela (frontend + backend, por exemplo) |
| **Arquivo .code-workspace** | `File > Open Workspace from File` | Salva a configuração multi-root em um arquivo para reabrir depois |

**Pasta `.vscode/` dentro do workspace:**

Quando você cria configurações específicas do projeto, elas ficam em `.vscode/`:

```
meu_projeto/                    ← workspace (pasta aberta no VS Code)
├── .vscode/
│   ├── settings.json           ← configurações do projeto
│   ├── launch.json             ← configurações de debug
│   ├── tasks.json              ← tarefas automatizadas (build, test)
│   └── extensions.json         ← extensões recomendadas para o time
├── app/
│   └── main.py
└── tests/
    └── test_main.py
```

> A pasta `.vscode/` costuma ser **versionada no Git** para que todos do time usem as mesmas configurações. Já dados pessoais (como o caminho absoluto da sua máquina) devem usar variáveis como `${workspaceFolder}`.

---

### 00.6 Onde ficam os arquivos de configuração do VS Code

O VS Code separa configurações em dois níveis: **globais** (do usuário) e **de workspace** (do projeto).

#### Configurações globais (User Settings)

São as preferências pessoais que valem para **todos** os projetos. O arquivo fica em:

| SO | Caminho |
|---|---|
| **Linux** | `~/.config/Code/User/settings.json` |
| **macOS** | `~/Library/Application Support/Code/User/settings.json` |
| **Windows** | `%APPDATA%\Code\User\settings.json` |

Para abrir: `Ctrl+Shift+P` → `Preferences: Open User Settings (JSON)`.

#### Configurações de workspace

Ficam em `<projeto>/.vscode/settings.json` e sobrescrevem as globais para aquele projeto.

Para abrir: `Ctrl+Shift+P` → `Preferences: Open Workspace Settings (JSON)`.

#### Outros arquivos de configuração importantes

| Arquivo | Onde fica | O que configura |
|---|---|---|
| `settings.json` (global) | Pasta do usuário (veja acima) | Tema, fonte, atalhos, comportamento geral |
| `settings.json` (workspace) | `.vscode/settings.json` | Interpretador Python, formatador, linter do projeto |
| `keybindings.json` | Pasta do usuário | Atalhos de teclado personalizados |
| `launch.json` | `.vscode/launch.json` | Configurações do debugger |
| `tasks.json` | `.vscode/tasks.json` | Tarefas de build, test, lint |
| `extensions.json` | `.vscode/extensions.json` | Lista de extensões recomendadas para o projeto |

> **Dica:** todas as configurações do VS Code são arquivos JSON editáveis. Você pode abrir e editar manualmente ou usar a interface gráfica (`Ctrl+,` / `Cmd+,`).

---

### 00.7 Menus principais

A barra de menus no topo dá acesso a funcionalidades agrupadas:

| Menu | Itens principais |
|---|---|
| **File** | Abrir pasta/arquivo, Salvar, Fechar, Preferências |
| **Edit** | Desfazer, Refazer, Buscar e Substituir (`Ctrl+H` / `Cmd+H`) |
| **Selection** | Selecionar tudo, selecionar linha, multicursor |
| **View** | Abrir/fechar terminal, painéis, barras laterais, paleta de comandos |
| **Go** | Ir para arquivo, linha, símbolo, definição, referências |
| **Run** | Iniciar debug, parar, breakpoints |
| **Terminal** | Novo terminal, dividir, selecionar shell padrão |
| **Help** | Documentação, atalhos de teclado, verificar atualizações |

> **No Linux**, se a barra de menus não aparece, pressione `Alt` para exibi-la. Você pode fixá-la em `View > Appearance > Menu Bar > classic`.

---

### 00.8 Extensões — adicionando funcionalidades

**O que é:** extensões são plugins que adicionam suporte a linguagens, ferramentas, temas e funcionalidades ao VS Code. O marketplace tem mais de 40 mil extensões.

**Como instalar:**
1. Clique no ícone de extensões na barra lateral (`Ctrl+Shift+X` / `Cmd+Shift+X`).
2. Digite o nome da extensão no campo de busca.
3. Clique em **Install**.

**Extensões essenciais para Python:**

| Extensão | Autor | O que faz |
|---|---|---|
| **Python** | Microsoft | IntelliSense, linting, debug, formatação, Jupyter |
| **Pylance** | Microsoft | Servidor de linguagem rápido (type checking, autocomplete avançado) |
| **Python Debugger** | Microsoft | Debugger baseado em debugpy |
| **Ruff** | Astral Software | Linter e formatador ultrarrápido (substitui Flake8, Black, isort) |
| **Jupyter** | Microsoft | Suporte a notebooks `.ipynb` dentro do VS Code |

**Extensões recomendadas para o time:**

Crie `.vscode/extensions.json` para que o VS Code sugira as extensões quando alguém abrir o projeto:

```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "charliermarsh.ruff"
    ]
}
```

Quando um colega abrir o projeto, o VS Code mostra uma notificação: *"This workspace has extension recommendations. Would you like to install them?"*.

---

### 00.9 Configuração de interpretador de linguagens

**O que é:** o VS Code precisa saber **qual programa usar** para entender, executar e debugar o código da linguagem que você está escrevendo. Cada linguagem tem seu próprio interpretador ou compilador.

**Para Python**, o interpretador é definido em:
- `Ctrl+Shift+P` → `Python: Select Interpreter`
- Ou via `settings.json` com `python.defaultInterpreterPath`

**Para outras linguagens**, a extensão correspondente cuida da configuração:

| Linguagem | Extensão | O que configurar |
|---|---|---|
| Python | Python (Microsoft) | `python.defaultInterpreterPath` |
| JavaScript/TypeScript | Embutido no VS Code | Node.js no PATH é suficiente |
| Java | Extension Pack for Java | Caminho do JDK |
| Go | Go (Google) | Caminho do `go` binary |
| Rust | rust-analyzer | Cargo e Rust toolchain no PATH |

O VS Code mostra o interpretador/runtime selecionado na **barra de status** (canto inferior direito). Se aparecer algo errado, clique ali para trocar.

---

### 00.10 Integração com Git

**O que é:** o VS Code tem suporte nativo a Git, sem precisar de extensão extra. A aba **Source Control** (`Ctrl+Shift+G` / `Cmd+Shift+G`) mostra o estado dos arquivos e permite fazer operações sem sair do editor.

**Funcionalidades integradas:**

| Ação | Como fazer no VS Code |
|---|---|
| Ver arquivos modificados | Aba Source Control — lista de Changes |
| Ver diff de um arquivo | Clique no arquivo na lista de Changes |
| Stage (adicionar ao commit) | Clique no `+` ao lado do arquivo |
| Commit | Digite a mensagem no campo de texto e clique no ✓ |
| Push / Pull | Botão de sync na barra de status, ou paleta: `Git: Push` |
| Trocar de branch | Clique no nome da branch na barra de status (canto inferior esquerdo) |
| Resolver conflitos | O VS Code mostra editor de merge com "Accept Current/Incoming/Both" |

**Indicadores visuais no editor:**

- Linha verde na margem = linha adicionada
- Linha azul = linha modificada
- Linha vermelha (triângulo) = linha removida

**Extensão recomendada:** **GitLens** (GitKraken) — mostra quem alterou cada linha, histórico de commits inline e gráfico de branches.

> O VS Code usa o Git instalado no sistema. Verifique com `git --version` no terminal. Se não tiver, instale:
> - **Linux:** `sudo apt install git`
> - **macOS:** `xcode-select --install` ou `brew install git`
> - **Windows:** Baixe em git-scm.com

---

### 00.11 Perfil de usuário e sincronização de conta

**O que é:** o VS Code permite criar **perfis** (conjuntos de configurações, extensões e atalhos) e **sincronizar** tudo via conta Microsoft ou GitHub.

#### Perfis (Profiles)

Cada perfil salva: settings, atalhos, extensões, snippets e estado da UI. Útil quando você trabalha com várias linguagens e quer ambientes diferentes.

**Como criar:**
1. `Ctrl+Shift+P` → `Profiles: Create Profile`.
2. Dê um nome (ex.: "Python Dev").
3. Escolha o que incluir (settings, extensões etc.).

**Como trocar:**
- `Ctrl+Shift+P` → `Profiles: Switch Profile`.
- Ou clique no ícone de engrenagem (canto inferior esquerdo) → `Profiles`.

#### Sincronização (Settings Sync)

Sincroniza suas configurações entre máquinas diferentes (ex.: notebook pessoal e computador do trabalho).

**Como ativar:**
1. Clique no ícone de engrenagem (canto inferior esquerdo) → `Turn on Settings Sync...`.
2. Escolha o que sincronizar: Settings, Atalhos, Extensões, Perfis, Snippets.
3. Faça login com conta **Microsoft** ou **GitHub**.

A partir daí, qualquer mudança de configuração é automaticamente propagada para todas as máquinas logadas na mesma conta.

> **Importante:** a sincronização é da sua conta pessoal. As configurações de workspace (`.vscode/settings.json`) continuam sendo por projeto e versionadas no Git.

---

### 00.12 MCP (Model Context Protocol) no VS Code

**O que é:** MCP é um protocolo aberto que permite conectar o VS Code (via GitHub Copilot) a **ferramentas e fontes de dados externas** — bancos de dados, APIs, documentação, serviços da nuvem etc.

Com MCP, o assistente de IA (Copilot Chat) pode:
- Consultar um banco de dados do projeto e usar os resultados nas respostas.
- Acessar documentação interna da empresa.
- Executar ações em serviços externos (criar issue, consultar API, deploy).

**Como configurar um servidor MCP:**

Os servidores MCP são configurados no `settings.json`:

```json
// .vscode/settings.json (workspace) ou settings.json (global)
{
    "mcp": {
        "servers": {
            "meu-servidor": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/caminho/pasta"]
            }
        }
    }
}
```

**Servidores MCP populares:**

| Servidor | O que faz |
|---|---|
| `server-filesystem` | Acessa arquivos e pastas |
| `server-postgres` | Consulta bancos PostgreSQL |
| `server-github` | Interage com repositórios, issues e PRs |
| `server-fetch` | Busca conteúdo de URLs |

> MCP é recurso avançado e requer o GitHub Copilot ativo. Para o curso básico de Python, você não precisa configurar MCP — mas é bom saber que existe para quando o projeto crescer.

---

### 00.13 Atalhos de teclado essenciais — referência rápida

| Ação | Linux / Windows | macOS |
|---|---|---|
| Paleta de comandos | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Buscar arquivo pelo nome | `Ctrl+P` | `Cmd+P` |
| Buscar texto no projeto | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Abrir/fechar terminal | `` Ctrl+` `` | `` Cmd+` `` |
| Salvar arquivo | `Ctrl+S` | `Cmd+S` |
| Desfazer | `Ctrl+Z` | `Cmd+Z` |
| Comentar/descomentar linha | `Ctrl+/` | `Cmd+/` |
| Mover linha para cima/baixo | `Alt+↑` / `Alt+↓` | `Option+↑` / `Option+↓` |
| Duplicar linha | `Shift+Alt+↓` | `Shift+Option+↓` |
| Selecionar palavra igual (multicursor) | `Ctrl+D` | `Cmd+D` |
| Dividir editor | `Ctrl+\` | `Cmd+\` |
| Fechar aba | `Ctrl+W` | `Cmd+W` |
| Iniciar debug | `F5` | `F5` |
| Selecionar interpretador Python | `Ctrl+Shift+P` → digitar "interpreter" | `Cmd+Shift+P` → digitar "interpreter" |

> **Dica:** para ver e customizar todos os atalhos: `Ctrl+K Ctrl+S` (Linux/Windows) ou `Cmd+K Cmd+S` (macOS).

---

### 00.14 Temas e aparência

**O que é:** o VS Code permite trocar o esquema de cores (tema), o conjunto de ícones e o tamanho da fonte para deixar o editor confortável para os seus olhos.

#### Trocar o tema de cores

1. Pressione `Ctrl+K Ctrl+T` (Linux/Windows) ou `Cmd+K Cmd+T` (macOS).
2. Navegue pela lista com as setas — o preview é aplicado em tempo real.
3. Pressione `Enter` para confirmar.

**Temas populares:**

| Tema | Estilo | Já vem instalado? |
|---|---|---|
| Dark+ | Escuro (padrão do VS Code) | Sim |
| Light+ | Claro (padrão) | Sim |
| One Dark Pro | Escuro inspirado no Atom | Não — instalar via extensão |
| Dracula | Escuro com roxo/rosa | Não — instalar via extensão |
| GitHub Theme | Claro/escuro no estilo GitHub | Não — instalar via extensão |
| Catppuccin | Paleta pastel suave | Não — instalar via extensão |

#### Trocar o tema de ícones

Os ícones que aparecem ao lado dos nomes de arquivo no Explorer podem ser trocados:

1. `Ctrl+Shift+P` → `Preferences: File Icon Theme`.
2. Escolha entre os instalados ou instale via extensão.

**Tema de ícones popular:** **Material Icon Theme** — mostra ícones coloridos diferentes para `.py`, `.json`, `.md`, pastas `tests/`, etc.

#### Tamanho da fonte

No `settings.json` (global ou workspace):

```json
{
    "editor.fontSize": 16,
    "editor.fontFamily": "'JetBrains Mono', 'Fira Code', monospace",
    "editor.fontLigatures": true,
    "terminal.integrated.fontSize": 14
}
```

| Configuração | O que faz |
|---|---|
| `editor.fontSize` | Tamanho da fonte no editor de código |
| `editor.fontFamily` | Família da fonte (entre aspas se tiver espaço no nome) |
| `editor.fontLigatures` | Habilita ligaduras (ex.: `!=` vira `≠` em fontes como Fira Code) |
| `terminal.integrated.fontSize` | Tamanho da fonte no terminal integrado |

> **Dica rápida:** para aumentar/diminuir a fonte de tudo (editor + interface): `Ctrl+=` / `Ctrl+-` (Linux/Windows) ou `Cmd+=` / `Cmd+-` (macOS).

---

### 00.15 Snippets — templates de código

**O que é:** snippets são **atalhos de texto** que expandem em blocos de código completos quando você pressiona `Tab`. Economizam digitação para padrões repetitivos.

#### Snippets embutidos

A extensão Python já traz snippets prontos. No editor, digite o prefixo e pressione `Tab`:

| Prefixo | Expande para |
|---|---|
| `def` | Esqueleto de função com docstring |
| `class` | Esqueleto de classe com `__init__` |
| `if` | Bloco `if` |
| `for` | Loop `for ... in ...` |
| `try` | Bloco `try/except` |
| `main` | Bloco `if __name__ == "__main__":` |

#### Criando seus próprios snippets

1. `Ctrl+Shift+P` → `Snippets: Configure Snippets`.
2. Selecione `python.json` (snippets globais para Python).
3. Adicione o snippet:

```json
// Snippets globais:
// Linux: ~/.config/Code/User/snippets/python.json
// macOS: ~/Library/Application Support/Code/User/snippets/python.json
// Windows: %APPDATA%\Code\User\snippets\python.json
{
    "Função de cálculo": {
        "prefix": "calc",
        "body": [
            "def ${1:nome_funcao}(${2:params}):",
            "    \"\"\"${3:Descrição.}\"\"\"",
            "    ${0:pass}"
        ],
        "description": "Cria função com docstring"
    }
}
```

**Como funciona:**
- `prefix` — o que você digita para acionar o snippet.
- `body` — o código gerado. `${1:texto}` são **tab stops**: posições onde o cursor para, permitindo preencher cada campo com `Tab`.
- `${0:pass}` — posição final do cursor.

Após salvar, digite `calc` em qualquer arquivo `.py`, pressione `Tab`, e o esqueleto aparece com o cursor posicionado no nome da função.

---

### 00.16 IntelliSense e Autocomplete

**O que é:** IntelliSense é o nome que o VS Code dá ao sistema de **autocomplete inteligente**. Ele sugere nomes de variáveis, funções, métodos, classes e parâmetros enquanto você digita.

#### Como funciona

Quando você digita, o VS Code analisa o código e abre um menu suspenso com sugestões. Você pode:
- Navegar com `↑` / `↓`.
- Aceitar com `Tab` ou `Enter`.
- Forçar a abertura com `Ctrl+Space` (`Cmd+Space` no macOS) se não aparecer sozinho.

#### IntelliSense básico vs Pylance

| Recurso | IntelliSense básico | Com Pylance |
|---|---|---|
| Autocomplete de nomes locais | Sim | Sim |
| Autocomplete de métodos de objetos | Parcial | Completo, com tipo inferido |
| Verificação de tipos em tempo real | Não | Sim — mostra erros antes de rodar |
| Autocomplete de imports | Básico | Sugere import automático |
| Documentação inline (hover) | Nome e assinatura | Docstring completa, tipo de retorno |
| Rename Symbol (`F2`) | Renomeia no arquivo | Renomeia em todo o projeto |
| Go to Definition (`F12`) | Funciona para imports locais | Funciona inclusive para bibliotecas |

> **Recomendação:** instale sempre a extensão **Pylance** (Microsoft) junto com a extensão Python. A diferença de qualidade é enorme.

#### Configuração no settings.json

```json
{
    "python.languageServer": "Pylance",
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "editor.quickSuggestions": {
        "other": true,
        "comments": false,
        "strings": false
    }
}
```

| Configuração | O que faz |
|---|---|
| `python.languageServer` | Define o servidor de linguagem (`"Pylance"`, `"Jedi"` ou `"None"`) |
| `python.analysis.typeCheckingMode` | Nível de verificação de tipos: `"off"`, `"basic"` ou `"strict"` |
| `python.analysis.autoImportCompletions` | Se `true`, sugere imports automaticamente ao digitar um nome não importado |
| `editor.quickSuggestions` | Controla quando o autocomplete aparece automaticamente |

---

### 00.17 Auto Save — salvamento automático

**O que é:** o VS Code pode salvar seus arquivos automaticamente, sem precisar de `Ctrl+S`. Isso evita perder trabalho e mantém o código sempre atualizado para ferramentas como linters.

**Como ativar:** `File > Auto Save` (clique para alternar) ou configure no `settings.json`:

```json
{
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000
}
```

| Valor de `files.autoSave` | Comportamento |
|---|---|
| `"off"` | Desligado — só salva com `Ctrl+S` / `Cmd+S` (padrão) |
| `"afterDelay"` | Salva automaticamente após X milissegundos (definido em `autoSaveDelay`) |
| `"onFocusChange"` | Salva quando você muda para outro arquivo ou outra janela |
| `"onWindowChange"` | Salva quando você muda para outro aplicativo |

> **Dica para Python:** `"afterDelay"` com `1000` ms (1 segundo) funciona bem. Assim o linter (Ruff ou Pylance) roda automaticamente a cada salvamento, mostrando erros em tempo real.

---

### 00.18 Multicursor — editar várias linhas ao mesmo tempo

**O que é:** multicursor permite colocar **vários cursores** no editor e digitar em todos os pontos simultaneamente. É extremamente útil para edições repetitivas.

**Formas de criar múltiplos cursores:**

| Ação | Linux / Windows | macOS |
|---|---|---|
| Adicionar cursor acima/abaixo | `Ctrl+Alt+↑` / `Ctrl+Alt+↓` | `Cmd+Option+↑` / `Cmd+Option+↓` |
| Adicionar cursor em ponto específico | `Alt+Clique` no local desejado | `Option+Clique` |
| Selecionar próxima ocorrência igual | `Ctrl+D` | `Cmd+D` |
| Selecionar **todas** as ocorrências iguais | `Ctrl+Shift+L` | `Cmd+Shift+L` |
| Selecionar todas as linhas selecionadas | `Shift+Alt+I` | `Shift+Option+I` (cursor no fim de cada linha) |

**Exemplo prático:** você tem uma lista de variáveis e quer trocar todas de `valor_` para `montante_`:
1. Selecione `valor_` na primeira ocorrência.
2. Pressione `Ctrl+D` repetidamente para selecionar cada próxima ocorrência.
3. Digite `montante_` — todas são substituídas ao mesmo tempo.

> Para sair do multicursor e voltar ao cursor único, pressione `Esc`.

---

### 00.19 Minimap, Breadcrumbs e Outline

**O que é:** três recursos de navegação visual que ajudam a se orientar em arquivos grandes.

#### Minimap

A faixa fina no **canto direito do editor** mostra uma visão miniatura do arquivo inteiro. Você pode:
- Clicar nela para pular para uma parte do código.
- Arrastar para navegar rapidamente.

Para ativar/desativar: `settings.json` → `"editor.minimap.enabled": true` ou `false`.

#### Breadcrumbs

A barra logo **acima do editor** que mostra o caminho do arquivo e a posição atual no código:

```
app/ > services/ > credito.py > class SimulacaoCredito > def calcular_parcela
```

Clique em qualquer parte do breadcrumb para navegar rapidamente. Para ativar: `View > Breadcrumbs` ou `"breadcrumbs.enabled": true` no settings.

#### Outline

A view **Outline** aparece na barra lateral (Explorer) e lista todas as funções, classes e variáveis do arquivo atual em formato de árvore. Clique em qualquer item para ir direto até ele.

Para abrir: na barra lateral do Explorer, expanda a seção **OUTLINE** (na parte inferior).

> **Dica:** a Outline é especialmente útil em arquivos Python grandes — em vez de rolar procurando uma função, clique no nome dela.

---

### 00.20 Zen Mode — foco total

**O que é:** modo que esconde todas as barras, painéis e distrações, deixando só o código na tela.

| Ação | Linux / Windows | macOS |
|---|---|---|
| Entrar no Zen Mode | `Ctrl+K Z` | `Cmd+K Z` |
| Sair do Zen Mode | `Esc Esc` (pressione Esc duas vezes) | `Esc Esc` |

O Zen Mode:
- Esconde a barra lateral, barra de status, painel inferior e abas.
- Centraliza o editor na tela.
- Fica em tela cheia.

Útil quando você precisa se concentrar em um trecho de código sem distrações.

---

### 00.21 Remote Development — desenvolvimento remoto

**O que é:** o VS Code permite editar código que está em **outra máquina**, dentro de um **container Docker** ou no **WSL** (Windows Subsystem for Linux), como se fosse local.

**Extensões necessárias:**

| Extensão | Cenário |
|---|---|
| **Remote - SSH** | Editar código em um servidor remoto via SSH |
| **Dev Containers** | Editar código dentro de um container Docker |
| **WSL** | Editar código no Linux rodando dentro do Windows |
| **Remote - Tunnels** | Conectar a qualquer máquina via túnel (sem SSH configurado) |

> **Dica:** instale o pacote **Remote Development** (Microsoft) que inclui todas de uma vez.

#### Como conectar via SSH

1. Instale a extensão **Remote - SSH**.
2. `Ctrl+Shift+P` → `Remote-SSH: Connect to Host`.
3. Digite `usuario@ip-do-servidor` (ex.: `madson@192.168.1.100`).
4. O VS Code abre uma nova janela conectada ao servidor — o terminal, o Explorer e o IntelliSense rodam todos no servidor.

#### Como usar no WSL (Windows)

1. Instale o WSL no Windows: `wsl --install` no PowerShell como administrador.
2. Instale a extensão **WSL**.
3. `Ctrl+Shift+P` → `WSL: Connect to WSL`.
4. O VS Code reabre dentro do ambiente Linux. Agora `python3`, `pip`, caminhos Linux — tudo funciona.

> **Quando usar:** se você está no Windows mas quer um ambiente Linux para rodar Python, o WSL é a melhor opção. O VS Code no WSL é praticamente idêntico ao VS Code nativo no Linux.

#### Como usar com Dev Containers

1. Instale Docker Desktop (Linux/macOS/Windows).
2. Instale a extensão **Dev Containers**.
3. Crie um arquivo `.devcontainer/devcontainer.json` na raiz do projeto:

```json
// .devcontainer/devcontainer.json
{
    "name": "Python 3.12",
    "image": "mcr.microsoft.com/devcontainers/python:3.12",
    "postCreateCommand": "pip install -r requirements.txt",
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance"
            ]
        }
    }
}
```

4. `Ctrl+Shift+P` → `Dev Containers: Reopen in Container`.
5. O VS Code reabre dentro do container com Python 3.12 e todas as dependências instaladas.

> **Vantagem:** todo o time roda exatamente o mesmo ambiente, independente do SO de cada um.

---

### 00.22 GitHub Copilot — assistente de IA no editor

**O que é:** o GitHub Copilot é um assistente de IA integrado ao VS Code que sugere código, responde perguntas e ajuda a resolver problemas diretamente no editor.

**Funcionalidades principais:**

| Recurso | O que faz | Como usar |
|---|---|---|
| **Autocomplete inline** | Sugere código enquanto você digita (texto fantasma em cinza) | Aceite com `Tab`, rejeite com `Esc` |
| **Copilot Chat** | Chat com IA na barra lateral | `Ctrl+Alt+I` (Linux/Win) / `Cmd+Alt+I` (macOS) |
| **Inline Chat** | Chat dentro do editor, no ponto do código | `Ctrl+I` / `Cmd+I` |
| **Explain** | Explica um trecho de código selecionado | Selecione o código → Copilot Chat → `/explain` |
| **Fix** | Sugere correção para erros | Selecione o erro → Copilot Chat → `/fix` |
| **Tests** | Gera testes para o código selecionado | Selecione o código → Copilot Chat → `/tests` |

**Como instalar:**
1. `Ctrl+Shift+X` → busque `GitHub Copilot`.
2. Instale a extensão **GitHub Copilot** (GitHub).
3. Faça login com sua conta GitHub (requer assinatura Copilot ou acesso gratuito via Copilot Free).

**Agentes no Copilot Chat:**

No chat, você pode direcionar perguntas para agentes especializados:

| Agente | O que faz |
|---|---|
| `@workspace` | Analisa o projeto inteiro para responder |
| `@terminal` | Ajuda com comandos de terminal |
| `@vscode` | Ajuda com configurações do VS Code |

> **Exemplo:** no Copilot Chat, digite `@workspace como rodar os testes deste projeto?` e ele analisa a estrutura do projeto para responder.

> **Nota:** o Copilot é uma ferramenta de auxílio — sempre revise o código gerado. Ele pode sugerir código incorreto ou desatualizado.

---

### 00.23 Extensões para programar em Python no VS Code

**O que é:** o VS Code "cru" não sabe quase nada sobre Python. Quem dá inteligência a ele são as **extensões**. Esta seção lista as extensões mais importantes, organizadas por categoria, explicando para que serve cada uma.

Para instalar qualquer extensão: `Ctrl+Shift+X` (`Cmd+Shift+X` no macOS), digite o nome e clique em **Install**.

---

#### Essenciais — instale antes de tudo

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **Python** | Microsoft | `ms-python.python` | Extensão principal. Sem ela o VS Code não reconhece Python. Traz: seleção de interpretador, execução de scripts (botão ▶), gerenciamento de ambientes virtuais, integração com linters e formatadores, e suporte a Jupyter. |
| **Pylance** | Microsoft | `ms-python.vscode-pylance` | Servidor de linguagem que substitui o Jedi. Oferece autocomplete rápido, inferência de tipos, verificação de tipos em tempo real, auto-import, Go to Definition (`F12`), Rename Symbol (`F2`) e documentação inline ao passar o mouse. É o que faz o IntelliSense funcionar de verdade. |
| **Python Debugger** | Microsoft | `ms-python.debugpy` | Debugger baseado em `debugpy`. Permite breakpoints, inspeção de variáveis, step into/over/out, watch expressions e debug de scripts, testes e aplicações web. Instalado automaticamente com a extensão Python, mas pode ser atualizado separadamente. |

> **Na prática:** instale **Python** e **Pylance** — as duas juntas transformam o VS Code em uma IDE Python completa.

---

#### Linting e Formatação — manter o código limpo

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **Ruff** | Astral Software | `charliermarsh.ruff` | Linter + formatador escrito em Rust, extremamente rápido. Substitui Flake8, Black, isort, pycodestyle e muitos outros em uma única ferramenta. Verifica erros de estilo, imports não usados, complexidade ciclomática e formata o código ao salvar. É o padrão moderno. |
| **Black Formatter** | Microsoft | `ms-python.black-formatter` | Formatador opinado — reformata o código automaticamente seguindo um estilo fixo (sem opções de customização). Se você usa Ruff, não precisa do Black (Ruff já faz o mesmo). |
| **isort** | Microsoft | `ms-python.isort` | Organiza automaticamente a ordem dos `import` no topo do arquivo, agrupando stdlib, terceiros e locais. Se você usa Ruff, não precisa (Ruff já organiza imports). |
| **Flake8** | Microsoft | `ms-python.flake8` | Linter clássico que verifica erros de estilo (PEP 8), erros lógicos e complexidade. Muito usado em projetos legados. Para projetos novos, prefira Ruff. |
| **Pylint** | Microsoft | `ms-python.pylint` | Linter mais rigoroso e opinado que o Flake8. Verifica estilo, erros, convenções e até dá notas para o código. Mais lento, mas mais detalhado. |
| **autopep8** | Microsoft | `ms-python.autopep8` | Formatador que corrige apenas violações PEP 8 (menos agressivo que Black). Útil em projetos que não querem reformatação total. |

**Como configurar o Ruff para formatar ao salvar:**

```json
// .vscode/settings.json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports.ruff": "explicit"
        }
    }
}
```

> **Recomendação para iniciantes:** instale **Ruff** e configure `formatOnSave`. Ele cuida de tudo sozinho — estilo, imports e erros comuns.

---

#### Testes — rodar e visualizar testes

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **Python Test Explorer** | (integrado na extensão Python) | — | A extensão Python já traz suporte a `pytest` e `unittest`. Mostra os testes na aba Testing (ícone de tubo de ensaio na Activity Bar), permite rodar testes individuais, ver resultados com ✓/✕ e debugar testes com breakpoints. |
| **Python Test Adapter** | LittleFoxTeam | `littlefoxteam.vscode-python-test-adapter` | Alternativa que usa o Test Explorer UI, com mais opções de visualização em árvore. Útil se a integração nativa não atender. |

**Como ativar pytest no VS Code:**

```json
// .vscode/settings.json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": ["tests/"]
}
```

Depois, clique no ícone de **Testing** (tubo de ensaio) na Activity Bar para ver todos os testes detectados.

---

#### Jupyter e Ciência de Dados

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **Jupyter** | Microsoft | `ms-toolsai.jupyter` | Abre e edita notebooks `.ipynb` diretamente no VS Code. Permite rodar células, ver gráficos, usar markdown e exportar. Não precisa de `jupyter notebook` no navegador. |
| **Jupyter Keymap** | Microsoft | `ms-toolsai.jupyter-keymap` | Adiciona atalhos de teclado do Jupyter clássico (ex.: `Shift+Enter` para rodar célula). Instalada junto com Jupyter. |
| **Jupyter Renderers** | Microsoft | `ms-toolsai.jupyter-renderers` | Renderiza outputs ricos (gráficos, HTML, LaTeX) dentro das células do notebook. |
| **Data Wrangler** | Microsoft | `ms-toolsai.datawrangler` | Interface visual para explorar e transformar DataFrames pandas sem escrever código. Ótimo para análise exploratória. |

---

#### Ambiente e Dependências

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **Python Environment Manager** | Don Jayamanne | `donjayamanne.python-environment-manager` | Interface visual para gerenciar ambientes virtuais (venv, conda, pyenv, poetry). Mostra todos os ambientes detectados, permite criar, deletar e trocar. |
| **pip-updater** | Various | — | Verifica pacotes desatualizados no `requirements.txt` e oferece atualização com um clique. |

---

#### Docker e Containers

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **Docker** | Microsoft | `ms-azuretools.vscode-docker` | Gerencia containers, images, volumes e redes Docker direto no VS Code. Mostra containers rodando, permite parar/iniciar, ver logs e abrir terminal dentro do container. Também dá IntelliSense para `Dockerfile` e `docker-compose.yml`. |
| **Dev Containers** | Microsoft | `ms-vscode-remote.remote-containers` | Permite abrir o VS Code **dentro** de um container Docker, com todo o ambiente (Python, pacotes, extensões) isolado. Já mencionado na seção 00.21. |

---

#### Banco de Dados

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **SQLite Viewer** | Florian Klampfer | `qwtel.sqlite-viewer` | Abre arquivos `.sqlite3` e `.db` diretamente no VS Code em formato de tabela. Útil para inspecionar bancos SQLite sem ferramenta externa. |
| **PostgreSQL** | Chris Kolkman | `ckolkman.vscode-postgres` | Conecta a bancos PostgreSQL, permite rodar queries, ver tabelas e resultados no VS Code. |
| **Database Client** | Weijan Chen | `cweijan.vscode-database-client2` | Cliente universal que suporta MySQL, PostgreSQL, SQLite, MongoDB, Redis e outros. Interface visual para queries e navegação de tabelas. |

---

#### Git e Colaboração

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **GitLens** | GitKraken | `eamodio.gitlens` | Mostra quem alterou cada linha (blame), histórico de commits inline, comparação de branches, gráfico de histórico e muito mais. Essencial para trabalhar em equipe. |
| **GitHub Pull Requests** | GitHub | `github.vscode-pull-request-github` | Cria, revisa e faz merge de Pull Requests direto no VS Code, sem precisar abrir o navegador. |
| **Git Graph** | mhutchie | `mhutchie.git-graph` | Mostra o histórico de commits em formato gráfico visual (árvore de branches). |

---

#### Produtividade Geral

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **Error Lens** | Alexander | `usernamehw.errorlens` | Mostra mensagens de erro e warning **na mesma linha** do código, em vez de só no painel Problems. Você vê o problema imediatamente, sem precisar passar o mouse. |
| **indent-rainbow** | oderwat | `oderwat.indent-rainbow` | Colore cada nível de indentação com uma cor diferente. Em Python, onde indentação define blocos, isso é muito útil para visualizar a estrutura. |
| **Path Intellisense** | Christian Kohler | `christian-kohler.path-intellisense` | Autocomplete de caminhos de arquivo ao digitar strings com paths (ex.: `open("data/...")`). |
| **Todo Tree** | Gruntfuggly | `gruntfuggly.todo-tree` | Encontra todos os comentários `# TODO`, `# FIXME`, `# HACK` no projeto e lista em uma árvore na barra lateral. |
| **Better Comments** | Aaron Bond | `aaron-bond.better-comments` | Colore comentários por tipo: `# !` fica vermelho (alerta), `# ?` fica azul (pergunta), `# TODO` fica laranja. |
| **Material Icon Theme** | Philipp Kief | `pkief.material-icon-theme` | Ícones coloridos no Explorer que diferenciam `.py`, `.json`, `.md`, pastas `tests/`, `app/`, `.vscode/` etc. |
| **Bracket Pair Colorizer** | (embutido) | — | O VS Code já colore pares de parênteses/colchetes com cores diferentes (ativado por padrão desde v1.67). Verifique com `"editor.bracketPairColorization.enabled": true`. |

---

#### REST API e Requisições HTTP

| Extensão | Autor | ID no Marketplace | Para que serve |
|---|---|---|---|
| **Thunder Client** | Ranga Vadhineni | `rangav.vscode-thunder-client` | Cliente HTTP leve dentro do VS Code (alternativa ao Postman). Permite enviar requisições GET, POST, PUT, DELETE e ver as respostas, sem sair do editor. |
| **REST Client** | Huachao Mao | `humao.rest-client` | Permite escrever requisições HTTP em arquivos `.http` ou `.rest` e executar com um clique. Útil para testar APIs do projeto. |

---

#### Exemplo de `.vscode/extensions.json` completo para um projeto Python

```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "charliermarsh.ruff",
        "ms-toolsai.jupyter",
        "ms-azuretools.vscode-docker",
        "eamodio.gitlens",
        "usernamehw.errorlens",
        "oderwat.indent-rainbow",
        "gruntfuggly.todo-tree",
        "pkief.material-icon-theme"
    ]
}
```

Quando alguém do time abrir o projeto, o VS Code pergunta se quer instalar as extensões recomendadas. Isso padroniza o ambiente de desenvolvimento da equipe.

> **Resumo:** para começar com Python, instale **Python + Pylance + Ruff + Error Lens**. Essas quatro extensões já cobrem 90% do que você precisa no dia a dia. As demais, instale conforme a necessidade do projeto crescer.

---

## 01. Preparação do ambiente Python

Aqui o objetivo é deixar a máquina pronta para rodar e depurar Python. Cada subtopic abaixo cobre uma ação prática.

### 01.1 Instalação do Python

**O que é:** instalar o interpretador oficial do Python no sistema operacional para conseguir executar arquivos `.py`.

**Exemplo:** comando para verificar se o Python está instalado.

```python
# arquivo: check_python.py
import sys
print(sys.version)
print(sys.executable)
```

---

#### O que é `import`

`import` é o comando que **carrega um módulo** para dentro do seu código. Um módulo é simplesmente um arquivo `.py` (ou um pacote embutido) que contém funções, classes e variáveis prontas para uso.

Quando você escreve `import sys`, está dizendo ao Python: *"traga tudo que está dentro do módulo `sys` para que eu possa usar"*. Depois disso, você acessa o conteúdo com `sys.alguma_coisa`.

```python
import sys          # carrega o módulo inteiro
print(sys.version)  # usa algo de dentro dele

from sys import version   # carrega só o que precisa
print(version)            # usa direto, sem "sys."
```

Sem o `import`, o Python não sabe que `sys` existe e lança `NameError: name 'sys' is not defined`.

---

#### O que é `sys` e de onde vem

`sys` é um **módulo da biblioteca padrão** do Python. Ele já vem instalado junto com o Python — não precisa baixar nada. A biblioteca padrão é uma coleção de módulos prontos que cobrem tarefas comuns (arquivos, rede, matemática, sistema operacional etc.).

O módulo `sys` dá acesso a **informações e configurações do interpretador** em si:

| Atributo | O que retorna |
|---|---|
| `sys.version` | String com a versão completa do Python (ex.: `"3.12.3 ..."`) |
| `sys.executable` | Caminho do binário do Python que está rodando (ex.: `"/usr/bin/python3"`) |
| `sys.argv` | Lista de argumentos passados pela linha de comando |
| `sys.path` | Lista de pastas onde o Python procura módulos para importar |
| `sys.platform` | Sistema operacional (`"linux"`, `"win32"`, `"darwin"`) |

#### Onde o `sys` fica no disco

O `sys` é um módulo **built-in** — ele está compilado dentro do próprio interpretador Python, não existe como um arquivo `.py` separado. Você pode confirmar isso rodando:

```python
import sys
print(sys)  # <module 'sys' (built-in)>
```

A indicação `(built-in)` mostra que ele faz parte do binário do Python. Diferente de outros módulos da biblioteca padrão (como `os` ou `json`), que são arquivos `.py` dentro de uma pasta, o `sys` já está embutido no executável.

Para ver onde ficam os módulos da biblioteca padrão **que são arquivos**, rode:

```python
import os
print(os.__file__)  # ex.: /usr/lib/python3.12/os.py
```

Essa pasta (ex.: `/usr/lib/python3.12/`) é onde moram os módulos da biblioteca padrão no Linux. No Windows, costuma ser `C:\Python312\Lib\`. Mas o `sys` não aparece lá — ele vive dentro do executável `/usr/bin/python3` em si.

> **Resumo:** `import` é o mecanismo de reuso de código do Python. `sys` é um dos módulos que já vêm de fábrica. Você não precisa instalar nada para usá-lo — basta `import sys`.

---

**Passo a passo:**
1. Baixe o instalador em python.org (ou use `apt install python3` no Linux).
2. Salve o código acima em `check_python.py`.
3. Rode `python check_python.py` no terminal.
4. Confirme que aparece a versão (ex.: `3.12.x`) e o caminho do executável.

**Código explicado:** `import sys` carrega o módulo de sistema que já vem com o Python. `sys.version` mostra a versão instalada e `sys.executable` mostra o caminho do binário usado. Se imprimiu, o Python está acessível e funcionando.

### 01.2 Configuração do VS Code para Python

**O que é:** ajustar o VS Code para reconhecer o interpretador correto e executar Python sem fricção. O VS Code armazena configurações em arquivos JSON e permite separar o que vale para **todos os projetos** (global) do que vale **só para este projeto** (workspace).

---

#### O que é o `.vscode/settings.json`

Quando você abre uma pasta no VS Code (`File > Open Folder`), essa pasta se torna o **workspace** (área de trabalho). Dentro dela você pode criar uma pasta `.vscode/` com arquivos de configuração que afetam **apenas aquele projeto**.

O arquivo `.vscode/settings.json` é onde ficam as configurações **de workspace**. Tudo que você colocar ali sobrescreve as configurações globais, mas **só enquanto esse projeto estiver aberto**.

| Arquivo | Escopo | Onde fica |
|---|---|---|
| **Settings globais** | Todos os projetos | Linux: `~/.config/Code/User/settings.json` · macOS: `~/Library/Application Support/Code/User/settings.json` · Windows: `%APPDATA%\Code\User\settings.json` |
| **Settings de workspace** | Só o projeto atual | `<projeto>/.vscode/settings.json` (igual em todos os SOs) |

> **Dica:** para abrir as settings globais, use `Ctrl+Shift+P` (ou `Cmd+Shift+P` no macOS) → `Preferences: Open User Settings (JSON)`. Para abrir as de workspace, use `Preferences: Open Workspace Settings (JSON)`.

**Por que separar?** Imagine que você tem dois projetos: um usa Python 3.10 e outro usa Python 3.12. A setting global define um padrão, mas cada projeto pode apontar para o seu próprio interpretador via `.vscode/settings.json`.

---

#### O que é `${workspaceFolder}` e as variáveis do VS Code

Dentro dos arquivos de configuração do VS Code (como `settings.json` e `launch.json`), você pode usar **variáveis predefinidas** com a sintaxe `${NOME}`. Elas são substituídas automaticamente pelo VS Code no momento em que a configuração é lida.

| Variável | O que vale | Exemplo real |
|---|---|---|
| `${workspaceFolder}` | Caminho absoluto da pasta aberta no VS Code | `/home/madson/meu_projeto` (Linux) · `C:\Users\madson\meu_projeto` (Windows) · `/Users/madson/meu_projeto` (macOS) |
| `${file}` | Caminho do arquivo atualmente aberto no editor | `/home/madson/meu_projeto/app/main.py` |
| `${fileBasename}` | Só o nome do arquivo aberto | `main.py` |
| `${fileDirname}` | Pasta do arquivo aberto | `/home/madson/meu_projeto/app` |
| `${env:NOME}` | Valor de uma variável de ambiente do sistema | `${env:HOME}` → `/home/madson` |

**Por que usar `${workspaceFolder}` em vez do caminho fixo?**

```json
// ❌ caminho fixo — só funciona na máquina do Madson
"python.defaultInterpreterPath": "/home/madson/meu_projeto/.venv/bin/python"

// ✅ caminho relativo ao workspace — funciona na máquina de qualquer pessoa do time
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
```

Quando outro desenvolvedor abre o mesmo projeto em outro computador, `${workspaceFolder}` se ajusta automaticamente para o caminho correto da máquina dele. Isso é essencial quando o `.vscode/settings.json` é versionado no Git.

> **Resumo:** `${}` é a forma do VS Code dizer "substitua isso por um valor real em tempo de execução". Funciona igual em Linux, macOS e Windows.

---

#### O que é `.venv` e por que ter um Python dentro do projeto

O `.venv` é uma pasta que contém uma **cópia isolada do Python** e suas bibliotecas, separada do Python do sistema operacional. É chamado de **virtual environment** (ambiente virtual).

**Por que usar?**
- Cada projeto pode ter suas próprias versões de bibliotecas sem conflitar com outros projetos.
- Você não precisa de permissão de administrador para instalar pacotes.
- O projeto fica reprodutível — outro desenvolvedor cria o `.venv` e tem o mesmo ambiente.

**Criando e ativando o `.venv`:**

| Ação | Linux / macOS | Windows (cmd) | Windows (PowerShell) |
|---|---|---|---|
| Criar o ambiente | `python3 -m venv .venv` | `python -m venv .venv` | `python -m venv .venv` |
| Ativar | `source .venv/bin/activate` | `.venv\Scripts\activate.bat` | `.venv\Scripts\Activate.ps1` |
| Desativar | `deactivate` | `deactivate` | `deactivate` |

Após ativar, o prompt do terminal muda para mostrar `(.venv)` no início:

```bash
# antes de ativar:
madson@pc:~/meu_projeto$

# depois de ativar:
(.venv) madson@pc:~/meu_projeto$
```

Agora `python` e `pip` dentro desse terminal apontam para a cópia dentro de `.venv/`, não para o Python do sistema.

**Estrutura interna do `.venv`:**

```
meu_projeto/
├── .venv/                      ← pasta do ambiente virtual
│   ├── bin/                    ← Linux/macOS (no Windows: Scripts/)
│   │   ├── python              ← cópia do interpretador
│   │   ├── pip                 ← gerenciador de pacotes
│   │   └── activate            ← script de ativação
│   ├── lib/
│   │   └── python3.12/
│   │       └── site-packages/  ← pacotes instalados com pip
│   └── pyvenv.cfg              ← configuração do ambiente
├── app/
│   └── main.py
└── requirements.txt
```

> **Nota sobre pastas ocultas no Linux/macOS:** pastas que começam com `.` (ponto) são ocultas por padrão. Para ver no terminal, use `ls -la` (o `-a` mostra ocultos). No gerenciador de arquivos do Linux, use `Ctrl+H` para alternar a exibição. No VS Code, o `.venv` aparece normalmente no explorador de arquivos.
>
> **No Windows:** pastas com `.` no início **não** são ocultas; elas aparecem normalmente no Explorer.

> **Importante:** adicione `.venv/` ao `.gitignore`. O ambiente virtual não deve ser versionado — cada pessoa recria o seu com `python -m venv .venv` e `pip install -r requirements.txt`.

---

#### O que é `pyenv` — gerenciador de versões do Python

O `pyenv` é uma ferramenta que permite **instalar e alternar entre múltiplas versões do Python** no mesmo computador. É diferente do `.venv`:

| Ferramenta | Para que serve |
|---|---|
| `pyenv` | Instalar e alternar **versões do Python** (3.10, 3.11, 3.12...) |
| `venv` | Criar **ambientes isolados** com pacotes separados por projeto |

Você pode (e deve) usar os dois juntos: `pyenv` para ter a versão certa do Python, e `venv` para isolar os pacotes de cada projeto.

**Instalação do pyenv:**

```bash
# Linux / macOS
curl https://pyenv.run | bash
# Depois adicione ao seu ~/.bashrc ou ~/.zshrc:
# export PATH="$HOME/.pyenv/bin:$PATH"
# eval "$(pyenv init -)"

# Windows: use pyenv-win
# https://github.com/pyenv-win/pyenv-win
```

**Uso básico:**

```bash
# listar versões disponíveis para instalar
pyenv install --list | grep 3.12

# instalar uma versão
pyenv install 3.12.0

# definir a versão global (padrão do sistema)
pyenv global 3.12.0

# definir a versão local (só para este projeto)
cd meu_projeto/
pyenv local 3.12.0   # cria arquivo .python-version

# ver qual está ativa
pyenv version
```

Quando você roda `pyenv install 3.12.0`, o Python fica em:
- **Linux/macOS:** `~/.pyenv/versions/3.12.0/bin/python`
- **Windows (pyenv-win):** `%USERPROFILE%\.pyenv\pyenv-win\versions\3.12.0\python.exe`

**Combinando pyenv + venv no VS Code:**

```bash
# 1. Defina a versão do Python para o projeto
cd meu_projeto/
pyenv local 3.12.0

# 2. Crie o venv usando essa versão
~/.pyenv/versions/3.12.0/bin/python -m venv .venv

# 3. Ative
source .venv/bin/activate     # Linux/macOS
# .venv\Scripts\activate.bat  # Windows cmd
# .venv\Scripts\Activate.ps1  # Windows PowerShell
```

---

#### Por que usar `python.defaultInterpreterPath` — o que muda no VS Code

Sem essa configuração, o VS Code tenta adivinhar qual Python usar. Ele procura na seguinte ordem: `python3` no PATH, `python` no PATH, eventuais virtualenvs detectados. Nem sempre ele acerta — especialmente se você tem várias versões instaladas.

Ao definir `python.defaultInterpreterPath`, você **garante** que o VS Code use exatamente o Python que você quer. Veja o que muda com e sem:

| Funcionalidade do VS Code | Sem `defaultInterpreterPath` | Com `defaultInterpreterPath` |
|---|---|---|
| **Barra inferior** (canto direito) | Pode mostrar Python errado ou "nenhum encontrado" | Mostra a versão correta do projeto |
| **IntelliSense / Pylance** | Autocomplete pode sugerir bibliotecas que não estão instaladas no seu venv | Autocomplete reconhece exatamente os pacotes do seu `.venv` |
| **Botão Run (▶)** | Pode rodar com o Python do sistema, ignorando seu venv | Roda com o Python do projeto |
| **Debugger (F5)** | Pode debugar com interpretador errado | Usa o interpretador correto |
| **Verificação de erros** | Pylance pode marcar imports como "não encontrados" mesmo que estejam instalados no venv | Pylance reconhece todos os pacotes do venv |
| **Terminal integrado** | Pode não ativar o venv automaticamente | Com `activateEnvironment: true`, ativa o venv certo |

**Exemplo prático do problema:** você instala `pip install pandas` no `.venv`, mas o Pylance mostra `Import "pandas" could not be resolved`. Isso acontece porque o VS Code está olhando para o Python do sistema, não para o do `.venv`. Ao configurar `defaultInterpreterPath` apontando para `.venv/bin/python`, o erro some.

---

#### Exemplo completo com explicação de cada campo

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true
}
```

> **No Windows**, o caminho do interpretador dentro do venv é diferente:
> ```json
> "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe"
> ```
> O VS Code substitui `${workspaceFolder}` pelo caminho correto do SO automaticamente.

**`python.defaultInterpreterPath`**

Diz ao VS Code **qual binário do Python** usar como padrão neste workspace. O valor é o caminho completo do executável. Exemplos comuns:

| Caminho | Quando usar | SO |
|---|---|---|
| `"${workspaceFolder}/.venv/bin/python"` | Projeto com virtualenv local | Linux / macOS |
| `"${workspaceFolder}/.venv/Scripts/python.exe"` | Projeto com virtualenv local | Windows |
| `"/usr/bin/python3"` | Python do sistema | Linux |
| `"/usr/local/bin/python3"` | Python instalado via Homebrew | macOS |
| `"C:\\Python312\\python.exe"` | Python instalado para todos os usuários | Windows |
| `"${env:HOME}/.pyenv/versions/3.12.0/bin/python"` | Versão gerenciada pelo pyenv | Linux / macOS |
| `"${env:USERPROFILE}\\.pyenv\\pyenv-win\\versions\\3.12.0\\python.exe"` | Versão gerenciada pelo pyenv-win | Windows |

> Se você mudar essa configuração e o VS Code não reagir, abra a paleta (`Ctrl+Shift+P` / `Cmd+Shift+P`) e rode `Python: Select Interpreter` para forçar a atualização.

**`python.terminal.activateEnvironment`**

Quando está `true`, toda vez que o VS Code abre um **novo terminal integrado**, ele roda automaticamente o comando de ativação do ambiente virtual. O comando que ele executa depende do SO:

| SO | Comando executado automaticamente |
|---|---|
| Linux / macOS | `source .venv/bin/activate` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

Isso garante que:
- `pip install` instale pacotes no ambiente correto.
- `python` dentro do terminal aponte para o interpretador do projeto.
- Você não precise ativar manualmente toda vez.

Quando está `false`, o terminal abre "limpo" — usando o Python do sistema, ignorando qualquer virtualenv.

---

#### Workspace vs Global — quando usar cada um

| Situação | Onde configurar |
|---|---|
| Tema de cores, tamanho de fonte, atalhos | **Global** — preferência pessoal |
| Caminho do interpretador Python do projeto | **Workspace** — cada projeto pode ter o seu |
| Ativar/desativar virtualenv automático | **Workspace** — depende se o projeto usa venv |
| Extensões recomendadas para o time | **Workspace** — via `.vscode/extensions.json` |

> **Importante:** o `.vscode/settings.json` costuma ser **versionado** no Git junto com o projeto, para que todos do time usem as mesmas configurações. Já o settings global é pessoal e **não** vai para o repositório.

---

**Passo a passo:**
1. Abra a pasta do projeto no VS Code com `File > Open Folder`.
2. Crie o ambiente virtual: `python3 -m venv .venv` (Linux/macOS) ou `python -m venv .venv` (Windows).
3. Crie a pasta `.vscode/` na raiz do projeto (se não existir).
4. Crie o arquivo `.vscode/settings.json` com o conteúdo do exemplo acima (ajuste o caminho se estiver no Windows).
5. Abra a paleta com `Ctrl+Shift+P` (`Cmd+Shift+P` no macOS) e rode `Python: Select Interpreter`.
6. Confirme que a barra inferior do VS Code mostra o interpretador do `.venv`.
7. Abra um novo terminal (`Ctrl+`` ) e verifique que o prompt mostra `(.venv)` no início.

**Código explicado:** o arquivo `.vscode/settings.json` é a forma do VS Code saber como tratar este projeto especificamente. `${workspaceFolder}` garante que o caminho funcione em qualquer máquina. `defaultInterpreterPath` resolve "qual Python usar" — e com isso o IntelliSense, o Run e o debugger passam a funcionar corretamente com os pacotes do seu projeto. `activateEnvironment` resolve "ativar o ambiente virtual sozinho ou não". Juntos, eliminam a necessidade de configurar o terminal manualmente toda vez que abrir o projeto.

### 01.3 Configuração do Debug Python no VS Code

**O que é:** criar e ajustar o arquivo `launch.json` para que o VS Code saiba como iniciar o debugger Python, permitindo breakpoints, inspeção de variáveis e execução passo a passo.

**Exemplo:** arquivo de configuração do debugger.

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Arquivo Atual",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Main do Projeto",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/app/main.py",
            "console": "integratedTerminal",
            "args": [],
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

**Passo a passo:**
1. Abra a paleta de comandos com `Ctrl+Shift+P` e digite `Debug: Open launch.json`.
2. Selecione `Python Debugger` na lista de ambientes.
3. O VS Code cria `.vscode/launch.json` com uma configuração básica.
4. Substitua o conteúdo pelo exemplo acima para ter duas opções: debugar o arquivo aberto ou o `main.py` do projeto.
5. Pressione `F5` para iniciar o debug; use o seletor no topo da aba Run para alternar entre as configurações.

**Campos importantes do `launch.json`:**
- `"type": "debugpy"` — usa o debugger oficial do Python (debugpy), que substituiu o antigo `"python"`.
- `"request": "launch"` — inicia um novo processo; use `"attach"` para conectar a um processo já rodando.
- `"program"` — caminho do arquivo a executar; `${file}` é o arquivo aberto no editor.
- `"console": "integratedTerminal"` — roda no terminal integrado, permitindo entrada do teclado.
- `"justMyCode": true` — ignora código de bibliotecas durante o debug; mude para `false` se precisar entrar em libs.
- `"args"` — lista de argumentos passados ao script (ex.: `["--verbose", "Ana"]`).
- `"env"` — variáveis de ambiente extras; `PYTHONPATH` garante que imports do projeto funcionem.

**Código explicado:** o `launch.json` é o contrato entre o VS Code e o debugger. Cada objeto dentro de `configurations` aparece como opção no menu de debug. Com essas duas entradas, você pode debugar qualquer arquivo avulso ou sempre o ponto de entrada principal do projeto.

### 01.4 Debug de um Hello World

**O que é:** rodar um arquivo em modo debug, parando em pontos do código para inspecionar valores.

**Exemplo:** arquivo simples para inserir breakpoint.

```python
# arquivo: debug_hello.py
nome = "Ana"
saldo = 1500
mensagem = f"{nome} tem saldo de {saldo}"
print(mensagem)
```

**Passo a passo:**
1. Salve o arquivo `debug_hello.py`.
2. Clique no número da linha 3 para colocar um breakpoint vermelho.
3. Pressione `F5` e escolha `Python File`.
4. Quando parar, veja `nome` e `saldo` na aba Variables; aperte `F10` para avançar.

**Código explicado:** o breakpoint pausa antes de executar a linha, permitindo inspecionar os valores já existentes em memória.

### 01.5 Execução de scripts pelo terminal

**O que é:** rodar arquivos `.py` direto pelo terminal, sem depender da IDE.

**Exemplo:** script que recebe argumento.

```python
# arquivo: run_terminal.py
import sys

nome = sys.argv[1] if len(sys.argv) > 1 else "Mundo"
print(f"Olá, {nome}")
```

**Passo a passo:**
1. Salve como `run_terminal.py`.
2. Abra o terminal na pasta.
3. Rode `python run_terminal.py Ana`.
4. Confirme a saída `Olá, Ana`.

**Código explicado:** `sys.argv` é a lista de argumentos passados pela linha de comando; o primeiro item é o próprio nome do script.

### 01.6 Organização inicial de arquivos .py

**O que é:** estruturar o projeto em pastas separando código, dados e testes desde o começo.

**Exemplo:** layout mínimo do projeto.

```python
# estrutura sugerida
# meu_projeto/
# ├── app/
# │   ├── __init__.py
# │   └── main.py
# ├── tests/
# │   └── test_main.py
# └── README.md
```

**Passo a passo:**
1. Crie a pasta `meu_projeto/`.
2. Dentro dela crie `app/` e `tests/`.
3. Dentro de `app/` crie `__init__.py` (vazio) e `main.py`.
4. Em `main.py` escreva `print("Projeto pronto")` e rode com `python -m app.main`.

**Código explicado:** o `__init__.py` transforma a pasta em pacote, e a flag `-m` faz Python tratar a pasta como módulo importável.

### 01.7 Tipos de extensão de arquivos Python

**O que é:** o ecossistema Python usa diferentes extensões de arquivo, cada uma com uma função específica. Saber identificá-las evita confusão ao navegar projetos.

| Extensão | O que é | Quem cria | Você edita? |
|---|---|---|---|
| `.py` | Código-fonte Python (texto puro) | Você, o desenvolvedor | **Sim** — é o arquivo principal de trabalho |
| `.pyc` | Bytecode compilado (binário) | O interpretador, automaticamente | **Não** — é gerado ao importar um `.py` |
| `.pyo` | Bytecode otimizado (obsoleto desde Python 3.5) | Era gerado com `python -O` | **Não** — substituído por `.opt-1.pyc` |
| `.pyi` | Stub de tipos (type hints) | Você ou bibliotecas como `mypy` | **Às vezes** — define tipos sem implementação |
| `.pyw` | Script Python sem janela de terminal (Windows) | Você | **Sim** — usado para apps com interface gráfica no Windows |
| `.pyd` | Extensão compilada em C (Windows) | Compilador C/C++ | **Não** — equivalente a `.so` no Linux |
| `.so` | Extensão compilada em C (Linux/Mac) | Compilador C/C++ | **Não** — módulo nativo de alta performance |
| `.ipynb` | Notebook Jupyter (JSON com células de código) | Jupyter / VS Code | **Sim** — usado para análise de dados e ensino |

---

#### `.py` — o arquivo que você escreve

Todo código Python que você cria é um arquivo `.py`. É texto puro, legível por humanos, editável em qualquer editor.

```python
# arquivo: simulacao.py
valor = 120000
parcela = valor / 120
print(f"Parcela: R$ {parcela:.2f}")
```

---

#### `.pyc` — o cache que o Python gera sozinho

Quando você faz `import` de um módulo, o Python compila o `.py` para bytecode e salva como `.pyc` dentro da pasta `__pycache__/`. Na próxima vez, se o `.py` não mudou, ele pula a compilação e usa o `.pyc` direto — isso acelera a importação.

```
meu_projeto/
├── app/
│   ├── __init__.py
│   ├── calculos.py
│   └── __pycache__/
│       ├── __init__.cpython-312.pyc    ← gerado automaticamente
│       └── calculos.cpython-312.pyc    ← gerado automaticamente
```

> **Dica:** a pasta `__pycache__/` deve estar no `.gitignore`. Nunca versione arquivos `.pyc`.

---

#### `.pyi` — stubs de tipagem

Arquivos `.pyi` descrevem os **tipos** de um módulo sem conter a implementação. São usados por ferramentas como `mypy` e `Pylance` (no VS Code) para fazer verificação estática de tipos.

```python
# arquivo: calculos.pyi
def parcela(valor: float, meses: int) -> float: ...
def ltv(imovel: float, solicitado: float) -> float: ...
```

O `...` (reticências) indica que o corpo da função está em outro lugar (no `.py`). O `.pyi` só serve para o analisador de tipos, não é executado.

---

#### `.ipynb` — notebooks interativos

Arquivos `.ipynb` são **Jupyter Notebooks** — documentos que misturam código, texto e gráficos em células. O formato interno é JSON. Você pode abrir e editar direto no VS Code (com a extensão Jupyter) ou no navegador com `jupyter notebook`.

```
# para abrir no terminal:
jupyter notebook analise.ipynb
```

São muito usados em ciência de dados, machine learning e ensino, mas **não** são recomendados para código de produção.

---

**Resumo prático:** no dia a dia você vai trabalhar quase exclusivamente com `.py`. Os `.pyc` aparecem sozinhos e devem ser ignorados pelo Git. Os `.pyi` só importam se você usar tipagem estática. Os `.ipynb` são para exploração e análise interativa.

---

## 02. Como Python executa código

Cada subtopic abaixo mostra um pedaço do que acontece entre você apertar Run e ver a saída.

### 02.1 Interpretador Python

**O que é:** programa que lê seu arquivo `.py`, traduz para bytecode e executa instrução por instrução.

**Exemplo:**

```python
# arquivo: 02_1_interpretador.py
import sys
print("Interpretador:", sys.executable)
print("Versão:", sys.version_info.major, sys.version_info.minor)
```

**Passo a passo:**
1. Salve como `02_1_interpretador.py`.
2. Rode `python 02_1_interpretador.py`.
3. Verifique caminho do binário e versão major.minor.

**Código explicado:** `sys.executable` é exatamente o programa interpretador que está rodando seu script naquele momento.

### 02.2 CPython e bytecode

**O que é:** CPython é a implementação padrão. Antes de executar, ele compila seu código em bytecode (`.pyc`) guardado em `__pycache__`.

**Exemplo:**

```python
# arquivo: 02_2_bytecode.py
import dis

def soma(a, b):
    return a + b

dis.dis(soma)
```

**Passo a passo:**
1. Salve como `02_2_bytecode.py`.
2. Rode `python 02_2_bytecode.py`.
3. Veja as instruções `LOAD_FAST`, `BINARY_OP`, `RETURN_VALUE`.

**Código explicado:** `dis.dis` mostra o bytecode real que o CPython executa internamente para a função `soma`.

### 02.3 Ciclo de vida de um programa Python

**O que é:** as fases que um programa passa: leitura do arquivo, compilação para bytecode, execução, finalização.

**Exemplo:**

```python
# arquivo: 02_3_ciclo.py
print("1. início")

def encerrar():
    print("3. fim")

import atexit
atexit.register(encerrar)

print("2. meio")
```

**Passo a passo:**
1. Salve como `02_3_ciclo.py`.
2. Rode com `python 02_3_ciclo.py`.
3. Veja a ordem: `1. início`, `2. meio`, `3. fim`.

**Código explicado:** `atexit.register` agenda uma função para rodar quando o programa estiver encerrando, mostrando claramente a fase final.

### 02.4 Script, módulo e pacote

**O que é:** **script** é um `.py` para rodar; **módulo** é um `.py` para ser importado; **pacote** é uma pasta com módulos.

**Exemplo:**

```python
# pacote: credito/
# credito/__init__.py  -> vazio
# credito/calculos.py
def parcela(valor, meses):
    return valor / meses
```

```python
# arquivo: 02_4_uso.py (script)
from credito.calculos import parcela
print(parcela(120000, 120))
```

**Passo a passo:**
1. Crie a pasta `credito/` com `__init__.py` vazio.
2. Crie `credito/calculos.py` com a função `parcela`.
3. Crie `02_4_uso.py` ao lado da pasta.
4. Rode `python 02_4_uso.py` e veja `1000.0`.

**Código explicado:** `02_4_uso.py` é script, `calculos.py` é módulo e a pasta `credito` é pacote.

### 02.5 Arquivo `__init__.py`

**O que é:** marca uma pasta como pacote e pode definir o que é exportado quando o pacote é importado.

**Exemplo:**

```python
# arquivo: credito/__init__.py
from credito.calculos import parcela

VERSAO = "1.0"
```

```python
# arquivo: 02_5_init.py
import credito
print(credito.VERSAO)
print(credito.parcela(120000, 120))
```

**Passo a passo:**
1. Edite `credito/__init__.py` com o conteúdo acima.
2. Crie `02_5_init.py` no mesmo diretório do pacote.
3. Rode `python 02_5_init.py`.

**Código explicado:** o `__init__.py` reexporta `parcela` e expõe `VERSAO`, então basta `import credito` para usar os dois.

### 02.6 Ponto de entrada `__name__ == "__main__"`

**O que é:** bloco que só roda quando o arquivo é executado direto, não quando é importado.

**Exemplo:**

```python
# arquivo: 02_6_entrada.py
def saudacao(nome):
    return f"Olá, {nome}"

if __name__ == "__main__":
    print(saudacao("Ana"))
```

**Passo a passo:**
1. Salve como `02_6_entrada.py`.
2. Rode `python 02_6_entrada.py` e veja a saudação.
3. Em outro arquivo faça `import 02_6_entrada` (renomeie sem dígitos no início) — note que nada é impresso.

**Código explicado:** quando o arquivo é executado direto, `__name__` vale `"__main__"` e o bloco roda; quando é importado, `__name__` recebe o nome do módulo.

---

## 03. Sintaxe essencial

### 03.1 Indentação e blocos

**O que é:** Python usa a indentação (espaços no início da linha) para definir blocos, no lugar de chaves.

**Exemplo:**

```python
def aprovar(score):
    if score >= 0.7:
        return "aprovado"
    return "recusado"

print(aprovar(0.85))
```

**Passo a passo:**
1. Salve como `03_1_indent.py`.
2. Mantenha **4 espaços** dentro da função.
3. Rode `python 03_1_indent.py` e veja `aprovado`.

**Código explicado:** o bloco do `if` está dentro do bloco da função; os dois níveis de indentação mostram o aninhamento.

### 03.2 Instruções e expressões

**O que é:** **expressão** produz valor (`2 + 2`); **instrução** executa ação (`x = 4`, `if`, `def`).

**Exemplo:**

```python
# expressões
total = 2 + 3 * 4              # expressão aritmética
maior = max(10, 20)            # expressão de chamada

# instruções
if total > 10:                  # instrução de controle
    print(total)
```

**Passo a passo:**
1. Salve como `03_2_expr.py` e rode.
2. Note que `2 + 3 * 4` produz `14`; isso é expressão.
3. Note que `if ...:` não produz valor; isso é instrução.

**Código explicado:** expressões podem ser usadas dentro de instruções, mas instruções não podem aparecer onde se espera valor.

### 03.3 Comentários

**O que é:** trechos ignorados pelo interpretador; servem para o leitor.

**Exemplo:**

```python
# Calcula a parcela mensal de um financiamento
valor = 120000           # valor solicitado em reais
meses = 120              # prazo em meses
parcela = valor / meses  # parcela sem juros
print(parcela)
```

**Passo a passo:**
1. Salve como `03_3_comentarios.py`.
2. Rode e veja `1000.0`.
3. Apague os comentários e rode de novo: a saída é a mesma.

**Código explicado:** tudo após `#` na mesma linha é ignorado; serve para explicar intenção.

### 03.4 Docstrings

**O que é:** texto entre `"""..."""` no início de função, classe ou módulo, lido por ferramentas como `help()`.

**Exemplo:**

```python
def calcular_ltv(imovel, solicitado):
    """Retorna o LTV como decimal.

    LTV = valor_solicitado / valor_imovel.
    """
    return solicitado / imovel

print(calcular_ltv.__doc__)
help(calcular_ltv)
```

**Passo a passo:**
1. Salve como `03_4_docstring.py`.
2. Rode `python 03_4_docstring.py`.
3. Veja a docstring impressa por `__doc__` e por `help`.

**Código explicado:** a docstring fica acessível em `funcao.__doc__` e é a base para documentação automática.

### 03.5 Quebra de linha

**O que é:** dividir uma instrução longa em várias linhas usando parênteses, colchetes, chaves ou `\`.

**Exemplo:**

```python
total = (
    1000
    + 2000
    + 3000
)

mensagem = (
    "Cliente aprovado "
    "com observações"
)

print(total, mensagem)
```

**Passo a passo:**
1. Salve como `03_5_quebra.py`.
2. Rode e veja `6000 Cliente aprovado com observações`.

**Código explicado:** dentro de parênteses, Python permite quebrar livremente; strings adjacentes são concatenadas automaticamente.

### 03.6 Convenções de nomes

**O que é:** padrões PEP 8: `snake_case` para variáveis e funções, `PascalCase` para classes, `MAIUSCULO` para constantes.

**Exemplo:**

```python
TAXA_PADRAO = 0.012

def calcular_juros(valor):
    return valor * TAXA_PADRAO

class SimulacaoCredito:
    pass

print(calcular_juros(10000))
```

**Passo a passo:**
1. Salve como `03_6_nomes.py` e rode.
2. Veja `120.0`.
3. Note as três convenções no mesmo arquivo.

**Código explicado:** seguir a convenção facilita ler código de qualquer projeto Python.

### 03.7 Palavras reservadas

**O que é:** palavras que pertencem à linguagem e não podem ser usadas como nome de variável.

**Exemplo:**

```python
import keyword
print(keyword.kwlist[:8])

# isto não compila:
# class = "x"   -> SyntaxError
classe = "Simulacao"  # use sinônimo
print(classe)
```

**Passo a passo:**
1. Salve como `03_7_reservadas.py`.
2. Rode e veja a lista de palavras-chave (ex.: `False`, `None`, `class`, `def`).

**Código explicado:** `keyword.kwlist` lista todas as palavras reservadas; nenhuma pode ser usada como identificador.

---

## 04. Variáveis e modelo de objetos

Em Python, variável é só um **nome** que aponta para um **objeto**. Cada subtopic explora uma faceta desse modelo.

### 04.1 Nomes e referências

**O que é:** atribuir uma variável é amarrar um nome a um objeto já existente em memória; várias variáveis podem apontar para o mesmo objeto.

**Exemplo:**

```python
a = [1, 2, 3]
b = a            # b aponta para o mesmo objeto
b.append(4)
print(a)         # [1, 2, 3, 4]
print(a is b)    # True
```

**Passo a passo:**
1. Salve como `04_1_ref.py`.
2. Rode e observe que mexer em `b` afeta `a`.
3. Confirme com `is` que são o mesmo objeto.

**Código explicado:** `b = a` não copia a lista; só copia a referência.

### 04.2 Tipagem dinâmica

**O que é:** o mesmo nome pode apontar para tipos diferentes ao longo do programa.

**Exemplo:**

```python
valor = 100         # int
print(type(valor))

valor = "alto"      # agora str
print(type(valor))

valor = [1, 2]      # agora list
print(type(valor))
```

**Passo a passo:**
1. Salve como `04_2_dinamica.py` e rode.
2. Veja `int`, `str`, `list` impressos.

**Código explicado:** Python não trava o tipo da variável; o tipo está no objeto, não no nome.

### 04.3 Tipagem forte

**O que é:** apesar de dinâmica, Python não converte tipos sem você pedir; misturar tipos incompatíveis dá erro.

**Exemplo:**

```python
idade = 30
texto = "anos"

try:
    resultado = idade + texto   # erro!
except TypeError as e:
    print("erro:", e)

resultado = str(idade) + " " + texto  # conversão explícita
print(resultado)
```

**Passo a passo:**
1. Salve como `04_3_forte.py` e rode.
2. Veja a mensagem de erro e depois `30 anos`.

**Código explicado:** `int + str` falha; é preciso converter com `str(...)` antes.

### 04.4 Identidade, valor e tipo

**O que é:** todo objeto tem três atributos: `id` (endereço), valor e `type`.

**Exemplo:**

```python
score = 0.82
print("valor:", score)
print("tipo:", type(score))
print("id:", id(score))
```

**Passo a passo:**
1. Salve como `04_4_idtype.py` e rode.
2. Anote o `id` e rode de novo: pode mudar entre execuções.

**Código explicado:** `type` mostra a classe do objeto, `id` o local na memória, e o valor é o conteúdo.

### 04.5 Mutabilidade e imutabilidade

**O que é:** objetos **imutáveis** (`int`, `float`, `str`, `tuple`) não mudam; objetos **mutáveis** (`list`, `dict`, `set`) mudam.

**Exemplo:**

```python
texto = "ana"
print(id(texto))
texto = texto + " silva"
print(id(texto))     # id diferente: novo objeto

clientes = ["ana"]
print(id(clientes))
clientes.append("silva")
print(id(clientes))  # mesmo id: mesmo objeto
```

**Passo a passo:**
1. Salve como `04_5_mutab.py` e rode.
2. Compare os `id` em strings e em listas.

**Código explicado:** alterar string cria objeto novo; alterar lista altera o mesmo objeto.

### 04.6 Escopo LEGB

**O que é:** ordem de busca de nomes — **L**ocal, **E**nclosing, **G**lobal, **B**uilt-in.

**Exemplo:**

```python
TAXA = 0.05  # global

def externa():
    fator = 2  # enclosing
    def interna():
        bonus = 10  # local
        print(bonus, fator, TAXA, len("ok"))  # local, enclosing, global, builtin
    interna()

externa()
```

**Passo a passo:**
1. Salve como `04_6_legb.py` e rode.
2. Veja `10 2 0.05 2`.

**Código explicado:** Python procura cada nome nessa ordem; a primeira ocorrência encontrada é usada.

### 04.7 Escopo global

**O que é:** `global` permite uma função alterar uma variável definida no escopo do módulo.

**Exemplo:**

```python
contador = 0

def registrar():
    global contador
    contador += 1

registrar()
registrar()
print(contador)  # 2
```

**Passo a passo:**
1. Salve como `04_7_global.py` e rode.
2. Sem `global`, a linha `contador += 1` dá `UnboundLocalError`.

**Código explicado:** `global contador` avisa que a função vai alterar o nome no escopo do módulo.

### 04.8 Escopo nonlocal

**O que é:** `nonlocal` permite uma função interna alterar variável da função de fora (enclosing), sem ser global.

**Exemplo:**

```python
def contador():
    n = 0
    def incrementar():
        nonlocal n
        n += 1
        return n
    return incrementar

c = contador()
print(c(), c(), c())  # 1 2 3
```

**Passo a passo:**
1. Salve como `04_8_nonlocal.py` e rode.
2. Veja a contagem persistir entre chamadas.

**Código explicado:** `nonlocal n` aponta para o `n` da função externa, criando um pequeno estado privado.

### 04.9 Ciclo de vida dos objetos

**O que é:** um objeto vive enquanto houver referência. Quando o último nome some, o garbage collector libera a memória.

**Exemplo:**

```python
import sys

dados = [1, 2, 3]
print(sys.getrefcount(dados))   # contador de referências

outra = dados
print(sys.getrefcount(dados))   # subiu

del outra
print(sys.getrefcount(dados))   # voltou
```

**Passo a passo:**
1. Salve como `04_9_ciclo.py` e rode.
2. Observe o contador subir e descer.

**Código explicado:** cada nome que aponta para o objeto soma 1 no contador; quando chega a zero, o objeto é descartado.

---

## 05. Tipos primitivos

### 05.1 None

**O que é:** valor único que representa “sem valor”.

**Exemplo:**

```python
observacao = None
print(observacao is None)
print(observacao == None)  # funciona, mas prefira `is`
```

**Passo a passo:**
1. Salve como `05_1_none.py` e rode.
2. Veja `True True`.

**Código explicado:** use `is None` para checar ausência; é mais idiomático.

### 05.2 bool

**O que é:** `True` ou `False`. Internamente, são `int` (1 e 0).

**Exemplo:**

```python
aprovado = True
print(aprovado + 1)        # 2
print(True == 1)           # True
print(bool(0), bool(""))   # False False
```

**Passo a passo:**
1. Salve como `05_2_bool.py` e rode.
2. Confirme que `True` se comporta como `1`.

**Código explicado:** `bool` é subclasse de `int`; útil em somas e flags.

### 05.3 int

**O que é:** número inteiro, sem limite de tamanho em Python.

**Exemplo:**

```python
parcelas = 120
saldo = 10**30  # número enorme
print(parcelas, saldo)
print(divmod(120000, 12))  # (10000, 0)
```

**Passo a passo:**
1. Salve como `05_3_int.py` e rode.

**Código explicado:** `int` cresce dinamicamente; `divmod` retorna divisão inteira e resto.

### 05.4 float

**O que é:** número decimal de ponto flutuante (precisão limitada).

**Exemplo:**

```python
renda = 8500.50
print(renda * 0.3)
print(0.1 + 0.2)        # 0.30000000000000004
print(round(0.1 + 0.2, 2))  # 0.3
```

**Passo a passo:**
1. Salve como `05_4_float.py` e rode.
2. Veja a imprecisão clássica e o uso de `round`.

**Código explicado:** floats têm pequenas imprecisões; arredonde quando exibir.

### 05.5 complex

**O que é:** número complexo `a + bj`.

**Exemplo:**

```python
z = 3 + 4j
print(z.real, z.imag)
print(abs(z))   # 5.0 (módulo)
```

**Passo a passo:**
1. Salve como `05_5_complex.py` e rode.

**Código explicado:** raro em apps de negócio, comum em ciência de dados; tem `.real`, `.imag` e `abs`.

### 05.6 str

**O que é:** sequência imutável de caracteres Unicode.

**Exemplo:**

```python
nome = "Ana"
print(nome.upper(), len(nome), nome[0])
print(nome + " Silva")
```

**Passo a passo:**
1. Salve como `05_6_str.py` e rode.

**Código explicado:** strings têm muitos métodos (`upper`, `lower`, `split`) e suportam indexação.

### 05.7 bytes

**O que é:** sequência imutável de bytes (números 0-255), usada para dados binários.

**Exemplo:**

```python
b = b"renda"
print(b, type(b))
print(b.decode("utf-8"))
texto = "ação"
print(texto.encode("utf-8"))
```

**Passo a passo:**
1. Salve como `05_7_bytes.py` e rode.

**Código explicado:** `encode` vira bytes, `decode` vira str; útil em I/O e rede.

### 05.8 Conversão de tipos

**O que é:** transformar valores com `int(...)`, `float(...)`, `str(...)`, `bool(...)`.

**Exemplo:**

```python
entrada = "120000"
valor = float(entrada)
print(valor + 1000)
print(str(valor))
print(int("0b1010", 2))  # 10
```

**Passo a passo:**
1. Salve como `05_8_conv.py` e rode.

**Código explicado:** conversões falham se a string não for compatível (`float("abc")` lança `ValueError`).

### 05.9 Truthy e falsy

**O que é:** todo objeto pode ser avaliado como verdadeiro ou falso. Falsy: `None`, `0`, `""`, `[]`, `{}`, `set()`, `False`.

**Exemplo:**

```python
for valor in [0, 1, "", "ok", [], [0], None]:
    print(valor, "->", bool(valor))
```

**Passo a passo:**
1. Salve como `05_9_truthy.py` e rode.
2. Note quais valores são `False`.

**Código explicado:** isso permite escrever `if lista:` em vez de `if len(lista) > 0:`.

---

## 06. Operadores

### 06.1 Operadores aritméticos

**O que é:** `+ - * / // % **` para somar, subtrair, multiplicar, dividir, divisão inteira, resto e potência.

**Exemplo:**

```python
valor = 120000
meses = 12
print(valor + 1000)       # soma
print(valor * 1.05)       # juros 5%
print(valor / meses)      # 10000.0
print(valor // meses)     # 10000  (inteiro)
print(valor % meses)      # 0  (resto)
print(2 ** 10)            # 1024
```

**Passo a passo:**
1. Salve como `06_1_arit.py` e rode.
2. Compare `/` e `//` para ver float vs inteiro.

**Código explicado:** `/` sempre devolve float; `//` corta as casas decimais; `**` é potência.

### 06.2 Operadores de comparação

**O que é:** `== != < <= > >=` retornam `bool`.

**Exemplo:**

```python
score = 0.72
print(score >= 0.7)
print(score == 0.72)
print(0.6 < score < 0.8)   # comparação encadeada
```

**Passo a passo:**
1. Salve como `06_2_comp.py` e rode.

**Código explicado:** Python permite encadear comparações: `a < b < c` é o mesmo que `a < b and b < c`.

### 06.3 Operadores lógicos

**O que é:** `and`, `or`, `not` combinam booleanos com avaliação curto-circuito.

**Exemplo:**

```python
renda = 8000
parcela = 2000
ltv = 0.55

aprovado = (parcela <= renda * 0.3) and (ltv <= 0.6)
print(aprovado)
print(not aprovado)
print(0 or "padrao")   # short-circuit: "padrao"
```

**Passo a passo:**
1. Salve como `06_3_logicos.py` e rode.

**Código explicado:** `or` devolve o primeiro valor truthy; útil para defaults.

### 06.4 Operadores de atribuição

**O que é:** `=` atribui; `+= -= *= /=` etc atualizam no lugar.

**Exemplo:**

```python
saldo = 1000
saldo += 500     # 1500
saldo -= 200     # 1300
saldo *= 1.1     # 1430.0
print(saldo)
```

**Passo a passo:**
1. Salve como `06_4_atrib.py` e rode.

**Código explicado:** `x += y` é equivalente a `x = x + y`, mas para tipos mutáveis pode alterar o objeto in-place.

### 06.5 Operadores de identidade

**O que é:** `is` e `is not` comparam **identidade** (mesmo objeto), não valor.

**Exemplo:**

```python
a = [1, 2]
b = [1, 2]
print(a == b)    # True (mesmo valor)
print(a is b)    # False (objetos distintos)

c = a
print(a is c)    # True
print(None is None)  # True
```

**Passo a passo:**
1. Salve como `06_5_id.py` e rode.

**Código explicado:** use `is` apenas para comparar com `None`, `True`, `False` ou para checar se duas variáveis apontam ao mesmo objeto.

### 06.6 Operadores de pertencimento

**O que é:** `in` e `not in` checam se um valor está numa coleção.

**Exemplo:**

```python
riscos = ["ltv alto", "renda baixa"]
print("ltv alto" in riscos)
print("score" not in riscos)
print("a" in "Ana")
```

**Passo a passo:**
1. Salve como `06_6_in.py` e rode.

**Código explicado:** `in` funciona com listas, tuplas, strings, dicts (chaves) e sets.

### 06.7 Operadores bit a bit

**O que é:** `& | ^ ~ << >>` operam em bits.

**Exemplo:**

```python
flags = 0b0000
LIDO     = 0b0001
APROVADO = 0b0010

flags |= LIDO        # liga bit
flags |= APROVADO    # liga outro bit
print(bin(flags))    # 0b11
print(bool(flags & APROVADO))
```

**Passo a passo:**
1. Salve como `06_7_bits.py` e rode.

**Código explicado:** `|` liga bit, `&` testa, `^` inverte; útil em flags compactas.

### 06.8 Expressão condicional ternária

**O que é:** `valor_se_verdadeiro if condicao else valor_se_falso` — escolhe valor em uma linha.

**Exemplo:**

```python
score = 0.82
status = "aprovado" if score >= 0.7 else "recusado"
print(status)
```

**Passo a passo:**
1. Salve como `06_8_ternario.py` e rode.

**Código explicado:** Python coloca a condição no meio, diferente de C/Java.

### 06.9 Precedência de operadores

**O que é:** ordem em que operadores são avaliados quando não há parênteses.

**Exemplo:**

```python
print(2 + 3 * 4)        # 14, não 20
print((2 + 3) * 4)      # 20
print(not False and True)   # True
print(2 ** 3 ** 2)      # 512 (associativo à direita)
```

**Passo a passo:**
1. Salve como `06_9_prec.py` e rode.

**Código explicado:** `*` tem precedência maior que `+`; em dúvida, **use parênteses**.

---

## 07. Strings

### 07.1 Literais de string

**O que é:** texto entre aspas simples, duplas ou triplas.

**Exemplo:**

```python
a = 'aspas simples'
b = "aspas duplas"
c = '''triplas:
multiplas linhas'''
print(a, b)
print(c)
```

**Passo a passo:**
1. Salve como `07_1_literais.py` e rode.

**Código explicado:** simples e duplas são equivalentes; triplas mantêm quebras.

### 07.2 Escape de caracteres

**O que é:** usar `\` para representar caracteres especiais.

**Exemplo:**

```python
print("linha1\nlinha2")
print("tab\tseparado")
print("aspas: \"ok\"")
print(r"sem escape: C:\Users\ana")  # raw string
```

**Passo a passo:**
1. Salve como `07_2_escape.py` e rode.

**Código explicado:** `\n` é nova linha, `\t` tab; o prefixo `r` desliga escapes.

### 07.3 F-strings

**O que é:** strings com `f"..."` que avaliam expressões dentro de `{}`.

**Exemplo:**

```python
nome = "Ana"
score = 0.823
print(f"{nome} tem score {score}")
print(f"{nome.upper()} -> {score * 100:.1f}%")
print(f"{nome=} {score=}")  # debug
```

**Passo a passo:**
1. Salve como `07_3_fstring.py` e rode.

**Código explicado:** `{var=}` imprime `var=valor`, ótimo para debug.

### 07.4 Formatação de valores

**O que é:** usar mini-linguagem dentro de `{}` para controlar largura, casas decimais, percentual, etc.

**Exemplo:**

```python
valor = 12345.6789
print(f"{valor:.2f}")        # 12345.68
print(f"{valor:,.2f}")       # 12,345.68
print(f"{0.82:.0%}")         # 82%
print(f"{'Ana':>10}")        # alinhado à direita
print(f"{42:08d}")           # 00000042
```

**Passo a passo:**
1. Salve como `07_4_format.py` e rode.

**Código explicado:** `.2f` casas decimais, `,` separador de milhar, `%` percentual, `>10` largura.

### 07.5 Indexação de strings

**O que é:** acessar caractere por posição (0-based; índice negativo conta do fim).

**Exemplo:**

```python
nome = "Ana Silva"
print(nome[0])    # A
print(nome[-1])   # a
print(nome[4])    # S
```

**Passo a passo:**
1. Salve como `07_5_index.py` e rode.

**Código explicado:** strings são sequências; cada caractere é também uma string de tamanho 1.

### 07.6 Slicing de strings

**O que é:** pegar pedaços com `[inicio:fim:passo]`.

**Exemplo:**

```python
nome = "Ana Silva"
print(nome[:3])      # Ana
print(nome[4:])      # Silva
print(nome[::-1])    # invertido
print(nome[::2])     # pular de 2 em 2
```

**Passo a passo:**
1. Salve como `07_6_slice.py` e rode.

**Código explicado:** `fim` é exclusivo; passo negativo inverte.

### 07.7 Strings multilinha

**O que é:** texto longo entre `"""..."""` mantendo quebras.

**Exemplo:**

```python
relatorio = """
Cliente: Ana
Score:   0.82
Status:  aprovado
""".strip()
print(relatorio)
```

**Passo a passo:**
1. Salve como `07_7_multi.py` e rode.

**Código explicado:** `.strip()` remove espaços e quebras nas pontas.

### 07.8 Strings como objetos imutáveis

**O que é:** métodos de string nunca alteram o original; sempre retornam nova string.

**Exemplo:**

```python
nome = "ana"
maiuscula = nome.upper()
print(nome)        # ana (intacto)
print(maiuscula)   # ANA
print(id(nome) != id(maiuscula))
```

**Passo a passo:**
1. Salve como `07_8_imut.py` e rode.

**Código explicado:** se quiser guardar a alteração, **atribua o retorno** a uma variável.

---

## 08. Estruturas de dados

### 08.1 list

**O que é:** sequência ordenada e mutável.

**Exemplo:**

```python
clientes = ["Ana", "Bruno", "Carla"]
clientes.append("Diego")
clientes.remove("Bruno")
print(clientes)
print(len(clientes))
```

**Passo a passo:**
1. Salve como `08_1_list.py` e rode.

**Código explicado:** `append` adiciona, `remove` retira pelo valor; aceita itens de qualquer tipo.

### 08.2 tuple

**O que é:** sequência ordenada e **imutável**.

**Exemplo:**

```python
ponto = (10, 20)
registro = ("Ana", 35, "aprovado")
print(ponto[0], registro[2])
# ponto[0] = 99   # TypeError: tuple não permite alteração
```

**Passo a passo:**
1. Salve como `08_2_tuple.py` e rode.

**Código explicado:** use tuple para registros fixos; é mais rápida e segura.

### 08.3 dict

**O que é:** mapeamento chave→valor, ordenado por inserção.

**Exemplo:**

```python
simulacao = {"cliente": "Ana", "valor": 120000, "score": 0.82}
print(simulacao["cliente"])
simulacao["status"] = "aprovado"
print(simulacao.get("origem", "site"))  # default
print(list(simulacao.keys()))
```

**Passo a passo:**
1. Salve como `08_3_dict.py` e rode.

**Código explicado:** `[]` lança erro se a chave não existe; `.get` retorna default.

### 08.4 set

**O que é:** conjunto não ordenado de itens **únicos**.

**Exemplo:**

```python
riscos_a = {"ltv", "renda"}
riscos_b = {"renda", "score"}
print(riscos_a | riscos_b)   # união
print(riscos_a & riscos_b)   # interseção
print(riscos_a - riscos_b)   # diferença
```

**Passo a passo:**
1. Salve como `08_4_set.py` e rode.

**Código explicado:** sets são ótimos para deduplicar e fazer operações de conjunto.

### 08.5 frozenset

**O que é:** versão **imutável** de set; pode ser chave de dict.

**Exemplo:**

```python
permissoes = frozenset({"ler", "escrever"})
cache = {permissoes: "perfil padrão"}
print(cache[permissoes])
# permissoes.add("admin")   # AttributeError
```

**Passo a passo:**
1. Salve como `08_5_frozen.py` e rode.

**Código explicado:** por ser imutável, tem hash; pode ser usado como chave.

### 08.6 Indexação de coleções

**O que é:** acessar item por posição em listas/tuples e por chave em dicts.

**Exemplo:**

```python
clientes = ["Ana", "Bruno", "Carla"]
print(clientes[0], clientes[-1])

simulacao = {"cliente": "Ana", "valor": 120000}
print(simulacao["cliente"])
```

**Passo a passo:**
1. Salve como `08_6_idx.py` e rode.

**Código explicado:** sequência usa inteiro; dict usa chave (string, int, tuple imutável).

### 08.7 Slicing de listas

**O que é:** mesmo `[i:f:p]` das strings, agora retornando lista nova.

**Exemplo:**

```python
valores = [10, 20, 30, 40, 50]
print(valores[1:4])     # [20, 30, 40]
print(valores[::-1])    # invertido
print(valores[::2])     # de 2 em 2
copia = valores[:]      # cópia rasa
print(copia)
```

**Passo a passo:**
1. Salve como `08_7_slice.py` e rode.

**Código explicado:** `[:]` é a forma rápida de fazer cópia rasa.

### 08.8 Chaves e valores em dicionários

**O que é:** `dict.keys()`, `dict.values()`, `dict.items()` retornam views iteráveis.

**Exemplo:**

```python
simulacao = {"cliente": "Ana", "valor": 120000}
for chave, valor in simulacao.items():
    print(chave, "->", valor)
print(list(simulacao.values()))
```

**Passo a passo:**
1. Salve como `08_8_kv.py` e rode.

**Código explicado:** `items()` é a forma idiomática de iterar pares.

### 08.9 Mutabilidade em coleções

**O que é:** listas, dicts e sets são mutáveis; cuidado com aliasing.

**Exemplo:**

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)   # [1, 2, 3, 4]

import copy
c = copy.copy(a)
c.append(99)
print(a)   # [1, 2, 3, 4]  -- inalterado
```

**Passo a passo:**
1. Salve como `08_9_mut.py` e rode.

**Código explicado:** `b = a` compartilha a referência; `copy.copy` cria objeto separado.

### 08.10 Cópia rasa e cópia profunda

**O que é:** rasa copia o objeto externo; profunda copia tudo recursivamente.

**Exemplo:**

```python
import copy

original = {"riscos": ["ltv", "renda"]}
rasa = copy.copy(original)
profunda = copy.deepcopy(original)

rasa["riscos"].append("novo")
print(original["riscos"])    # afetado!
profunda["riscos"].append("outro")
print(original["riscos"])    # não afetado
```

**Passo a passo:**
1. Salve como `08_10_deep.py` e rode.

**Código explicado:** quando há objetos dentro de objetos, só `deepcopy` isola completamente.

---

## 09. Desempacotamento e combinação de dados

### 09.1 Desempacotamento de tuplas

**O que é:** atribuir vários nomes a partir de uma tupla numa única linha.

**Exemplo:**

```python
ponto = (10, 20)
x, y = ponto
print(x, y)

a, b = b, a = 1, 2  # swap
print(a, b)
```

**Passo a passo:**
1. Salve como `09_1_tuple.py` e rode.

**Código explicado:** o swap funciona porque Python avalia o lado direito primeiro como tupla.

### 09.2 Desempacotamento de listas

**O que é:** mesma ideia, agora com listas.

**Exemplo:**

```python
clientes = ["Ana", "Bruno", "Carla"]
primeiro, segundo, terceiro = clientes
print(primeiro, terceiro)

primeiro, *resto = clientes
print(primeiro, resto)
```

**Passo a passo:**
1. Salve como `09_2_list.py` e rode.

**Código explicado:** `*resto` captura todos os itens restantes em uma lista.

### 09.3 Desempacotamento de dicionários

**O que é:** dict não desempacota direto em variáveis, mas sim via `.items()` ou `**`.

**Exemplo:**

```python
simulacao = {"cliente": "Ana", "valor": 120000}

for chave, valor in simulacao.items():
    print(chave, valor)

def imprimir(cliente, valor):
    print(cliente, valor)

imprimir(**simulacao)  # passa cada chave como kwarg
```

**Passo a passo:**
1. Salve como `09_3_dict.py` e rode.

**Código explicado:** `**dict` espalha pares chave=valor como argumentos nomeados.

### 09.4 Operador `*`

**O que é:** espalha iterável em chamadas e atribuições.

**Exemplo:**

```python
nums = [1, 2, 3]
print(sum([*nums, 4, 5]))   # 15

a, *meio, b = [1, 2, 3, 4, 5]
print(a, meio, b)            # 1 [2, 3, 4] 5
```

**Passo a passo:**
1. Salve como `09_4_star.py` e rode.

**Código explicado:** `*` em literais espalha; em alvo de atribuição, captura.

### 09.5 Operador `**`

**O que é:** espalha dicionário em chamadas ou em outros dicionários.

**Exemplo:**

```python
base = {"status": "pendente"}
extra = {"cliente": "Ana"}
combinado = {**base, **extra}
print(combinado)

def f(cliente, status):
    print(cliente, status)

f(**combinado)
```

**Passo a passo:**
1. Salve como `09_5_dstar.py` e rode.

**Código explicado:** `**` em dicionários funde; em chamadas, vira kwargs.

### 09.6 Merge de dicionários

**O que é:** combinar dois dicts; chave repetida fica com o último valor.

**Exemplo:**

```python
defaults = {"timeout": 5, "retries": 3}
config   = {"retries": 10, "host": "api"}

merged = {**defaults, **config}
print(merged)
# Python 3.9+: defaults | config
print(defaults | config)
```

**Passo a passo:**
1. Salve como `09_6_merge.py` e rode.

**Código explicado:** o `|` em dicts (Python 3.9+) é uma forma curta para o mesmo merge.

### 09.7 Argumentos nomeados por dicionário

**O que é:** passar opções de configuração de uma vez via `**dict`.

**Exemplo:**

```python
def conectar(host, porta, timeout=5):
    print(f"{host}:{porta} t={timeout}")

opcoes = {"host": "api", "porta": 8080, "timeout": 30}
conectar(**opcoes)
```

**Passo a passo:**
1. Salve como `09_7_kwargs.py` e rode.

**Código explicado:** as chaves do dict precisam **bater** com os nomes dos parâmetros.

---

## 10. Comprehensions e expressões geradoras

### 10.1 List comprehension

**O que é:** monta lista em uma linha: `[expr for item in iter]`.

**Exemplo:**

```python
valores = [80000, 120000, 95000]
dobrados = [v * 2 for v in valores]
print(dobrados)
```

**Passo a passo:**
1. Salve como `10_1_list.py` e rode.

**Código explicado:** lê-se "para cada `v` em `valores`, gere `v * 2`".

### 10.2 Dict comprehension

**O que é:** monta dict em uma linha: `{k: v for ... in ...}`.

**Exemplo:**

```python
clientes = ["Ana", "Bruno"]
mapa = {nome: len(nome) for nome in clientes}
print(mapa)
```

**Passo a passo:**
1. Salve como `10_2_dict.py` e rode.

**Código explicado:** cria pares calculados a partir do iterável.

### 10.3 Set comprehension

**O que é:** monta set em uma linha; remove duplicados automaticamente.

**Exemplo:**

```python
palavras = ["renda", "ltv", "renda", "score"]
unicas = {p.upper() for p in palavras}
print(unicas)
```

**Passo a passo:**
1. Salve como `10_3_set.py` e rode.

**Código explicado:** o resultado é um set, então repetidos somem.

### 10.4 Generator expression

**O que é:** sintaxe igual a list comp mas com `()`; gera valores sob demanda.

**Exemplo:**

```python
valores = [100, 200, 300, 400]
gen = (v * 2 for v in valores)
print(next(gen))
print(next(gen))
print(sum(v * 2 for v in valores))
```

**Passo a passo:**
1. Salve como `10_4_gen.py` e rode.

**Código explicado:** ocupa pouca memória; ideal quando você só precisa iterar uma vez.

### 10.5 Filtros em comprehensions

**O que é:** adicionar `if` ao final para filtrar.

**Exemplo:**

```python
valores = [80000, 120000, 95000, 200000]
altos = [v for v in valores if v > 100000]
pares_altos = {v: v * 0.01 for v in valores if v > 100000}
print(altos)
print(pares_altos)
```

**Passo a passo:**
1. Salve como `10_5_filtro.py` e rode.

**Código explicado:** o `if` decide quais itens entram no resultado.

### 10.6 Comprehensions aninhadas

**O que é:** usar mais de um `for` para iterar matrizes ou produtos cartesianos.

**Exemplo:**

```python
matriz = [[1, 2, 3], [4, 5, 6]]
plana = [v for linha in matriz for v in linha]
print(plana)

pares = [(a, b) for a in [1, 2] for b in ["x", "y"]]
print(pares)
```

**Passo a passo:**
1. Salve como `10_6_aninhada.py` e rode.

**Código explicado:** a ordem dos `for` é a mesma de loops aninhados.

---

## 11. Controle de fluxo

### 11.1 if

**O que é:** roda bloco se a condição for verdadeira.

**Exemplo:**

```python
score = 0.82
if score >= 0.7:
    print("aprovado")
```

**Passo a passo:**
1. Salve como `11_1_if.py` e rode.

**Código explicado:** o bloco indentado roda apenas quando a expressão é truthy.

### 11.2 elif

**O que é:** condição alternativa após `if`.

**Exemplo:**

```python
score = 0.65
if score >= 0.8:
    print("alto")
elif score >= 0.6:
    print("médio")
elif score >= 0.4:
    print("baixo")
```

**Passo a passo:**
1. Salve como `11_2_elif.py` e rode.

**Código explicado:** Python testa em ordem; o primeiro `True` ganha.

### 11.3 else

**O que é:** bloco executado quando nenhum `if/elif` foi verdadeiro.

**Exemplo:**

```python
score = 0.3
if score >= 0.7:
    print("aprovado")
else:
    print("recusado")
```

**Passo a passo:**
1. Salve como `11_3_else.py` e rode.

**Código explicado:** `else` não tem condição; é o "caso restante".

### 11.4 match e case

**O que é:** estrutura de pattern matching (Python 3.10+).

**Exemplo:**

```python
status = "aprovado"
match status:
    case "aprovado":
        print("liberar contrato")
    case "pendente":
        print("aguardar análise")
    case _:
        print("status desconhecido")
```

**Passo a passo:**
1. Salve como `11_4_match.py` e rode.

**Código explicado:** `_` é o padrão default; cobre qualquer caso.

### 11.5 for

**O que é:** percorre iterável.

**Exemplo:**

```python
for cliente in ["Ana", "Bruno", "Carla"]:
    print(cliente)

for i in range(3):
    print(i)
```

**Passo a passo:**
1. Salve como `11_5_for.py` e rode.

**Código explicado:** `range(3)` gera `0, 1, 2`.

### 11.6 while

**O que é:** repete enquanto condição for verdadeira.

**Exemplo:**

```python
saldo = 1000
mes = 0
while saldo > 0:
    saldo -= 250
    mes += 1
print(f"acabou no mês {mes}")
```

**Passo a passo:**
1. Salve como `11_6_while.py` e rode.

**Código explicado:** lembre-se de garantir progresso para evitar loop infinito.

### 11.7 break

**O que é:** sai do loop imediatamente.

**Exemplo:**

```python
for tentativa in range(1, 11):
    if tentativa == 4:
        print("achou na", tentativa)
        break
```

**Passo a passo:**
1. Salve como `11_7_break.py` e rode.

**Código explicado:** após o `break`, o loop é abandonado por completo.

### 11.8 continue

**O que é:** pula para a próxima iteração do loop.

**Exemplo:**

```python
for n in range(1, 6):
    if n % 2 == 0:
        continue
    print(n)
```

**Passo a passo:**
1. Salve como `11_8_continue.py` e rode.

**Código explicado:** quando `n` é par, o `continue` pula o `print`.

### 11.9 pass

**O que é:** instrução nula; ocupa espaço sintático.

**Exemplo:**

```python
def funcao_a_implementar():
    pass

class TodoModelar:
    pass

print("ok")
```

**Passo a passo:**
1. Salve como `11_9_pass.py` e rode.

**Código explicado:** útil para deixar bloco vazio sem dar erro de sintaxe.

### 11.10 else em loops

**O que é:** bloco que roda se o loop terminar **sem** `break`.

**Exemplo:**

```python
for n in range(5):
    if n == 99:
        break
else:
    print("não encontrou 99")

for n in range(5):
    if n == 2:
        break
else:
    print("não roda, pois houve break")
```

**Passo a passo:**
1. Salve como `11_10_else.py` e rode.

**Código explicado:** combinação rara mas útil em buscas: "vasculhei tudo e não achei".

---

## 12. Funções

### 12.1 def

**O que é:** palavra-chave para definir função.

**Exemplo:**

```python
def saudacao(nome):
    return f"Olá, {nome}"

print(saudacao("Ana"))
```

**Passo a passo:**
1. Salve como `12_1_def.py` e rode.

**Código explicado:** `def` cria objeto função com nome; pode ser chamada quantas vezes quiser.

### 12.2 Parâmetros posicionais

**O que é:** valores passados na ordem dos parâmetros.

**Exemplo:**

```python
def calcular_ltv(imovel, solicitado):
    return solicitado / imovel

print(calcular_ltv(300000, 150000))
```

**Passo a passo:**
1. Salve como `12_2_pos.py` e rode.

**Código explicado:** a ordem importa: `imovel` recebe `300000` e `solicitado` recebe `150000`.

### 12.3 Parâmetros nomeados

**O que é:** passar valor citando o nome do parâmetro.

**Exemplo:**

```python
def calcular_ltv(imovel, solicitado):
    return solicitado / imovel

print(calcular_ltv(solicitado=150000, imovel=300000))
```

**Passo a passo:**
1. Salve como `12_3_nom.py` e rode.

**Código explicado:** com nomes, a ordem da chamada deixa de importar e o código fica mais legível.

### 12.4 Valores padrão

**O que é:** parâmetro com valor default usado quando o caller não passa.

**Exemplo:**

```python
def calcular_ltv(imovel, solicitado, limite=0.6):
    return solicitado / imovel <= limite

print(calcular_ltv(300000, 150000))
print(calcular_ltv(300000, 200000, limite=0.5))
```

**Passo a passo:**
1. Salve como `12_4_default.py` e rode.

**Código explicado:** parâmetros com default precisam vir **depois** dos sem default.

### 12.5 Parâmetros keyword-only

**O que é:** parâmetros que **só** podem ser passados por nome; ficam após `*`.

**Exemplo:**

```python
def aprovar(cliente, *, limite=0.6, ltv):
    return ltv <= limite

print(aprovar("Ana", ltv=0.55))
# aprovar("Ana", 0.55)  # TypeError
```

**Passo a passo:**
1. Salve como `12_5_kwonly.py` e rode.

**Código explicado:** o `*` sozinho marca o início dos keyword-only; obriga clareza nos chamadores.

### 12.6 Parâmetros positional-only

**O que é:** parâmetros que **só** podem ser passados por posição; ficam antes de `/`.

**Exemplo:**

```python
def dividir(a, b, /):
    return a / b

print(dividir(10, 2))
# dividir(a=10, b=2)  # TypeError
```

**Passo a passo:**
1. Salve como `12_6_posonly.py` e rode.

**Código explicado:** útil para esconder o nome do parâmetro como detalhe interno.

### 12.7 *args

**O que é:** captura número variável de argumentos posicionais como tupla.

**Exemplo:**

```python
def somar(*valores):
    return sum(valores)

print(somar(10, 20, 30, 40))
print(somar(*[1, 2, 3]))
```

**Passo a passo:**
1. Salve como `12_7_args.py` e rode.

**Código explicado:** dentro da função, `valores` é uma tupla com tudo que veio.

### 12.8 **kwargs

**O que é:** captura argumentos nomeados extras como dict.

**Exemplo:**

```python
def registrar(cliente, **extras):
    print(cliente, extras)

registrar("Ana", origem="site", canal="mobile")
```

**Passo a passo:**
1. Salve como `12_8_kwargs.py` e rode.

**Código explicado:** `extras` é um dict com tudo que não casou com parâmetros nomeados.

### 12.9 return

**O que é:** devolve um valor (ou tupla) ao caller e encerra a função.

**Exemplo:**

```python
def calcular(valor, meses):
    parcela = valor / meses
    return parcela, parcela * 1.1

p, p_juros = calcular(120000, 12)
print(p, p_juros)
```

**Passo a passo:**
1. Salve como `12_9_return.py` e rode.

**Código explicado:** `return a, b` devolve uma tupla, fácil de desempacotar.

### 12.10 Retorno implícito None

**O que é:** sem `return`, a função devolve `None`.

**Exemplo:**

```python
def imprimir(msg):
    print(msg)

retorno = imprimir("oi")
print(retorno)   # None
```

**Passo a passo:**
1. Salve como `12_10_none.py` e rode.

**Código explicado:** funções sem `return` ainda retornam algo: `None`.

### 12.11 Funções aninhadas

**O que é:** uma função definida dentro de outra; só visível no escopo da função externa.

**Exemplo:**

```python
def aprovar(score):
    def explicar(s):
        return f"score {s} avaliado"
    return explicar(score)

print(aprovar(0.82))
```

**Passo a passo:**
1. Salve como `12_11_aninhada.py` e rode.

**Código explicado:** a função interna pode ler variáveis da externa.

### 12.12 Closures

**O que é:** função interna que **lembra** do estado da função externa, mesmo após ela retornar.

**Exemplo:**

```python
def make_multiplier(fator):
    def aplicar(x):
        return x * fator
    return aplicar

dobro = make_multiplier(2)
triplo = make_multiplier(3)
print(dobro(10), triplo(10))
```

**Passo a passo:**
1. Salve como `12_12_closure.py` e rode.

**Código explicado:** `aplicar` carrega consigo o `fator` capturado.

### 12.13 Lambda

**O que é:** função anônima curta de uma única expressão.

**Exemplo:**

```python
quadrado = lambda x: x * x
print(quadrado(5))

valores = [1, -2, 3, -4]
print(sorted(valores, key=lambda v: abs(v)))
```

**Passo a passo:**
1. Salve como `12_13_lambda.py` e rode.

**Código explicado:** ótimo para passar como argumento (`key=`); evite para lógicas grandes.

### 12.14 Recursão

**O que é:** função que chama a si mesma; precisa de caso base.

**Exemplo:**

```python
def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)

print(fatorial(5))   # 120
```

**Passo a passo:**
1. Salve como `12_14_rec.py` e rode.

**Código explicado:** sem caso base, recursão estoura a pilha (`RecursionError`).

---

## 13. Módulos, pacotes e imports

### 13.1 import

**O que é:** carrega um módulo inteiro; o uso fica `modulo.funcao`.

**Exemplo:**

```python
import math

print(math.sqrt(81))
print(math.pi)
```

**Passo a passo:**
1. Salve como `13_1_import.py` e rode.

**Código explicado:** `math` é um módulo da stdlib; precisa do prefixo para acessar membros.

### 13.2 from import

**O que é:** importa nomes específicos do módulo, sem o prefixo.

**Exemplo:**

```python
from math import sqrt, pi

print(sqrt(81), pi)
```

**Passo a passo:**
1. Salve como `13_2_fromimport.py` e rode.

**Código explicado:** importa só o que vai usar; deixa o código mais curto.

### 13.3 Alias com `as`

**O que é:** a palavra-chave `as` nos imports permite **renomear** o que está sendo importado. O nome original continua existindo no módulo de origem, mas dentro do seu arquivo você usa o apelido (alias).

**Por que usar:**
- **Nomes longos** — encurtar para digitar menos.
- **Conflito de nomes** — dois módulos com funções de mesmo nome.
- **Convenção da comunidade** — algumas bibliotecas têm aliases padrão que todo mundo usa.

---

#### Exemplo 1 — alias de módulo inteiro

```python
import math as m
import datetime as dt

print(m.pi)                    # 3.141592653589793
print(m.sqrt(144))             # 12.0
print(dt.date.today())         # 2026-04-28
```

Sem o `as`, você teria que escrever `math.pi` e `datetime.date.today()`. Com o alias, fica mais curto.

---

#### Exemplo 2 — alias de item específico

```python
from math import sqrt as raiz
from math import factorial as fatorial

print(raiz(81))       # 9.0
print(fatorial(5))    # 120
```

Aqui só a função importada ganha alias; o módulo `math` em si não fica acessível.

---

#### Exemplo 3 — aliases convencionais da comunidade

```python
# estes aliases são padrão — qualquer pessoa de Python reconhece
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

# usar:
# np.array([1, 2, 3])
# pd.DataFrame({"col": [1, 2]})
# plt.plot([1, 2, 3])
```

> **Importante:** use os aliases convencionais. Se todo mundo usa `np` para numpy e você usa `n`, o código fica confuso para o time.

---

#### Exemplo 4 — resolvendo conflito de nomes

```python
# dois módulos têm função "calcular"
from credito.score import calcular as calcular_score
from credito.parcela import calcular as calcular_parcela

print(calcular_score(renda=8000, dividas=2000))
print(calcular_parcela(valor=120000, meses=120))
```

Sem o `as`, o segundo `import` sobrescreveria o primeiro — ambos se chamam `calcular`. O alias resolve isso.

---

#### Exemplo 5 — alias em `with` e `except`

A palavra `as` também aparece fora de imports:

```python
# no with — dá nome ao recurso
with open("dados.txt", "r", encoding="utf-8") as arquivo:
    print(arquivo.read())

# no except — dá nome à exceção
try:
    int("abc")
except ValueError as erro:
    print(f"falhou: {erro}")
```

> Esses usos são cobertos em detalhes nas seções 14.3 e 15.2.

---

**Passo a passo:**
1. Salve os exemplos 1 e 2 como `13_3_alias.py` e rode.
2. Teste digitar `math.pi` sem o `import math` (só com `import math as m`) — dá `NameError` porque o nome original não existe no seu arquivo, só o alias.
3. Teste o exemplo 4 para ver o conflito resolvido.

**Código explicado:** `as` cria um apelido local para o que foi importado. O módulo original não muda — só o nome que você usa no seu código. É útil para encurtar, desambiguar e seguir convenções.

### 13.4 Imports absolutos

**O que é:** caminho completo a partir da raiz do projeto/pacote.

**Exemplo:**

```python
# estrutura:
# app/__init__.py
# app/credito/__init__.py
# app/credito/calculos.py
# main.py

# em main.py:
from app.credito.calculos import parcela
print(parcela(120000, 12))
```

**Passo a passo:**
1. Crie a estrutura acima.
2. Em `calculos.py` defina `def parcela(v, m): return v / m`.
3. Rode `python main.py`.

**Código explicado:** import absoluto não depende da posição relativa do arquivo.

### 13.5 Imports relativos

**O que é:** import baseado na posição do módulo atual: `.modulo` (mesma pasta), `..modulo` (pasta acima).

**Exemplo:**

```python
# em app/credito/api.py
from .calculos import parcela
from ..config import VERSAO
```

**Passo a passo:**
1. Coloque `api.py` ao lado de `calculos.py` dentro de `app/credito/`.
2. Rode pelo módulo: `python -m app.credito.api`.

**Código explicado:** relativo só funciona dentro de pacotes; com `python arquivo.py` direto, falha.

### 13.6 Imports locais

**O que é:** import feito dentro de função, atrasando o carregamento.

**Exemplo:**

```python
def relatorio_pesado():
    import csv  # importado só quando a função é chamada
    print(csv.__name__)

print("antes")
relatorio_pesado()
```

**Passo a passo:**
1. Salve como `13_6_local.py` e rode.

**Código explicado:** evita custo de import se a função nunca é chamada e quebra ciclos.

### 13.7 Imports circulares

**O que é:** dois módulos importando um ao outro; pode dar `ImportError`.

**Exemplo:**

```python
# a.py
# from b import valor_b
# valor_a = 1

# b.py
# from a import valor_a   # quebra
# valor_b = 2

# solução: import local ou reorganizar
def usar_b():
    from b import valor_b
    return valor_b
```

**Passo a passo:**
1. Reproduza com dois arquivos `a.py` e `b.py` referenciando o outro no topo.
2. Veja `ImportError`.
3. Mova o `import` para dentro da função.

**Código explicado:** import locais quebram o ciclo; reorganizar o design é a melhor solução.

### 13.8 Namespace de módulo

**O que é:** cada módulo tem seu próprio espaço de nomes; nada vaza para fora.

**Exemplo:**

```python
# arquivo: utils.py
TAXA = 0.05
def aplicar(v): return v * (1 + TAXA)
```

```python
# arquivo: 13_8_ns.py
import utils

print(utils.TAXA)
print(utils.__name__)
print(dir(utils))
```

**Passo a passo:**
1. Crie `utils.py` e `13_8_ns.py` no mesmo diretório.
2. Rode `python 13_8_ns.py`.

**Código explicado:** `dir(modulo)` lista tudo que está no namespace do módulo.

### 13.9 __all__

**O que é:** lista que define quais nomes são exportados em `from modulo import *`.

**Exemplo:**

```python
# arquivo: api.py
__all__ = ["publica"]

def publica(): return "ok"
def _interna(): return "secreta"
```

```python
# arquivo: 13_9_all.py
from api import *

print(publica())
# print(_interna())  # NameError
```

**Passo a passo:**
1. Crie `api.py` e `13_9_all.py`.
2. Rode `python 13_9_all.py`.

**Código explicado:** `__all__` controla a API pública do módulo para `import *`.

---

## 14. Exceções

### 14.1 try

**O que é:** marca um bloco onde erros podem acontecer e devem ser tratados.

**Exemplo:**

```python
try:
    resultado = 10 / 0
except ZeroDivisionError:
    resultado = 0
print(resultado)
```

**Passo a passo:**
1. Salve como `14_1_try.py` e rode.

**Código explicado:** se a divisão der erro, o `except` assume e o programa segue.

### 14.2 except

**O que é:** captura um tipo específico de exceção.

**Exemplo:**

```python
try:
    int("abc")
except ValueError:
    print("não é número")
except TypeError:
    print("tipo errado")
```

**Passo a passo:**
1. Salve como `14_2_except.py` e rode.

**Código explicado:** vários `except` permitem tratar tipos diferentes separadamente.

### 14.3 `except as` — capturando a exceção numa variável

**O que é:** quando você escreve `except TipoErro as e`, o Python captura a **instância da exceção** e atribui ao nome `e`. Com isso, você pode inspecionar a mensagem de erro, o tipo, os argumentos e até a cadeia de exceções.

**Por que usar:**
- **Logar o erro** com detalhes (mensagem, tipo, traceback).
- **Reprogar o erro** após registrar informações.
- **Tomar decisões** diferentes dependendo da mensagem do erro.
- **Encadear exceções** com `raise ... from e`.

---

#### Exemplo 1 — inspecionando a exceção

```python
try:
    int("abc")
except ValueError as e:
    print("mensagem:", e)                    # invalid literal for int()...
    print("tipo:", type(e).__name__)         # ValueError
    print("args:", e.args)                   # ('invalid literal...',)
    print("repr:", repr(e))                  # ValueError("invalid literal...")
```

O objeto `e` é uma instância da classe `ValueError`. Ele carrega:
- `e.args` — tupla com os argumentos passados ao construtor da exceção.
- `str(e)` ou `print(e)` — a mensagem legível.
- `type(e)` — a classe da exceção.
- `repr(e)` — representação completa com o nome da classe.

---

#### Exemplo 2 — logando e repropagando

```python
import logging

logging.basicConfig(level=logging.ERROR)

def processar_valor(texto):
    try:
        return float(texto)
    except ValueError as e:
        logging.error(f"valor inválido '{texto}': {e}")
        raise  # repropaga a mesma exceção com o traceback original

try:
    processar_valor("abc")
except ValueError:
    print("erro tratado no nível superior")
```

> **`raise` sem argumentos** dentro do `except` repropaga a exceção original com o traceback completo. Nunca faça `raise e` — isso recria o traceback a partir deste ponto.

---

#### Exemplo 3 — tratando vários tipos com `as`

```python
def converter(valor):
    try:
        return int(valor)
    except (ValueError, TypeError) as e:
        print(f"erro ao converter {valor!r}: {type(e).__name__}: {e}")
        return None

print(converter("42"))       # 42
print(converter("abc"))      # erro... ValueError → None
print(converter(None))       # erro... TypeError → None
print(converter([1, 2]))     # erro... TypeError → None
```

Ao capturar vários tipos numa tupla, o `as e` recebe qualquer um deles. Use `type(e).__name__` para saber qual tipo caiu ali.

---

#### Exemplo 4 — encadeamento de exceções com `from`

```python
def buscar_cliente(id_cliente):
    clientes = {"1": "Ana", "2": "Bruno"}
    try:
        return clientes[id_cliente]
    except KeyError as e:
        raise ValueError(f"cliente {id_cliente} não encontrado") from e

try:
    buscar_cliente("99")
except ValueError as e:
    print(f"erro: {e}")
    print(f"causa original: {e.__cause__}")  # KeyError('99')
```

O `raise ... from e` liga a nova exceção à original. Quando o traceback aparece, Python mostra as duas:
```
KeyError: '99'
The above exception was the direct cause of the following exception:
ValueError: cliente 99 não encontrado
```

---

#### Exemplo 5 — a variável `e` é deletada ao sair do `except`

```python
try:
    1 / 0
except ZeroDivisionError as e:
    erro = str(e)  # salve o que precisa ANTES de sair do bloco

# print(e)  # NameError! O Python deleta 'e' ao sair do except
print(erro)  # "division by zero" — funciona porque salvamos em outra variável
```

> **Cuidado:** o Python **deleta** a variável do `as` ao sair do bloco `except` para evitar referências circulares com o traceback. Se precisar do valor depois, copie para outra variável dentro do bloco.

---

#### Exemplo 6 — exceção personalizada com atributos extras

```python
class ErroCredito(Exception):
    def __init__(self, mensagem, codigo, cliente):
        super().__init__(mensagem)
        self.codigo = codigo
        self.cliente = cliente

try:
    raise ErroCredito("score insuficiente", codigo=403, cliente="Ana")
except ErroCredito as e:
    print(f"erro: {e}")              # score insuficiente
    print(f"código: {e.codigo}")     # 403
    print(f"cliente: {e.cliente}")   # Ana
```

Com `as e` você acessa todos os atributos personalizados da exceção, não só a mensagem.

---

**Passo a passo:**
1. Salve o exemplo 1 como `14_3_except_as.py` e rode.
2. Teste o exemplo 5 — tente acessar `e` fora do bloco `except` e veja o `NameError`.
3. Teste o exemplo 4 para ver o encadeamento no traceback.

**Código explicado:** `as e` dá nome à exceção capturada, permitindo inspecionar mensagem, tipo, argumentos e causa original. A variável é deletada ao sair do `except`, então copie o que precisar antes de sair do bloco.

### 14.4 else em exceções

**O que é:** bloco que roda **se não** houve exceção.

**Exemplo:**

```python
try:
    valor = int("42")
except ValueError:
    print("erro")
else:
    print("ok:", valor)
```

**Passo a passo:**
1. Salve como `14_4_else.py` e rode.

**Código explicado:** isola lógica que só faz sentido após o `try` ter sucesso.

### 14.5 finally

**O que é:** bloco que **sempre** roda, com ou sem erro.

**Exemplo:**

```python
try:
    print("processando")
    raise RuntimeError("falha")
except RuntimeError:
    print("erro tratado")
finally:
    print("liberando recursos")
```

**Passo a passo:**
1. Salve como `14_5_finally.py` e rode.

**Código explicado:** ideal para liberar conexão, fechar arquivo etc.

### 14.6 raise

**O que é:** lança uma exceção manualmente.

**Exemplo:**

```python
def calcular_parcela(v, m):
    if m <= 0:
        raise ValueError("meses deve ser > 0")
    return v / m

try:
    calcular_parcela(100, 0)
except ValueError as e:
    print(e)
```

**Passo a passo:**
1. Salve como `14_6_raise.py` e rode.

**Código explicado:** valide entradas e lance erro descritivo cedo.

### 14.7 Repropagação de exceções

**O que é:** logar e relançar para a camada superior.

**Exemplo:**

```python
try:
    int("abc")
except ValueError:
    print("logando antes de subir")
    raise   # relança a mesma exceção
```

**Passo a passo:**
1. Salve como `14_7_reraise.py` e rode (vai mostrar traceback no fim).

**Código explicado:** `raise` sem argumento relança a exceção atual.

### 14.8 Encadeamento de exceções

**O que é:** lançar nova exceção mantendo a original via `raise X from y`.

**Exemplo:**

```python
class CreditoError(Exception):
    pass

try:
    int("abc")
except ValueError as e:
    raise CreditoError("entrada inválida") from e
```

**Passo a passo:**
1. Salve como `14_8_chain.py` e rode.
2. Veja "The above exception was the direct cause...".

**Código explicado:** `from e` preserva a causa raiz no traceback.

### 14.9 Exceções customizadas

**O que é:** classe que herda de `Exception` para domínio específico.

**Exemplo:**

```python
class ScoreInsuficiente(Exception):
    def __init__(self, score):
        super().__init__(f"score {score} abaixo do mínimo")
        self.score = score

try:
    raise ScoreInsuficiente(0.4)
except ScoreInsuficiente as e:
    print(e, e.score)
```

**Passo a passo:**
1. Salve como `14_9_custom.py` e rode.

**Código explicado:** exceções próprias deixam a intenção clara no domínio.

### 14.10 SystemExit

**O que é:** exceção especial usada por `sys.exit()` para terminar o programa.

**Exemplo:**

```python
import sys

try:
    sys.exit(2)
except SystemExit as e:
    print("saindo com código", e.code)
```

**Passo a passo:**
1. Salve como `14_10_sysexit.py` e rode.

**Código explicado:** `SystemExit` herda de `BaseException`, não de `Exception`; `except Exception` não a captura.

---

## 15. Context managers

Context managers são o mecanismo do Python para **garantir que um recurso seja liberado** (arquivo fechado, conexão encerrada, lock liberado) mesmo que ocorra um erro no meio do caminho. O comando `with` é a porta de entrada.

### 15.1 with — o problema que ele resolve

**O que é:** o `with` é um bloco que abre um recurso, executa código e **garante que o recurso será liberado no final**, mesmo se houver exceção.

**O problema sem `with`:**

```python
# ❌ sem with — se der erro antes do close, o arquivo fica aberto
f = open("scores.txt", "w", encoding="utf-8")
f.write("Ana;0.82")
# se aqui acontecer um erro, f.close() nunca roda!
f.close()
```

```python
# ❌ com try/finally — funciona, mas é verboso
f = open("scores.txt", "w", encoding="utf-8")
try:
    f.write("Ana;0.82")
finally:
    f.close()
```

**A solução com `with`:**

```python
# ✅ com with — limpo, seguro, Pythonic
with open("scores.txt", "w", encoding="utf-8") as f:
    f.write("Ana;0.82")
# aqui o arquivo já está fechado, mesmo se deu erro dentro do bloco
print("arquivo fechado automaticamente")
```

**Passo a passo:**
1. Salve como `15_1_with.py` e rode.
2. Verifique que o arquivo `scores.txt` foi criado com o conteúdo.
3. Após o bloco `with`, tente `f.write("teste")` — vai dar `ValueError: I/O operation on closed file` porque o arquivo já foi fechado.

**O que acontece internamente:**
1. Python chama o método `__enter__()` do objeto (no caso, `open()` retorna um file object que tem `__enter__`).
2. O valor retornado por `__enter__()` é atribuído à variável após `as` (no caso, `f`).
3. O bloco indentado é executado.
4. Ao sair do bloco (com ou sem erro), Python chama `__exit__()`, que fecha o arquivo.

> **Regra de ouro:** sempre que abrir um recurso que precisa ser fechado (arquivo, conexão de banco, socket, lock), use `with`.

**Código explicado:** o `with` substitui o padrão `try/finally` de forma mais limpa. Mesmo se houver erro dentro do bloco, o recurso é liberado.

### 15.2 as — dando nome ao recurso

**O que é:** a cláusula `as` captura o valor retornado por `__enter__()` e dá um nome para usar dentro do bloco.

**Exemplo:**

```python
# o "as f" recebe o file object retornado por __enter__
with open("scores.txt", "r", encoding="utf-8") as f:
    conteudo = f.read()
    print(conteudo)

# f ainda existe aqui, mas o arquivo já está fechado
print(f.closed)  # True
```

**Sem `as`:** você pode usar `with` sem `as` quando não precisa de referência ao objeto:

```python
from contextlib import suppress

# suppress é um context manager que ignora exceções específicas
with suppress(FileNotFoundError):
    import os
    os.remove("arquivo_que_nao_existe.txt")
# se o arquivo não existia, nenhum erro é levantado
print("continuou normalmente")
```

**Múltiplos context managers no mesmo `with`:**

```python
# Python 3.10+ permite parênteses para quebrar linha
with (
    open("entrada.txt", "r", encoding="utf-8") as entrada,
    open("saida.txt", "w", encoding="utf-8") as saida,
):
    saida.write(entrada.read().upper())

# versão compatível com Python < 3.10
with open("entrada.txt", "r", encoding="utf-8") as entrada, \
     open("saida.txt", "w", encoding="utf-8") as saida:
    saida.write(entrada.read().upper())
```

**Passo a passo:**
1. Crie `scores.txt` com algum conteúdo.
2. Salve o primeiro exemplo como `15_2_as.py` e rode.
3. Note que `f.closed` é `True` fora do bloco — o arquivo já foi fechado.

**Código explicado:** `as` recebe o retorno de `__enter__()`. A variável continua existindo fora do `with`, mas o recurso já foi liberado. Use múltiplos `as` para abrir vários recursos ao mesmo tempo.

### 15.3 Protocolo `__enter__` e `__exit__` — criando seu próprio context manager

**O que é:** qualquer classe que implemente os métodos `__enter__()` e `__exit__()` pode ser usada com `with`. Isso é chamado de **protocolo de context manager**.

**Exemplo completo:**

```python
class Conexao:
    def __init__(self, banco):
        self.banco = banco
        self.conectado = False

    def __enter__(self):
        # chamado quando o "with" começa
        print(f"conectando ao {self.banco}...")
        self.conectado = True
        return self  # esse valor vai para o "as"

    def __exit__(self, exc_type, exc_value, traceback):
        # chamado quando o "with" termina (com ou sem erro)
        print(f"desconectando do {self.banco}...")
        self.conectado = False
        return False  # False = propaga a exceção, se houver

    def executar(self, query):
        if not self.conectado:
            raise RuntimeError("não conectado")
        print(f"executando: {query}")


# uso:
with Conexao("credito_db") as db:
    db.executar("SELECT * FROM clientes")
    db.executar("SELECT * FROM simulacoes")

# aqui db.conectado já é False
print(f"conectado: {db.conectado}")
```

**Parâmetros do `__exit__`:**

| Parâmetro | O que contém | Quando não há erro |
|---|---|---|
| `exc_type` | A **classe** da exceção (ex.: `ValueError`) | `None` |
| `exc_value` | A **instância** da exceção (ex.: `ValueError("valor inválido")`) | `None` |
| `traceback` | O **traceback** (pilha de chamadas) | `None` |

**Retorno do `__exit__`:**
- `return False` (ou nada) → a exceção é **propagada** normalmente.
- `return True` → a exceção é **engolida** (suprimida). Use com cuidado!

**Passo a passo:**
1. Salve como `15_3_proto.py` e rode.
2. Veja a sequência: "conectando...", as queries, "desconectando...".
3. Adicione `raise ValueError("teste")` dentro do `with` e rode de novo — note que "desconectando..." aparece **antes** do traceback do erro.

**Código explicado:** `__enter__` prepara o recurso e retorna o objeto para o `as`. `__exit__` libera o recurso e decide se engole ou propaga a exceção. O Python garante que `__exit__` sempre roda, mesmo com erro.

### 15.4 Limpeza automática de recursos — segurança contra exceções

**O que é:** a maior vantagem do context manager é que a limpeza acontece **sempre**, mesmo quando o código dentro do `with` explode com uma exceção.

**Exemplo — comparando com e sem `with`:**

```python
class Recurso:
    def __init__(self, nome):
        self.nome = nome

    def __enter__(self):
        print(f"[{self.nome}] abrindo recurso")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        print(f"[{self.nome}] fechando recurso")
        if exc_type:
            print(f"[{self.nome}] erro detectado: {exc_value}")
        return False  # propaga a exceção

# teste 1: sem erro
print("--- SEM ERRO ---")
with Recurso("teste1"):
    print("usando recurso normalmente")

# teste 2: com erro
print("\n--- COM ERRO ---")
try:
    with Recurso("teste2"):
        print("usando recurso...")
        raise RuntimeError("algo deu errado!")
except RuntimeError:
    print("erro tratado fora do with")
```

**Saída:**
```
--- SEM ERRO ---
[teste1] abrindo recurso
usando recurso normalmente
[teste1] fechando recurso

--- COM ERRO ---
[teste2] abrindo recurso
usando recurso...
[teste2] fechando recurso
[teste2] erro detectado: algo deu errado!
erro tratado fora do with
```

**Passo a passo:**
1. Salve como `15_4_clean.py` e rode.
2. Observe que no teste 2, "fechando recurso" aparece **antes** de "erro tratado fora do with".
3. O `__exit__` roda primeiro, depois a exceção é propagada para o `except` externo.

**Casos reais onde isso importa:**
- **Arquivo aberto** — se não fechar, outros processos não conseguem acessar (especialmente no Windows).
- **Conexão de banco** — se não fechar, o pool de conexões esgota.
- **Lock de thread** — se não liberar, outras threads ficam travadas para sempre (deadlock).
- **Transação de banco** — se não fizer commit ou rollback, a transação fica pendurada.

**Código explicado:** o `__exit__` é o "seguro de vida" do recurso. Não importa o que aconteça dentro do `with`, a limpeza é garantida.

### 15.5 Context managers com `yield` — forma simplificada

**O que é:** em vez de criar uma classe com `__enter__` e `__exit__`, você pode criar um context manager como uma **função geradora** usando o decorator `@contextmanager` do módulo `contextlib`.

**Como funciona:**
1. Tudo **antes** do `yield` é o `__enter__`.
2. O valor do `yield` é o que vai para o `as`.
3. Tudo **depois** do `yield` é o `__exit__`.

**Exemplo — cronômetro:**

```python
from contextlib import contextmanager
import time

@contextmanager
def cronometro(nome):
    # __enter__: antes do yield
    inicio = time.time()
    print(f"[{nome}] iniciando...")
    
    yield nome  # esse valor vai para o "as"
    
    # __exit__: depois do yield
    duracao = time.time() - inicio
    print(f"[{nome}] finalizado em {duracao:.4f}s")


with cronometro("calculo") as operacao:
    total = sum(range(1_000_000))
    print(f"{operacao}: resultado = {total}")
```

**Exemplo — gerenciador de conexão simulado:**

```python
from contextlib import contextmanager

@contextmanager
def conectar(banco):
    print(f"abrindo conexão com {banco}")
    conexao = {"banco": banco, "ativa": True}
    try:
        yield conexao  # entrega a conexão para o bloco with
    finally:
        conexao["ativa"] = False
        print(f"fechando conexão com {banco}")


with conectar("credito_db") as conn:
    print(f"usando: {conn}")
    # mesmo com erro, o finally garante o fechamento

print(f"conexão ativa: {conn['ativa']}")  # False
```

> **Importante:** coloque o `yield` dentro de `try/finally` para garantir a limpeza mesmo com exceção. Sem o `try/finally`, se houver erro dentro do `with`, o código após o `yield` não roda.

**Comparação — classe vs função:**

```python
# Classe (5 linhas de setup)
class MeuCM:
    def __enter__(self):
        print("abrindo")
        return self
    def __exit__(self, *args):
        print("fechando")

# Função (3 linhas de setup)
@contextmanager
def meu_cm():
    print("abrindo")
    try:
        yield
    finally:
        print("fechando")
```

**Passo a passo:**
1. Salve o exemplo do cronômetro como `15_5_yield.py` e rode.
2. Veja o tempo impresso ao final.
3. Teste adicionar um `raise` dentro do `with` para confirmar que a limpeza roda.

**Código explicado:** `@contextmanager` transforma uma função com `yield` em context manager. O que vem antes do `yield` é a preparação; o que vem depois é a limpeza. Use `try/finally` ao redor do `yield` para garantir que a limpeza aconteça mesmo com erro.

### 15.6 Context managers assíncronos

**O que é:** versão `async` dos context managers, para uso com `async with`. Usa `__aenter__` e `__aexit__` (note o prefixo `a` de async).

**Quando usar:** quando o recurso que você está abrindo ou fechando envolve operações assíncronas (requisições HTTP, conexões a banco async, WebSockets etc.).

**Exemplo — classe async:**

```python
import asyncio

class ConexaoAsync:
    def __init__(self, url):
        self.url = url

    async def __aenter__(self):
        # simula conexão assíncrona
        print(f"conectando a {self.url}...")
        await asyncio.sleep(0.1)  # simula latência de rede
        print("conectado!")
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        print(f"desconectando de {self.url}...")
        await asyncio.sleep(0.05)  # simula fechamento
        print("desconectado!")
        return False

    async def consultar(self, query):
        print(f"consultando: {query}")
        await asyncio.sleep(0.05)
        return {"resultado": "ok"}


async def main():
    async with ConexaoAsync("https://api.credito.com") as conn:
        resultado = await conn.consultar("GET /clientes")
        print(resultado)

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `15_6_async_cm.py` e rode.
2. Veja a sequência: conectando → consultando → desconectando.
3. Note que `__aenter__` e `__aexit__` são funções `async def`.

**Código explicado:** `__aenter__` e `__aexit__` são corrotinas (usam `await`). O `async with` funciona igual ao `with` normal, mas permite operações assíncronas na abertura e no fechamento do recurso.

### 15.7 `async with` e `@asynccontextmanager`

**O que é:** assim como `@contextmanager` simplifica context managers síncronos, `@asynccontextmanager` simplifica os assíncronos.

**Exemplo:**

```python
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def sessao_http(url):
    print(f"abrindo sessão para {url}")
    sessao = {"url": url, "ativa": True}
    try:
        yield sessao
    finally:
        sessao["ativa"] = False
        print(f"fechando sessão para {url}")


async def main():
    async with sessao_http("https://api.credito.com") as s:
        print(f"usando sessão: {s}")
        # simula requisições
        await asyncio.sleep(0.1)

    print(f"sessão ativa: {s['ativa']}")  # False

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `15_7_async_with.py` e rode.
2. Observe a mesma lógica de yield, agora com `async def` e `await`.

**Código explicado:** `@asynccontextmanager` é o equivalente assíncrono de `@contextmanager`. Mesma lógica: antes do `yield` é o setup, depois é a limpeza. Use `try/finally` para garantir a limpeza.

### 15.8 Context managers úteis da biblioteca padrão

**O que é:** o módulo `contextlib` traz vários context managers prontos que resolvem padrões comuns.

**Exemplo:**

```python
from contextlib import suppress, redirect_stdout, closing
import io

# suppress — ignora exceções específicas
with suppress(FileNotFoundError):
    import os
    os.remove("arquivo_que_nao_existe.txt")
print("continuou sem erro")

# redirect_stdout — redireciona print para outro lugar
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("isso vai para o buffer, não para o terminal")
print(f"capturado: {buffer.getvalue().strip()}")

# closing — chama .close() em objetos que não são context managers
class Recurso:
    def close(self):
        print("recurso fechado")

with closing(Recurso()) as r:
    print("usando recurso")
# "recurso fechado" é impresso automaticamente
```

**Tabela de context managers do `contextlib`:**

| Context Manager | O que faz |
|---|---|
| `suppress(ExcType)` | Ignora exceções do tipo especificado dentro do bloco |
| `redirect_stdout(buffer)` | Redireciona `print()` para outro destino (arquivo, StringIO) |
| `redirect_stderr(buffer)` | Igual, mas para stderr |
| `closing(obj)` | Chama `obj.close()` ao sair, para objetos que não têm `__exit__` |
| `nullcontext(valor)` | Context manager que não faz nada — útil para código condicional |
| `ExitStack()` | Gerencia uma pilha de context managers dinamicamente |

**`nullcontext` — context manager condicional:**

```python
from contextlib import nullcontext

def processar(arquivo=None):
    # se passou arquivo, abre com with
    # se não, usa stdout (que não precisa fechar)
    cm = open(arquivo, "w", encoding="utf-8") if arquivo else nullcontext(
        __import__("sys").stdout
    )
    with cm as f:
        f.write("resultado: aprovado\n")

processar("resultado.txt")  # escreve no arquivo
processar()                  # escreve no terminal
```

**Passo a passo:**
1. Salve como `15_8_stdlib.py` e rode.
2. Teste cada context manager separadamente para ver o efeito.

**Código explicado:** a biblioteca padrão já traz soluções prontas para padrões comuns. Use `suppress` em vez de `try/except: pass`, e `closing` para objetos que têm `.close()` mas não implementam o protocolo completo.

---

## 16. Iteráveis, iteradores e generators

### 16.1 Iterable

**O que é:** objeto que implementa `__iter__`; pode ser usado em `for`.

**Exemplo:**

```python
clientes = ["Ana", "Bruno"]   # iterable
print(hasattr(clientes, "__iter__"))
for c in clientes:
    print(c)
```

**Passo a passo:**
1. Salve como `16_1_iter.py` e rode.

**Código explicado:** listas, tuplas, dicts, sets, strings, arquivos: todos são iterables.

### 16.2 Iterator

**O que é:** objeto retornado por `iter()`; tem `__next__`.

**Exemplo:**

```python
clientes = ["Ana", "Bruno"]
it = iter(clientes)
print(type(it))
print(next(it))
print(next(it))
```

**Passo a passo:**
1. Salve como `16_2_iterator.py` e rode.

**Código explicado:** o iterador é "consumível"; cada `next` avança uma posição.

### 16.3 iter

**O que é:** built-in que pega iterable e devolve iterador.

**Exemplo:**

```python
it = iter("oi")
print(next(it))  # 'o'
print(next(it))  # 'i'
```

**Passo a passo:**
1. Salve como `16_3_iter_fn.py` e rode.

**Código explicado:** `for` chama `iter()` internamente.

### 16.4 next

**O que é:** built-in que avança o iterador; aceita default.

**Exemplo:**

```python
it = iter([10, 20])
print(next(it))
print(next(it))
print(next(it, "fim"))  # com default não dá StopIteration
```

**Passo a passo:**
1. Salve como `16_4_next.py` e rode.

**Código explicado:** sem default, esgotar gera `StopIteration`.

### 16.5 StopIteration

**O que é:** exceção lançada para sinalizar fim do iterador.

**Exemplo:**

```python
it = iter([1, 2])
while True:
    try:
        print(next(it))
    except StopIteration:
        print("acabou")
        break
```

**Passo a passo:**
1. Salve como `16_5_stop.py` e rode.

**Código explicado:** `for` captura `StopIteration` automaticamente para encerrar.

### 16.6 yield — transformando função em generator

**O que é:** quando uma função contém `yield`, ela **não roda normalmente**. Em vez de executar tudo e retornar um valor, ela se torna um **generator** — um objeto que produz valores **um de cada vez**, pausando entre cada entrega.

**Diferença fundamental:**
- `return` — encerra a função e devolve um valor. A função morre.
- `yield` — pausa a função e devolve um valor. A função fica "congelada" e pode ser retomada.

---

#### Exemplo 1 — o básico: `return` vs `yield`

```python
# com return — cria lista inteira na memória
def parcelas_lista(valor, meses):
    resultado = []
    p = valor / meses
    for i in range(1, meses + 1):
        resultado.append((i, p))
    return resultado

# com yield — gera uma parcela por vez
def parcelas_gen(valor, meses):
    p = valor / meses
    for i in range(1, meses + 1):
        yield i, p

# ambos funcionam no for:
for n, v in parcelas_gen(120000, 3):
    print(f"parcela {n}: R$ {v:.2f}")
```

A diferença? `parcelas_lista` cria **toda** a lista na memória de uma vez. `parcelas_gen` cria **um item por vez** — usa memória constante mesmo para 1 milhão de parcelas.

---

#### Exemplo 2 — entendendo a pausa com `next()`

```python
def contador():
    print("antes do primeiro yield")
    yield 1
    print("entre o primeiro e o segundo")
    yield 2
    print("entre o segundo e o terceiro")
    yield 3
    print("depois do último yield")

g = contador()
print(type(g))    # <class 'generator'>

print(next(g))    # imprime "antes do primeiro yield", retorna 1
print(next(g))    # imprime "entre o primeiro e o segundo", retorna 2
print(next(g))    # imprime "entre o segundo e o terceiro", retorna 3
# next(g)         # imprime "depois do último yield", levanta StopIteration
```

**O que acontece:**
1. Chamar `contador()` **não executa nada** — só cria o objeto generator.
2. Cada `next(g)` roda até o próximo `yield`, retorna o valor e pausa.
3. A função "lembra" onde parou (variáveis locais, ponto de execução).
4. Quando não há mais `yield`, o código restante roda e `StopIteration` é levantado.

---

#### Exemplo 3 — yield dentro de condicionais

```python
def clientes_aprovados(lista):
    for cliente in lista:
        if cliente["score"] >= 0.7:
            yield cliente

clientes = [
    {"nome": "Ana", "score": 0.82},
    {"nome": "Bruno", "score": 0.55},
    {"nome": "Carla", "score": 0.91},
    {"nome": "Diego", "score": 0.60},
]

for c in clientes_aprovados(clientes):
    print(f"{c['nome']} aprovado (score: {c['score']})")
# Ana aprovado (score: 0.82)
# Carla aprovado (score: 0.91)
```

O `yield` não precisa estar dentro de um loop simples — pode estar em qualquer ponto da função, inclusive dentro de `if`, `try`, ou loops aninhados.

---

#### Exemplo 4 — yield com lógica de transformação

```python
def calcular_parcelas(valor, taxa_mensal, meses):
    """Gera parcelas com juros compostos (tabela Price simplificada)."""
    saldo = valor
    parcela = valor * (taxa_mensal / (1 - (1 + taxa_mensal) ** -meses))
    
    for mes in range(1, meses + 1):
        juros = saldo * taxa_mensal
        amortizacao = parcela - juros
        saldo -= amortizacao
        yield {
            "mes": mes,
            "parcela": round(parcela, 2),
            "juros": round(juros, 2),
            "amortizacao": round(amortizacao, 2),
            "saldo": round(max(saldo, 0), 2),
        }

for p in calcular_parcelas(100000, 0.01, 5):
    print(p)
```

Cada `yield` entrega um dicionário completo com os dados daquele mês. O saldo é recalculado a cada iteração.

---

#### Exemplo 5 — generator como pipeline (encadeando generators)

```python
def ler_valores(lista):
    for item in lista:
        yield item

def filtrar_positivos(gen):
    for valor in gen:
        if valor > 0:
            yield valor

def dobrar(gen):
    for valor in gen:
        yield valor * 2

# pipeline: ler → filtrar → dobrar
dados = [-5, 10, -3, 20, 0, 15]
pipeline = dobrar(filtrar_positivos(ler_valores(dados)))

print(list(pipeline))  # [20, 40, 30]
```

Cada generator processa **um item por vez** e passa adiante. Nenhuma lista intermediária é criada em memória.

---

#### Exemplo 6 — `yield` com `send()` — comunicação bidirecional

```python
def acumulador():
    total = 0
    while True:
        valor = yield total  # yield retorna total; recebe valor via send()
        if valor is None:
            break
        total += valor

g = acumulador()
next(g)           # inicializa (roda até o primeiro yield)
print(g.send(100))  # 100
print(g.send(200))  # 300
print(g.send(50))   # 350
# g.send(None)      # encerra (valor is None → break → StopIteration)
```

Com `send()`, o chamador pode **enviar dados de volta** para o generator. O `yield` age como ponto de troca: entrega um valor e recebe outro.

---

#### Exemplo 7 — expressão geradora (versão compacta do yield)

```python
# generator expression — igual a list comprehension, mas com ()
quadrados = (x ** 2 for x in range(1_000_000))

print(type(quadrados))  # <class 'generator'>
print(next(quadrados))  # 1
print(next(quadrados))  # 4
print(sum(quadrados))   # soma dos restantes — sem criar lista na memória
```

A expressão geradora `(expr for x in iter)` é um atalho para um generator simples com `yield`.

---

**Passo a passo:**
1. Salve o exemplo 2 como `16_6_yield.py` e rode — observe as mensagens de print entre cada `next()`.
2. Descomente o último `next(g)` para ver o `StopIteration`.
3. Salve o exemplo 5 como `16_6_pipeline.py` e rode para ver o encadeamento.

**Código explicado:** `yield` transforma uma função em generator — um objeto que produz valores sob demanda. A função pausa no `yield`, lembra seu estado e retoma quando pedida. Isso economiza memória e permite processar dados em pipeline, um item por vez.

### 16.7 `yield from` — delegando para outro iterável

**O que é:** `yield from` permite que um generator **delegue** a produção de valores para outro iterável (lista, tupla, range, outro generator etc.). Em vez de fazer um loop manual com `for x in iter: yield x`, você escreve `yield from iter`.

**Diferença visual:**

```python
# ❌ sem yield from — loop manual
def numeros_manual():
    for x in range(3):
        yield x
    for x in [10, 20]:
        yield x

# ✅ com yield from — limpo e direto
def numeros():
    yield from range(3)
    yield from [10, 20]

print(list(numeros()))  # [0, 1, 2, 10, 20]
```

---

#### Exemplo 1 — concatenando vários iteráveis

```python
def todos_os_dados():
    yield from ["Ana", "Bruno"]          # lista
    yield from ("Carla", "Diego")        # tupla
    yield from {"Eva", "Fábio"}          # set
    yield from range(1, 4)               # range

print(list(todos_os_dados()))
# ['Ana', 'Bruno', 'Carla', 'Diego', 'Eva', 'Fábio', 1, 2, 3]
# (a ordem do set pode variar)
```

`yield from` aceita qualquer iterável — listas, tuplas, sets, ranges, strings, arquivos, outros generators.

---

#### Exemplo 2 — delegando para outro generator

```python
def parcelas_normais(valor, meses):
    p = valor / meses
    for i in range(1, meses + 1):
        yield {"tipo": "normal", "mes": i, "valor": round(p, 2)}

def parcelas_carencia(meses_carencia):
    for i in range(1, meses_carencia + 1):
        yield {"tipo": "carencia", "mes": i, "valor": 0}

def plano_completo(valor, meses_carencia, meses_pagamento):
    yield from parcelas_carencia(meses_carencia)
    yield from parcelas_normais(valor, meses_pagamento)

for p in plano_completo(120000, 3, 4):
    print(p)
# {'tipo': 'carencia', 'mes': 1, 'valor': 0}
# {'tipo': 'carencia', 'mes': 2, 'valor': 0}
# {'tipo': 'carencia', 'mes': 3, 'valor': 0}
# {'tipo': 'normal', 'mes': 1, 'valor': 30000.0}
# {'tipo': 'normal', 'mes': 2, 'valor': 30000.0}
# ...
```

O `plano_completo` não sabe os detalhes — ele só delega para cada sub-generator.

---

#### Exemplo 3 — percorrendo árvore recursivamente

```python
def percorrer_arvore(no):
    """Percorre uma estrutura de árvore (dict com 'filhos') em profundidade."""
    yield no["nome"]
    for filho in no.get("filhos", []):
        yield from percorrer_arvore(filho)  # recursão com yield from

organograma = {
    "nome": "Diretoria",
    "filhos": [
        {
            "nome": "Crédito",
            "filhos": [
                {"nome": "Análise"},
                {"nome": "Cobrança"},
            ]
        },
        {
            "nome": "TI",
            "filhos": [
                {"nome": "Backend"},
                {"nome": "Frontend"},
            ]
        }
    ]
}

print(list(percorrer_arvore(organograma)))
# ['Diretoria', 'Crédito', 'Análise', 'Cobrança', 'TI', 'Backend', 'Frontend']
```

Sem `yield from`, a versão recursiva ficaria assim:
```python
for item in percorrer_arvore(filho):
    yield item
```
Funciona, mas `yield from` é mais limpo e também propaga `send()`, `throw()` e `close()` corretamente.

---

#### Exemplo 4 — achatando listas aninhadas

```python
def achatar(lista):
    for item in lista:
        if isinstance(item, list):
            yield from achatar(item)  # recursão para sublistas
        else:
            yield item

dados = [1, [2, 3], [4, [5, 6]], 7]
print(list(achatar(dados)))  # [1, 2, 3, 4, 5, 6, 7]
```

---

#### Exemplo 5 — `yield from` com strings (cuidado!)

```python
def letras():
    yield from "Ana"
    yield from "Bruno"

print(list(letras()))  # ['A', 'n', 'a', 'B', 'r', 'u', 'n', 'o']
```

> **Cuidado:** `yield from "Ana"` itera **caractere por caractere**, não a string inteira. Se quer entregar a string como um item só, use `yield "Ana"` (sem `from`).

---

#### Exemplo 6 — capturando o valor de retorno do sub-generator

```python
def sub_gen():
    yield 1
    yield 2
    return "resultado final"  # valor retornado pelo sub-generator

def principal():
    resultado = yield from sub_gen()
    print(f"sub-generator retornou: {resultado}")
    yield 99

print(list(principal()))
# sub-generator retornou: resultado final
# [1, 2, 99]
```

O `return` dentro de um generator define o valor que `yield from` recebe de volta. Isso é útil para pipelines que precisam comunicar um resultado final.

---

#### Exemplo 7 — pipeline de processamento de dados

```python
def ler_linhas(texto):
    yield from texto.strip().split("\n")

def filtrar_vazias(gen):
    for linha in gen:
        if linha.strip():
            yield linha

def parsear_csv(gen):
    for linha in gen:
        campos = linha.split(";")
        yield {"nome": campos[0], "score": float(campos[1])}

def aprovados(gen):
    for registro in gen:
        if registro["score"] >= 0.7:
            yield registro

dados = """
Ana;0.82
Bruno;0.55

Carla;0.91
Diego;0.60
"""

pipeline = aprovados(parsear_csv(filtrar_vazias(ler_linhas(dados))))
for r in pipeline:
    print(r)
# {'nome': 'Ana', 'score': 0.82}
# {'nome': 'Carla', 'score': 0.91}
```

Cada etapa é um generator que processa um item por vez. Nenhuma lista intermediária é criada.

---

**Passo a passo:**
1. Salve o exemplo 1 como `16_7_yield_from.py` e rode.
2. Salve o exemplo 3 e rode para ver a árvore percorrida.
3. Teste o exemplo 5 para entender o comportamento com strings.
4. Salve o exemplo 6 para ver o valor de retorno do sub-generator.

**Código explicado:** `yield from` delega a produção de valores para outro iterável ou generator. É mais limpo que um loop manual com `yield`, funciona com recursão, e propaga corretamente `send()`, `throw()` e `close()`. Use para compor generators e percorrer estruturas aninhadas.

### 16.8 Lazy evaluation

**O que é:** valores são gerados sob demanda, economizando memória.

**Exemplo:**

```python
def infinitos():
    n = 0
    while True:
        yield n
        n += 1

g = infinitos()
print(next(g), next(g), next(g))
```

**Passo a passo:**
1. Salve como `16_8_lazy.py` e rode.

**Código explicado:** generators só calculam o próximo quando você pede.

### 16.9 Generators infinitos

**O que é:** generator sem condição de parada; só funciona porque é lazy.

**Exemplo:**

```python
from itertools import islice

def contador():
    n = 0
    while True:
        yield n
        n += 1

print(list(islice(contador(), 5)))  # [0,1,2,3,4]
```

**Passo a passo:**
1. Salve como `16_9_inf.py` e rode.

**Código explicado:** `islice` corta os primeiros 5 elementos sem travar.

---

## 17. Decorators

### 17.1 Decorators de função

**O que é:** função que envolve outra adicionando comportamento.

**Exemplo:**

```python
def logar(func):
    def wrapper(*a, **kw):
        print("antes")
        r = func(*a, **kw)
        print("depois")
        return r
    return wrapper

@logar
def somar(a, b):
    return a + b

print(somar(2, 3))
```

**Passo a passo:**
1. Salve como `17_1_func.py` e rode.

**Código explicado:** `@logar` é açúcar para `somar = logar(somar)`.

### 17.2 Decorators de classe

**O que é:** decorator aplicado a classe; modifica/agrega à definição.

**Exemplo:**

```python
def adicionar_versao(cls):
    cls.versao = "1.0"
    return cls

@adicionar_versao
class Servico:
    pass

print(Servico.versao)
```

**Passo a passo:**
1. Salve como `17_2_classe.py` e rode.

**Código explicado:** `dataclass`, por exemplo, é um decorator de classe.

### 17.3 Decorators com parâmetros

**O que é:** função que recebe parâmetros e devolve um decorator.

**Exemplo:**

```python
def repetir(vezes):
    def decorator(func):
        def wrapper(*a, **kw):
            for _ in range(vezes):
                func(*a, **kw)
        return wrapper
    return decorator

@repetir(3)
def saudacao(nome):
    print("oi", nome)

saudacao("Ana")
```

**Passo a passo:**
1. Salve como `17_3_param.py` e rode.

**Código explicado:** três níveis: factory → decorator → wrapper.

### 17.4 Ordem de aplicação dos decorators

**O que é:** decorators são aplicados de **baixo para cima**.

**Exemplo:**

```python
def a(f):
    def w(*x): print("a"); return f(*x)
    return w

def b(f):
    def w(*x): print("b"); return f(*x)
    return w

@a
@b
def func():
    print("func")

func()  # a, b, func
```

**Passo a passo:**
1. Salve como `17_4_ordem.py` e rode.

**Código explicado:** `@a @b` equivale a `func = a(b(func))`; `a` é a camada de fora.

### 17.5 Decorators empilhados

**O que é:** combinar múltiplos decorators na mesma função.

**Exemplo:**

```python
import functools

def cache(f):
    return functools.lru_cache()(f)

def logar(f):
    def w(*a, **kw):
        print("call", a)
        return f(*a, **kw)
    return w

@logar
@cache
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

print(fib(10))
```

**Passo a passo:**
1. Salve como `17_5_pilha.py` e rode.

**Código explicado:** `cache` armazena resultados; `logar` imprime chamadas.

### 17.6 Funções como objetos

**O que é:** funções são valores; podem ser passadas, retornadas e armazenadas.

**Exemplo:**

```python
def somar(a, b): return a + b
def aplicar(op, x, y): return op(x, y)

print(aplicar(somar, 2, 3))

operacoes = {"soma": somar}
print(operacoes["soma"](4, 5))
```

**Passo a passo:**
1. Salve como `17_6_obj.py` e rode.

**Código explicado:** decorators só existem porque funções são objetos de primeira classe.

---

## 18. Orientação a objetos

### 18.1 class

**O que é:** define molde para criar objetos.

**Exemplo:**

```python
class Cliente:
    pass

c = Cliente()
print(type(c))
```

**Passo a passo:**
1. Salve como `18_1_class.py` e rode.

**Código explicado:** mesmo classe vazia já cria objetos com identidade.

### 18.2 Objetos e instâncias

**O que é:** objeto = instância de classe; cada um com atributos próprios.

**Exemplo:**

```python
class Cliente:
    pass

a = Cliente()
b = Cliente()
a.nome = "Ana"
b.nome = "Bruno"
print(a.nome, b.nome)
```

**Passo a passo:**
1. Salve como `18_2_inst.py` e rode.

**Código explicado:** `a` e `b` são objetos distintos; cada atributo vive em sua instância.

### 18.3 Atributos de instância

**O que é:** atributos definidos em `__init__` ou diretamente em `self`; pertencem a cada objeto.

**Exemplo:**

```python
class Cliente:
    def __init__(self, nome):
        self.nome = nome

a = Cliente("Ana")
b = Cliente("Bruno")
print(a.nome, b.nome)
```

**Passo a passo:**
1. Salve como `18_3_attr_inst.py` e rode.

**Código explicado:** mudar `a.nome` não afeta `b.nome`.

### 18.4 Atributos de classe

**O que é:** atributos definidos no corpo da classe; compartilhados por todas as instâncias.

**Exemplo:**

```python
class Cliente:
    taxa_padrao = 0.05
    def __init__(self, nome):
        self.nome = nome

a = Cliente("Ana")
print(a.taxa_padrao)
print(Cliente.taxa_padrao)
```

**Passo a passo:**
1. Salve como `18_4_attr_classe.py` e rode.

**Código explicado:** se a instância não tem o atributo, Python sobe para a classe.

### 18.5 Métodos de instância

**O que é:** funções definidas dentro da classe que recebem `self`.

**Exemplo:**

```python
class Conta:
    def __init__(self, saldo):
        self.saldo = saldo
    def depositar(self, v):
        self.saldo += v

c = Conta(100)
c.depositar(50)
print(c.saldo)
```

**Passo a passo:**
1. Salve como `18_5_metodo.py` e rode.

**Código explicado:** ao chamar `c.depositar(50)`, Python passa `c` como `self` automaticamente.

### 18.6 self

**O que é:** referência à instância atual dentro do método.

**Exemplo:**

```python
class Pessoa:
    def __init__(self, nome):
        self.nome = nome
    def saudar(self):
        return f"Olá, eu sou {self.nome}"

print(Pessoa("Ana").saudar())
```

**Passo a passo:**
1. Salve como `18_6_self.py` e rode.

**Código explicado:** `self` é só convenção, mas todo método de instância recebe a instância como primeiro argumento.

### 18.7 __init__

**O que é:** método chamado ao criar a instância; serve para inicializar atributos.

**Exemplo:**

```python
class Simulacao:
    def __init__(self, cliente, valor):
        self.cliente = cliente
        self.valor = valor
        self.status = "pendente"

s = Simulacao("Ana", 120000)
print(s.cliente, s.status)
```

**Passo a passo:**
1. Salve como `18_7_init.py` e rode.

**Código explicado:** `__init__` não retorna nada; só preenche `self`.

### 18.8 Encapsulamento por convenção

**O que é:** Python não tem `private`, mas usa `_nome` (interno) e `__nome` (name mangling).

**Exemplo:**

```python
class Conta:
    def __init__(self):
        self._saldo = 100        # interno, não mexa
        self.__chave = "secreta" # name mangling

c = Conta()
print(c._saldo)
# print(c.__chave)  # AttributeError
print(c._Conta__chave)  # acessa via nome mangled
```

**Passo a passo:**
1. Salve como `18_8_encap.py` e rode.

**Código explicado:** `__attr` vira `_Classe__attr` para evitar conflitos em herança.

### 18.9 Herança

**O que é:** classe filha herda atributos e métodos da classe pai.

**Exemplo:**

```python
class Animal:
    def respirar(self):
        return "inspira/expira"

class Cachorro(Animal):
    def latir(self):
        return "au au"

c = Cachorro()
print(c.respirar(), c.latir())
```

**Passo a passo:**
1. Salve como `18_9_heranca.py` e rode.

**Código explicado:** `Cachorro` herda `respirar` sem reescrever.

### 18.10 Composição

**O que é:** objeto contendo outros objetos como atributos (alternativa à herança).

**Exemplo:**

```python
class Motor:
    def ligar(self): return "vrum"

class Carro:
    def __init__(self):
        self.motor = Motor()
    def acelerar(self):
        return self.motor.ligar()

print(Carro().acelerar())
```

**Passo a passo:**
1. Salve como `18_10_comp.py` e rode.

**Código explicado:** "tem-um" (composição) costuma ser mais flexível que "é-um" (herança).

### 18.11 super

**O que é:** chama método da classe pai sem citar o nome dela.

**Exemplo:**

```python
class Pessoa:
    def __init__(self, nome):
        self.nome = nome

class Cliente(Pessoa):
    def __init__(self, nome, valor):
        super().__init__(nome)
        self.valor = valor

c = Cliente("Ana", 120000)
print(c.nome, c.valor)
```

**Passo a passo:**
1. Salve como `18_11_super.py` e rode.

**Código explicado:** `super()` resolve o pai pela MRO; útil em herança múltipla.

### 18.12 MRO

**O que é:** Method Resolution Order — ordem em que Python procura métodos em hierarquias.

**Exemplo:**

```python
class A:
    def f(self): print("A")
class B(A):
    def f(self): print("B")
class C(A):
    def f(self): print("C")
class D(B, C):
    pass

D().f()           # B (segue MRO)
print(D.__mro__)
```

**Passo a passo:**
1. Salve como `18_12_mro.py` e rode.

**Código explicado:** Python usa C3 linearization; veja a ordem em `__mro__`.

### 18.13 Métodos dunder

**O que é:** métodos `__nome__` que integram o objeto à linguagem (`+`, `len`, `print`...).

**Exemplo:**

```python
class Valor:
    def __init__(self, v): self.v = v
    def __repr__(self): return f"Valor({self.v})"
    def __add__(self, other): return Valor(self.v + other.v)
    def __len__(self): return self.v

a = Valor(10) + Valor(5)
print(a, len(a))
```

**Passo a passo:**
1. Salve como `18_13_dunder.py` e rode.

**Código explicado:** `__add__` ativa `+`; `__len__` ativa `len`; `__repr__` define `print`.

### 18.14 Objetos chamáveis

**O que é:** objeto com `__call__` pode ser usado como função: `obj()`.

**Exemplo:**

```python
class Multiplicador:
    def __init__(self, fator): self.fator = fator
    def __call__(self, x): return x * self.fator

dobro = Multiplicador(2)
print(dobro(10))
print(callable(dobro))
```

**Passo a passo:**
1. Salve como `18_14_call.py` e rode.

**Código explicado:** alternativa a closures quando o "callable" precisa guardar estado complexo.

---

## 19. Modelagem de dados em Python

### 19.1 Dataclasses

**O que é:** decorator que gera `__init__`, `__repr__` e `__eq__` automaticamente.

**Exemplo:**

```python
from dataclasses import dataclass

@dataclass
class Cliente:
    nome: str
    score: float

c = Cliente("Ana", 0.82)
print(c)
print(c == Cliente("Ana", 0.82))
```

**Passo a passo:**
1. Salve como `19_1_dc.py` e rode.

**Código explicado:** elimina código repetitivo; ótimo para DTOs e value objects.

### 19.2 field

**O que é:** controle fino sobre atributos do dataclass.

**Exemplo:**

```python
from dataclasses import dataclass, field

@dataclass
class Pedido:
    id: int
    itens: list = field(default_factory=list)
    interno: str = field(default="x", repr=False)

print(Pedido(1))
```

**Passo a passo:**
1. Salve como `19_2_field.py` e rode.

**Código explicado:** `field` permite controlar `default_factory`, `repr`, `compare` etc.

### 19.3 default_factory

**O que é:** função chamada para criar default mutável a cada instância.

**Exemplo:**

```python
from dataclasses import dataclass, field

@dataclass
class Carrinho:
    itens: list = field(default_factory=list)

a = Carrinho()
b = Carrinho()
a.itens.append("livro")
print(a.itens, b.itens)
```

**Passo a passo:**
1. Salve como `19_3_factory.py` e rode.

**Código explicado:** `b` recebe lista nova, sem compartilhar com `a`.

### 19.4 Defaults mutáveis

**O que é:** **nunca** use `def f(lista=[])` ou `field(default=[])`; o objeto é compartilhado.

**Exemplo:**

```python
def adicionar(item, lista=[]):    # PEGADINHA
    lista.append(item)
    return lista

print(adicionar(1))     # [1]
print(adicionar(2))     # [1, 2]   <-- inesperado!

def correto(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista

print(correto(1), correto(2))
```

**Passo a passo:**
1. Salve como `19_4_mut.py` e rode.

**Código explicado:** o default é avaliado **uma vez** na definição; use `None` + criação interna.

### 19.5 Enum

**O que é:** define conjunto fechado de valores nomeados.

**Exemplo:**

```python
from enum import Enum

class Status(str, Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"

print(Status.APROVADO, Status.APROVADO.value)
print(Status("pendente"))
```

**Passo a passo:**
1. Salve como `19_5_enum.py` e rode.

**Código explicado:** herdar de `str` deixa o enum comparável a strings em APIs.

### 19.6 Classes abstratas

**O que é:** classes que não podem ser instanciadas; servem de contrato.

**Exemplo:**

```python
from abc import ABC, abstractmethod

class Repositorio(ABC):
    @abstractmethod
    def salvar(self, dado): ...

class RepoMemoria(Repositorio):
    def salvar(self, dado):
        print("salvo:", dado)

# Repositorio()       # TypeError
RepoMemoria().salvar("ok")
```

**Passo a passo:**
1. Salve como `19_6_abc.py` e rode.

**Código explicado:** quem herda **deve** implementar todos os métodos abstratos.

### 19.7 Métodos abstratos

**O que é:** método marcado com `@abstractmethod`; obriga implementação na filha.

**Exemplo:**

```python
from abc import ABC, abstractmethod

class Notificador(ABC):
    @abstractmethod
    def enviar(self, msg): ...

class Email(Notificador):
    def enviar(self, msg): print("email:", msg)

Email().enviar("oi")
```

**Passo a passo:**
1. Salve como `19_7_abstract.py` e rode.

**Código explicado:** sem implementar, instanciar a filha dá `TypeError`.

### 19.8 TypedDict

**O que é:** dict tipado, usado para checagem estática.

**Exemplo:**

```python
from typing import TypedDict

class Cliente(TypedDict):
    nome: str
    score: float

c: Cliente = {"nome": "Ana", "score": 0.82}
print(c["nome"])
```

**Passo a passo:**
1. Salve como `19_8_td.py` e rode.

**Código explicado:** em runtime é dict comum; ferramentas como mypy validam estrutura.

### 19.9 Literal

**O que é:** restringe um valor a um conjunto fixo de literais.

**Exemplo:**

```python
from typing import Literal

def definir_status(s: Literal["pendente", "aprovado"]):
    print(s)

definir_status("aprovado")
# definir_status("outro")  # mypy reclama
```

**Passo a passo:**
1. Salve como `19_9_literal.py` e rode.

**Código explicado:** alternativa leve a `Enum` quando só interessa o valor texto.

---

## 20. Type hints e annotations

### 20.1 Anotações de variáveis

**O que é:** declarar tipo esperado de uma variável com `: tipo`.

**Exemplo:**

```python
nome: str = "Ana"
idade: int = 35
scores: list[float] = [0.82, 0.91]
print(nome, idade, scores)
```

**Passo a passo:**
1. Salve como `20_1_var.py` e rode.

**Código explicado:** Python não checa em runtime, mas Pylance/mypy avisam erros.

### 20.2 Anotações de parâmetros

**O que é:** declarar tipo de cada parâmetro de função.

**Exemplo:**

```python
def calcular(valor: float, meses: int) -> float:
    return valor / meses

print(calcular(120000, 12))
```

**Passo a passo:**
1. Salve como `20_2_param.py` e rode.

**Código explicado:** anotações documentam a função e auxiliam o autocomplete.

### 20.3 Anotações de retorno

**O que é:** declarar tipo do retorno com `-> tipo`.

**Exemplo:**

```python
def saudacao(nome: str) -> str:
    return f"Olá, {nome}"

def nada() -> None:
    print("efeito colateral")
```

**Passo a passo:**
1. Salve como `20_3_ret.py` e rode.

**Código explicado:** `-> None` declara função sem retorno útil.

### 20.4 Tipos genéricos nativos

**O que é:** `list[T]`, `dict[K, V]`, `tuple[T, ...]`, `set[T]` (Python 3.9+).

**Exemplo:**

```python
nomes: list[str] = ["Ana", "Bruno"]
mapa: dict[str, int] = {"a": 1}
ponto: tuple[int, int] = (10, 20)

def soma(valores: list[float]) -> float:
    return sum(valores)

print(soma([1.0, 2.0]))
```

**Passo a passo:**
1. Salve como `20_4_gen.py` e rode.

**Código explicado:** dispensa `from typing import List, Dict` em projetos modernos.

### 20.5 Union com |

**O que é:** indicar que valor pode ser de mais de um tipo (Python 3.10+).

**Exemplo:**

```python
def parsear(v: int | str) -> int:
    return int(v)

print(parsear(10), parsear("42"))
```

**Passo a passo:**
1. Salve como `20_5_union.py` e rode.

**Código explicado:** equivalente a `Union[int, str]` da `typing`.

### 20.6 Optional

**O que é:** atalho para `T | None`.

**Exemplo:**

```python
from typing import Optional

def buscar(id_: int) -> Optional[str]:
    return "Ana" if id_ == 1 else None

print(buscar(1), buscar(2))
```

**Passo a passo:**
1. Salve como `20_6_opt.py` e rode.

**Código explicado:** prefira `str | None` (mais novo) em código moderno.

### 20.7 Any

**O que é:** "qualquer tipo"; desliga a checagem.

**Exemplo:**

```python
from typing import Any

def logar(valor: Any) -> None:
    print(repr(valor))

logar(10)
logar("ok")
logar([1, 2])
```

**Passo a passo:**
1. Salve como `20_7_any.py` e rode.

**Código explicado:** use `Any` com parcimônia; é uma porta aberta para erros.

### 20.8 Annotated

**O que é:** anexa metadados a um tipo (usado por FastAPI, Pydantic etc).

**Exemplo:**

```python
from typing import Annotated

Idade = Annotated[int, "anos"]

def cadastrar(idade: Idade) -> None:
    print(idade)

cadastrar(35)
```

**Passo a passo:**
1. Salve como `20_8_annot.py` e rode.

**Código explicado:** o segundo argumento é livre; cada framework define o que faz com ele.

### 20.9 Forward references

**O que é:** citar uma classe ainda não definida usando string.

**Exemplo:**

```python
class No:
    def __init__(self, valor: int, prox: "No | None" = None):
        self.valor = valor
        self.prox = prox

n = No(1, No(2))
print(n.valor, n.prox.valor)
```

**Passo a passo:**
1. Salve como `20_9_fwd.py` e rode.

**Código explicado:** sem string, o nome `No` ainda não existiria no momento da leitura.

### 20.10 from __future__ import annotations

**O que é:** transforma todas as anotações em strings, eliminando forward references.

**Exemplo:**

```python
from __future__ import annotations

class No:
    def __init__(self, valor: int, prox: No | None = None):
        self.valor = valor
        self.prox = prox

print(No(1).valor)
```

**Passo a passo:**
1. Salve como `20_10_future.py` e rode.

**Código explicado:** com isso, `No | None` funciona mesmo em versões antigas do Python.

### 20.11 Type hints em tempo de execução

**O que é:** acessar anotações via `__annotations__` ou `typing.get_type_hints`.

**Exemplo:**

```python
def f(x: int, y: str) -> bool:
    return True

print(f.__annotations__)

import typing
print(typing.get_type_hints(f))
```

**Passo a passo:**
1. Salve como `20_11_runtime.py` e rode.

**Código explicado:** frameworks como FastAPI leem isso para gerar validação automática.

### 20.12 Type hints em análise estática

**O que é:** ferramentas como mypy/Pylance leem anotações **sem executar** o código.

**Exemplo:**

```python
def soma(a: int, b: int) -> int:
    return a + b

# mypy reclamaria desta linha:
# soma("a", "b")
print(soma(1, 2))
```

**Passo a passo:**
1. Salve como `20_12_static.py`.
2. Instale mypy (`pip install mypy`) e rode `mypy 20_12_static.py`.
3. Sem erros nesse arquivo; descomente a linha errada para ver alerta.

**Código explicado:** type hints são contrato verificado **fora** do runtime.

---

## 21. Programação assíncrona

### 21.1 Funções síncronas

**O que é:** funções comuns; cada chamada bloqueia até retornar.

**Exemplo:**

```python
import time

def buscar(cliente):
    time.sleep(1)
    return cliente.upper()

print(buscar("ana"))
print(buscar("bruno"))
```

**Passo a passo:**
1. Salve como `21_1_sync.py` e rode.
2. Note os 2 segundos de espera total.

**Código explicado:** chamadas em série esperam uma a uma.

### 21.2 Funções assíncronas

**O que é:** funções que podem **pausar** sem bloquear o programa todo.

**Exemplo:**

```python
import asyncio

async def buscar(cliente):
    await asyncio.sleep(1)
    return cliente.upper()

async def main():
    a, b = await asyncio.gather(buscar("ana"), buscar("bruno"))
    print(a, b)

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `21_2_async.py` e rode.
2. Note que demora ~1s no total, não 2s.

**Código explicado:** `gather` roda em paralelo cooperativo.

### 21.3 async def

**O que é:** define corrotina; chamar não executa, devolve um objeto.

**Exemplo:**

```python
import asyncio

async def saudar(nome):
    return f"oi {nome}"

c = saudar("Ana")
print(c)                 # <coroutine object ...>
print(asyncio.run(c))
```

**Passo a passo:**
1. Salve como `21_3_async_def.py` e rode.

**Código explicado:** sem `await` ou `run`, a corrotina nunca roda.

### 21.4 await

**O que é:** pausa a corrotina atual até a outra terminar.

**Exemplo:**

```python
import asyncio

async def passo(n):
    await asyncio.sleep(0.5)
    return n * 2

async def main():
    a = await passo(10)
    b = await passo(20)
    print(a, b)

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `21_4_await.py` e rode.

**Código explicado:** `await` só pode aparecer dentro de `async def`.

### 21.5 Coroutine

**O que é:** objeto retornado por `async def`; precisa de event loop para rodar.

**Exemplo:**

```python
import asyncio

async def f():
    return 1

c = f()
print(type(c))    # <class 'coroutine'>
print(asyncio.run(c))
```

**Passo a passo:**
1. Salve como `21_5_coro.py` e rode.

**Código explicado:** corrotinas são "promessas" — o trabalho só acontece quando você dá `run`.

### 21.6 Event loop

**O que é:** mecanismo que despacha corrotinas e callbacks.

**Exemplo:**

```python
import asyncio

async def tarefa(nome, t):
    await asyncio.sleep(t)
    print("ok", nome)

async def main():
    await asyncio.gather(tarefa("A", 0.3), tarefa("B", 0.1))

asyncio.run(main())   # cria, roda e fecha o loop
```

**Passo a passo:**
1. Salve como `21_6_loop.py` e rode.
2. Veja "ok B" antes de "ok A".

**Código explicado:** `asyncio.run` orquestra tudo; B termina antes pois dorme menos.

### 21.7 async for

**O que é:** itera sobre async generator.

**Exemplo:**

```python
import asyncio

async def numeros():
    for i in range(3):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for n in numeros():
        print(n)

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `21_7_async_for.py` e rode.

**Código explicado:** cada `yield` é entregue após a pausa.

### 21.8 async with

**O que é:** usar context manager assíncrono (já visto em 15.7).

**Exemplo:**

```python
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def recurso():
    print("abrindo")
    yield "x"
    print("fechando")

async def main():
    async with recurso() as r:
        print("usando", r)

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `21_8_async_with.py` e rode.

**Código explicado:** abertura e fechamento podem aguardar I/O.

### 21.9 Async generators

**O que é:** generator com `async def` e `yield`; produz valores assincronamente.

**Exemplo:**

```python
import asyncio

async def stream():
    for v in [10, 20, 30]:
        await asyncio.sleep(0.05)
        yield v

async def main():
    async for v in stream():
        print(v)

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `21_9_async_gen.py` e rode.

**Código explicado:** ideal para streams de rede e WebSocket.

### 21.10 Tratamento de exceções em código async

**O que é:** mesmo `try/except`, agora envolvendo `await`.

**Exemplo:**

```python
import asyncio

async def falhar():
    raise RuntimeError("oops")

async def main():
    try:
        await falhar()
    except RuntimeError as e:
        print("tratado:", e)

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `21_10_exc.py` e rode.

**Código explicado:** exceções em corrotinas se propagam ao `await`.

### 21.11 Cancelamento de tarefas

**O que é:** interromper corrotina via `task.cancel()`.

**Exemplo:**

```python
import asyncio

async def trabalho():
    try:
        await asyncio.sleep(5)
    except asyncio.CancelledError:
        print("cancelado")
        raise

async def main():
    t = asyncio.create_task(trabalho())
    await asyncio.sleep(0.1)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("ok")

asyncio.run(main())
```

**Passo a passo:**
1. Salve como `21_11_cancel.py` e rode.

**Código explicado:** `cancel` envia `CancelledError` para a tarefa; trate-a para limpar recursos.

---

## 22. Funções built-in essenciais

### 22.1 print

**O que é:** envia texto à saída padrão.

**Exemplo:**

```python
print("oi")
print("a", "b", sep="-")
print("sem quebra", end="!")
print(" continua")
```

**Passo a passo:**
1. Salve como `22_1_print.py` e rode.

**Código explicado:** `sep` muda o separador; `end` muda o final (default `\n`).

### 22.2 input

**O que é:** lê uma linha do teclado como string.

**Exemplo:**

```python
nome = input("Nome: ")
print(f"Olá, {nome}")
```

**Passo a passo:**
1. Salve como `22_2_input.py` e rode `python 22_2_input.py`.
2. Digite o nome e Enter.

**Código explicado:** `input` sempre devolve `str`; converta com `int(...)` se necessário.

### 22.3 len

**O que é:** retorna tamanho de sequência ou coleção.

**Exemplo:**

```python
print(len("Ana"))
print(len([1, 2, 3]))
print(len({"a": 1, "b": 2}))
```

**Passo a passo:**
1. Salve como `22_3_len.py` e rode.

**Código explicado:** funciona em qualquer objeto que implemente `__len__`.

### 22.4 type

**O que é:** retorna a classe do objeto.

**Exemplo:**

```python
print(type(10))
print(type(10) is int)
```

**Passo a passo:**
1. Salve como `22_4_type.py` e rode.

**Código explicado:** prefira `isinstance` para checagens com herança.

### 22.5 isinstance

**O que é:** testa se objeto é instância de classe (ou tupla de classes).

**Exemplo:**

```python
print(isinstance(10, int))
print(isinstance(True, int))   # True (bool é int)
print(isinstance("x", (int, str)))
```

**Passo a passo:**
1. Salve como `22_5_isinst.py` e rode.

**Código explicado:** considera herança; `bool` é subclasse de `int`.

### 22.6 range

**O que é:** sequência de inteiros gerada sob demanda.

**Exemplo:**

```python
print(list(range(5)))         # [0..4]
print(list(range(2, 10, 2)))  # [2,4,6,8]
print(list(range(10, 0, -2))) # [10,8,6,4,2]
```

**Passo a passo:**
1. Salve como `22_6_range.py` e rode.

**Código explicado:** parâmetros são `(start, stop, step)`; `stop` é exclusivo.

### 22.7 enumerate

**O que é:** itera fornecendo `(indice, valor)`.

**Exemplo:**

```python
for i, c in enumerate(["Ana", "Bruno"], start=1):
    print(i, c)
```

**Passo a passo:**
1. Salve como `22_7_enum.py` e rode.

**Código explicado:** evita controlar índice manualmente.

### 22.8 zip

**O que é:** combina iteráveis pareando elementos.

**Exemplo:**

```python
nomes = ["Ana", "Bruno"]
scores = [0.82, 0.67]
for n, s in zip(nomes, scores):
    print(n, s)
```

**Passo a passo:**
1. Salve como `22_8_zip.py` e rode.

**Código explicado:** para no fim do menor iterável.

### 22.9 map

**O que é:** aplica função a cada item de iterável; retorna iterador.

**Exemplo:**

```python
valores = ["1", "2", "3"]
inteiros = list(map(int, valores))
print(inteiros)
```

**Passo a passo:**
1. Salve como `22_9_map.py` e rode.

**Código explicado:** equivalente lazy a list comp `[int(v) for v in valores]`.

### 22.10 filter

**O que é:** mantém só os itens em que a função retorna truthy.

**Exemplo:**

```python
valores = [10, 50, 80, 120]
altos = list(filter(lambda v: v > 60, valores))
print(altos)
```

**Passo a passo:**
1. Salve como `22_10_filter.py` e rode.

**Código explicado:** equivalente a `[v for v in valores if v > 60]`.

### 22.11 sorted

**O que é:** retorna lista nova ordenada.

**Exemplo:**

```python
clientes = [("Ana", 0.82), ("Bruno", 0.67)]
print(sorted(clientes, key=lambda c: c[1], reverse=True))
```

**Passo a passo:**
1. Salve como `22_11_sorted.py` e rode.

**Código explicado:** `key` decide o critério; `reverse` inverte a ordem.

### 22.12 sum

**O que é:** soma os itens de um iterável numérico.

**Exemplo:**

```python
print(sum([10, 20, 30]))
print(sum(range(1, 101)))
print(sum(v for v in [1, 2, 3] if v > 1))
```

**Passo a passo:**
1. Salve como `22_12_sum.py` e rode.

**Código explicado:** aceita generator expression direto, sem `[]`.

### 22.13 min e max

**O que é:** menor/maior elemento; aceitam `key`.

**Exemplo:**

```python
print(min([3, 1, 2]))
print(max(["Ana", "Bruno", "Carla"], key=len))
```

**Passo a passo:**
1. Salve como `22_13_minmax.py` e rode.

**Código explicado:** `key=len` faz `max` escolher pela contagem de letras.

### 22.14 any e all

**O que é:** `any` é `True` se **algum** for truthy; `all` se **todos** forem.

**Exemplo:**

```python
scores = [0.5, 0.7, 0.9]
print(any(s >= 0.8 for s in scores))   # True
print(all(s > 0 for s in scores))      # True
```

**Passo a passo:**
1. Salve como `22_14_anyall.py` e rode.

**Código explicado:** ambos param assim que decidem (curto-circuito).

### 22.15 open

**O que é:** abre arquivo em modo texto ou binário.

**Exemplo:**

```python
with open("nota.txt", "w", encoding="utf-8") as f:
    f.write("ok")

with open("nota.txt", encoding="utf-8") as f:
    print(f.read())
```

**Passo a passo:**
1. Salve como `22_15_open.py` e rode.

**Código explicado:** sempre prefira `with` para fechamento automático.

---

## 23. Arquivos e recursos

### 23.1 Leitura de arquivos

**O que é:** ler conteúdo via `read`, `readline`, ou iteração.

**Exemplo:**

```python
with open("dados.txt", "w", encoding="utf-8") as f:
    f.write("linha1\nlinha2\nlinha3\n")

with open("dados.txt", encoding="utf-8") as f:
    for linha in f:
        print(linha.rstrip())
```

**Passo a passo:**
1. Salve como `23_1_read.py` e rode.

**Código explicado:** iterar o arquivo entrega uma linha por vez, eficiente para arquivos grandes.

### 23.2 Escrita de arquivos

**O que é:** escrever com `write` ou `writelines`.

**Exemplo:**

```python
with open("scores.txt", "w", encoding="utf-8") as f:
    f.write("Ana;0.82\n")
    f.writelines(["Bruno;0.67\n", "Carla;0.91\n"])
```

**Passo a passo:**
1. Salve como `23_2_write.py` e rode.

**Código explicado:** `writelines` não adiciona quebra; inclua `\n` no fim de cada item.

### 23.3 Modos de abertura

**O que é:** `"r"` ler, `"w"` sobrescrever, `"a"` adicionar, `"x"` criar (falha se existir), `"b"` binário, `"+"` leitura+escrita.

**Exemplo:**

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("evento\n")

with open("foto.bin", "rb") as f:
    cabecalho = f.read(8)
print(cabecalho)
```

**Passo a passo:**
1. Salve como `23_3_modos.py` e rode.

**Código explicado:** `"a"` preserva conteúdo prévio; `"rb"` evita conversão de encoding.

### 23.4 Encoding

**O que é:** define como bytes são decodificados em texto.

**Exemplo:**

```python
with open("acentos.txt", "w", encoding="utf-8") as f:
    f.write("ação")

with open("acentos.txt", encoding="utf-8") as f:
    print(f.read())
```

**Passo a passo:**
1. Salve como `23_4_enc.py` e rode.

**Código explicado:** sempre informe `encoding="utf-8"` para evitar dor de cabeça em outros sistemas.

### 23.5 Manipulação segura com with

**O que é:** garante fechamento mesmo com erro.

**Exemplo:**

```python
try:
    with open("dados.txt", encoding="utf-8") as f:
        primeiro = f.readline()
        raise RuntimeError("oops")
except RuntimeError:
    print("erro tratado, arquivo já fechado")
```

**Passo a passo:**
1. Salve como `23_5_safe.py` e rode.

**Código explicado:** o `__exit__` do file handle é chamado durante a propagação do erro.

### 23.6 Bytes e texto

**O que é:** modo texto retorna `str`; modo binário retorna `bytes`.

**Exemplo:**

```python
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("ok")

with open("a.txt", "rb") as f:
    print(f.read())          # b'ok'

with open("a.txt", "r", encoding="utf-8") as f:
    print(f.read())          # 'ok'
```

**Passo a passo:**
1. Salve como `23_6_bytes.py` e rode.

**Código explicado:** binário é necessário para imagens, áudio, PDFs; texto para .txt, .csv, .md.

---

## 24. Testes e depuração na linguagem

### 24.1 assert

**O que é:** verifica condição; lança `AssertionError` se falsa.

**Exemplo:**

```python
def calcular_parcela(v, m):
    assert m > 0, "meses > 0"
    return v / m

print(calcular_parcela(120000, 12))
# calcular_parcela(120000, 0)   # AssertionError
```

**Passo a passo:**
1. Salve como `24_1_assert.py` e rode.

**Código explicado:** útil em testes e validações internas; rodar com `python -O` desativa asserts.

### 24.2 breakpoint

**O que é:** pausa o programa e abre o `pdb` (debugger interativo).

**Exemplo:**

```python
def calcular(v, m):
    parcela = v / m
    breakpoint()    # pause aqui
    return parcela

print(calcular(120000, 12))
```

**Passo a passo:**
1. Salve como `24_2_break.py` e rode.
2. Use `n` (next), `p var` (print), `c` (continue) no prompt `(Pdb)`.

**Código explicado:** `breakpoint()` substitui `import pdb; pdb.set_trace()`.

### 24.3 Traceback

**O que é:** rastreamento que Python imprime quando há exceção não tratada.

**Exemplo:**

```python
def a():
    return 10 / 0

def b():
    return a()

b()
```

**Passo a passo:**
1. Salve como `24_3_trace.py` e rode.
2. Veja a sequência b → a → ZeroDivisionError.

**Código explicado:** leia o traceback de baixo para cima; o erro está na última linha.

### 24.4 Inspeção de tipos

**O que é:** investigar atributos de objetos com `type`, `dir`, `vars`, `help`.

**Exemplo:**

```python
class Cliente:
    def __init__(self, nome):
        self.nome = nome

c = Cliente("Ana")
print(type(c))
print(dir(c)[-3:])
print(vars(c))
help(Cliente.__init__)
```

**Passo a passo:**
1. Salve como `24_4_insp.py` e rode.

**Código explicado:** ferramentas perfeitas para descobrir o que um objeto desconhecido suporta.

### 24.5 Erros de sintaxe

**O que é:** detectados antes da execução; o programa nem inicia.

**Exemplo:**

```python
# arquivo: 24_5_syntax.py (com erro)
# def f()
#     return 1

# correto:
def f():
    return 1

print(f())
```

**Passo a passo:**
1. Salve a versão errada e rode: aparecerá `SyntaxError`.
2. Corrija com os dois-pontos e rode.

**Código explicado:** Python compila o arquivo inteiro antes de rodar; erros de sintaxe quebram tudo.

### 24.6 Erros de runtime

**O que é:** ocorrem durante a execução; alguns dependem de input.

**Exemplo:**

```python
def parsear(v):
    return int(v)

print(parsear("10"))
try:
    print(parsear("abc"))
except ValueError as e:
    print("runtime error:", e)
```

**Passo a passo:**
1. Salve como `24_6_runtime.py` e rode.

**Código explicado:** trate com `try/except` o que **pode** falhar com entradas reais.

---

## 25. Tópicos avançados de Python

### 25.1 Descritores

**O que é:** objeto que controla acesso de atributo via `__get__`/`__set__`.

**Exemplo:**

```python
class Positivo:
    def __set_name__(self, owner, name): self.name = name
    def __get__(self, obj, owner): return obj.__dict__[self.name]
    def __set__(self, obj, valor):
        if valor <= 0:
            raise ValueError("deve ser > 0")
        obj.__dict__[self.name] = valor

class Conta:
    saldo = Positivo()

c = Conta()
c.saldo = 100
print(c.saldo)
# c.saldo = -1   # ValueError
```

**Passo a passo:**
1. Salve como `25_1_desc.py` e rode.

**Código explicado:** descritores são a base de `property`, `classmethod`, dataclass fields etc.

### 25.2 property

**O que é:** transforma método em atributo computado.

**Exemplo:**

```python
class Valor:
    def __init__(self, q): self._q = q

    @property
    def em_reais(self):
        return f"R$ {self._q:,.2f}"

    @em_reais.setter
    def em_reais(self, v):
        self._q = float(v)

v = Valor(120000)
print(v.em_reais)
v.em_reais = 200000
print(v.em_reais)
```

**Passo a passo:**
1. Salve como `25_2_prop.py` e rode.

**Código explicado:** API de atributo com lógica embutida; chama o getter/setter automaticamente.

### 25.3 Metaclasses

**O que é:** "classe de classes" — controla como classes são criadas.

**Exemplo:**

```python
class Logger(type):
    def __new__(mcs, name, bases, attrs):
        print("criando classe", name)
        return super().__new__(mcs, name, bases, attrs)

class Servico(metaclass=Logger):
    pass
```

**Passo a passo:**
1. Salve como `25_3_meta.py` e rode.
2. Veja "criando classe Servico" antes do `print` final.

**Código explicado:** poderosa, mas raramente necessária; frameworks como ORMs usam.

### 25.4 Protocolos de objetos

**O que é:** "interface implícita": basta implementar os dunders certos para se comportar como X.

**Exemplo:**

```python
class Distancia:
    def __init__(self, m): self.m = m
    def __add__(self, o): return Distancia(self.m + o.m)
    def __repr__(self): return f"{self.m}m"
    def __bool__(self): return self.m > 0

print(Distancia(10) + Distancia(5))
print(bool(Distancia(0)))
```

**Passo a passo:**
1. Salve como `25_4_proto.py` e rode.

**Código explicado:** implementar o "protocolo numérico" faz seu objeto suportar `+`, `-`, `*`...

### 25.5 Data model do Python

**O que é:** conjunto de dunders que definem como objetos interagem com a linguagem.

**Exemplo:**

```python
class Carrinho:
    def __init__(self): self.itens = []
    def __len__(self): return len(self.itens)
    def __getitem__(self, i): return self.itens[i]
    def __iter__(self): return iter(self.itens)
    def __contains__(self, x): return x in self.itens

c = Carrinho()
c.itens = ["a", "b"]
print(len(c), c[0], "a" in c)
for x in c: print(x)
```

**Passo a passo:**
1. Salve como `25_5_dm.py` e rode.

**Código explicado:** com 4 dunders seu objeto vira coleção quase completa.

### 25.6 Gerenciamento de memória

**O que é:** Python usa contagem de referências + garbage collector cíclico.

**Exemplo:**

```python
import sys, gc

a = []
b = a
print(sys.getrefcount(a))   # >= 3
del b
print(sys.getrefcount(a))

class No:
    pass

x = No(); y = No()
x.outro = y; y.outro = x   # ciclo
del x; del y
print(gc.collect(), "objetos coletados")
```

**Passo a passo:**
1. Salve como `25_6_gc.py` e rode.

**Código explicado:** ciclos de referência são limpos pelo `gc` periodicamente.

### 25.7 GIL

**O que é:** Global Interpreter Lock — só uma thread executa bytecode Python por vez no CPython.

**Exemplo:**

```python
import threading, time

def trabalho(n):
    s = 0
    for i in range(n):
        s += i
    return s

inicio = time.time()
t1 = threading.Thread(target=trabalho, args=(10**7,))
t2 = threading.Thread(target=trabalho, args=(10**7,))
t1.start(); t2.start(); t1.join(); t2.join()
print(f"threads: {time.time() - inicio:.2f}s")
```

**Passo a passo:**
1. Salve como `25_7_gil.py` e rode.
2. Compare com versão sequencial: pouca diferença em CPU-bound.

**Código explicado:** para CPU-bound, use `multiprocessing`; para I/O-bound, threads/async resolvem.

### 25.8 Introspection

**O que é:** examinar objetos em tempo de execução.

**Exemplo:**

```python
import inspect

def somar(a: int, b: int) -> int:
    """soma dois inteiros"""
    return a + b

print(inspect.signature(somar))
print(inspect.getdoc(somar))
print(inspect.getsource(somar))
```

**Passo a passo:**
1. Salve como `25_8_inspect.py` e rode.

**Código explicado:** `inspect` é base de docs automáticas, validações e plugins.

### 25.9 Monkey patching

**O que é:** trocar atributos/métodos em runtime.

**Exemplo:**

```python
class Servico:
    def saudar(self): return "oi"

def saudar_novo(self):
    return "olá!"

Servico.saudar = saudar_novo
print(Servico().saudar())
```

**Passo a passo:**
1. Salve como `25_9_monkey.py` e rode.

**Código explicado:** poderoso para testes, perigoso em produção; deixa código surpreendente.

### 25.10 Duck typing

**O que é:** "se anda como pato e quaca como pato, é pato"; importa o **comportamento**, não a classe.

**Exemplo:**

```python
class Pato:
    def quack(self): return "quack"

class Pessoa:
    def quack(self): return "imitando quack"

def fazer_barulho(obj):
    return obj.quack()

print(fazer_barulho(Pato()))
print(fazer_barulho(Pessoa()))
```

**Passo a passo:**
1. Salve como `25_10_duck.py` e rode.

**Código explicado:** Python não exige herança comum; basta ter o método.

---

## Conclusão

Cada subtopic deste ebook tem seu próprio exemplo executável. A recomendação é:

1. Crie uma pasta de estudo (`estudo_python/`).
2. Para cada subtopic, copie o exemplo e rode.
3. Modifique o código e veja o que muda.
4. Marque os subtopics em que se sentir inseguro e revise antes da próxima entrevista.
