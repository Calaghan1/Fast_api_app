tests:
	docker-compose -f docker-compose-test.yaml up
start:
	docker-compose -f docker-compose.yaml up -d
stop:
	docker-compose stop