/**
 * Script Principal do Portfólio - Enzo Amancio
 * Funções: Navegação, Animações, Formulário de Contato com Turnstile
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // NAVBAR - Scroll Effect
    // ========================================
    window.addEventListener('scroll', function() {
        const navbar = document.getElementById('navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ========================================
    // MOBILE MENU - Toggle
    // ========================================
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    // ========================================
    // TYPING EFFECT - Hero Section
    // ========================================
    const typingText = document.getElementById('typing-text');
    if (typingText) {
        const words = ['Soluções', 'Aplicações', 'Inovações', 'Sites'];
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;

        function typeEffect() {
            const currentWord = words[wordIndex];
            
            if (isDeleting) {
                charIndex--;
            } else {
                charIndex++;
            }

            // Always show cursor during typing/deleting
            typingText.innerHTML = currentWord.substring(0, charIndex) + '<span class="cursor">_</span>';

            let typeSpeed = 150;

            if (isDeleting) {
                typeSpeed = 75;
            }

            if (!isDeleting && charIndex === currentWord.length) {
                typeSpeed = 2000; // Pause at end
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                typeSpeed = 500;
            }

            setTimeout(typeEffect, typeSpeed);
        }

        // Start typing effect after a short delay
        setTimeout(() => {
            typeEffect();
        }, 800);
    }

    // ========================================
    // FORMULÁRIO DE CONTATO - Com Turnstile
    // ========================================
    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');
    const btnText = document.querySelector('.btn-text');
    const btnLoading = document.querySelector('.btn-loading');
    const submitBtn = document.querySelector('.btn-send');

    // URL da API (vem do config.js)
    const API_BASE = API_CONFIG.getBaseURL();
    const API_URL = `${API_BASE}${API_CONFIG.endpoints.sendEmail}`;
    
    // Log apenas em desenvolvimento
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('🌍 Frontend rodando em:', window.location.hostname);
        console.log('🔗 API configurada para:', API_BASE);
    }

    if (!contactForm) return;

    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Mostrar estado de carregamento
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'flex';
        formMessage.classList.remove('show', 'success', 'error');

        // ===== CLOUDFLARE TURNSTILE - Captcha =====
        const turnstileResponse = document.querySelector('[name="cf-turnstile-response"]');
        const tokenCaptcha = turnstileResponse ? turnstileResponse.value : null;

        if (!tokenCaptcha) {
            showMessage('🤖 Por favor, complete a verificação de segurança (captcha).', 'error');
            resetButton();
            return;
        }

        // Coletar dados do formulário + token captcha
        const formData = {
            name: document.getElementById('name').value.trim(),
            email: document.getElementById('email').value.trim(),
            subject: document.getElementById('subject').value.trim(),
            message: document.getElementById('message').value.trim(),
            token_captcha: tokenCaptcha
        };

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: API_CONFIG.headers,
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Sucesso
                showMessage('✅ ' + data.message, 'success');
                contactForm.reset();
                
                // Reset do widget Turnstile
                resetTurnstile();
            } else {
                // Erro
                showMessage('❌ ' + (data.message || 'Erro ao enviar mensagem. Tente novamente.'), 'error');
                resetTurnstile();
            }
        } catch (error) {
            console.error('❌ Erro ao enviar formulário:', error);
            showMessage('❌ Erro de conexão com o servidor. Tente novamente mais tarde.', 'error');
            resetTurnstile();
        } finally {
            resetButton();
            
            // Esconder mensagem após 5 segundos
            setTimeout(() => {
                formMessage.classList.remove('show');
            }, 5000);
        }
    });

    // ===== FUNÇÕES AUXILIARES DO FORMULÁRIO =====
    
    function showMessage(text, type) {
        formMessage.textContent = text;
        formMessage.classList.add('show', type);
    }

    function resetButton() {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }

    function resetTurnstile() {
        if (window.turnstile) {
            try {
                turnstile.reset();
            } catch (e) {
                console.warn('⚠️ Não foi possível resetar Turnstile:', e);
            }
        }
    }

    // ========================================
    // INTERSECTION OBSERVER - Animações
    // ========================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);

    // Observar elementos com animação
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    animateElements.forEach(el => observer.observe(el));

    // ========================================
    // PARALLAX HERO - Apenas Desktop
    // ========================================
    let ticking = false;
    
    // Verifica se é desktop (>= 768px)
    function isDesktop() {
        return window.innerWidth >= 768;
    }
    
    window.addEventListener('scroll', () => {
        // Só aplica parallax em desktop
        if (!ticking && isDesktop()) {
            window.requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                const hero = document.querySelector('.hero');
                const heroContent = document.querySelector('.hero-content');
                const heroImage = document.querySelector('.hero-image');
                
                // Só aplica efeito se hero ainda está visível
                if (hero && scrolled < window.innerHeight) {
                    if (heroContent) {
                        heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
                        heroContent.style.opacity = 1 - (scrolled / 500);
                    }
                    if (heroImage) {
                        heroImage.style.transform = `translate(${scrolled * 0.5}px, ${scrolled * 0.15}px)`;
                        heroImage.style.opacity = 1 - (scrolled / 600);
                    }
                }
                ticking = false;
            });
            ticking = true;
        }
    });
    
    // Reset estilos no mobile quando redimensiona
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if (!isDesktop()) {
                const heroContent = document.querySelector('.hero-content');
                const heroImage = document.querySelector('.hero-image');
                
                // Reseta estilos inline em mobile
                if (heroContent) {
                    heroContent.style.transform = '';
                    heroContent.style.opacity = '';
                }
                if (heroImage) {
                    heroImage.style.transform = '';
                    heroImage.style.opacity = '';
                }
            }
        }, 250);
    });
});
