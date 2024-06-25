import login
import app
import util

if not util.is_dev_mode():
    login.login_page()
else:
    app.run_app()
