# POP Distribution System

Sistema de distribuição centralizada e automatizada de Procedimentos Operacionais Padrão (POPs) para ambientes corporativos.

## Sobre o projeto

O **POP Distribution System** é um projeto de automação desenvolvido com o objetivo de centralizar e facilitar a distribuição de documentos operacionais em ambientes corporativos com múltiplos computadores conectados à rede.

Em ambientes que possuem diversas estações de trabalho, manter documentos atualizados e distribuí-los manualmente pode gerar retrabalho, inconsistências, dificuldades de gerenciamento e dependência de processos manuais.

A proposta deste projeto é desenvolver uma solução que permita disponibilizar documentos a partir de um repositório central, automatizando o processo de distribuição e atualização dos arquivos nas máquinas clientes.

O projeto está sendo desenvolvido de forma incremental, utilizando tecnologias relacionadas a infraestrutura, redes, automação, APIs e práticas DevOps.

---

## Objetivo

Desenvolver um sistema capaz de centralizar documentos POP e automatizar sua distribuição para computadores de um ambiente corporativo, permitindo que os arquivos sejam disponibilizados e atualizados de maneira mais organizada, eficiente e padronizada.

### Objetivos específicos

- Centralizar os documentos operacionais em um repositório.
- Automatizar a distribuição de arquivos para computadores clientes.
- Reduzir a necessidade de transferências manuais por pendrives.
- Facilitar futuras atualizações dos documentos.
- Manter uma estrutura padronizada de arquivos e diretórios.
- Aplicar conceitos de redes, infraestrutura, automação e DevOps em um cenário prático.

---

## Problema que o projeto busca resolver

Em ambientes corporativos, a distribuição de procedimentos operacionais para diversas máquinas pode depender de processos manuais, dificultando a manutenção e a atualização dos documentos.

Entre os principais problemas estão:

- Distribuição manual de arquivos para múltiplos computadores.
- Dificuldade para garantir que todos os computadores recebam versões atualizadas.
- Dependência de dispositivos USB ou transferências individuais.
- Falta de centralização dos documentos.
- Retrabalho durante atualizações de arquivos.
- Dificuldade para padronizar a estrutura dos documentos nas máquinas clientes.

O sistema busca reduzir esses problemas por meio de uma estrutura centralizada e de mecanismos automatizados de distribuição.

---

## Funcionalidades

### Implementadas

- API para disponibilização dos documentos POP.
- Endpoint para verificação do status da aplicação.
- Repositório central de documentos.
- Localização automática de arquivos dentro do diretório de POPs.
- Suporte à organização de documentos em subdiretórios.
- Compactação dos documentos em arquivo ZIP.
- Disponibilização do pacote ZIP para download através da API.
- Documentação interativa dos endpoints utilizando Swagger UI.

### Em desenvolvimento / planejadas

- Distribuição automatizada para computadores Windows.
- Script para download e atualização dos POPs nas máquinas clientes.
- Extração automática dos documentos baixados.
- Padronização da estrutura de diretórios nos computadores clientes.
- Validação da integridade dos arquivos distribuídos.
- Controle de versões dos documentos.
- Registro de logs das operações de distribuição e atualização.
- Tratamento de erros durante o processo de atualização.
- Automatização da execução nos computadores clientes.
- Melhorias de segurança e controle de acesso à API.

---

## Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem utilizada no desenvolvimento do sistema |
| FastAPI | Desenvolvimento da API de distribuição |
| Uvicorn | Servidor ASGI para execução da aplicação |
| Linux / Ubuntu | Ambiente de desenvolvimento e execução |
| Git | Controle de versão do código |
| GitHub | Hospedagem do repositório e acompanhamento do desenvolvimento |
| PowerShell | Planejado para automação de distribuição nas máquinas Windows |

---

## Arquitetura atual

Atualmente, o sistema possui uma API desenvolvida em Python utilizando FastAPI, responsável por localizar os documentos armazenados no repositório central, compactá-los e disponibilizá-los para download.

```text
                    ┌───────────────────────┐
                    │   Repositório POPs    │
                    │                       │
                    │  Documentos e pastas │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      FastAPI          │
                    │                       │
                    │ Localiza os arquivos │
                    │ e cria o ZIP          │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Pacote POPs.zip     │
                    │                       │
                    │ Disponível via API    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Download do ZIP    │
                    │                       │
                    │     Cliente/API       │
                    └───────────────────────┘
```

