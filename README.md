# API Profiler 🌀

A plug-and-play Django middleware profiler that tracks API performance and SQL query usage — **no code changes required** in your existing Django app.

## ✨ Features

- ✅ Profiles total execution time of each request.
- ✅ Logs detailed SQL queries executed per request.
- ✅ Color-coded, structured, and readable output.
- ✅ Works with existing Django projects out of the box.
- ✅ Installs as a global CLI: `profile run`

---

## 📦 Installation

Once packaged and uploaded:

```bash
pip install api-profiler
````

(For local development, run from the root of the repo:)

```bash
pip install <<built_whl_file>>
```

---

## 🚀 Usage

Navigate to your Django project folder and run:

```bash
profile --set all #set all metrics as active
profile run  #run django server
profile --unset all #deactivate all metrics
profile --set sql response-headers
profile --unset sql response-body
```

This:

* Injects the `api_profiler` middleware at runtime.
* Runs your Django app at port `8000` (or any custom port).
* Outputs profiling logs in your console.

---

## 📊 Sample Output

```bash
[INFO] 2025-05-26 16:49:31,674 - METHOD: GET     PATH: /users/ - None
[INFO] 2025-05-26 16:49:31,678 - Params:
        None - None
[INFO] 2025-05-26 16:49:31,678 - Headers:
        Content-Length:
        Content-Type: text/plain
        Host: 127.0.0.1:8000
        Connection: keep-alive
        Cache-Control: max-age=0
        Sec-Ch-Ua: "Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"
        Sec-Ch-Ua-Mobile: ?0
        Sec-Ch-Ua-Platform: "Windows"
        Dnt: 1
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Sec-Fetch-Site: none
        Sec-Fetch-Mode: navigate
        Sec-Fetch-User: ?1
        Sec-Fetch-Dest: document
        Accept-Encoding: gzip, deflate, br, zstd
        Accept-Language: en-US,en;q=0.9,hi;q=0.8
        Cookie: csrftoken=XHCl7rQYwFje2xGEgFB2eNwLAV74A3Ru - None
[INFO] 2025-05-26 16:49:31,678 - Body:
 Size: 0 bytes - None
[INFO] 2025-05-26 16:49:31,678 -
--------------------------------------------------------------------------------
SQL Queries Summary
Path     : /users/
Total    : 10 queries
[001]
SELECT auth_user.id AS id,  auth_user.username AS username,  auth_user.email AS email
FROM auth_user
       Repeated: 10x | Total Time: 0.000 sec

Total Execution Time: 0.000 sec
--------------------------------------------------------------------------------
 - None
[INFO] 2025-05-26 16:49:31,679 - Response: []
 Size: 2 bytes - None
[INFO] 2025-05-26 16:49:31,679 - Response Headers:
        Content-Type: application/json - None
[INFO] 2025-05-26 16:49:31,679 - Status: 200 Total time taken: 0.005 seconds
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
git clone git@github.com:Av-sek/api-profiler.git
cd api_profiler
pip install -e .

OR

You can also build it using

pip install --upgrade build
python -m build (on project root dir)
pip install dist/api_profiler-0.1.0-py3-none-any.whl
```

Run it on any Django project:

```bash
profile run
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
