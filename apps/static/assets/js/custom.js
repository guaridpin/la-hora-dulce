document.addEventListener('DOMContentLoaded', function () {
    const scrapeButton = document.getElementById('scrape-button');
    const confirmScrapeButton = document.getElementById('confirm-scrape');
    const resultModal = new bootstrap.Modal(document.getElementById('result-modal'));
    const resultMessage = document.getElementById('result-message');

    // Mostrar el modal de confirmación
    scrapeButton.addEventListener('click', function () {
        const confirmModal = new bootstrap.Modal(document.getElementById('confirm-modal'));
        confirmModal.show();
    });

    // Confirmar y ejecutar el scraping
    confirmScrapeButton.addEventListener('click', function () {
        fetch('/scraping/start/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            resultMessage.textContent = data.success ? data.message : 'Ocurrió un error durante el scraping.';
            resultModal.show();
        })
        .catch(error => {
            resultMessage.textContent = 'Error de conexión: ' + error.message;
            resultModal.show();
        });
    });    

    // Función para obtener el CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
