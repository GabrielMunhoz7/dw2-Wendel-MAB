# 🔧 GUIA COMPLETO: Configuração Supabase para Persistência Global

## 🎯 Objetivo
Fazer com que suas edições de moedas sejam salvas permanentemente e acessíveis de qualquer lugar.

## 📋 PASSO A PASSO

### 1️⃣ **Configurar Supabase**

1. Acesse: https://supabase.com/dashboard
2. Faça login ou crie uma conta
3. Clique em "New Project" ou selecione um projeto existente
4. Anote as informações do projeto

### 2️⃣ **Obter String de Conexão**

1. No painel do Supabase, vá em **Settings > Database**
2. Role até **Connection string**
3. Selecione **PostgreSQL** (não URI)
4. Copie a string que parece com:
   ```
   postgresql://postgres.abc123:[YOUR-PASSWORD]@db.abc123.supabase.co:5432/postgres
   ```
5. Substitua `[YOUR-PASSWORD]` pela senha real do seu projeto

### 3️⃣ **Configurar Arquivo .env**

1. Abra o arquivo `api/.env` 
2. Na linha `DATABASE_URL=`, cole sua string de conexão:
   ```
   DATABASE_URL=postgresql://postgres.abc123:suaSenhaReal@db.abc123.supabase.co:5432/postgres
   ```
3. Salve o arquivo

### 4️⃣ **Executar Migração**

Execute no terminal:
```bash
cd api
python setup_supabase.py
```

O script irá:
- ✅ Verificar se o .env está configurado
- ✅ Testar conexão com o Supabase
- ✅ Criar as tabelas no banco
- ✅ Configurar usuário admin

### 5️⃣ **Configurar Deploy (Vercel)**

1. No painel da Vercel, vá em **Settings > Environment Variables**
2. Adicione:
   - **Name**: `DATABASE_URL`
   - **Value**: Sua string de conexão do Supabase
3. Adicione:
   - **Name**: `SECRET_KEY`
   - **Value**: `moedinhas-app-super-secret-key-2025-wendel`

## ✅ **Resultado Final**

Após configurar:

- 🌍 **Persistência Global**: Dados salvos na nuvem
- 📱 **Acesso Universal**: Funciona de qualquer dispositivo/local
- 🚀 **Deploy Funcional**: Produção funcionando perfeitamente
- 💾 **Backup Automático**: Supabase cuida dos backups
- 🔒 **Segurança**: Dados protegidos e autenticados

## 🧪 **Como Testar**

1. Adicione uma moeda no seu site
2. Acesse de outro navegador/dispositivo
3. A moeda deve aparecer
4. Exclua a moeda
5. Deve sumir de todos os lugares

## 🆘 **Problemas Comuns**

- **"Conexão recusada"**: Verifique se o projeto Supabase está ativo
- **"Senha incorreta"**: Confirme a senha no arquivo .env
- **"Tabela não existe"**: Execute `python setup_supabase.py` novamente

## 📞 **Suporte**

Se algo não funcionar, envie:
1. Mensagem de erro completa
2. Qual passo estava fazendo
3. Print da tela se necessário