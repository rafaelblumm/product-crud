import login
import app
import util


if not login.is_logged_in() and not util.is_dev_mode():
    login.login_page()
    if login.is_logged_in():
        app.run_app()
else:
    app.run_app()
