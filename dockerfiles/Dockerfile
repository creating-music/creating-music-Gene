# Define custom function directory
ARG CODE_DIR="/code"

# FROM python:3.12-slim as build-image
FROM showpang/fastapi-base

# Include global arg in this stage of the build
ARG CODE_DIR

# Copy function code
RUN mkdir -p ${CODE_DIR}
COPY . ${CODE_DIR}

RUN mkdir -p /tmp/assets/music && cp -r /code/app/assets/* /tmp/assets/

# Install the function's dependencies
RUN pip install \
    --target ${CODE_DIR} \
        awslambdaric

WORKDIR ${CODE_DIR}

RUN pip install --no-cache-dir -r /code/requirements.txt

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "app.main.handler" ]

