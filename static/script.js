/**
 * EcoVolt AI - Smart Microgrid System
 * Frontend Dashboard Script
 * Production-Ready JavaScript with Chart.js integration
 */

// ================================================
// GLOBAL STATE
// ================================================

let dashboardState = {
    mode: 'Urban',
    outageSimulated: false,
    autoRefreshInterval: null,
    charts: {},
    currentData: null,
    refreshRate: 5000, // 5 seconds
    isAutoRefresh: false, // Track if it's auto-refresh or manual
};

// Chart instances
let dailyChart = null;
let sourceChart = null;
let predictionsChart = null;

// ================================================
// INITIALIZATION
// ================================================

function initializeDashboard() {
    console.log('Initializing EcoVolt AI Dashboard...');
    
    // Setup event listeners
    setupEventListeners();
    
    // Load theme preference
    loadTheme();
    
    // Initial data load
    updateDashboard();
    
    // Initialize charts
    initializeCharts();
    
    // Load tips
    loadEnergySavingTips();
    
    console.log('Dashboard initialized successfully!');
}

function setupEventListeners() {
    // Mode selector buttons
    document.querySelectorAll('.btn-mode').forEach(btn => {
        btn.addEventListener('click', handleModeChange);
    });
    
    // Outage toggle
    document.getElementById('outageToggle').addEventListener('change', handleOutageToggle);
    
    // Theme toggle
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    
    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', updateDashboard);
}

// ================================================
// THEME MANAGEMENT
// ================================================

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.classList.toggle('dark-theme', savedTheme === 'dark');
}

function toggleTheme() {
    const isDark = document.body.classList.contains('dark-theme');
    document.body.classList.toggle('dark-theme', !isDark);
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
    
    // Update theme button
    document.getElementById('themeToggle').textContent = isDark ? '🌙' : '☀️';
    
    // Re-render charts with new theme
    recreateCharts();
}

// ================================================
// MODE MANAGEMENT
// ================================================

function handleModeChange(e) {
    const newMode = e.target.dataset.mode;
    
    // Update UI
    document.querySelectorAll('.btn-mode').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');
    
    // Update state
    dashboardState.mode = newMode;
    
    // Refresh data
    updateDashboard();
}

// ================================================
// OUTAGE SIMULATION
// ================================================

function handleOutageToggle(e) {
    dashboardState.outageSimulated = e.target.checked;
    
    const outageStatus = document.getElementById('outageStatus');
    if (dashboardState.outageSimulated) {
        outageStatus.textContent = '🔴 Outage Active';
        outageStatus.classList.add('alert');
    } else {
        outageStatus.textContent = '🟢 Grid Normal';
        outageStatus.classList.remove('alert');
    }
    
    // Refresh data immediately
    updateDashboard();
}

// ================================================
// MAIN DATA FETCHING & UPDATING
// ================================================

async function updateDashboard() {
    try {
        // Only show loading for manual refresh, not auto-refresh
        if (!dashboardState.isAutoRefresh) {
            showLoading(true);
        }
        
        // Fetch current energy data
        const energyData = await fetchEnergyData();
        
        if (!energyData) {
            showLoading(false);
            return;
        }
        
        // Store current data
        dashboardState.currentData = energyData;
        
        // Update all UI elements
        updateEnergyCards(energyData);
        
        // Get optimization decision
        const decision = await fetchOptimization(energyData);
        if (decision) {
            updateOptimizationDisplay(decision, energyData);
        }
        
        // Get daily report
        const report = await fetchDailyReport();
        if (report) {
            updateDailyReport(report);
        }
        
        // Update charts
        updateAllCharts(energyData);
        
        // Get and display predictions
        const predictions = await fetchPredictions();
        if (predictions) {
            updatePredictionsChart(predictions);
        }
        
        if (!dashboardState.isAutoRefresh) {
            showLoading(false);
        }
    } catch (error) {
        console.error('Error updating dashboard:', error);
        if (!dashboardState.isAutoRefresh) {
            showLoading(false);
        }
        showAlert('Error updating dashboard. Please try again.', 'error');
    }
}

