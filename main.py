from website import create_app
from openai import OpenAI

app = create_app()

if(__name__ == '__main__'): # We now have a running web server, but only if this file is run directly
    app.run(debug=True) # run flask application, debug=true means it will automatically rerun when we make a change (turn this off in production)
