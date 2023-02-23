FROM python:3.11 AS build

ARG TLC_BOT_TOKEN
ENV TLC_BOT_TOKEN = $TLC_BOT_TOKEN

WORKDIR tcbot
ADD poetry.lock /tcbot/
ADD pyproject.toml /tcbot/
RUN pip install --upgrade pip && \
	pip install -U poetry 
RUN poetry config virtualenvs.create false --local && \
	poetry install

FROM build AS tclbot
ADD . /tcbot
CMD ["python ./run.py"]