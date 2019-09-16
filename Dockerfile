FROM python:3.6

RUN echo "Asia/Taipei" > /etc/timezone \
 && rm /etc/localtime &&  dpkg-reconfigure -f noninteractive tzdata

ENV PYTHONPATH=/app

COPY requirements.txt /app/
RUN pip install --upgrade pip \
 && pip install wheel \
 && pip install -r /app/requirements.txt \
 && rm -rf ~/.cache/pip

COPY . /app/

EXPOSE 1000

# Use docker command
# CMD ["gunicorn", "-b", "0.0.0.0:100", "--workers", "4", "--threads", "8", "--worker-connections", "200" , "--max-requests" , "180000" ,"run"]
