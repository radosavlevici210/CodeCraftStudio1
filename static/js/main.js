// CodeCraft Studio Main JavaScript
// © 2025 Ervin Remus Radosavlevici

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        });
    }, 5000);

    // Theme selection handlers
    const themeInput = document.getElementById('theme');
    const voiceSelect = document.getElementById('voice_style');
    const musicSelect = document.getElementById('music_style');

    if (themeInput && voiceSelect && musicSelect) {
        themeInput.addEventListener('input', function() {
            const theme = this.value.toLowerCase();
            
            // Auto-suggest voice style based on theme
            if (theme.includes('battle') || theme.includes('war') || theme.includes('champion')) {
                voiceSelect.value = 'heroic_male';
            } else if (theme.includes('sacred') || theme.includes('divine') || theme.includes('eternal')) {
                voiceSelect.value = 'choir';
            } else if (theme.includes('emotional') || theme.includes('love') || theme.includes('heart')) {
                voiceSelect.value = 'soprano';
            } else if (theme.includes('mystery') || theme.includes('secret')) {
                voiceSelect.value = 'whisper';
            }

            // Auto-suggest music style based on theme
            if (theme.includes('gladiator') || theme.includes('arena')) {
                musicSelect.value = 'gladiator';
            } else if (theme.includes('sacred') || theme.includes('prayer')) {
                musicSelect.value = 'gregorian';
            } else if (theme.includes('dark') || theme.includes('shadow')) {
                musicSelect.value = 'dark';
            } else if (theme.includes('magic') || theme.includes('fantasy')) {
                musicSelect.value = 'fantasy';
            } else if (theme.includes('emotional') || theme.includes('heart')) {
                musicSelect.value = 'emotional';
            } else if (theme.includes('modern') || theme.includes('pop')) {
                musicSelect.value = 'pop';
            }
        });
    }

    // Add loading states to download buttons
    document.querySelectorAll('a[href*="/download/"]').forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Downloading...';
            this.classList.add('disabled');
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.classList.remove('disabled');
            }, 2000);
        });
    });

    // Animated counters for stats
    function animateCounter(element, target, duration = 2000) {
        const start = parseInt(element.textContent) || 0;
        const increment = (target - start) / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            element.textContent = Math.floor(current);
            
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    }

    // Animate stats on page load
    document.querySelectorAll('.stat-value').forEach(stat => {
        const value = parseInt(stat.textContent);
        if (value > 0) {
            stat.textContent = '0';
            setTimeout(() => animateCounter(stat, value), 500);
        }
    });

    // Add particle effect to hero section
    function createParticles() {
        const heroSection = document.querySelector('.hero-section');
        if (!heroSection) return;

        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: #FFD700;
                border-radius: 50%;
                opacity: 0.6;
                animation: float ${Math.random() * 3 + 2}s linear infinite;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                z-index: 1;
            `;
            heroSection.appendChild(particle);
        }
    }

    // Add CSS animation for particles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); opacity: 0; }
            10% { opacity: 0.6; }
            90% { opacity: 0.6; }
            100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    // Initialize particles
    createParticles();

    // Add hover effects to cards
    document.querySelectorAll('.generation-card, .feature-card, .download-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add typing effect to main title
    const titleElement = document.querySelector('.hero-section .display-4');
    if (titleElement) {
        const originalText = titleElement.textContent;
        titleElement.textContent = '';
        
        let i = 0;
        const typeInterval = setInterval(() => {
            titleElement.textContent += originalText.charAt(i);
            i++;
            
            if (i >= originalText.length) {
                clearInterval(typeInterval);
            }
        }, 100);
    }

    // System health monitoring
    function checkSystemHealth() {
        fetch('/health')
            .then(response => response.json())
            .then(data => {
                const healthIndicator = document.querySelector('.system-health-indicator');
                if (healthIndicator) {
                    healthIndicator.className = 'system-health-indicator ' + 
                        (data.overall_health === 'excellent' ? 'text-success' : 'text-warning');
                }
            })
            .catch(error => {
                console.log('Health check failed:', error);
            });
    }

    // Check system health every 30 seconds
    setInterval(checkSystemHealth, 30000);

    // Add RADOS protection notice
    const protectionNotice = document.createElement('div');
    protectionNotice.innerHTML = `
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 1000;">
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
                <div class="toast-header bg-dark text-gold">
                    <i class="fas fa-shield-alt me-2"></i>
                    <strong class="me-auto">RADOS Protection</strong>
                </div>
                <div class="toast-body bg-dark text-light">
                    Content protected by Quantum Enforcement Policy v2.7
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(protectionNotice);
    
    // Show protection notice after 3 seconds
    setTimeout(() => {
        const toast = new bootstrap.Toast(protectionNotice.querySelector('.toast'));
        toast.show();
    }, 3000);

    console.log('🎵 CodeCraft Studio - AI Music & Video Generator');
    console.log('© 2025 Ervin Remus Radosavlevici');
    console.log('Protected by RADOS Quantum Enforcement Policy v2.7');
});
