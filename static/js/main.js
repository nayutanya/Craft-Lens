    document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[action="/upload-web"]');
    const loadingOverlay = document
    .getElementById('loadingOverlay');

    if (form) {
        form.addEventListener('submit', function() {
            loadingOverlay.style.display = 'flex';
            
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = "解析中...";
            }
        });
    }
});
