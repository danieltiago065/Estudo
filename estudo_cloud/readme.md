# 🏢 Relatório de Implementação de Serviços AWS

**Empresa:** Abstergo Industries  
**Responsável:** Daniel Tiago  
**Cargo:** Cloud Analyst / Data Engineer Júnior  
**Status:** Confidencial / Uso Interno  

---

# 📌 Introdução

Este projeto apresenta a implementação de uma infraestrutura cloud utilizando serviços da Amazon Web Services (AWS) para modernização do sistema de distribuição farmacêutica da Abstergo Industries.

O principal objetivo da solução foi reduzir custos operacionais, aumentar a escalabilidade da plataforma e modernizar a arquitetura da aplicação utilizando serviços gerenciados e arquitetura serverless.

---

# 🛠️ Descrição do Projeto

A arquitetura foi dividida em três etapas principais, cobrindo processamento backend, persistência de dados e entrega de conteúdo web.

A solução foi desenvolvida utilizando serviços gerenciados da AWS com foco em:

- Escalabilidade automática
- Segurança de infraestrutura
- Redução de gerenciamento manual
- Alta disponibilidade
- Automação de deploy

---

# ⚡ Etapa 1

## Nome da Ferramenta
AWS Lambda

## Foco da Ferramenta
Backend serverless para execução das regras de negócio sem necessidade de gerenciamento de servidores físicos.

## Descrição de Caso de Uso
O AWS Lambda foi utilizado para processar pedidos de medicamentos, autenticar usuários parceiros através de tokens JWT e validar dados antes da persistência no banco de dados.

A solução permite escalabilidade automática sob demanda e redução significativa de custos operacionais.

---

# 🗄️ Etapa 2

## Nome da Ferramenta
Amazon RDS PostgreSQL

## Foco da Ferramenta
Banco de dados relacional gerenciado focado em segurança, alta disponibilidade e armazenamento persistente de dados corporativos.

## Descrição de Caso de Uso
O Amazon RDS PostgreSQL foi utilizado para armazenar informações de estoque, catálogo de medicamentos, pedidos, usuários e registros financeiros.

A instância foi implementada em subnets privadas dentro da VPC, garantindo isolamento de rede e segurança da camada de persistência.

---

# 🌐 Etapa 3

## Nome da Ferramenta
Amazon S3 + CloudFront

## Foco da Ferramenta
Hospedagem segura de arquivos estáticos e distribuição global de conteúdo através de CDN.

## Descrição de Caso de Uso
O Amazon S3 foi utilizado para armazenar os arquivos da aplicação frontend desenvolvida em React.

O Amazon CloudFront foi implementado como CDN para distribuição global do conteúdo com baixa latência, HTTPS seguro e alta disponibilidade.

---

# 📈 Conclusão

A arquitetura implementada moderniza a infraestrutura da Abstergo Industries através da utilização de serviços cloud escaláveis, seguros e totalmente gerenciados.

A solução reduz custos operacionais, melhora a disponibilidade da aplicação e automatiza processos de deploy e gerenciamento de infraestrutura.

Como evolução futura, recomenda-se a implementação de serviços como Amazon ElastiCache para otimização de performance e AWS WAF para proteção avançada contra ataques web.

```
