# IMAGE STORAGE SERVICE

## Run locally
Requirements: `python3`, `docker` and `pip` package manager
1. Run localstack for imitate AWS service: [docs](https://docs.localstack.cloud/getting-started/quickstart/)
2. Run database `make -C db start-db`
3. Run database migrations: TBD
4. Setup venv `make setup-venv`
5. Install dependencies `make install-deps`
6. Start server `make run-server`

**Example queries**
Create JWT, signed by the same secret as in service configuration.  
The JWT must include `user_id` value. You can use https://jwt.io for that.  
Set token in env vars: `export JWT=<your token here>`  

* Upload image  
```curl -X POST http://localhost:8080/v1/image -H "authorization: Bearer $JWT"  -F "file=@<PATH_TO_IMAGE>"```

* Get image link  
```curl http://localhost:8080/v1/image/<IMAGE_ID> -H "authorization: Bearer $JWT"```
