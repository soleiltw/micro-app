from bottle import run
import boto3
from codeguru_profiler_agent import Profiler

from app.app import init_app

app = application = init_app()

if __name__ == '__main__':
    custom_session = boto3.session.Session(profile_name='dev',
                                           region_name='ap-northeast-1')
    Profiler(profiling_group_name="Microservice",
             aws_session=custom_session).start()
    run(app, debug=True, reloader=True, port=1000)
