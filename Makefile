build:
	sam validate && \
	sam build --use-container

test:
	sam local start-api
