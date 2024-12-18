// Fonction pour formater la date au format français
function formatDate(date) {
    return new Date(date).toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Fonction pour confirmer la suppression d'une tâche
function confirmDelete(taskId) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) {
        window.location.href = `/task/${taskId}/delete`;
    }
}

// Initialisation des éléments de l'interface
document.addEventListener('DOMContentLoaded', function() {
    // Formatage automatique des dates dans le tableau
    const dateElements = document.querySelectorAll('.task-date');
    dateElements.forEach(element => {
        const date = element.getAttribute('data-date');
        if (date) {
            element.textContent = formatDate(date);
        }
    });

    // Gestion des messages flash
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 3000);
    });
});
