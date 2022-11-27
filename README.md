<p align="center">
  <img src="https://pyronear.org/img/logo_letters.png" width="60%">
</p>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) ![Test Status](https://github.com/pyronear/pyro-crowdsourcer/workflows/tests/badge.svg)  [![Codacy Badge](https://app.codacy.com/project/badge/Grade/1c73a45c6b3f4bc88c6725d50a2771fe)](https://www.codacy.com/gh/pyronear/pyro-crowdsourcer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pyronear/pyro-crowdsourcer&amp;utm_campaign=Badge_Grade) [![CodeFactor](https://www.codefactor.io/repository/github/pyronear/pyro-crowdsourcer/badge)](https://www.codefactor.io/repository/github/pyronear/pyro-crowdsourcer)


The image crowdsourcing platform for wildfire visual data.

## Quick Tour

### Running/stopping the service

You can run the platform as a container using this command:

```shell
make run
```

You can now navigate to `http://localhost:8050` to interact with the platform.

![App screenshot](https://user-images.githubusercontent.com/26927750/173859047-d4e0a9ad-10d8-44cf-9e8b-a0835717b1b6.png)

In order to stop the service, run:
```shell
make stop
```

## Installation

### Prerequisites

- [Docker](https://docs.docker.com/engine/install/)
- [Docker compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/) (optional)

The project was designed so that everything runs with Docker orchestration (standalone virtual environment) that will run itself the [Dash](https://plotly.com/dash/) interface, so you won't need to install any additional libraries.

## Configuration

In order to run the project, you will need to specific some information, which can be done using a `.env` file.
This file will have to hold the following information:
- `API_URL`: the endpoint URL of your [pyro-storage](https://github.com/pyronear/pyro-storage) instance
- `API_LOGIN`: the login for your API access
- `API_PWD`: the password for your API access

So your `.env` file should look like something similar to:
```
API_URL='https://replace.with.your.api.endpoint/'
API_LOGIN=my_dummy_login
API_PWD=my_dummy_password
```

The file should be placed at the root folder of your local copy of the project.


## Contributing

If you scrolled down to this section, you most likely appreciate open source. Do you feel like helping with unresolved issues? Or perhaps submitting a new feature idea? Or contributing in any other way?

You're in luck, we compiled a short guide (cf. [`CONTRIBUTING`](CONTRIBUTING.md)) for you to easily do so!


## License

Distributed under the Apache 2.0 License. See [`LICENSE`](LICENSE) for more information.

