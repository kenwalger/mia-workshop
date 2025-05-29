# heroku-jupyter

Use this application to deploy [Jupyter Notebook](https://jupyter.org/) to
Heroku. If a postgres database is available,
[pgcontents](https://github.com/quantopian/pgcontents) is used to power persistant notebook
storage.

If you want to customize your app, feel free to fork this repository.

## Quick start - Installation instructions

The fastest & easiest way to get started is to choose option 1 below: automatic deployment on Heroku.

### 1. Heroku - Automatic Deployment (faster & easier)

First, click on this handy dandy button:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/heroku-reference-apps/heroku-jupyter)

Go through the form that the ^^ above button leads you to, and choose an app name, password, and whether to run Jupyter notebook or Jupyter lab. Then click the purple 'deploy app' button at the bottom of the form.

It will take a couple of minutes for your app to deploy, and then you'll be able to click links to 1) manage your app, and 2) view your live, interactive jupyter application running on a heroku dyno (with persistant storage!).

Note: If you choose later to fork this repository, you can link your new repo to your heroku app afterwards.

### 2. Heroku - Manual Deployment (does the same thing as 1, but nice for learning / understanding)

Push this repository to your app or fork this repository on github and link your
repository to your heroku app.

To create a new app, run:
```
export APP_NAME=<your_app_name>
export JUPYTER_NOTEBOOK_PASSWORD=<your_jupyter_password>
# set to 'notebook' or 'lab' to choose which jupyter application to launch:
export JUPYTER_NOTEBOOK_OR_LAB=<notebook_or_lab>

# if you don't have git:
brew install git
# clone this repo (swap with your forked repo if you wish):
git clone git@github.com:heroku-reference-apps/heroku-jupyter.git
cd heroku-jupyter

# Create a new app (or use an existing one you've made)
heroku create $APP_NAME

# Set the stack:
heroku stack:set heroku-24 --app $APP_NAME

# Set your required config variable:
heroku config:set JUPYTER_NOTEBOOK_PASSWORD=$JUPYTER_NOTEBOOK_PASSWORD -a $APP_NAME
heroku config:set JUPYTER_NOTEBOOK_OR_LAB=$JUPYTER_NOTEBOOK_OR_LAB -a $APP_NAME

# Specify the buildpacks it should use:
heroku buildpacks:add --index 1 heroku-community/apt -a $APP_NAME
heroku buildpacks:add --index 2 heroku/python -a $APP_NAME

# Attach the postgres addon:
heroku addons:create heroku-postgresql:essential-1 --app $APP_NAME
heroku addons:create heroku-inference:claude-4-sonnet --app $APP_NAME

# Connect your app to the repo:
heroku git:remote -a $APP_NAME

# deploy
git push heroku main

# Follow the URL from ^^ to view your app! To view logs, run `heroku logs --tail -a $APP_NAME`
```

Optional useful commands:
```
# show config variables:
heroku config --app $APP_NAME

# ssh into build
heroku run bash --app $APP_NAME

# view logs
heroku logs --tail -a $APP_NAME
```

If you are really sure that you do not want a password protected notebook and server (not recommended), you can set `JUPYTER_NOTEBOOK_PASSWORD_DISABLED` to `DangerZone!`:
```
heroku config:set JUPYTER_NOTEBOOK_PASSWORD_DISABLED=DangerZone! -a $APP_NAME
```

## Environment / Config variables
- `JUPYTER_NOTEBOOK_PASSWORD`: Set password for notebooks
- `JUPYTER_NOTEBOOK_OR_LAB`: Set to `notebook` or `lab` to determine which Jupyter application to launch
- `JUPYTER_NOTEBOOK_PASSWORD_DISABLED`: Set to `DangerZone!` to disable password protection
- `JUPYTER_NOTEBOOK_ARGS`: Additional command line args passed to `jupyter notebook`; e.g. get a more verbose logging using `--debug`


## Python version

If you want to use a different Python version, you should set it in the `.python-version` file, for example:
```
3.11
```

## Loading and Using Notebooks

The `notebooks/main.ipynb` file included in this repository is designed to be **automatically loaded** into your Jupyter environment when the application starts. This is handled by an internal script (`load_initial_notebooks.py`) that runs during the Heroku application startup process, regardless of whether you used the "Deploy to Heroku" button or performed a manual deployment.

This means:
*   **Automatic Deployment (Heroku Button):** The `notebooks/main.ipynb` will be available in your Jupyter session once the app is deployed.
*   **Manual Deployment (`git push heroku main`):** If you follow the manual deployment steps, `notebooks/main.ipynb` will also be automatically loaded and available.

### Adding Your Own Notebooks (Post-Deployment)

If you wish to add *other* Jupyter notebooks to your running application:
1.  Access your deployed Jupyter application in your web browser (the URL will be provided after deployment).
2.  Use the "Upload" button in the Jupyter interface to upload your `.ipynb` files from your local computer.
3.  These notebooks will be saved persistently in the Heroku Postgres database by `pgcontents`.

### Customizing the Auto-Loaded Notebook

If you want to change the default notebook that is automatically loaded when the application starts:
1.  **Fork this repository** to your own GitHub account.
2.  In your forked repository, you can:
    *   Replace the content of `notebooks/main.ipynb` with your own notebook content.
    *   Or, if you want to load a notebook with a different filename or from a different path within your repository, modify the `notebook_path_in_repo` and `notebook_path_in_jupyter` variables at the top of the `load_initial_notebooks.py` script.
3.  Commit your changes to your fork.
4.  Deploy your forked repository to Heroku. Your customized notebook will then be the one that's auto-loaded.