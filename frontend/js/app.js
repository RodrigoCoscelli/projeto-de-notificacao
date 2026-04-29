window.tailwindConfig = {
    darkMode: "class",
    theme: {
        extend: {
            "colors": {
                "primary-fixed": "#d6e3ff",
                "tertiary-fixed-dim": "#ffb691",
                "surface-dim": "#d9dadb",
                "surface-container-high": "#e7e8e9",
                "on-tertiary-container": "#ffcfb9",
                "on-secondary": "#ffffff",
                "surface-container-lowest": "#ffffff",
                "on-error-container": "#93000a",
                "surface": "#f8f9fa",
                "on-tertiary-fixed": "#341100",
                "on-primary": "#ffffff",
                "on-primary-fixed-variant": "#00468c",
                "outline-variant": "#c2c6d4",
                "tertiary-container": "#9f4300",
                "on-surface-variant": "#424752",
                "primary-fixed-dim": "#a9c7ff",
                "on-primary-container": "#c8daff",
                "on-surface": "#191c1d",
                "error-container": "#ffdad6",
                "on-tertiary-fixed-variant": "#793100",
                "background": "#f8f9fa",
                "on-error": "#ffffff",
                "on-primary-fixed": "#001b3d",
                "on-secondary-fixed-variant": "#2e476f",
                "on-secondary-container": "#3f5881",
                "tertiary-fixed": "#ffdbcb",
                "primary": "#00478d",
                "surface-container-low": "#f3f4f5",
                "tertiary": "#793100",
                "secondary-fixed": "#d6e3ff",
                "secondary": "#465f88",
                "secondary-container": "#b6d0ff",
                "inverse-surface": "#2e3132",
                "surface-variant": "#e1e3e4",
                "surface-tint": "#005db6",
                "inverse-on-surface": "#f0f1f2",
                "surface-container-highest": "#e1e3e4",
                "outline": "#727783",
                "inverse-primary": "#a9c7ff",
                "secondary-fixed-dim": "#aec7f7",
                "primary-container": "#005eb8",
                "surface-container": "#edeeef",
                "on-tertiary": "#ffffff",
                "error": "#ba1a1a",
                "surface-bright": "#f8f9fa",
                "on-secondary-fixed": "#001b3d",
                "on-background": "#191c1d"
            },
            "fontFamily": {
                "headline": ["Manrope"],
                "body": ["Inter"],
                "label": ["Inter"]
            }
        }
    }
};

async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('token');
    const headers = options.headers || {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        ...options,
        headers
    };
    
    const response = await fetch(url, config);
    if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/';
        throw new Error('Unauthorized');
    }
    return response;
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}

function decodeToken(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

function getStatusColorClass(status) {
    if (!status) return 'bg-surface-variant text-on-surface';
    
    const s = status.toLowerCase();
    
    // Verde (Sucesso / Concluído)
    if (s.includes('encerrada') || s.includes('concluíd') || s.includes('aprovado') || s.includes('respondida')) {
        return 'bg-green-100 text-green-800 border border-green-200';
    }
    
    // Vermelho (Recusado / Bloqueado)
    if (s.includes('recusado') || s.includes('cancelado') || s.includes('bloqueada')) {
        return 'bg-red-100 text-red-800 border border-red-200';
    }
    
    // Laranja (Aguardando conclusão do setor)
    if (s.includes('aguardando conclusão')) {
        return 'bg-orange-100 text-orange-800 border border-orange-200';
    }
    
    // Azul / Laranja / Amarelo (Em andamento / Aguardando)
    if (s.includes('aguardando triagem') || s.includes('pendente')) {
        return 'bg-yellow-100 text-yellow-800 border border-yellow-200';
    }
    
    if (s.includes('análise nsp') || s.includes('plano de ação 5w2h')) {
        return 'bg-blue-100 text-blue-800 border border-blue-200';
    }
    
    // Default
    return 'bg-surface-variant text-on-surface border border-outline-variant/30';
}
