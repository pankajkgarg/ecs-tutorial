import os
from flask import Flask, render_template
import redis
import pprint


if os.getenv("REDIS_ENV_AWS_EXECUTION_ENV", None) == "AWS_ECS_EC2":
	# AWS ECS environment
	REDIS_HOST = os.getenv('REDIS_PORT_6379_TCP_ADDR', 'localhost')
	REDIS_PORT = os.getenv('REDIS_PORT_6379_TCP_PORT', 6379)
else:
	# local environment
	REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
	REDIS_PORT = os.getenv('REDIS_PORT', 6379)



redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

app = Flask(__name__)

@app.route('/')
def hello_world():
	info = ""
	visitor_count = 1
	info = redis_instance.info("memory")

	visitor_count = redis_instance.incr("visitor_count")

	render_data = {
		"visitor_count": visitor_count,
		"environ_data": pprint.pformat(get_environ_data()),
		"redis_data": pprint.pformat(info),
	}

	return render_template("index.html", **render_data)
	


def get_environ_data():
	return { key: value for key, value in dict(os.environ).items() if key.startswith("REDIS_PORT") }

