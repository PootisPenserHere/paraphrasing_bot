FROM python:3.9-alpine3.15

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.1.4

WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml /usr/src/app/

RUN \
    apk add --no-cache --virtual .build-deps g++ musl-dev libffi-dev openssl-dev python3-dev rust cargo && \
    # System deps
    apk add --no-cache tzdata postgresql-dev && \
    # Dependency manager for python
    pip install --no-cache-dir poetry==$POETRY_VERSION && \
    # Project initialization:
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    apk --purge del .build-deps

RUN addgroup -S slothgroup && adduser -S container_sloth -G slothgroup
RUN chown container_sloth:slothgroup -R /usr/src/app

RUN mkdir -p /etc/paraphrasing_bot/templates && chown -R container_sloth /etc/paraphrasing_bot/templates
COPY paraphrasing_bot/templates /etc/paraphrasing_bot/templates
VOLUME /etc/paraphrasing_bot/templates

RUN mkdir -p /var/log/paraphrasing_bot && chown -R container_sloth /var/log/paraphrasing_bot
VOLUME /var/log/paraphrasing_bot

RUN mkdir -p /etc/paraphrasing_bot/static && chown -R container_sloth /etc/paraphrasing_bot/static
COPY paraphrasing_bot/static /etc/paraphrasing_bot/static
VOLUME /etc/paraphrasing_bot/static

COPY . .
RUN chmod 755 /usr/src/app

USER container_sloth


HEALTHCHECK --interval=10s --timeout=2s --start-period=15s \
    CMD wget --quiet --tries=1 --spider http://localhost:5000/health-check || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--reload", "app:app", "–w", "2", "--threads", "3"]
