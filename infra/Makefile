all: setup deploy
setup:
	npm install -g aws-cdk
	python -m venv .venv
	. .venv/bin/activate; python -m pip install -r requirements.txt

deploy:
	. .venv/bin/activate; cdk diff && cdk deploy


