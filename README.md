# MOVIE_API_INTEGRATION

## DO THE FOLLOWING STEPS TO GET STARTED

```
pip install -r requirements.txt
```

```
python3 run.py
```


## API - ENDPOINTS  
  
  To access secured endpoints, you will need to provide an access token. The register route is the only unprotected route. It will register your user and provide your access token valid for the next 60 minutes.  
  Subsequently add the field "x-access-token" to your request headers to access these protected routes.
  
  ```
	http://127.0.0.1:5000/register  

	Request Payload:
	{
	 “username”: <desired username>,
	 “password”: <desired password>
	}

	Response:
	{
	 “access_token”: <Access Token>
	}

	

  ``` 