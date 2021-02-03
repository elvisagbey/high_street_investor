from app.main import main


@main.app_errorhandler(404)
def not_found():
    return "Page Not Found", 404
