---

# 🌀 API Profiler

A plug-and-play **Django middleware profiler** that tracks API performance, SQL query behavior, and more — all **without code changes** or server restarts.

Perfect for developers who want real-time insight into their API behavior during development.

---

## ✨ Features

* ✅ Profiles **total request execution time**
* ✅ Logs **detailed SQL queries** per request
* ✅ **Detects N+1 issues** with repeated query tracking
* ✅ Beautiful, structured console logs (headers, body, SQL, etc.)
* ✅ **No code changes** — injects middleware at runtime
* ✅ Global CLI-based usage via `profile run`

---

## 📦 Installation

Once published:

```bash
pip install api-profiler
```

For local development (from repo root):

```bash
pip install dist/api_profiler-0.1.0-py3-none-any.whl
```

Or install in editable mode:

```bash
pip install -e .
```

---

## 🚀 Usage

From your Django project folder, use the CLI to control profiling:

### Step 1: Start Django with profiling

```bash
profile run
```

### Step 2: In another terminal, toggle profiling live

```bash
# Activate all metrics
profile --set all

# Deactivate all
profile --unset all

# Enable specific profiling
profile --set sql response-headers

# Disable specific profiling
profile --unset sql response-body
```

⚡ This works **on the live running server** — no restart required.

---

## 🧠 What It Profiles

| Metric             | Description                               |
| ------------------ | ----------------------------------------- |
| `sql`              | Query count, total time, repeated queries |
| `headers`          | Request and response headers              |
| `params` / `body`  | URL params and request body               |
| `response`         | Response content and size                 |
| `response-headers` | Response headers                          |
| `all`              | Enables or disables all of the above      |

---

## 📊 Sample Output

```plaintext
[INFO] METHOD: GET     PATH: /users/
[INFO] Headers:
    Content-Type: text/plain
    Host: 127.0.0.1:8000
    ...
[INFO] Body: Size: 0 bytes
--------------------------------------------------------------------------------
SQL Queries Summary
Path     : /users/
Total    : 10 queries
[001]
SELECT ... FROM auth_user
       Repeated: 10x | Total Time: 0.000 sec

Total Execution Time: 0.000 sec
--------------------------------------------------------------------------------
[INFO] Response: [] Size: 2 bytes
[INFO] Status: 200 Total time taken: 0.005 seconds
```

---

## 🛠️ How It Works

* 🧩 **Middleware Injection**: Runtime patching (no `settings.py` modification)
* 📡 **Live Toggle**: CLI commands modify profiling behavior in real time
* ⚙️ **Auto Project Detection**: Automatically detects Django apps in the current directory
* 📋 **Clean Logging**: Powered by `logging.config.dictConfig`

---

## 🔧 Developer Setup

```bash
git clone https://github.com/Av-sek/api-profiler.git
cd api_profiler
pip install -e .

# OR build and install from source
pip install --upgrade build
python -m build
pip install dist/api_profiler-0.1.0-py3-none-any.whl
```

To use on your Django app:

```bash
profile run
```

## 👤 Author

**Abhishek Ghorashainee**
[🔗 GitHub](https://github.com/Av-sek) · [🔗 LinkedIn](https://www.linkedin.com/in/abhishek-ghorashainee-92318419a/)

---

## 📄 License

MIT License — open to all contributions.

---