async function fetchEnergyData() {
    try {
        const mode = dashboardState.mode;
        const response = await fetch(`/api/energy-data?mode=${mode}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching energy data:', error);
        return null;
    }
}

async function fetchOptimization(energyData) {
    try {
        const payload = {
            solar: energyData.solar.current,
            battery_current: energyData.battery.current,
            battery_capacity: energyData.battery.capacity,
            grid_available: energyData.grid.available,
            demand: energyData.demand.current,
            mode: dashboardState.mode,
            outage_simulated: dashboardState.outageSimulated
        };
        
        const response = await fetch('/api/optimize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching optimization:', error);
        return null;
    }
}

async function fetchDailyReport() {
    try {
        const response = await fetch('/api/daily-report');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching daily report:', error);
        return null;
    }
}

async function fetchPredictions() {
    try {
        const response = await fetch('/api/predictions');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching predictions:', error);
        return null;
    }
}

// ================================================
// UI UPDATE FUNCTIONS
// ================================================

function updateEnergyCards(data) {
    // Solar
    document.getElementById('solarValue').textContent = `${formatNumber(data.solar.current)} W`;
    document.getElementById('solarMax').textContent = `${formatNumber(data.solar.max)} W`;
    const solarPercent = (data.solar.current / data.solar.max) * 100;
    document.getElementById('solarProgress').style.width = `${solarPercent}%`;
    
    // Battery
    document.getElementById('batteryPercent').textContent = `${data.battery.percent.toFixed(1)}%`;
    document.getElementById('batteryProgress').style.width = `${data.battery.percent}%`;
    
    const chargeStatus = data.battery.charging ? '⚡ Charging' : '📊 Discharging';
    document.getElementById('batteryStatus').textContent = chargeStatus;
    
    // Grid
    document.getElementById('gridStatus').textContent = data.grid.status;
    const gridBadge = document.getElementById('gridBadge');
    if (dashboardState.outageSimulated || !data.grid.available) {
        gridBadge.textContent = '🔴 Offline';
        gridBadge.style.color = '#ef4444';
    } else {
        gridBadge.textContent = '🟢 Online';
        gridBadge.style.color = '#10b981';
    }
    document.getElementById('gridPower').textContent = `${formatNumber(data.grid.power)} W available`;
    
    // Demand
    document.getElementById('demandValue').textContent = `${formatNumber(data.demand.current)} W`;
    document.getElementById('estimatedDemand').textContent = `${formatNumber(data.demand.estimated)} W`;
    const demandPercent = Math.min(100, (data.demand.current / 3000) * 100);
    document.getElementById('demandProgress').style.width = `${demandPercent}%`;
}

function updateOptimizationDisplay(decision, energyData) {
    // Source selection with icon
    const sourceIcons = {
        'Solar': '☀️',
        'Battery': '🔋',
        'Grid': '📡',
        'Solar+Battery': '☀️⚡',
        'Charging Battery': '⚡📥',
        'Emergency Battery': '🚨🔋'
    };
    
    document.getElementById('sourceIcon').textContent = sourceIcons[decision.source] || '⚡';
    document.getElementById('selectedSource').textContent = decision.source;
    document.getElementById('recommendation').textContent = decision.recommendation;
    
    // Metrics
    document.getElementById('efficiencyValue').textContent = `${decision.efficiency}%`;
    document.getElementById('costValue').textContent = `$${decision.cost.toFixed(4)}`;
    document.getElementById('savingsValue').textContent = `$${decision.savings.toFixed(4)}`;
    
    // Update today's savings in sidebar
    document.getElementById('todaySavings').textContent = `$${decision.savings.toFixed(2)}`;
    document.getElementById('efficiencyScore').textContent = `${decision.efficiency}%`;
    
    // Display alerts if present
    displayAlerts(decision.alert);
}

function displayAlerts(alert) {
    const container = document.getElementById('alertsContainer');
    container.innerHTML = ''; // Clear previous alerts
    
    if (alert) {
        const alertBox = document.createElement('div');
        alertBox.className = `alert-box ${alert.type}`;
        
        const iconMap = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'critical': '🚨'
        };
        
        alertBox.innerHTML = `
            <span class="alert-icon">${iconMap[alert.type] || 'i'}</span>
            <span class="alert-text">${alert.message}</span>
        `;
        
        container.appendChild(alertBox);
        alertBox.style.animation = 'slideDown 0.3s ease-out';
    }
}

function updateDailyReport(report) {
    document.getElementById('reportTotalEnergy').textContent = `${report.total_energy.toFixed(2)} kWh`;
    document.getElementById('reportTotalCost').textContent = `$${report.total_cost.toFixed(2)}`;
    document.getElementById('reportTotalSavings').textContent = `$${report.total_savings.toFixed(2)}`;
    document.getElementById('reportRecords').textContent = report.records_count;
}

// ================================================
// CHARTS INITIALIZATION & UPDATES
// ================================================

function initializeCharts() {
    const isDark = document.body.classList.contains('dark-theme');
    const textColor = isDark ? '#cbd5e0' : '#4a5568';
    const gridColor = isDark ? '#4a5568' : '#e2e8f0';
    
    // Daily Usage Chart
    const dailyCtx = document.getElementById('dailyChart');
    if (dailyCtx) {
        dailyChart = new Chart(dailyCtx, {
            type: 'line',
            data: {
                labels: generateHourLabels(),
                datasets: [{
                    label: 'Energy Usage (W)',
                    data: generateDummyData(24),
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#00d4ff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: textColor }
                    }
                },
                scales: {
                    y: {
                        ticks: { color: textColor },
                        grid: { color: gridColor }
                    },
                    x: {
                        ticks: { color: textColor },
                        grid: { color: gridColor }
                    }
                }
            }
        });
    }
    
    // Source Distribution Chart
    const sourceCtx = document.getElementById('sourceChart');
    if (sourceCtx) {
        sourceChart = new Chart(sourceCtx, {
            type: 'doughnut',
            data: {
                labels: ['Solar', 'Battery', 'Grid'],
                datasets: [{
                    data: [35, 45, 20],
                    backgroundColor: [
                        '#fbbf24',
                        '#8b5cf6',
                        '#06b6d4'
                    ],
                    borderColor: isDark ? '#2d3748' : '#ffffff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: textColor }
                    }
                }
            }
        });
    }
}

function updateAllCharts(energyData) {
    // Update daily chart with new data point
    if (dailyChart) {
        const now = new Date();
        const hour = now.getHours();
        dailyChart.data.datasets[0].data[hour] = energyData.demand.current;
        dailyChart.update('none'); // Update without animation
    }
}

function updatePredictionsChart(predictionsData) {
    const predictionsCtx = document.getElementById('predictionsChart');
    if (!predictionsCtx) return;
    
    if (predictionsChart) {
        predictionsChart.destroy();
    }
    
    const isDark = document.body.classList.contains('dark-theme');
    const textColor = isDark ? '#cbd5e0' : '#4a5568';
    const gridColor = isDark ? '#4a5568' : '#e2e8f0';
    
    const predictions = predictionsData.next_24h || [];
    const labels = predictions.map(p => `${p.hour}:00`);
    const data = predictions.map(p => p.predicted_demand);
    
    predictionsChart = new Chart(predictionsCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Predicted Demand (W)',
                data: data,
                backgroundColor: 'rgba(0, 212, 255, 0.6)',
                borderColor: '#00d4ff',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: textColor }
                }
            },
            scales: {
                y: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                },
                x: {
                    ticks: { color: textColor },
                    grid: { color: gridColor }
                }
            }
        }
    });
}

function recreateCharts() {
    // Destroy existing charts
    if (dailyChart) dailyChart.destroy();
    if (sourceChart) sourceChart.destroy();
    if (predictionsChart) predictionsChart.destroy();
    
    // Reinitialize
    initializeCharts();
}

// ================================================
// ENERGY SAVING TIPS
// ================================================

async function loadEnergySavingTips() {
    try {
        const response = await fetch('/api/tips');
        const data = await response.json();
        
        const container = document.getElementById('tipsContainer');
        container.innerHTML = '';
        
        data.tips.forEach((tip, index) => {
            const tipCard = document.createElement('div');
            tipCard.className = 'tip-card';
            tipCard.innerHTML = `
                <div class="tip-title">💡 Tip ${index + 1}</div>
                <div class="tip-description">${tip}</div>
            `;
            container.appendChild(tipCard);
        });
    } catch (error) {
        console.error('Error loading tips:', error);
    }
}

// ================================================
// AUTO-REFRESH FUNCTIONALITY
// ================================================

function startAutoRefresh() {
    // Clear existing interval if any
    if (dashboardState.autoRefreshInterval) {
        clearInterval(dashboardState.autoRefreshInterval);
    }
    
    // Set new interval
    dashboardState.autoRefreshInterval = setInterval(() => {
        dashboardState.isAutoRefresh = true; // Mark as auto-refresh
        updateDashboard().finally(() => {
            dashboardState.isAutoRefresh = false; // Reset flag
        });
    }, dashboardState.refreshRate);
}

// ================================================
// HELPER FUNCTIONS
// ================================================

function formatNumber(num) {
    if (num === null || num === undefined) return '--';
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
    }
    return Math.round(num).toString();
}

function generateHourLabels() {
    const labels = [];
    for (let i = 0; i < 24; i++) {
        labels.push(`${String(i).padStart(2, '0')}:00`);
    }
    return labels;
}

function generateDummyData(count) {
    const data = [];
    for (let i = 0; i < count; i++) {
        // Simulate realistic usage pattern
        if (i >= 6 && i <= 9) { // Morning peak
            data.push(2000 + Math.random() * 500);
        } else if (i >= 18 && i <= 21) { // Evening peak
            data.push(2500 + Math.random() * 500);
        } else if (i < 6 || i > 22) { // Night
            data.push(500 + Math.random() * 200);
        } else { // Day
            data.push(1200 + Math.random() * 400);
        }
    }
    return data;
}

function showLoading(show) {
    const loader = document.getElementById('loadingIndicator');
    if (show) {
        loader.classList.add('active');
    } else {
        loader.classList.remove('active');
    }
}

function showAlert(message, type = 'info') {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type}`;
    alertBox.innerHTML = `
        <span class="alert-icon">✓</span>
        ${message}
    `;
    
    // Insert after header
    const header = document.querySelector('.dashboard-header');
    header.parentNode.insertBefore(alertBox, header.nextSibling);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertBox.remove();
    }, 5000);
}

// ================================================
// ERROR HANDLING
// ================================================

window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
});

// ================================================
// CLEANUP ON PAGE UNLOAD
// ================================================

window.addEventListener('beforeunload', function() {
    if (dashboardState.autoRefreshInterval) {
        clearInterval(dashboardState.autoRefreshInterval);
    }
});
