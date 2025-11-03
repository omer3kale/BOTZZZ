// Admin Reports and Analytics

let currentChart = null;
let currentReportTab = 'payments';

// Initialize chart on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeChart();
});

// Initialize main chart
function initializeChart() {
    const ctx = document.getElementById('mainChart');
    if (!ctx) return;

    // Sample data matching the screenshot (revenue spike at start of month)
    const data = {
        labels: ['Nov 1', 'Nov 2', 'Nov 3', 'Nov 4', 'Nov 5', 'Nov 6', 'Nov 7', 'Nov 8', 'Nov 9', 'Nov 10'],
        datasets: [{
            label: 'Revenue',
            data: [11000, 8500, 6200, 4800, 3500, 2800, 1900, 1200, 800, 400],
            borderColor: '#FF1494',
            backgroundColor: 'rgba(255, 20, 148, 0.1)',
            tension: 0.4,
            fill: true
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: '#1a1a1a',
                    titleColor: '#ffffff',
                    bodyColor: '#a0a0a0',
                    borderColor: '#2a2a2a',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: '#2a2a2a'
                    },
                    ticks: {
                        color: '#a0a0a0',
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                },
                x: {
                    grid: {
                        color: '#2a2a2a'
                    },
                    ticks: {
                        color: '#a0a0a0'
                    }
                }
            }
        }
    };

    currentChart = new Chart(ctx, config);
}

// Switch report tab
function switchReportTab(tab) {
    currentReportTab = tab;
    
    // Update active tab
    document.querySelectorAll('.chart-tab').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update chart data based on tab
    updateChartData(tab);
}

// Update chart data
function updateChartData(tab) {
    if (!currentChart) return;
    
    let newData, label, color;
    
    switch(tab) {
        case 'payments':
            newData = [11000, 8500, 6200, 4800, 3500, 2800, 1900, 1200, 800, 400];
            label = 'Revenue';
            color = '#FF1494';
            break;
        case 'orders':
            newData = [450, 380, 320, 280, 240, 200, 160, 120, 80, 40];
            label = 'Orders';
            color = '#22c55e';
            break;
        case 'tickets':
            newData = [25, 32, 28, 35, 30, 22, 18, 15, 12, 10];
            label = 'Tickets';
            color = '#eab308';
            break;
        case 'profits':
            newData = [3200, 2800, 2400, 2100, 1800, 1500, 1200, 900, 600, 300];
            label = 'Profits';
            color = '#3b82f6';
            break;
        case 'services':
            newData = [156, 156, 155, 154, 153, 152, 151, 150, 149, 148];
            label = 'Active Services';
            color = '#a855f7';
            break;
        case 'users':
            newData = [1109, 1095, 1082, 1070, 1058, 1045, 1032, 1020, 1008, 995];
            label = 'Users';
            color = '#f97316';
            break;
        case 'providers':
            newData = [3, 3, 3, 2, 2, 2, 2, 2, 2, 2];
            label = 'Active Providers';
            color = '#06b6d4';
            break;
    }
    
    currentChart.data.datasets[0].data = newData;
    currentChart.data.datasets[0].label = label;
    currentChart.data.datasets[0].borderColor = color;
    currentChart.data.datasets[0].backgroundColor = color + '20';
    currentChart.update();
}

// Update charts based on date range
function updateCharts() {
    const dateRange = document.getElementById('dateRange').value;
    showNotification(`Updated reports for ${dateRange.replace('-', ' ')}`, 'success');
    
    // In production, fetch new data based on date range
    updateChartData(currentReportTab);
}

// Toggle between chart and table view
function toggleView(view) {
    const chartView = document.getElementById('chartView');
    const tableView = document.getElementById('tableView');
    const buttons = document.querySelectorAll('.toggle-btn');
    
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    if (view === 'chart') {
        chartView.style.display = 'block';
        tableView.style.display = 'none';
    } else {
        chartView.style.display = 'none';
        tableView.style.display = 'block';
    }
}

// Export report
function exportReport(format) {
    showNotification(`Exporting report as ${format.toUpperCase()}...`, 'success');
    
    setTimeout(() => {
        showNotification(`Report exported successfully!`, 'success');
    }, 1500);
}
