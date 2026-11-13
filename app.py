#used to call the localstorage to be stored, subprocess is used to make sure that the code is running in a more complex way(similar to extension)
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import subprocess

#naming the flask
app = Flask(__name__)
CORS(app)

#display when nothing happen or no data is sended
current_clipboard = {"text": ""}

#this is the function that is used to make the user entered the dat that desire so that it can store
def set_windows_clipboard(text: str):
    """Pushes text onto your laptop's clipboard."""
    try:
        process = subprocess.Popen(
          #tells the python location to execute 
            ["powershell", "-command", "Set-Clipboard", "-Value", "$input"],
            stdin=subprocess.PIPE,
            #tell ur function that the code must be in letter not byte
            text=True,
            #handle speacial letter emoji ....etx
            encoding="utf-8",
        )
        process.communicate(input=text)
        return True
    except Exception as e:
        print(f"[-] Clipboard error: {e}")
        return False


def get_windows_clipboard():
    """Reads text from your laptop's physical clipboard."""
    try:
        process = subprocess.run(
            ["powershell", "-command", "Get-Clipboard"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        return process.stdout.strip()
    except Exception as e:
        print(f"[-] Read clipboard error: {e}")
        return current_clipboard["text"]


@app.route("/update", methods=["POST"])
def update_clipboard():
    data = request.json
    if data and "text" in data:
        text_content = data["text"]
        current_clipboard["text"] = text_content
        set_windows_clipboard(text_content)
        return jsonify({"status": "success", "message": "Clipboard updated!"})
    return jsonify({"status": "error", "message": "No text provided"}), 400


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["GET"])
def get_clipboard():
    pc_text = get_windows_clipboard()
    if pc_text:
        current_clipboard["text"] = pc_text
    return jsonify(current_clipboard)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)