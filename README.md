# Logz.io API Query Tool App
[![Made with Flask](https://img.shields.io/badge/Made%20with-Flask-1f425f.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dive into our Flask interface, purposefully built to simplify your querying and data retrieval journey with Logz.io.

> **🚫 Disclaimer**: This is a community-driven tool and is NOT officially associated with or endorsed by Logz.io.

<div align="center">

![App Preview](images/appPreview.gif)

</div>

## 📌 Features

- **Web-Based Queries**: Seamlessly input your Logz.io queries and fetch log data through an intuitive web interface.
  
- **Data Export**: Export data in your choice of CSV or TXT formats.

---

## 🔧 Data Expectations & Limitations

- **Query Format**: Our interface is tailored to accept the specific query format that the Logz.io API supports.

- **Data Parsing**: The `data_processor.py` script is structured with predefined configurations tailored for standard Logz.io responses.

- **Network Access**: Ensure your app can freely communicate with Logz.io. Ensure no restrictive firewalls or proxies are in place.

- **Community Reminder**: This isn't an official product of Logz.io, but a project from our community.

---

## 🚀 Getting Started

### macOS and Linux:

To set everything up, simply run the command below:

```bash
git clone https://github.com/orbenharoshprojects/Logz.io-API-Query-Tool "Logz.io-API-Query-Tool App" && cd "Logz.io-API-Query-Tool App" && chmod +x setup_and_run.sh && ./setup_and_run.sh
```

### Windows:

Just execute the command below:

```batch
git clone https://github.com/orbenharoshprojects/Logz.io-API-Query-Tool "Logz.io-API-Query-Tool App" && cd "Logz.io-API-Query-Tool App" && setup_and_run.bat
```

Post-setup, you can access the interface at [http://localhost:8000](http://localhost:8000).

<div align="center">

![GetData Preview](images/success.gif)

</div>

---

## 🧐 Finding & Setting Required Data

If you need to tweak data verification or patterns, adjustments can be made in `form.html` and `data_processor.py`.

The details below guide you on sourcing the needed information:

- **API Token**: Can be found in Logz.io under the "Settings" -> "Manage Tokens" page for the needed account. 

- **Lucene Query**: A valid format witout the usage of wiilecards. 

- **Region - Endpoint**: The Can be found in Logz.io under the "Settings" page. 

- **Time Frame And OpenSearch TZ**: The "start" and "end" time frame for the used query. Can be taken directly via Logz.io OpenSearch UI with the addition of the OpenSearch UI timezone.
> Ex. with IDT: Oct 23, 2023 @ 13:05:08.275 - Oct 24, 2023 @ 13:05:08.275 - idt

<div align="center">

![GetData Preview](images/getdata.gif)

</div>

> Additional options are described in the `data_processor.py` file. Remember, the default timezone in your Logz.io OpenSearch is set to your browser's timezone. If needed, contact the Logz.io Support team for modifications.

---

## 🐞 Debugging & Troubleshooting

- **Data Mismatches**: If the fetched data looks off, inspect the raw API responses. The `data_processor.py` script interprets the data in specific ways and can be modified.

- **UI Issues**: If the interface doesn't render correctly, ensure that all static assets are being served properly and that all that all the dependencies were installed via 'requirements.txt' file.

- **Connectivity Issues**: If you can't fetch data, ensure that you can reach Logz.io. Check network permissions and configurations.

---

## 🤲 Contribute

Found something amiss? Have an enhancement in mind? We're all ears. Be a part of our growing community and help us make this tool even better!

