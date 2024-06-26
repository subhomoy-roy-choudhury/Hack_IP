<br/>
<p align="center">
  <a href="https://github.com/subhomoy-roy-choudhury/Hack_IP">
    <img src="https://svg-banners.vercel.app/api?type=luminance&text1=Hack%20IP%20🕵🏻‍♂️&width=800&height=300" alt="Hack_IP" width="640" height="320" />
  </a>

  <!-- <h3 align="center">Hack IP</h3> -->

  <p align="center">
    CLI Tool to gather System Information, IP Address, and device location.
    <br/>
    <br/>
    <a href="https://github.com/subhomoy-roy-choudhury/Hack_IP"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/subhomoy-roy-choudhury/Hack_IP">View Demo</a>
    .
    <a href="https://github.com/subhomoy-roy-choudhury/Hack_IP/issues">Report Bug</a>
    .
    <a href="https://github.com/subhomoy-roy-choudhury/Hack_IP/issues">Request Feature</a>
  </p>
</p>

<p align="center">
    <img alt="Test Cases" src="https://github.com/subhomoy-roy-choudhury/Hack_IP/actions/workflows/master-lint-and-test.yml/badge.svg" />
    <img alt="Downloads" src="https://img.shields.io/github/downloads/subhomoy-roy-choudhury/Hack_IP/total" />
    <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/subhomoy-roy-choudhury/Hack_IP?color=dark-green" />
    <img alt="Github Issues" src="https://img.shields.io/github/issues/subhomoy-roy-choudhury/Hack_IP" />
    <img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/subhomoy-roy-choudhury/Hack_IP" />
    <img alt="Repo Size" src="https://img.shields.io/github/repo-size/subhomoy-roy-choudhury/Hack_IP" />
    <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/subhomoy-roy-choudhury/Hack_IP" />
    <img alt="Github License" src="https://img.shields.io/github/license/subhomoy-roy-choudhury/Hack_IP" />
    <img alt="Test Cases" src="https://github.com/subhomoy-roy-choudhury/Hack_IP/actions/workflows/python-publish.yml/badge.svg" />


</p>

## Table Of Contents

* [About the Project](#about-the-project)
* [Features](#features)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

## About The Project

**HackIP** is an innovative system information and network analysis tool that combines the power of system diagnostics with advanced natural language processing capabilities provided by GPT. HackIP fetches detailed system information, scans for open network ports, identifies public IP addresses, and leverages GPT to provide insightful analysis and interaction with the gathered data.

## Features

HackIP comes with a multitude of features:

- **System Information Gathering**: Retrieves comprehensive details about your system's hardware and software configuration.
- **Network Port Scanning**: Efficiently scans and reports open network ports, providing crucial information for network security analysis.
- **Public IP Geolocation**: Identifies the geolocation of your public IP address, offering valuable context for network traffic analysis.
- **GPT-Enabled Data Interaction**: Uses the latest GPT models to interpret, analyze, and interact with the collected data, offering a user-friendly interface and actionable insights.


## Getting Started

To install HackIP, follow these steps:

### Prerequisites

1. [Python >=3.9](https://www.python.org/)
2. [OpenAI Key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key)
3.  [Cuttly API key](https://cutt.ly/) (optional)

### Installation

With pip:

```sh
pip install hack-ip
```

Next, run:

```
hackip
```

## Usage

You can run the HackIp using the following command:

```sh
hackip run [--details]
```
Each option for the hackip run command is detailed below:

- `--details`: Enables advanced detailed scanning using Nmap. This option is suitable for comprehensive network scanning.
- `--chat`: Activates a chat interface for interactive communication with the tool.
- `--no_fetch`: If set, the tool will chat without fetching system information. Ideal for chat-only interactions.
- `--cuttly_api_key`: Specify your Cuttly URL shortener API key with this option, necessary for URL shortening features.
- `--openai_key`: Your OpenAI API key. This is required for functionalities that utilize OpenAI services, such as chat response generation.

### Example Usage

Run HackIp with Advanced Scanning and Chat:

```sh
hackip run --details --chat --cuttly_api_key YOUR_CUTTLY_API_KEY --openai_key YOUR_OPENAI_API_KEY
```

Run HackIp with Chat Feature Only:

```sh
hackip run --chat --openai_key YOUR_OPENAI_API_KEY
```

*Note: Replace YOUR_CUTTLY_API_KEY and YOUR_OPENAI_API_KEY with your actual API keys.*


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=subhomoy-roy-choudhury/Hack_IP&type=Date)](https://star-history.com/#subhomoy-roy-choudhury/Hack_IP&Date)


## Roadmap

See the [open issues](https://github.com/subhomoy-roy-choudhury/Hack_IP/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/subhomoy-roy-choudhury/Hack_IP/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/<feature>`)
3. Commit your Changes (`git commit -m 'Add some <feature>'`)
4. Push to the Branch (`git push origin feature/<feature>`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/subhomoy-roy-choudhury/Hack_IP/blob/master/LICENSE) for more information.

## Contact
**Subhomoy Roy Choudhury** - *SDE at Fynd* - [Github](https://src-portfolio.oderna.in/link/GITHUB) - [Linkedin](https://src-portfolio.oderna.in/link/LINKEDIN) - [Twitter](https://src-portfolio.oderna.in/link/TWITTER)

Project Link: [https://github.com/subhomoy-roy-choudhury/Hack_IP](https://github.com/subhomoy-roy-choudhury/Hack_IP)

## Acknowledgements

* [Open AI](https://openai.com/)
* [Poetry](https://www.poetryfoundation.org/)
* [Nmap](https://nmap.org/)
* [Beautify Github Readme](https://github.com/rzashakeri/beautify-github-profile)
