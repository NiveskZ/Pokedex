run: 
	FLASK_DEBUG=true \
		./venv/bin/flask run

venv: 
	virtualenv -p python3 venv 
	./venv/bin/pip install -r requirements.txt

IMAGE_TAG=niveskz/pokedex

docker-build:
	docker build -t $(IMAGE_TAG) .

docker-run: docker-build
	docker run -it --rm -p 80:80 $(IMAGE_TAG) 

docker-debug: docker-build
	docker run -it --rm $(IMAGE_TAG) sh