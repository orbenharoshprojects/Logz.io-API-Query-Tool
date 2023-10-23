from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
import data_processor
import shutil
import os
from flask import jsonify

app = Flask(__name__)


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


@app.route("/success/<filename>")
def success(filename):
    return render_template("success.html", filename=filename)


@app.route("/success/<filename>")
def download_file(filename):
    print("Inside download_file function")  # <-- Here
    source_path = f"outputs/{filename}"
    destination_folder = f"{os.path.expanduser('~')}/Downloads/"
    print(f"Source: {source_path}")  # <-- And here
    print(f"Destination Folder: {destination_folder}")  # <-- And here

    try:
        destination_path = os.path.join(destination_folder, filename)
        print(f"Destination Path: {destination_path}")  # <-- And here
        shutil.move(source_path, destination_path)
    except Exception as e:
        print(f"Exception: {e}")  # <-- And here
        return f"Error: {e}"

    return render_template("success.html", filename=filename)


@app.route("/error")
def error_page():
    return render_template("form.html", error_message=f"An error occurred: {e}")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)