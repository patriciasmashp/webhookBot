# first stage
FROM python:3.10 AS builder
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# second stage
FROM python:3.10-slim
WORKDIR /app
EXPOSE 23456
# copy only the dependencies that are needed for our application and the source files
COPY --from=builder /root/.local /root/.local
COPY ./ .

# update PATH
ENV PATH=/root/.local:$PATH

# make sure you include the -u flag to have our stdout logged
CMD [ "python", "-u", "./main.py" ]