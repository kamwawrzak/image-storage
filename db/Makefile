.PHONY: start-db
start-db:
	@docker-compose up -d

.PHONY: apply-migrations
apply-migrations:
	yoyo apply

.PHONY: rollback-migrations
rollback-migrations:
	yoyo rollback
