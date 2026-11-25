# 07. Async/Await & Background Services (JS vs Python)

## Async / Await
```python
# JavaScript                      # Python
async function fetchData() {       async def fetch_data():
  const res = await apiCall();         res = await api_call()
  return res;                          return res
}                                  

# Running top-level async:
# JS: (async () => { await fetchData(); })();
import asyncio
asyncio.run(fetch_data())
```

## Running Concurrent Tasks (Promise.all)
```python
# JS: const [res1, res2] = await Promise.all([task1(), task2()]);
res1, res2 = await asyncio.gather(task1(), task2())
```

## How Python Developers Run Background Services in Production
In Node.js, `node server.js` stays running via event loop. In Python:

### 1. ASGI Web Server (FastAPI / Uvicorn)
* Runs web servers in production (non-blocking async):
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2. Task Queues (BullMQ / RabbitMQ equivalent)
* **Celery / Redis / RQ:** Offloads background jobs (sending emails, scraping) outside the HTTP cycle.
```python
@celery_app.task
def send_email_task(user_id):
    # runs asynchronously in worker process
    pass
```

### 3. Production Process Managers
* **Systemd (Linux VM):** Native service manager that keeps Python services running on system reboot.
* **Docker + Gunicorn/Uvicorn:** Standard containerized enterprise deployment.
* **Supervisord:** Process control system that automatically restarts crashed Python scripts.\n