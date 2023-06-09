# https://docs.docker.com/develop/develop-images/multistage-build/
# Setup build sectio
FROM  python:3.11-bullseye as build_stage

# Do not buffer stdout/stderr just dump it asap
ENV PYTHONUNBUFFERED 1

ARG WORKDIR=/opt/code

WORKDIR ${WORKDIR}

RUN python -m venv /opt/venv
# This "enables" venv by adding the venv path to ${PATH}
# https://stackoverflow.com/questions/48561981/activate-python-virtualenv-in-dockerfile
ENV PATH="/opt/venv/bin:${PATH}"

COPY ./requirements.txt ${WORKDIR}/requirements.txt
RUN ls ${WORKDIR}
RUN pip install --upgrade pip
RUN pip install -U -r requirements.txt


# Run build section
FROM  python:3.11-bullseye as run_stage
RUN echo 'alias ll="ls -lart --color=auto"' >> ~/.bashrc
ARG WORKDIR=/opt/code

WORKDIR ${WORKDIR}
COPY --from=build_stage /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . ${WORKDIR}

# Entry point of dev null used for debugging
CMD ["python", "data_app/main.py"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
