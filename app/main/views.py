from app.main import main


@main.route('/', methods=['GET'])
def index():
    return '<h1>Hello High street investor</h1>'
