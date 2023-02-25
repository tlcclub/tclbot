FROM python:3.11 AS build

ARG TLC_BOT_TOKEN
ENV TLC_BOT_TOKEN=$TLC_BOT_TOKEN

WORKDIR tlcbot
ADD poetry.lock /tlcbot/
ADD pyproject.toml /tlcbot/
RUN pip install --upgrade pip && \
    pip install -U poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install

FROM build AS tclbot
ADD . /tlcbot
CMD ["python ./run.py"]