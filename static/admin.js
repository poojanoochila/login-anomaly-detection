// ---------------- GLOBAL ----------------
let allLogs = [];
let loginChart, deviceChart, browserChart;
let map, markersLayer;

// ---------------- INIT ----------------
document.addEventListener("DOMContentLoaded", () => {
    allLogs = logs || [];

    initCharts();
    initMap();
    updateAll(allLogs);

    setInterval(fetchLogs, 5000);
});

// ---------------- FETCH ----------------
async function fetchLogs() {
    try {
        const res = await fetch("/api/logs");
        const data = await res.json();

        allLogs = data.logs || [];
        updateAll(allLogs);
    } catch (err) {
        console.error("Fetch error:", err);
    }
}

// ---------------- INIT CHARTS ----------------
function initCharts() {
    loginChart = new Chart(document.getElementById("loginChart"), {
        type: "doughnut",
        data: {
            labels: ["Normal", "Suspicious"],
            datasets: [{
                data: [0, 0],
                backgroundColor: ["#28a745", "#dc3545"],
                borderWidth: 1
            }]
        }
    });

    deviceChart = new Chart(document.getElementById("deviceChart"), {
        type: "bar",
        data: {
            labels: ["Mobile", "Desktop"],
            datasets: [{
                label: "Devices",
                data: [0, 0],
                backgroundColor: ["#3b82f6", "#6366f1"]
            }]
        }
    });

    browserChart = new Chart(document.getElementById("browserChart"), {
        type: "bar",
        data: {
            labels: ["Chrome", "Firefox", "Other"],
            datasets: [{
                label: "Browsers",
                data: [0, 0, 0],
                backgroundColor: ["#f59e0b", "#10b981", "#6b7280"]
            }]
        }
    });
}

// ---------------- UPDATE ALL ----------------
function updateAll(logs) {
    updateTable(logs);
    updateCharts(logs);
    updateAnomalies(logs);
    updateMap(logs);
}

// ---------------- TABLE ----------------
function updateTable(logs) {
    const tbody = document.getElementById("logTable");
    if (!tbody) return;

    let html = "";

    logs.forEach(log => {
        html += `
        <tr class="${log.prediction === 1 ? 'alert-row' : ''}">
            <td>${log.id}</td>
            <td>${log.username}</td>
            <td>${log.timestamp}</td>
            <td>${log.ip_address}</td>
            <td>${log.device === 1 ? "Mobile" : "Desktop"}</td>
            <td>${log.browser === 1 ? "Chrome" : log.browser === 2 ? "Firefox" : "Other"}</td>
            <td>${log.country === 0 ? "Local" : "Unknown"}</td>
            <td>${log.failed_attempts}</td>
            <td>
                ${log.prediction === 1
                    ? `<span class="badge danger">Suspicious</span>`
                    : `<span class="badge success">Normal</span>`}
            </td>
        </tr>`;
    });

    tbody.innerHTML = html;
}

// ---------------- UPDATE CHARTS ----------------
function updateCharts(logs) {
    let normal = 0, suspicious = 0;
    let mobile = 0, desktop = 0;
    let chrome = 0, firefox = 0, other = 0;

    logs.forEach(log => {
        log.prediction === 1 ? suspicious++ : normal++;
        log.device === 1 ? mobile++ : desktop++;

        if (log.browser === 1) chrome++;
        else if (log.browser === 2) firefox++;
        else other++;
    });

    if (loginChart) {
        loginChart.data.datasets[0].data = [normal, suspicious];
        loginChart.update();
    }

    if (deviceChart) {
        deviceChart.data.datasets[0].data = [mobile, desktop];
        deviceChart.update();
    }

    if (browserChart) {
        browserChart.data.datasets[0].data = [chrome, firefox, other];
        browserChart.update();
    }
}

// ---------------- ANOMALIES ----------------
function updateAnomalies(logs) {
    const list = document.getElementById("anomalyList");
    if (!list) return;

    list.innerHTML = "";

    logs.filter(l => l.prediction === 1).forEach(log => {
        const item = document.createElement("li");
        item.textContent = `🚨 ${log.username} suspicious login at ${log.timestamp}`;
        list.appendChild(item);
    });
}

// ---------------- MAP ----------------
function initMap() {
    if (typeof L === "undefined") return;

    map = L.map('map').setView([20.5937, 78.9629], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    markersLayer = L.layerGroup().addTo(map);

    setTimeout(() => {
        map.invalidateSize();
    }, 800);
}

function updateMap(logs) {
    if (!map || !markersLayer) return;

    markersLayer.clearLayers();
    let hasValidLocation = false;

    logs.forEach(log => {
        if (
            log.latitude !== null &&
            log.longitude !== null &&
            !isNaN(log.latitude) &&
            !isNaN(log.longitude)
        ) {
            hasValidLocation = true;

            const color = log.prediction === 1 ? "red" : "green";

            const marker = L.circleMarker(
                [parseFloat(log.latitude), parseFloat(log.longitude)],
                {
                    radius: 8,
                    color: color,
                    fillColor: color,
                    fillOpacity: 0.8
                }
            );

            marker.bindPopup(`
                <b>${log.username}</b><br>
                IP: ${log.ip_address}<br>
                Status: ${log.prediction === 1 ? "⚠️ Suspicious" : "Normal"}
            `);

            markersLayer.addLayer(marker);
        }
    });

    if (!hasValidLocation) {
        L.marker([12.9716, 77.5946])
            .addTo(markersLayer)
            .bindPopup("No location data available");
    }
}

/* =====================================================
   ✅ NEW FEATURES ADDED BELOW (Nothing Removed Above)
===================================================== */

// ---------------- APPLY FILTER ----------------
function applyFilters() {
    const userValue = document.getElementById("userFilter").value.toLowerCase();
    const dateValue = document.getElementById("dateFilter").value;

    let filtered = allLogs;

    if (userValue) {
        filtered = filtered.filter(log =>
            log.username.toLowerCase().includes(userValue)
        );
    }

    if (dateValue) {
        filtered = filtered.filter(log =>
            log.timestamp.startsWith(dateValue)
        );
    }

    updateAll(filtered);
}

// ---------------- EXPORT CSV ----------------
function exportCSV() {
    if (!allLogs.length) return;

    let csv = "ID,Username,Timestamp,IP,Device,Browser,Country,Fails,Status\n";

    allLogs.forEach(log => {
        const device = log.device === 1 ? "Mobile" : "Desktop";
        const browser = log.browser === 1 ? "Chrome" :
                        log.browser === 2 ? "Firefox" : "Other";
        const country = log.country === 0 ? "Local" : "Unknown";
        const status = log.prediction === 1 ? "Suspicious" : "Normal";

        csv += `${log.id},${log.username},${log.timestamp},${log.ip_address},${device},${browser},${country},${log.failed_attempts},${status}\n`;
    });

    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "login_logs.csv";
    a.click();

    window.URL.revokeObjectURL(url);
}

// ---------------- EXPORT PDF ----------------
function exportPDF() {
    if (!allLogs.length) return;

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.text("Login Activity Report", 14, 15);
    let y = 25;

    allLogs.forEach(log => {
        const status = log.prediction === 1 ? "Suspicious" : "Normal";

        doc.text(`${log.id} | ${log.username} | ${log.timestamp} | ${status}`, 14, y);
        y += 8;

        if (y > 280) {
            doc.addPage();
            y = 20;
        }
    });

    doc.save("login_report.pdf");
}