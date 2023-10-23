# Logz.io Flask API Interface 🌐

Harness the Logz.io API with this community-built Flask interface. This tool is designed to simplify querying and visualizing data from Logz.io. 

> **Disclaimer**: This is a community project and is not officially supported or affiliated with Logz.io.

![App Preview](images/appPreview.gif)

## 📌 Features

- **Web-Based Queries**: Input your Logz.io queries via a user-friendly web interface.
  
- **Processed Results**: The tool processes and presents the fetched data for better clarity and understanding.

- **Docker Integration**: Deployable using Docker for easy setup and scalability.

## 🔧 Expected Data Format & Limitations

- **Query Format**: The interface expects queries in the specific format supported by the Logz.io API.

- **Data Limitations**: The `data_processor.py` script has certain hardcoded structures and limitations. It's designed to process standard Logz.io responses.

- **Rate Limits**: The tool does not bypass any API rate limits set by Logz.io.

- **Network Constraints**: The Docker container needs network access to Logz.io. Ensure there's no blocking firewall or proxy.

- **Not Official**: Remember, this tool is a community project and isn't an official Logz.io product.

## 🚀 Getting Started

1. Pull the Docker image:
   ```bash
   docker pull orbenharoshprojects/logzio-api-app
   ```

2. Launch the Docker container:
   ```bash
   docker run -p 8000:8000 orbenharoshprojects/logzio-api-app
   ```

3. Navigate to [http://localhost:8000](http://localhost:8000) in your browser.

## 🛠 Debugging & Troubleshooting

- **Data Mismatches**: If the fetched data looks off, inspect the raw API responses. The `data_processor.py` script interprets the data in specific ways.

- **UI Issues**: If the interface doesn't render correctly, ensure that all static assets are being served properly.

- **Connectivity Issues**: If you can't fetch data, ensure that the Docker container can reach Logz.io. Check network permissions and configurations.
