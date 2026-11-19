
# POP Distribution System — Arquitetura

## 1. Objetivo

Desenvolver uma ferramenta de distribuição centralizada e automatizada de documentos POP (Procedimentos Operacionais Padrão), permitindo que um responsável publique ou atualize documentos em um servidor e que os computadores dos colaboradores recebam essas atualizações automaticamente.

O sistema deverá funcionar sem exigir ferramentas de desenvolvimento nos computadores dos colaboradores e sem depender de alterações na infraestrutura de rede local.

---

## 2. Cenário e restrições

O projeto está sendo desenvolvido considerando as seguintes condições:

- Não temos autorização para alterar a rede da república.
- Não temos acesso administrativo ao roteador ou às configurações da infraestrutura de rede.
- A gestão confirmou que a rede permite conexões de saída para a Internet.
- Não podemos depender da abertura de portas de entrada no roteador.
- Não podemos depender de IP público dedicado ou IP fixo local.
- Os computadores dos colaboradores utilizam Windows.
- Os colaboradores não devem precisar executar comandos ou realizar atualizações manualmente.
- O sistema deve minimizar interferências na operação dos usuários.

### Decisão

A arquitetura deverá permitir comunicação utilizando conexões de saída para Internet, sem exigir alterações no roteador ou na infraestrutura de rede da república.

---

## 3. Arquitetura planejada

### Servidor central

Responsável por armazenar, organizar, controlar e disponibilizar os documentos POP.

Tecnologias planejadas:

- Ubuntu/Linux
- Python
- FastAPI
- Docker
- Docker Compose
- Cloudflare Tunnel (avaliado para exposição segura do serviço)

### Agente Windows

Pequeno programa de automação instalado nos computadores dos colaboradores.

Responsabilidades:

- Consultar o servidor periodicamente.
- Verificar se existem atualizações.
- Baixar documentos atualizados.
- Validar os downloads.
- Atualizar os documentos locais.
- Preservar os documentos existentes em caso de falha.
- Registrar logs de execução.
- Executar em segundo plano.
- Evitar interferência na operação do usuário.

Tecnologias inicialmente planejadas:

- PowerShell
- Windows Task Scheduler (Agendador de Tarefas)
- Recursos nativos do Windows

---

## 4. Fluxo de funcionamento

1. O administrador adiciona ou atualiza documentos no repositório central.
2. O servidor identifica e disponibiliza as atualizações.
3. Os agentes Windows realizam consultas periódicas ao servidor.
4. O servidor informa se há atualizações disponíveis.
5. Caso existam atualizações, o agente baixa os arquivos.
6. O agente valida a integridade dos arquivos baixados.
7. Os arquivos são atualizados na pasta local definida.
8. O agente registra o resultado da operação.
9. Caso ocorra uma falha, os documentos locais existentes são preservados e uma nova tentativa poderá ocorrer posteriormente.

---

## 5. Comunicação

### Restrição de rede

Não serão necessárias configurações de rede administradas por nós na república.

A comunicação deverá funcionar por conexões de saída para Internet.

### Solução em avaliação

Cloudflare Tunnel:

- Permite disponibilizar um serviço hospedado localmente.
- Utiliza conexões iniciadas pelo servidor para a infraestrutura do túnel.
- Evita a necessidade de abrir portas de entrada no roteador.
- Permite disponibilizar uma URL HTTPS para os agentes.
- Não exige que os agentes instalem VPN.

A implementação definitiva dependerá da configuração do serviço, domínio/hostname, disponibilidade e requisitos de segurança.

### Comunicação dos agentes

Os agentes Windows deverão iniciar as consultas ao servidor.

O servidor não deverá depender de conexões iniciadas diretamente para os computadores dos colaboradores.

---

## 6. Segurança

Como o serviço poderá ser acessível pela Internet, segurança será requisito obrigatório.

Planejamento:

- HTTPS.
- Autenticação dos agentes.
- Controle de autorização.
- Validação de arquivos.
- Verificação de integridade por hash.
- Logs de operações.
- Proteção contra downloads inválidos.
- Preservação dos documentos existentes em caso de falha.
- Proteção das credenciais e tokens.
- Restrição dos endpoints administrativos.
- Avaliação de rate limiting.
- Evitar exposição desnecessária de informações.

O túnel não substitui a autenticação e a segurança da aplicação.

---

## 7. Comportamento esperado do agente

O agente deverá:

- Funcionar silenciosamente em segundo plano.
- Não exigir Python, Git, Docker ou VS Code.
- Verificar atualizações em intervalos configuráveis.
- Baixar arquivos para uma área temporária antes da substituição.
- Validar os arquivos antes de aplicar a atualização.
- Evitar corromper ou apagar documentos válidos.
- Não forçar o fechamento de programas do usuário.
- Tratar arquivos bloqueados e tentar novamente posteriormente.
- Registrar atualizações bem-sucedidas e falhas.
- Continuar funcionando mesmo quando o servidor estiver temporariamente indisponível.

---

## 8. Tecnologias planejadas

| Tecnologia | Finalidade |
|---|---|
| Ubuntu/Linux | Sistema operacional do servidor |
| Python | Desenvolvimento da aplicação e API |
| FastAPI | API de distribuição de documentos |
| Docker | Containerização da aplicação |
| Docker Compose | Gerenciamento dos containers |
| Cloudflare Tunnel | Acesso externo sem abertura de portas na rede |
| PowerShell | Automação do agente Windows |
| Windows Task Scheduler | Agendamento das verificações |
| Git | Versionamento do código |
| GitHub | Repositório e portfólio |
| HTTPS | Proteção da comunicação |
| Hash SHA-256 | Verificação da integridade dos arquivos |


