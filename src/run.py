import login
import app
import util


if not login.is_logged_in() and not util.is_dev_mode():
    login.login_page()
else:
    app.run_app()
