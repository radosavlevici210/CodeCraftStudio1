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
// CodeCraft Studio - Main JavaScript
// © 2025 Ervin Remus Radosavlevici

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎵 CodeCraft Studio - AI Music & Video Generator');
    console.log('© 2025 Ervin Remus Radosavlevici');
    console.log('Protected by RADOS Quantum Enforcement Policy v2.7');
    
    initializeApp();
});

function initializeApp() {
    const generateForm = document.getElementById('generateForm');
    if (generateForm) {
        setupGenerationForm();
    }
    
    setupGlobalEventListeners();
    setupSecurityMonitoring();
}

function setupGenerationForm() {
    const form = document.getElementById('generateForm');
    const generateBtn = document.getElementById('generateBtn');
    const progressSection = document.getElementById('progressSection');
    const resultsSection = document.getElementById('resultsSection');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        startGeneration();
    });
    
    async function startGeneration() {
        // Disable form and show progress
        generateBtn.disabled = true;
        progressSection.style.display = 'block';
        resultsSection.style.display = 'none';
        
        // Get form data
        const formData = new FormData(form);
        
        try {
            // Start progress animation
            animateProgress();
            
            // Submit generation request
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                showGenerationResults(result);
            } else {
                showError(result.error || 'Generation failed');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        } finally {
            // Re-enable form
            generateBtn.disabled = false;
            progressSection.style.display = 'none';
        }
    }
    
    function animateProgress() {
        const progressBar = document.querySelector('.progress-bar');
        const progressText = document.getElementById('progressText');
        
        const steps = [
            'Initializing AI systems...',
            'Analyzing theme and style...',
            'Generating lyrics with OpenAI...',
            'Creating musical composition...',
            'Synthesizing voice elements...',
            'Rendering cinematic video...',
            'Applying final effects...',
            'Completing generation...'
        ];
        
        let currentStep = 0;
        const stepDuration = 3000; // 3 seconds per step
        
        const interval = setInterval(() => {
            if (currentStep < steps.length) {
                const progress = ((currentStep + 1) / steps.length) * 100;
                progressBar.style.width = progress + '%';
                progressText.textContent = steps[currentStep];
                currentStep++;
            } else {
                clearInterval(interval);
            }
        }, stepDuration);
    }
    
    function showGenerationResults(result) {
        const resultsContent = document.getElementById('resultsContent');
        
        resultsContent.innerHTML = `
            <div class="generation-result">
                <h5><i class="fas fa-music"></i> Generation Complete!</h5>
                <p><strong>Voice Style:</strong> ${result.voice_style}</p>
                <p><strong>Music Style:</strong> ${result.music_style}</p>
                
                ${result.audio_file ? `
                    <div class="mt-3">
                        <label class="form-label"><i class="fas fa-headphones"></i> Audio</label>
                        <audio controls class="audio-player">
                            <source src="/static/audio/${result.audio_file}" type="audio/mpeg">
                            Your browser does not support audio playback.
                        </audio>
                    </div>
                ` : ''}
                
                ${result.video_file ? `
                    <div class="mt-3">
                        <label class="form-label"><i class="fas fa-video"></i> Video</label>
                        <video controls class="video-player">
                            <source src="/static/video/${result.video_file}" type="video/mp4">
                            Your browser does not support video playback.
                        </video>
                    </div>
                ` : ''}
                
                <div class="mt-3">
                    <a href="/results/${result.generation_id}" class="btn btn-primary">
                        <i class="fas fa-eye"></i> View Details
                    </a>
                    ${result.audio_file ? `
                        <a href="/download/audio/${result.generation_id}" class="btn btn-success ms-2">
                            <i class="fas fa-download"></i> Download Audio
                        </a>
                    ` : ''}
                    ${result.video_file ? `
                        <a href="/download/video/${result.generation_id}" class="btn btn-info ms-2">
                            <i class="fas fa-download"></i> Download Video
                        </a>
                    ` : ''}
                </div>
            </div>
        `;
        
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    function showError(message) {
        const resultsContent = document.getElementById('resultsContent');
        resultsContent.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>Generation Failed:</strong> ${message}
                <div class="mt-2">
                    <button type="button" class="btn btn-outline-danger btn-sm" onclick="location.reload()">
                        <i class="fas fa-refresh"></i> Try Again
                    </button>
                </div>
            </div>
        `;
        resultsSection.style.display = 'block';
    }
}

function setupGlobalEventListeners() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    });
    
    // Smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add loading states to buttons
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                const originalText = this.innerHTML;
                this.innerHTML = '<span class="loading-spinner"></span> Processing...';
                this.disabled = true;
                
                // Re-enable after timeout (fallback)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 30000);
            }
        });
    });
}

function setupSecurityMonitoring() {
    // Add security badge
    const securityBadge = document.createElement('div');
    securityBadge.className = 'security-badge';
    securityBadge.innerHTML = '<i class="fas fa-shield-alt"></i> RADOS Protected';
    document.body.appendChild(securityBadge);
    
    // Monitor for suspicious activity
    let activityCount = 0;
    const activityLimit = 100;
    
    document.addEventListener('click', function() {
        activityCount++;
        if (activityCount > activityLimit) {
            console.warn('High activity detected - RADOS monitoring active');
        }
    });
    
    // Prevent common attacks
    document.addEventListener('keydown', function(e) {
        // Prevent F12 (dev tools) in production
        if (e.key === 'F12' && window.location.hostname !== 'localhost') {
            e.preventDefault();
            return false;
        }
        
        // Prevent Ctrl+Shift+I (dev tools)
        if (e.ctrlKey && e.shiftKey && e.key === 'I') {
            e.preventDefault();
            return false;
        }
    });
    
    // Disable right-click context menu in production
    if (window.location.hostname !== 'localhost') {
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
        });
    }
}

// Utility functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 3000);
}

function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Copied to clipboard!', 'success');
    }
}

// Health monitoring
function checkSystemHealth() {
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            const healthIndicator = document.querySelector('.health-indicator');
            if (healthIndicator) {
                healthIndicator.className = `health-indicator status-${data.status}`;
                healthIndicator.title = `System Status: ${data.status}`;
            }
        })
        .catch(error => {
            console.warn('Health check failed:', error);
        });
}

// Initialize health monitoring
setInterval(checkSystemHealth, 60000); // Check every minute

// Export functions for global access
window.CodeCraftStudio = {
    showToast,
    formatDuration,
    copyToClipboard,
    checkSystemHealth
};