### 8.1 Servidor e API

O servidor central está implementado utilizando Python e FastAPI.

A API é responsável por disponibilizar os documentos POPs armazenados no repositório central, permitindo que os clientes realizem o download dos documentos.

Tecnologias atualmente implementadas:

- Python
- FastAPI
- Uvicorn
- Docker
- Docker Compose

### 8.2 Containerização

A aplicação foi containerizada utilizando Docker.

Arquivos responsáveis pela configuração:

| Arquivo | Responsabilidade |
|---|---|
| `Dockerfile` | Construção da imagem da API |
| `compose.yaml` | Gerenciamento do serviço e configurações do contêiner |
| `.dockerignore` | Exclusão de arquivos desnecessários do contexto de construção |
| `requirements.txt` | Dependências Python |

O serviço da API é gerenciado pelo Docker Compose.

Configurações atuais:

- Serviço: `api`
- Contêiner: `pop-server`
- Porta: `8000`
- Política de reinicialização: `unless-stopped`

A API pode ser iniciada utilizando:

```bash
docker compose up -d --build
---

## 9. Etapas de desenvolvimento

### Fase 1 — API e distribuição

- [x] Estrutura inicial do projeto.
- [x] API FastAPI.
- [x] Endpoint de saúde.
- [x] Endpoint de distribuição de POPs.
- [x] Download de documentos em ZIP.
- [x] Versionamento com Git.
- [x] Repositório publicado no GitHub.

### Fase 2 — Containerização

- [ ] Criar Dockerfile.
- [ ] Configurar Docker Compose.
- [ ] Containerizar a API.
- [ ] Definir armazenamento persistente.
- [ ] Testar a aplicação em containers.
- [ ] Documentar execução e logs.

### Fase 3 — Controle de atualizações

- [ ] Implementar controle de versão dos documentos.
- [ ] Identificar documentos novos ou modificados.
- [ ] Criar endpoint para consultar atualizações.
- [ ] Implementar hash dos arquivos.
- [ ] Evitar downloads desnecessários.

### Fase 4 — Agente Windows

- [ ] Criar agente em PowerShell.
- [ ] Consultar o servidor automaticamente.
- [ ] Baixar atualizações.
- [ ] Validar integridade dos arquivos.
- [ ] Atualizar arquivos locais de forma segura.
- [ ] Implementar logs.
- [ ] Tratar falhas e novas tentativas.

### Fase 5 — Instalação e automação

- [ ] Preparar instalação simplificada do agente.
- [ ] Configurar execução em segundo plano.
- [ ] Configurar Windows Task Scheduler.
- [ ] Definir intervalo de verificação.
- [ ] Testar sem ferramentas de desenvolvimento instaladas.

### Fase 6 — Comunicação externa

- [ ] Avaliar e configurar Cloudflare Tunnel.
- [ ] Disponibilizar endpoint HTTPS.
- [ ] Validar comunicação sem abertura de portas.
- [ ] Configurar autenticação dos agentes.
- [ ] Avaliar domínio e custos.
- [ ] Testar acesso a partir de outra rede.

### Fase 7 — Testes reais

- [ ] Testar em uma segunda máquina Windows.
- [ ] Confirmar que não exige Python, Git ou Docker no cliente.
- [ ] Testar atualização automática.
- [ ] Testar servidor indisponível.
- [ ] Testar download interrompido.
- [ ] Testar arquivos inválidos.
- [ ] Testar documento aberto/bloqueado.
- [ ] Confirmar preservação dos documentos existentes.
- [ ] Confirmar logs e rastreabilidade.

---

## 10. Critérios do MVP

O MVP será considerado funcional quando:

- O servidor disponibilizar documentos POP.
- A aplicação estiver executando em Docker.
- Os agentes Windows conseguirem se comunicar com o servidor.
- A comunicação não exigir alterações no roteador da república.
- Um computador Windows sem ferramentas de desenvolvimento conseguir receber atualizações.
- As atualizações forem realizadas automaticamente.
- O processo ocorrer sem intervenção do colaborador.
- Falhas não causarem perda de documentos válidos.
- O sistema possuir logs que permitam verificar as operações.

---

## 11. Fora do escopo inicial

Não faz parte dos requisitos iniciais:

- Alterar o roteador da república.
- Abrir portas de entrada na rede local.
- Configurar firewall administrado por terceiros.
- Instalar ferramentas de desenvolvimento nos computadores dos colaboradores.
- Exigir que os colaboradores atualizem documentos manualmente.
- Forçar encerramento de programas utilizados pelos colaboradores.

---

## 12. Objetivo de portfólio

O projeto tem como objetivo demonstrar conhecimentos práticos em:

- Linux e administração de servidores.
- Redes e comunicação cliente-servidor.
- Python e APIs.
- Docker e containerização.
- Deploy.
- Automação Windows com PowerShell.
- Git e GitHub.
- Segurança de aplicações.
- Logs e troubleshooting.
- Infraestrutura e Cloud.

O desenvolvimento será realizado progressivamente, com testes a cada etapa e registro das mudanças no GitHub.
