
# ml-api Emily API

To run the API, execute: 
```
python api.py
```

By default, your API will be accessible at http://0.0.0.0:4242.
To test it, try running: 
```
curl http://0.0.0.0:4242/api/health
```

You are able to test your API by running the following command in the terminal:
```
python evaluation_script.py
```

To change the predictor open the `ml/predictor.py` file and put in some code to accomplish the prediction.