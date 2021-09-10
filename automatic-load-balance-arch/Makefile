build_image:
	docker build --tag default_apache -f simple_apache.dockerfile .

srv_up:
	docker-compose -f "docker-compose-lb-cluster.yml" up -d --build

srv_web_scale:
	docker-compose -f "docker-compose-lb-cluster.yml" scale web=3

srv_down:
	docker-compose -f "docker-compose-lb-cluster.yml" down

.PHONY: build_image srv_up srv_down
