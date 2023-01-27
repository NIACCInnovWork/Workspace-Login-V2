GIT_VERSION=$(shell git log -1 --format="%h")

DOCKER_REPO=registry.digitalocean.com/workspace-login-app
DOCKER_WEB_APP=$(DOCKER_REPO)/web-app
DOCKER_API_TEST=$(DOCKER_REPO)/api-test
DOCKER_VERSION_TAG=1.0.0-alpha-$(GIT_VERSION)


run-ui:
	python -m ws_login_ui

run-api:
	flask --app ws_login_flaskr:create_app run --reload

test:
	python -m unittest discover

#####
# Build API server
#####
docker-api-build:
	docker build -f docker/api-service.dockerfile -t $(DOCKER_WEB_APP):latest -t $(DOCKER_WEB_APP):$(DOCKER_VERSION_TAG) .

docker-api-run: docker-api-build
	docker run -p 8000:8000 -e DB_HOST -e DB_USER -e DB_PASSWORD -e API_TOKEN $(DOCKER_WEB_APP):latest

docker-api-push: docker-api-build
	docker push $(DOCKER_WEB_APP):latest && docker push $(DOCKER_WEB_APP):$(DOCKER_VERSION_TAG)


#####
# Build test container
#####
docker-test-build:
	docker build -f docker/api-tests.dockerfile -t $(DOCKER_API_TEST):latest -t $(DOCKER_API_TEST):$(DOCKER_VERSION_TAG) .

docker-test-run: docker-test-build
	docker run -e API_TOKEN $(DOCKER_API_TEST):latest

docker-test-push: docker-test-build
	docker push $(DOCKER_API_TEST):latest && docker push $(DOCKER_API_TEST):$(DOCKER_VERSION_TAG)
