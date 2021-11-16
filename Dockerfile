FROM python:3.8.0-slim

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

# setup working directory for container
WORKDIR /usr/src/app
# copy project to the image
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

python
