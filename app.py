from flask import Flask, request, render_template_string, jsonify
from run import GoFile, Downloader, File

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Download from Gofile</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .spinner-border {
            display: none;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body>
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-6">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h2 class="text-center mb-4">Get Direct Link from Gofile.io</h2>
                    <form id="urlForm">
                        <div class="mb-3">
                            <label for="url" class="form-label">Gofile URL</label>
                            <input type="text" class="form-control" id="url" name="url" placeholder="https://gofile.io/d/CK3SlU" required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Get Link</button>
                        </div>
                        <div class="text-center mt-3">
                            <div class="spinner-border text-primary" role="status" id="spinner"></div>
                        </div>
                    </form>
                    <div class="mt-4" id="result"></div>
                </div>
            </div>
        </div>
    </div>
</div>
<script>
    const form = document.getElementById('urlForm');
    const spinner = document.getElementById('spinner');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        spinner.style.display = 'inline-block';
        resultDiv.innerHTML = '';

        const url = document.getElementById('url').value;

        const response = await fetch('/get-link', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        spinner.style.display = 'none';

        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `<div class="alert alert-success">
                <strong>Direct Link:</strong><br>
                <a href="${data.link}" target="_blank">${data.link}</a>
            </div>`;
        } else {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    });
</script>
<footer class="text-center mt-5 mb-3 text-muted">
  Made with 💻 by
  <a href="https://github.com/nahucai95" target="_blank" class="text-muted text-decoration-none ms-1">
    <i class="fab fa-github me-1"></i>@nahucai95
  </a>
</footer>

</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/get-link", methods=["POST"])
def get_link():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url or not url.startswith("https://gofile.io/d/"):
            return jsonify(success=False, error="Invalid URL.")

        gofile = GoFile()
        gofile.update_token()
        gofile.update_wt()
        files = gofile.get_files(dir="./", url=url)
        if files:
            return jsonify(success=True, link=files[0].link)
        else:
            return jsonify(success=False, error="No file found.")
    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
