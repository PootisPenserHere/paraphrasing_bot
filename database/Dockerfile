FROM postgres:12-alpine

# So that the timezone can be sent with the TZ environment
RUN apk add --no-cache tzdata

# Starting scripts
ADD . /docker-entrypoint-initdb.d
