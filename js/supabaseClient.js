// Inicialização do Supabase no frontend
// SUBSTITUA OS PLACEHOLDERS ABAIXO PELOS VALORES DO SEU PROJETO SUPABASE
// Para obter: Project Settings > API > Project URL e anon public key

const SUPABASE_URL = window.SUPABASE_URL_OVERRIDE || "https://hphxswhwwfxvxxylhmhm.supabase.co";
const SUPABASE_ANON_KEY = window.SUPABASE_ANON_KEY_OVERRIDE || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhwaHhzd2h3d2Z4dnh4eWxobWhtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc2MDc1NTcsImV4cCI6MjA3MzE4MzU1N30.vOJJ6rv9PuZ8gqD_Ds_y4pTIIlmY-76u2SAw8oQ10gs";

if (SUPABASE_URL.includes('SEU_PROJECT_ID')) {
  console.warn('[Supabase] Configure SUPABASE_URL e SUPABASE_ANON_KEY em supabaseClient.js');
}

// Carrega lib se ainda não carregada (caso ordem de scripts mude)
if (!window.supabase) {
  console.error('Biblioteca supabase-js não carregada. Adicione <script src="https://unpkg.com/@supabase/supabase-js@2"></script> antes deste arquivo.');
}

const supabaseClient = window.supabase?.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
window.supabaseClient = supabaseClient;

// Teste rápido de conexão (logs só no console do navegador)
if (supabaseClient) {
  supabaseClient.from('coins').select('id').limit(1)
    .then(({ error }) => {
      if (error) {
        console.error('[Supabase] Erro de conexão:', error.message);
      } else {
        console.log('[Supabase] Conectado com sucesso.');
      }
    });
}