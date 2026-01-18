from flask import Flask, render_template, request
from prometheus_flask_exporter import PrometheusMetrics
import datetime
from prometheus_client import Counter  # ← добавляем напрямую из prometheus_client

app = Flask(__name__)

# Инициализация Prometheus-метрик (автоматически создаёт /metrics)
metrics = PrometheusMetrics(app, group_paths=True)

# Кастомный счётчик (теперь правильно через prometheus_client)
records_counter = Counter(
    'vahter_records_total',
    'Общее количество зарегистрированных приходов',
    ['status']  # метка, если нужно (можно убрать)
)

# Хранилище в памяти
records = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        note = request.form.get('note', '').strip()

        if name and role:
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            records.append({
                'time': time_str,
                'name': name,
                'role': role,
                'note': note
            })
            records_counter.labels(status='success').inc()  # ← правильно увеличиваем

    # Новые записи сверху
    sorted_records = sorted(records, key=lambda x: x['time'], reverse=True)

    return render_template('index.html', records=sorted_records)


if __name__ == '__main__':
    print("Приложение запущено")
    print("Сайт     → http://localhost:3000")
    print("Метрики  → http://localhost:3000/metrics")
    print("Для остановки нажмите Ctrl+C\n")

    app.run(
        host='0.0.0.0',
        port=3000,
        debug=False,
        use_reloader=False
    )