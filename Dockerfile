# start from python base image
FROM python:3.11

# change working directory
WORKDIR /app

# add requirements file to image
COPY ./requirements.txt /app/requirements.txt

# install python libraries
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# add python code
COPY ./ /app/icebreaker/

# specify default commands
CMD ["python", "icebreaker/main.py"]