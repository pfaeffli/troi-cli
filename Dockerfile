ARG CI_PYTHON_IMAGE
ARG CI_OPENAPI_GENERATOR_IMAGE
ARG CI_INSTALL_DEV_REQUIREMENTS

# Stage 1: Use openapi-generator to generate code
FROM $CI_OPENAPI_GENERATOR_IMAGE AS generator

# Assuming you have your recommender-api-v1/openapi-specification.yml in the same directory as your Dockerfile.
COPY recommender-api-v1/ /local/recommender-api-v1/
# Generate openapi time_tracking_synchronisation-api
RUN bash /usr/local/bin/docker-entrypoint.sh generate -i /local/recommender-api-v1/openapi-specification.yml -g python -o local/openapi

# Stage 2: Use the Python base image
FROM $CI_PYTHON_IMAGE as app

ARG CI_INSTALL_DEV_REQUIREMENTS

ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

RUN apk add --update --no-cache git libgit2-dev build-base g++ libgit2 py3-pygit2 linux-headers
RUN pip3 install --upgrade pip --break-system-packages


# install app
COPY . /app
RUN rm -rf /app/recommender-api-v1

# Copy generated code from the first stage
COPY --from=generator local/openapi /app/openapi

RUN pip3 install /app/openapi --break-system-packages
RUN pip3 install /app  --break-system-packages

WORKDIR /app

# Install dev requirements
RUN if [ "$CI_INSTALL_DEV_REQUIREMENTS" = "true" ] ; then pip3 install -r requirements.dev.txt --break-system-packages; fi

EXPOSE 80
CMD ["python3", "-u", "recommender_api/__main__.py"]

