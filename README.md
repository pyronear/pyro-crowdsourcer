<p align="center">
  <img src="https://pyronear.org/img/logo_letters.png" width="60%">
</p>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) ![Test Status](https://github.com/pyronear/pyro-crowdsourcer/workflows/tests/badge.svg)  [![Codacy Badge](https://app.codacy.com/project/badge/Grade/1c73a45c6b3f4bc88c6725d50a2771fe)](https://www.codacy.com/gh/pyronear/pyro-crowdsourcer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pyronear/pyro-crowdsourcer&amp;utm_campaign=Badge_Grade) [![CodeFactor](https://www.codefactor.io/repository/github/pyronear/pyro-crowdsourcer/badge)](https://www.codefactor.io/repository/github/pyronear/pyro-crowdsourcer)



## Installation

### Prerequisites

Python 3.6 (or higher) and [pip](https://pip.pypa.io/en/stable/) are required to install docTR. 

### Developer mode
Alternatively, you can install it from source, which will require you to install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
First clone the project repository:

```shell
git clone https://github.com/pyronear/pyro-crowdsourcer.git
pip install -r pyro-crowdsourcer/requirements.txt
```


## Usage

![App screenshot](https://user-images.githubusercontent.com/26927750/148696958-bdc91784-cd3d-40e2-88c8-4ef74d309730.png)

The app was designed using [Streamlit](https://streamlit.io/) to crowdsource visual situations that can be encountered for wildfire surveillance.

### Running it locally

Run your app in your default browser with:

```shell
streamlit run src/app.py
```


## Docker container

If you wish to deploy containerized environments, you can use the provided Dockerfile to build a docker image:

```shell
docker build . -t <YOUR_IMAGE_TAG>
docker run -d -p 8001:8501 <YOUR_IMAGE_TAG>
```


## Contributing

If you scrolled down to this section, you most likely appreciate open source. Do you feel like extending the range of our supported characters? Or perhaps submitting a paper implementation? Or contributing in any other way?

You're in luck, we compiled a short guide (cf. [`CONTRIBUTING`](CONTRIBUTING.md)) for you to easily do so!


## License

Distributed under the Apache 2.0 License. See [`LICENSE`](LICENSE) for more information.

