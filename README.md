# 🛂 Vahter

**Vahter** is a lightweight web application for employee check-in registration with built-in **Prometheus metrics**, **Grafana dashboards**, logging, and **Kubernetes deployment using Helm and Argo CD**.

The project demonstrates a full end-to-end flow:
HTML form → Flask backend → metrics → Prometheus → Grafana → GitOps (Argo CD).

---

## 🚀 Quick Start (Local)

### 1. Requirements
- Python **3.12+**
- pip

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

After startup:
- 🌐 **Web UI**: http://localhost:3000  
- 📊 **Prometheus metrics**: http://localhost:3000/metrics

---

## 🐳 Run with Docker

```bash
docker build -t vahter-app .
docker run -p 3000:3000 vahter-app
```

---

## ☸️ Run in Kubernetes (Helm)

```bash
helm install vahter ./vahter-chart
```

Default configuration:
- **Service type**: NodePort
- **NodePort**: `30002`

Application URL:
```
http://<NODE_IP>:30002
```

---

## 📊 Prometheus & Grafana Integration

The application exposes metrics automatically:
- `/metrics` endpoint for Prometheus
- Pod annotations enable scraping

A `ServiceMonitor` is provided and compatible with **kube-prometheus-stack**.

### Key metrics
| Metric | Description |
|------|------------|
| `vahter_records_total` | Total number of registered check-ins |
| `flask_http_request_total` | Total HTTP requests |
| `flask_http_request_duration_seconds` | Request latency |

Grafana visualizes:
- number of records
- request rate
- latency
- service-level distribution

---

## 🧠 How the Application Works (Step by Step)

This section describes the **full lifecycle of a single request** — from a user clicking a button in the browser to metrics appearing in Grafana.

---

### 🔹 Step 0. Infrastructure (Before User Interaction)

Before any user opens the site:

- The application is built into a **Docker image**
- The image runs in **Kubernetes** as a `Deployment`
- A `Service` exposes port **3000**
- `ServiceMonitor` tells Prometheus where to scrape metrics
- Argo CD continuously reconciles Git and cluster state

➡️ At this point, a running Pod with the Flask application already exists.

---

### 🔹 Step 1. User Opens the Website

The user navigates to:
```
http://<NODE_IP>:30002
```

What happens internally:
- Request hits the Kubernetes Service
- Service forwards traffic to a Pod
- Flask handles **GET /**
- Server-rendered HTML (`index.html`) and CSS (`style.css`) are returned

📌 This is classic server-side rendering (no SPA, no frontend JS framework).

---

### 🔹 Step 2. User Submits the Form

The form contains:
- Name
- Role
- Optional note

After clicking submit:
- Browser sends a **POST /** request
- Data is sent as `application/x-www-form-urlencoded`

---

### 🔹 Step 3. Flask Processes the POST Request

Inside `app.py`:

- Flask reads form data via `request.form`
- Input strings are sanitized using `strip()`
- Required fields (`name`, `role`) are validated

If validation succeeds:
- Current timestamp is generated
- A record object is created
- The record is appended to the in-memory `records[]` list

---

### 🔹 Step 4. Prometheus Metrics Update

After a successful check-in:

```
vahter_records_total{status="success"} +1
```

Additionally, `prometheus-flask-exporter` automatically tracks:
- HTTP request count
- response status codes
- request duration

📊 All metrics are immediately available at `/metrics`.

---

### 🔹 Step 5. Response Rendering

After handling the POST request:

- Records are sorted (newest first)
- `index.html` is re-rendered
- The user instantly sees the new entry in the table

📌 The entire flow is synchronous.

---

### 🔹 Step 6. Prometheus Scrapes Metrics

Prometheus:
- Discovers the Service via `ServiceMonitor`
- Scrapes `/metrics` every **10 seconds**
- Stores time-series data

---

### 🔹 Step 7. Grafana Visualization

Grafana:
- Uses Prometheus as a data source
- Builds dashboards showing:
  - number of check-ins
  - request throughput
  - latency
  - service-level metrics

Drilldown and log correlation are used for deeper analysis.

---

### 🔹 Step 8. Autoscaling (If Enabled)

When HPA is enabled:

- Kubernetes monitors CPU and memory usage
- Additional Pods are created under load
- Service load-balances traffic automatically

📌 Each Pod maintains its own runtime state.

---

### 🔹 Step 9. Argo CD & GitOps

Argo CD:
- Watches the Helm chart stored in Git
- Compares desired vs actual cluster state
- Automatically applies changes

➡️ The cluster state always matches the Git repository.

---

## 📁 Project Structure

```
.
├── app.py                # Flask application
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container definition
├── templates/
│   └── index.html        # UI template
├── static/
│   └── style.css         # Styles
├── vahter-chart/         # Helm chart
│   ├── templates/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── servicemonitor.yaml
│   │   └── ingress.yaml
│   ├── values.yaml
│   └── Chart.yaml
```
```
link for photos
logs:https://github.com/Samandar5014/vahter-dashboard/blob/9352ba9e5eb30024751177b8d6cdac5d3a866a00/Logs%20from%20grafana.jpg
metriks:https://github.com/Samandar5014/vahter-dashboard/blob/2ffcf5d561c147f75b320858fc0ae94d3117f4d2/Screenshot%202026-01-18%20154958.png
```


