    function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    const btn = document.querySelector('.btn-analyze');
    const btnText = document.getElementById('btnText');

    if (overlay) overlay.style.display = 'flex';

    if (btnText) {
        btnText.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>AIが解析中...';
    }

    setTimeout(() => {
        if (btn) btn.disabled = true;
    }, 0);
        return true;
        }
