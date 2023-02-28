FROM python:3.11 AS build

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
