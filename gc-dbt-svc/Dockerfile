FROM ghcr.io/dbt-labs/dbt-bigquery:1.7.latest

# Define the environment variables

ENV PYTHONUNBUFFERED True
ENV APP_HOME /dbt-svc
ENV PORT 8080
ENV DBT_PROFILES_DIR ${APP_HOME}/profiles
ENV DBT_PROJECT_DIR ${APP_HOME}/dbt
ENV FLASK_SERVICE_DIR ${APP_HOME}/flask
ENV PRIVATE_KEY_ID ${PRIVATE_KEY_ID}
ENV PRIVATE_KEY ${PRIVATE_KEY}
ENV CLIENT_EMAIL ${CLIENT_EMAIL}

# Deploy the code

WORKDIR ${APP_HOME}

COPY dbt/ ${DBT_PROJECT_DIR}/
COPY profiles/ ${DBT_PROFILES_DIR}/
COPY flask ${FLASK_SERVICE_DIR}/

# Install dbt dependencies

WORKDIR ${DBT_PROJECT_DIR}

RUN dbt deps

# Install flask service dependencies

WORKDIR ${FLASK_SERVICE_DIR}

RUN python -m venv venv \
    && venv/bin/python -m pip install -r requirements.txt

# Start the flask service

ENTRYPOINT exec venv/bin/python -m gunicorn \
    --bind :${PORT} \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    main:app