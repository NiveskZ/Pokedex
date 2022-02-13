run: 
	FLASK_DEBUG=true \
		./venv/bin/flask run

venv: 
	virtualenv -p python3 venv 