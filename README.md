<h1 align="center">
    </br>
    <img src="./.github/img/dynatrace-internship-task.png" width="25%" height="25%">
    </br>
    Dynatrace internship task
    </br>
    <h3 align="center">NBP exchange rates API using Python and FastAPI</h3>
    <h4 align="center">Paweł Cichowski</h4>
</h1>

<p align="center">
    <a href="./LICENSE">
        <img src="https://img.shields.io/github/license/Silentsky0/dynatrace-internship-task">
    </a>
    <a href="https://github.com/tiangolo/fastapi">
        <img src="https://img.shields.io/pypi/pyversions/FastAPI">
    </a>
    <br/>
    <a href="https://github.com/Silentsky0/dynatrace-internship-task/actions/workflows/docker-publish.yml">
        <img src="https://github.com/Silentsky0/dynatrace-internship-task/actions/workflows/docker-publish.yml/badge.svg?branch=main">
    </a>
    <a href="https://github.com/Silentsky0/dynatrace-internship-task/actions/workflows/pytest-and-publish.yml">
        <img src="https://github.com/Silentsky0/dynatrace-internship-task/actions/workflows/pytest-and-publish.yml/badge.svg?branch=main">
    </a>
</p>

# Overview

REST API providing access to results of simple operations on exchange rates accessible via Narodowy Bank Polski's
public API

## Table of contents

## Prerequisites

- `python` *`3.7`* or higher
- `docker` - optional

# Setup

The preferred way to access this application is by using a docker container.
Here are some steps which should help you establish a local instance:

1. Prepare a docker image of the application, you can do that either by:
   -  Building one locally either using plain Dockerfile
      ```
      docker build -t dynatrace-internship-task:main .
      ```
      or alternatively using docker-compose
      ```
      docker compose up -d 
      ```
   - Pulling a premade image from the GitHub Repository
     ```
     docker pull ghcr.io/silentsky0/dynatrace-internship-task:main
     ```
2. Run a docker container
   ```
   docker run -d --name dynatrace-internship-task -p 80:80 dynatrace-internship-task:main
   ```
   The application should start in the background, it is available on `localhost:80`

*3. You can also run the app in an ordinary way just using python*

   - Install the necessary requirements
     ```
     pip install -r requirements.txt
     ```
   - Run the app
     ```
     python -m uvicorn api.api:app --reload
     ```

# Usage

The root endpoint is configured to provide SwaggerUI API docs and is available at `http://127.0.0.1/`

To query the operations provided by this API you can use `curl`, an exemplary usage of asking for the average exchange
rate of Pound Sterling on 14.04.2023 is show below:
```
curl -X 'GET' 'http://127.0.0.1/rates/gbp/average/2023-04-14'
```

You can also follow the documentation provided below and try other operations:

- **`GET`** `/rates/{currency_code}/average/{date}` - Average exchange rate of currency for a given date
  - params:
    - `currency_code` - three-letter currency code as specified by NBP
    - `date` - date as a string formatted to YYYY-MM-DD
  - returns:
    - an average exchange rate before a provided date
    - e.g. `http://127.0.0.1/rates/eur/average/2023-04-25` will return `"average_rate": 4.598`
- **`GET`** `/rates/{currency_code}/min-max-average/{quotations}` - Min and max average exchange rate for *n* given
  days (quotations)
  - params:
    - `currency_code` - three-letter currency code as specified by NBP
    - `quotations` - number of working days before the current date to take into consideration
  - returns:
    - the maximum and minimum average value of an exchange rate
    - e.g. `http://127.0.0.1/rates/sek/min-max-average/25` will return `{ "min_average_value": 0.4059, "max_average_value": 0.4231 }`
- **`GET`** `/rates/{currency_code}/buy-ask-difference/{quotations}` - Major buy and ask difference
  - params:
    - `currency_code` - three-letter currency code as specified by NBP
    - `quotations` - number of working days before the current date to take into consideration
  - returns:
    - maximum absolute difference between buy and ask rates for a provided currency
    - e.g. `http://127.0.0.1/rates/gbp/buy-ask-difference/40` will return `"major_buy_ask_difference": 0.1074`