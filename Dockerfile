FROM python:3.7

# os setup
RUN apt-get update && apt-get -y install \
  python-lxml \
  build-essential \
  libssl-dev \
  libffi-dev \
  python-dev \
  libxml2-dev \
  libxslt1-dev \
  && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# move codebase over
# COPY ukcavegis /usr/src/app/ukcavegis
 COPY app /usr/src/app

# run the spider
CMD ["python", "start.py"]
