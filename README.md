# Logz.io Flask API Interface 🌐

Harness the Logz.io API with this community-built Flask interface. This tool is designed to simplify querying and visualizing data from Logz.io. 

> **Disclaimer**: This is a community project and is not officially supported or affiliated with Logz.io.

![App Preview](images/appPreview.gif)

## 🌟 Features:

- 🖥️ **Web Interface**: A user-friendly interface for querying Logz.io Log data via API.
- 📊 **Data Interpretation**: The script `data_processor.py` interprets the insterted data to Logz.io API in a valid format.
- 📦 **Docker Integration**: Easily deployable using 2 Docker commands.
- 💁‍♂️ **Format Selection**: Select to save your data in a CSV or a TXT format.
- 🏅 **Log Result Amount Limition**: None. You can use it to retrive any amount of data with any (based on the used log account retention) timeframe. 
> ⏲️ **Note**, This app has taken in considuearion the Logz.io API limitions (regarding Log data) and for a big amount. or wide time range of data, it could take a few mintues or more. 


## 🔧 Expected Data Format & Limitations

- **Requered Data**: The interface expects an API token, Lucine querie, Region, Time frame and file format in a spisific fomat that needs to be summnited. That pattren can be modifyied in the `form.html` file and in the `data_processor.py` if needed.
- **Data Limitations**: The `data_processor.py` script has certain hardcoded structures and limitations to avoid abusing or reaching the Logz.io API and to ensure that all data hs been retrived. 
- **Rate Limits**: The tool does not bypass any API rate limits set by Logz.io.
- **Not Official**: Remember, this tool is a community project and isn't an official Logz.io product. Meaning, this is not a suppored feature by the Logz.io Support's Team or any other Logz.io supported team.  


## ⚡ Quick Start:

1. 📥 Pull the Docker image:
   ```bash
   docker pull orbenharoshprojects/logzio-api-app
   ```

2. 🚀 Launch the Docker container:
   ```bash
   docker run -p 8000:8000 orbenharoshprojects/logzio-api-app
   ```

3. 🌐 Visit the app: [http://localhost:8000](http://localhost:8000)


## 💡 Debugging:

- **Container Logs**: Check the Docker container logs to see if there are any issues or errors with the Flask server.
  ```bash
  docker logs [container_id]
  ```
- **API Responses**: The `data_processor.py` script processes API responses and also printed in the used terminal. 


## 🤝 Connect & Contribute:

Feedback and contributions are the backbone of open-source. Please reach out for issues, suggestions, or contributions, Let's grow together!
