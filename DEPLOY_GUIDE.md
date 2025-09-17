# Guia de Deploy no Vercel - Catálogo de Moedas

## Pré-requisitos

1. **Conta no Vercel**: Crie uma conta em [vercel.com](https://vercel.com)
2. **Conta no GitHub**: Tenha seu projeto em um repositório GitHub
3. **Database URL**: Configure um banco de dados (recomendo Supabase ou Neon)

## Configurações de Variáveis de Ambiente

✅ **Suas variáveis já estão configuradas no arquivo `.env`!**

Use os seguintes valores no Vercel (já configurados no seu projeto):

### 1. DATABASE_URL
- **Nome**: `DATABASE_URL`
- **Valor**: `postgresql://postgres.hphxswhwwfxvxxylhmhm:MabCoins73!@aws-1-sa-east-1.pooler.supabase.com:6543/postgres`
- ✅ **Supabase já configurado**

### 2. SECRET_KEY
- **Nome**: `SECRET_KEY`
- **Valor**: `mab_coins_rs`
- ✅ **Chave já definida**

### 3. ALLOWED_ORIGINS
- **Nome**: `ALLOWED_ORIGINS`
- **Valor**: Será preenchido após o deploy com a URL do Vercel
- **Exemplo**: `https://dw2-wendel-mab.vercel.app`

## Opção 1: Deploy via Interface Web do Vercel

### Passo 1: Conectar o Repositório
1. Acesse [vercel.com](https://vercel.com) e faça login
2. Clique em "New Project"
3. Conecte sua conta do GitHub se ainda não estiver conectada
4. Selecione o repositório `dw2-Wendel-MAB`

### Passo 2: Configurar o Projeto
1. **Framework Preset**: Selecione "Other"
2. **Root Directory**: Deixe como "." (raiz)
3. **Build Command**: Deixe vazio (o Vercel detectará automaticamente)
4. **Output Directory**: Deixe vazio
5. **Install Command**: Deixe vazio

### Passo 3: Configurar Variáveis de Ambiente
1. Na seção "Environment Variables", adicione exatamente estas variáveis:
   
   **DATABASE_URL**:
   ```
   postgresql://postgres.hphxswhwwfxvxxylhmhm:MabCoins73!@aws-1-sa-east-1.pooler.supabase.com:6543/postgres
   ```
   
   **SECRET_KEY**:
   ```
   mab_coins_rs
   ```
   
   **ALLOWED_ORIGINS**: Deixe vazio por enquanto (será preenchido após o deploy)

### Passo 4: Deploy
1. Clique em "Deploy"
2. Aguarde o processo de build e deploy
3. Após o deploy, anote a URL gerada (ex: `https://dw2-wendel-mab.vercel.app`)

### Passo 5: Atualizar ALLOWED_ORIGINS
1. Vá para o dashboard do projeto no Vercel
2. Clique em "Settings" > "Environment Variables"
3. Edite a variável `ALLOWED_ORIGINS` e adicione a URL do seu projeto
4. Exemplo: `https://dw2-wendel-mab.vercel.app`
5. Faça um novo deploy para aplicar as mudanças

## Opção 2: Deploy via CLI do Vercel

### Passo 1: Instalar o CLI do Vercel
```bash
npm i -g vercel
```

### Passo 2: Fazer Login
```bash
vercel login
```

### Passo 3: Deploy
```bash
# Na pasta raiz do projeto
vercel

# Ou para deploy de produção
vercel --prod
```

### Passo 4: Configurar Variáveis de Ambiente
```bash
# Adicionar suas variáveis de ambiente existentes
vercel env add DATABASE_URL
# Cole: postgresql://postgres.hphxswhwwfxvxxylhmhm:MabCoins73!@aws-1-sa-east-1.pooler.supabase.com:6543/postgres

vercel env add SECRET_KEY
# Cole: mab_coins_rs

vercel env add ALLOWED_ORIGINS
# Deixe vazio por enquanto

# Redeploy para aplicar as variáveis
vercel --prod
```

## Configuração do Banco de Dados

✅ **Seu banco Supabase já está configurado e funcionando!**

- **Provedor**: Supabase
- **Host**: aws-1-sa-east-1.pooler.supabase.com
- **Database**: postgres
- **Status**: ✅ Pronto para uso

Não é necessário configurar um novo banco de dados. Suas configurações atuais funcionarão perfeitamente no Vercel.

## Estrutura do Projeto Configurada

O projeto já está configurado com:

✅ **vercel.json**: Configuração de rotas e builds
✅ **requirements.txt**: Dependências Python
✅ **.vercelignore**: Arquivos ignorados no deploy
✅ **Handler do Vercel**: Função para servir a aplicação Flask

## Rotas Configuradas

- `/api/*` → Backend Flask (Python)
- `/assets/*` → Arquivos estáticos (imagens, etc.)
- `/js/*` → Arquivos JavaScript
- `/styles.css` → Arquivo CSS
- `/*` → Frontend (index.html)

## Testando o Deploy

Após o deploy, teste as seguintes funcionalidades:

1. **Frontend**: Acesse a URL principal do projeto
2. **API**: Teste `https://seu-projeto.vercel.app/api/health`
3. **Login**: Teste o sistema de autenticação
4. **CRUD de Moedas**: Teste as operações básicas

## Solução de Problemas

### Erro de CORS
- Verifique se `ALLOWED_ORIGINS` está configurado corretamente
- Inclua a URL completa do seu projeto Vercel

### Erro de Banco de Dados
- Verifique se `DATABASE_URL` está correto
- Confirme se o banco está acessível pela internet
- Teste a conexão localmente primeiro

### Erro 500 no Backend
- Verifique os logs no dashboard do Vercel
- Confirme se todas as variáveis de ambiente estão configuradas
- Teste o backend localmente para identificar erros

### Arquivos Estáticos Não Carregam
- Verifique se os caminhos no `vercel.json` estão corretos
- Confirme se os arquivos estão na estrutura esperada

## Comandos Úteis

```bash
# Ver logs do projeto
vercel logs

# Listar projetos
vercel list

# Remover projeto
vercel remove

# Ver status do deployment
vercel inspect
```

## Próximos Passos

1. Configure um domínio customizado (opcional)
2. Configure analytics do Vercel
3. Configure branch previews para desenvolvimento
4. Configure webhooks para automações
5. Monitore performance e erros

## Suporte

- [Documentação do Vercel](https://vercel.com/docs)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)