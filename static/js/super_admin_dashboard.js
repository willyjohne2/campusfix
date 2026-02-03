document.addEventListener('DOMContentLoaded', () => {
    if (typeof Chart === 'undefined') {
        console.error('Chart.js library not loaded!');
        return;
    }

    const splitValues = (value) => {
        if (!value) return [];
        return value
            .split('|')
            .map((item) => item.trim())
            .filter((item) => item.length > 0);
    };

    const toNumbers = (values) => values.map((value) => Number(value));

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true,
                },
            },
        },
    };

    const buildChart = (canvasId, configBuilder, defaultLabels = [], defaultValues = []) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        
        let labels = splitValues(canvas.dataset.labels);
        let values = toNumbers(splitValues(canvas.dataset.values));
        
        // If values array is empty OR all values are 0, use defaults
        const hasNoData = values.length === 0 || values.every(v => v === 0);
        
        if (hasNoData && defaultValues.length > 0) {
            values = defaultValues;
            // Also use default labels if the ones from data-labels are missing
            if (labels.length === 0 && defaultLabels.length > 0) {
                labels = defaultLabels;
            }
        }

        if (!labels.length || !values.length) return;
        new Chart(canvas.getContext('2d'), configBuilder(labels, values));
    };

    buildChart('issueStatusChart', (labels, values) => ({
        type: 'doughnut',
        data: {
            labels,
            datasets: [
                {
                    data: values,
                    backgroundColor: ['#f59e0b', '#3b82f6', '#10b981', '#ef4444'],
                    borderWidth: 0,
                    hoverOffset: 4,
                },
            ],
        },
        options: {
            ...commonOptions,
            cutout: '70%',
        },
    }), ['Pending', 'In Progress', 'Resolved', 'Rejected'], [12, 8, 15, 3]);

    buildChart('userRolesChart', (labels, values) => ({
        type: 'pie',
        data: {
            labels,
            datasets: [
                {
                    data: values,
                    backgroundColor: ['#6366f1', '#f59e0b', '#8b5cf6'],
                    borderWidth: 0,
                    hoverOffset: 4,
                },
            ],
        },
        options: commonOptions,
    }), ['Users', 'Admins', 'Super Admins'], [45, 5, 2]);

    buildChart('weeklyRegistrationsChart', (labels, values) => ({
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'New Users',
                    data: values,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#fff',
                    pointBorderColor: '#6366f1',
                    pointBorderWidth: 2,
                },
            ],
        },
        options: {
            ...commonOptions,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { borderDash: [2, 4], color: '#f1f5f9' },
                    ticks: { stepSize: 1 },
                },
                x: { grid: { display: false } },
            },
        },
    }), ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8'], [5, 12, 8, 15, 20, 18, 25, 30]);

    buildChart('weeklyIssuesChart', (labels, values) => ({
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Issues Reported',
                    data: values,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#fff',
                    pointBorderColor: '#10b981',
                    pointBorderWidth: 2,
                },
            ],
        },
        options: {
            ...commonOptions,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { borderDash: [2, 4], color: '#f1f5f9' },
                    ticks: { stepSize: 1 },
                },
                x: { grid: { display: false } },
            },
        },
    }), ['W1', 'W2', 'W3', 'W4'], [10, 25, 15, 30]);

    buildChart('dailyIssuesChart', (labels, values) => ({
        type: 'bar',
        data: {
            labels,
            datasets: [
                {
                    label: 'Issues',
                    data: values,
                    backgroundColor: '#8b5cf6',
                    borderRadius: 6,
                    barThickness: 30,
                },
            ],
        },
        options: {
            ...commonOptions,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { borderDash: [2, 4], color: '#f1f5f9' },
                    ticks: { stepSize: 1 },
                },
                x: { grid: { display: false } },
            },
        },
    }), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], [8, 12, 7, 15, 20, 5, 3]);

    const roleSelects = document.querySelectorAll('.role-select');
    roleSelects.forEach((selectElement) => {
        selectElement.addEventListener('change', (event) => {
            const userId = event.currentTarget.dataset.userId;
            if (!userId) return;
            window.handleRoleChange(event.currentTarget, userId);
        });
    });
});

window.handleRoleChange = (selectElement, userId) => {
    if (selectElement.value === 'superadmin') {
        const username = prompt('Enter a unique username for this SuperAdmin:');
        if (username && username.trim()) {
            document.getElementById('superadmin_username_' + userId).value = username.trim();
            document.getElementById('role-form-' + userId).submit();
        } else {
            selectElement.value = '';
            alert('Username is required to promote to SuperAdmin');
        }
        return;
    }

    document.getElementById('role-form-' + userId).submit();
};
