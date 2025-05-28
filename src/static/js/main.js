// Funções JavaScript para o CRM

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Inicializar popovers do Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Obter o token CSRF do campo oculto
    const csrfToken = document.getElementById('csrf_token').value;

    // Função para gerar mensagem personalizada a partir de template
    window.generateMessage = function(templateId, leadId) {
        fetch(`/templates/generate/${templateId}/${leadId}`, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.text())
        .then(html => {
            const modal = new bootstrap.Modal(document.getElementById('messageModal'));
            document.getElementById('messageModalContent').innerHTML = html;
            modal.show();
        })
        .catch(error => console.error('Erro ao gerar mensagem:', error));
    };

    // Função para copiar texto para a área de transferência
    window.copyToClipboard = function(elementId) {
        const element = document.getElementById(elementId);
        const text = element.innerText || element.textContent;
        
        navigator.clipboard.writeText(text).then(
            function() {
                // Mostrar feedback de sucesso
                const button = document.querySelector(`[onclick="copyToClipboard('${elementId}')"]`);
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="bi bi-check"></i> Copiado!';
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                }, 2000);
            },
            function() {
                alert('Não foi possível copiar o texto. Por favor, copie manualmente.');
            }
        );
    };

    // Função para confirmar exclusão
    window.confirmDelete = function(formId) {
        if (confirm('Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.')) {
            document.getElementById(formId).submit();
        }
    };

    // Função para filtrar tabelas
    window.filterTable = function(inputId, tableId) {
        const input = document.getElementById(inputId);
        const filter = input.value.toUpperCase();
        const table = document.getElementById(tableId);
        const rows = table.getElementsByTagName('tr');

        for (let i = 1; i < rows.length; i++) { // Começar do 1 para pular o cabeçalho
            let found = false;
            const cells = rows[i].getElementsByTagName('td');
            
            for (let j = 0; j < cells.length; j++) {
                const cell = cells[j];
                if (cell) {
                    const text = cell.textContent || cell.innerText;
                    if (text.toUpperCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
            }
            
            rows[i].style.display = found ? '' : 'none';
        }
    };

    // Inicializar gráficos do dashboard se estiverem presentes
    initializeDashboardCharts();
});

// Função para inicializar gráficos do dashboard
function initializeDashboardCharts() {
    // Verificar se estamos na página do dashboard
    const leadsStatusChart = document.getElementById('leadsStatusChart');
    if (!leadsStatusChart) return;

    // Gráfico de status de leads
    if (leadsStatusChart) {
        const leadsData = JSON.parse(leadsStatusChart.getAttribute('data-chart'));
        new Chart(leadsStatusChart, {
            type: 'doughnut',
            data: {
                labels: leadsData.labels,
                datasets: [{
                    data: leadsData.values,
                    backgroundColor: [
                        '#0d47a1', '#1b5e20', '#e65100', 
                        '#1a237e', '#4a148c', '#1b5e20', '#b71c1c'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Leads por Status'
                    }
                }
            }
        });
    }

    // Gráfico de leads por setor
    const leadsIndustryChart = document.getElementById('leadsIndustryChart');
    if (leadsIndustryChart) {
        const industryData = JSON.parse(leadsIndustryChart.getAttribute('data-chart'));
        new Chart(leadsIndustryChart, {
            type: 'pie',
            data: {
                labels: industryData.labels,
                datasets: [{
                    data: industryData.values,
                    backgroundColor: [
                        '#bbdefb', '#c8e6c9', '#ffe0b2', 
                        '#d1c4e9', '#f8bbd0', '#b2dfdb', '#ffcdd2'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Leads por Setor'
                    }
                }
            }
        });
    }

    // Gráfico de interações por tipo
    const interactionsTypeChart = document.getElementById('interactionsTypeChart');
    if (interactionsTypeChart) {
        const typeData = JSON.parse(interactionsTypeChart.getAttribute('data-chart'));
        new Chart(interactionsTypeChart, {
            type: 'bar',
            data: {
                labels: typeData.labels,
                datasets: [{
                    label: 'Quantidade',
                    data: typeData.values,
                    backgroundColor: '#0056b3',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Interações por Tipo'
                    }
                }
            }
        });
    }

    // Gráfico de interações por semana
    const interactionsWeekChart = document.getElementById('interactionsWeekChart');
    if (interactionsWeekChart) {
        const weekData = JSON.parse(interactionsWeekChart.getAttribute('data-chart'));
        new Chart(interactionsWeekChart, {
            type: 'line',
            data: {
                labels: weekData.labels,
                datasets: [{
                    label: 'Interações',
                    data: weekData.values,
                    borderColor: '#0056b3',
                    backgroundColor: 'rgba(0, 86, 179, 0.1)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Interações por Semana'
                    }
                }
            }
        });
    }
}