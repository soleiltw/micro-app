# Micro-App
## Micro-App(API)

Include health check API.

Docker command  
`docker build -t micro . && docker run -p 1000:1000 --env APP_ENV=DEV --name micro-app micro gunicorn -b 0.0.0.0:1000 -k gthread --workers 1 --threads 2 run`

## Micro-Worker

Need to setup AWS SQS, see config/base.ini.

Docker command  
`docker build -f Dockerfile -t micro . && docker run --env APP_ENV=DEV --env AWS_ACCESS_KEY_ID=******** --env AWS_DEFAULT_REGION=xxx --env AWS_SECRET_ACCESS_KEY=****** --name micro-worker micro python /app/run_worker.py`

## Micro-Job

Docker command
`docker build -t micro . && docker run --env APP_ENV=DEV --env AWS_ACCESS_KEY_ID=***** --env AWS_DEFAULT_REGION=ap-northeast-1 --env AWS_SECRET_ACCESS_KEY=***** --name micro-job micro python /app/run_job.py`

## Micro-APIDoc

Need to build up API doc into html static folder, and use docker to build the image

APIDoc command  
`apidoc -i app/ -o apidoc/`

Docker command  
`docker build -f Dockerfile-apidoc -t micro-apidoc . && docker run -p 81:80 --name micro-apidoc micro-apidoc`