> A distribuição automatizada para as máquinas clientes ainda faz parte das próximas etapas do desenvolvimento.

---

## Estrutura do projeto

```text
SistemaAlertasRede/
│
├── server/
│   └── spp/
│       ├── main.py
│       └── routes/
│           └── pops.py
│
├── storage/
│   └── POPs/
│       └── documentos/
│
├── README.md
└── ...
```

| Diretório / arquivo | Descrição |
|---|---|
| `server/` | Componentes relacionados ao servidor da aplicação |
| `server/spp/main.py` | Inicialização e configuração da API |
| `server/spp/routes/` | Rotas e endpoints da aplicação |
| `server/spp/routes/pops.py` | Endpoint responsável pela distribuição dos POPs |
| `storage/POPs/` | Repositório central dos documentos que serão distribuídos |

---

## Funcionamento atual

O processo de distribuição implementado atualmente funciona da seguinte maneira:

1. Os documentos POP são armazenados no diretório central `storage/POPs/`.
2. A API recebe uma solicitação de download.
3. O sistema localiza os arquivos disponíveis, incluindo documentos dentro de subdiretórios.
4. Os documentos são compactados em um arquivo ZIP.
5. O pacote `POPs.zip` é disponibilizado para download.
6. Após o envio da resposta, o arquivo ZIP temporário é removido do servidor.

---

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/` | Verifica se a API está online |
| `GET` | `/api/v1/pops/dowload` | Compacta os documentos POP e disponibiliza o ZIP para download |

> Nota: o endpoint de download utiliza atualmente a grafia `dowload`. A nomenclatura será padronizada durante a evolução do projeto.

---

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

### 2. Acessar o diretório

```bash
cd SistemaAlertasRede
```

### 3. Criar o ambiente virtual

```bash
python3 -m venv .venv
```

### 4. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

### 5. Instalar as dependências

```bash
pip install fastapi uvicorn
```

### 6. Executar a aplicação

```bash
uvicorn server.spp.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Acessar a aplicação

Com o servidor em execução:

| Recurso | Endereço |
|---|---|
| API | http://127.0.0.1:8000 |
| Documentação Swagger | http://127.0.0.1:8000/docs |
| Documentação ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

---

## Roadmap

O projeto será desenvolvido em etapas, priorizando a implementação, validação e versionamento de cada funcionalidade.

- [x] Criar estrutura inicial do projeto.
- [x] Desenvolver API utilizando FastAPI.
- [x] Implementar endpoint de status da aplicação.
- [x] Criar repositório central de documentos POP.
- [x] Implementar localização dos documentos.
- [x] Implementar compactação dos documentos em ZIP.
- [x] Disponibilizar os arquivos para download através da API.
- [x] Validar o download e a integridade básica do pacote.
- [ ] Organizar documentação do projeto.
- [ ] Implementar script de distribuição para clientes Windows.
- [ ] Automatizar download e extração nos computadores clientes.
- [ ] Implementar mecanismo de atualização dos documentos.
- [ ] Criar validação de integridade dos arquivos.
- [ ] Implementar logs de distribuição.
- [ ] Implementar controle de versões dos POPs.
- [ ] Avaliar autenticação e segurança da comunicação.
- [ ] Realizar testes em ambiente simulado de rede corporativa.
- [ ] Preparar implantação e execução em ambiente de rede.

---

## Segurança e ambiente de utilização

O projeto está em desenvolvimento e ainda não possui todos os mecanismos de segurança necessários para implantação em um ambiente corporativo real.

Antes de uma implantação em produção, deverão ser avaliados:

- Autenticação e autorização.
- Restrição de acesso ao repositório de documentos.
- Segurança na comunicação entre clientes e servidor.
- Proteção contra distribuição de arquivos não autorizados.
- Logs e auditoria de operações.
- Validação dos arquivos recebidos pelos computadores clientes.

Documentos corporativos reais, confidenciais ou internos não devem ser publicados no repositório GitHub.

---

## Status do projeto

**Em desenvolvimento.**

O projeto está sendo desenvolvido gradualmente, com foco na implementação de funcionalidades, testes práticos, automação, infraestrutura e versionamento utilizando Git e GitHub.

---

## Autor

Desenvolvido como projeto prático de estudos e portfólio, com foco em DevOps, infraestrutura, automação, redes e gerenciamento de sistemas.


