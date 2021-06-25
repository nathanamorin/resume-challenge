all: setup up test down deploy


up:
	docker-compose up -d

down:
	docker-compose down

test:
	. .venv/bin/activate; python ./infra/lambda-handler/index.py

setup:
	npm install -g aws-cdk
	python -m venv .venv
	. .venv/bin/activate; python -m pip install -r requirements.txt

deploy:
	. .venv/bin/activate; cdk diff && cdk deploy


