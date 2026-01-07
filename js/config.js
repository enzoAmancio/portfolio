/**
 * Configuração da API - NÃO COMMITAR ESTE ARQUIVO EM PRODUÇÃO
 * Use variáveis de ambiente ou arquivo .env.js ignorado pelo git
 */

const API_CONFIG = {
    // Detecção automática de ambiente
    getBaseURL: function() {
        const hostname = window.location.hostname;
        const isDevelopment = hostname === 'localhost' || hostname === '127.0.0.1';
        
        // Sempre usa localhost na porta 5000 (funciona em dev E produção)
        return 'http://127.0.0.1:5000';
    },
    
    // Endpoints
    endpoints: {
        sendEmail: '/api/send-email',
        health: '/api/health'
    },
    
    // Timeout para requests (ms)
    timeout: 10000,
    
    // Headers padrão
    headers: {
        'Content-Type': 'application/json'
    }
};

// Exporta configuração (se não estiver usando)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
