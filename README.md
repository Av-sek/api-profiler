# Dev Pulse 🌀

A plug-and-play Django middleware profiler that tracks API performance and SQL query usage — **no code changes required** in your existing Django app.

## ✨ Features

- ✅ Profiles total execution time of each request.
- ✅ Logs detailed SQL queries executed per request.
- ✅ Color-coded, structured, and readable output.
- ✅ Works with existing Django projects out of the box.
- ✅ Installs as a global CLI: `profile 8000`

---

## 📦 Installation

Once packaged and uploaded:

```bash
pip install dev-pulse
````

(For local development, run from the root of the repo:)

```bash
pip install <<build_whl_file>>
```

---

## 🚀 Usage

Navigate to your Django project folder and run:

```bash
profile 8000
```

This:

* Injects the `api_profiler` middleware at runtime.
* Runs your Django app at port `8000` (or any custom port).
* Outputs profiling logs in your console.

---

## 📊 Sample Output

```bash
[INFO] 2025-05-20 01:51:10 - METHOD: GET     PATH: /users/

--------------------------------------------------------------------------------
SQL Queries Summary
Path     : /users/
Total    : 1 queries
[001]
SELECT auth_user.id, auth_user.username, auth_user.email FROM auth_user
       Time: 0.000 sec

Total Execution Time: 0.000 sec
--------------------------------------------------------------------------------

[INFO] 2025-05-20 01:51:10 - Total time taken: 0.004 seconds
```

---

## 🛠️ How It Works

* Uses a runtime patching technique to inject middleware without needing to modify `settings.py`.
* Automatically detects the Django project in the current directory.
* Uses a CLI entry point (`profile`) for ease of use.
* Provides clear logging using `logging.config.dictConfig`.

---

## 🔧 Developer Setup

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/dev-pulse.git
cd dev-pulse
pip install -e .

OR

You can also build it using

pip install --upgrade build
python -m build (on project root dir)
pip install dist/api_profiler-0.1.0-py3-none-any.whl
```

Run it on any Django project:

```bash
profile 8000
```


---

## 📌 Roadmap Ideas

* 🔍 Per-view performance breakdown
* 📈 Export profiling data to JSON/CSV
* 🌐 Web dashboard integration
* 🔐 Auth headers masking
* 🧪 Unit test coverage and integration tests

---

## 👤 Author

**Abhishek Ghorashainee**
[GitHub](https://github.com/Av-sek) · [LinkedIn](https://www.linkedin.com/in/abhishek-ghorashainee-92318419a/)

---

## 📄 License

This project is licensed under the MIT License.

---
