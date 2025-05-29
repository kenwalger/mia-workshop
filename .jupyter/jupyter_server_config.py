try:
    import os
    import json
    import traceback
    import IPython.lib
    # import pgcontents # DEACTIVATED - Switched to FileSystemContentsManager

    c = get_config() # type: ignore # noqa F821

    # Root directory for notebook - This might be overridden by --notebook-dir in start_jupyter
    # c.ServerApp.root_dir='/'

    ### Password protection ###
    # http://jupyter-notebook.readthedocs.io/en/latest/security.html
    if os.environ.get('JUPYTER_NOTEBOOK_PASSWORD_DISABLED') != 'DangerZone!':
        passwd = os.environ.get('JUPYTER_NOTEBOOK_PASSWORD', 'heroku') # Provide default if not set
        c.ServerApp.password = IPython.lib.passwd(passwd)
    else:
        c.ServerApp.token = ''
        c.ServerApp.password = ''

    ### Make it so the default shell is bash & the prompt is not awful:
    c.ServerApp.terminado_settings = {'shell_command': ['/bin/bash']}

    ### PostresContentsManager ### # DEACTIVATED SECTION
    # database_url = os.getenv('DATABASE_URL', None)
    # if database_url and database_url.startswith("postgres://"):
    #     database_url = database_url.replace("postgres://", "postgresql://", 1)
    # if database_url:
    #     # Tell IPython to use PostgresContentsManager for all storage.
    #     c.ServerApp.contents_manager_class = pgcontents.PostgresContentsManager
    #
    #     # Set the url for the database used to store files.  See
    #     # http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#postgresql
    #     # for more info on db url formatting.
    #     c.PostgresContentsManager.db_url = database_url
    #
    #     # PGContents associates each running notebook server with a user, allowing
    #     # multiple users to connect to the same database without trampling each other's
    #     # notebooks. By default, we use the result of result of getpass.getuser(), but
    #     # a username can be specified manually like so:
    #     c.PostgresContentsManager.user_id = 'heroku'
    #
    #     # Set a maximum file size, if desired.
    #     #c.PostgresContentsManager.max_file_size_bytes = 1000000 # 1MB File cap

except Exception:
    traceback.print_exc()
    # if an exception occues, notebook normally would get started
    # without password set. For security reasons, execution is stopped.
    exit(-1)
