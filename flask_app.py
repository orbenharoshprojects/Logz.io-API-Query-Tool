from flask import Flask, render_template, request, jsonify, url_for, Response
from flask_socketio import SocketIO, emit
import data_processor
import shutil
import os
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins for simplicity; adjust as needed in a production setting
socketio = SocketIO(app, cors_allowed_origins="*")  # Adjust this for production

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            api_token = request.form["api_token"]
            lucene_query = request.form["lucene_query"]
            region_endpoint = request.form["region_endpoint"]
            time_range_NTZ = request.form["timeRangeNTZ"]
            account_ids = request.form["account_Ids"]
            file_format = request.form["file_format"]


            saved_file = data_processor.process_data(api_token, region_endpoint, lucene_query, time_range_NTZ, account_ids, file_format)
            filename = saved_file.split('/')[-1]


            return jsonify(status="success", redirect_url=url_for('success', filename=filename))
        except ValueError as ve:
            return jsonify(status="error", message=str(ve))
        except Exception as e:
            return jsonify(status="error", message=f"An unexpected error occurred: {e}")

    return render_template("form.html")

# Progress bar updates
@socketio.on('connect', namespace='/progress')

@app.route("/success/<filename>")
def success(filename):
    return render_template("success.html", filename=filename)


@app.route("/error")
def error_page():
    return render_template("form.html", error_message=f"An error occurred: {e}")


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)

