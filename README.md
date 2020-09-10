

## Run locally

First, activate the virtual environment (with Python 3) with `virtualenv env/bin/activate`. Then run the following command within the `soil-carbon` directory:

```
streamlit run app.py
```

A browser window should open at [localhost:8501](http://localhost:8501/). 


## Deploy

With the proper Heroku permissions, you'll be able to deploy the application with a simple command:

```
git push heroku master
```

Note, however, that if you are developing in `virtualenv` and you install a new package, then you'll have to add the packages to `requirements.txt`.  The deploy on Heroku runs on Docker, which rebuilds the environment from `requirements.txt` on each deploy.

