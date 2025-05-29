# heroku-jupyter

Use this application to deploy [Jupyter Notebook](https://jupyter.org/) or [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) to Heroku.

This version uses the Heroku dyno's local filesystem to serve notebooks. This means:
- The `notebooks/main.ipynb` included in this repository will be available when your app starts.
- **Changes made to notebooks within the Jupyter UI will NOT be persistent across dyno restarts or redeploys.**
- To save your work from a live session, you **must download** the notebook file(s) from the Jupyter UI.
- To change the default notebook that loads on startup, you should modify `notebooks/main.ipynb` (or other files in the `notebooks/` directory) in your forked Git repository and then redeploy your Heroku app.

If you want to customize your app, feel free to fork this repository.

## Quick start - Installation instructions

The fastest & easiest way to get started is to choose option 1 below: automatic deployment on Heroku.

### 1. Heroku - Automatic Deployment (faster & easier)

First, click on this handy dandy button:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/kenwalger/mia-workshop)

Go through the form that the ^^ above button leads you to, and choose an app name, password, and whether to run Jupyter notebook or Jupyter lab. Then click the purple 'deploy app' button at the bottom of the form.

It will take a couple of minutes for your app to deploy, and then you'll be able to click links to 1) manage your app, and 2) view your live, interactive jupyter application running on a heroku dyno.

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
# Note: The postgres addon is no longer strictly required for notebook storage but might be used by your notebooks.
heroku buildpacks:add --index 1 heroku-community/apt -a $APP_NAME
heroku buildpacks:add --index 2 heroku/python -a $APP_NAME

# Attach the postgres addon:
# heroku addons:create heroku-postgresql:essential-1 --app $APP_NAME # No longer required for notebook storage
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

The `notebooks/main.ipynb` file (and any other files you place in the `notebooks/` directory in your Git repository) are served directly from the application's filesystem. When your Heroku app starts, JupyterLab (or Notebook) is configured to use the `/app/notebooks` directory as its root.

This means:
*   **Automatic Availability:** The `notebooks/main.ipynb` will be available in your Jupyter session once the app is deployed.
*   **No Persistent Storage for UI Edits:** Any changes you make to notebooks (e.g., creating new notebooks, editing existing ones) directly within the JupyterLab/Notebook UI **will be lost** when the Heroku dyno restarts (which can happen due to deploys, daily cycling, or manual restarts).
*   **Saving Your Work:** To save any work done in a live Jupyter session, you **must download the notebook files** (.ipynb) to your local computer using the Jupyter UI's "File > Download" (or similar) option.

### Adding Your Own Notebooks for a Session

If you wish to work with *other* Jupyter notebooks temporarily during a live session:
1.  Access your deployed Jupyter application in your web browser.
2.  Use the "Upload" button in the Jupyter interface to upload your `.ipynb` files from your local computer.
3.  **Remember:** These uploaded notebooks will also be lost if the dyno restarts. Download them if you make changes you want to keep.

### Customizing the Default Notebook(s) for Future Deployments

If you want to change the default notebook(s) that are available every time the application starts:
1.  **Fork this repository** to your own GitHub account (if you haven't already).
2.  In your forked repository, you can:
    *   Modify or replace the content of `notebooks/main.ipynb`.
    *   Add new `.ipynb` files or other supporting files to the `notebooks/` directory.
    *   Remove files from the `notebooks/` directory.
3.  Commit your changes to your fork.
4.  Deploy your forked repository to Heroku. Your customized set of notebooks will then be available on startup.
