# TODO: Implement bank simulator
# TODO: Add unit tests for bank simulator
# TODO: Add API docs with curl examples
# TODO: Add docs on how start/run the app
# TODO: Add docs for cloud technologies you’d use and why
# TODO: Add HTTP api tests
# TODO: Add e2e test for the entire flow
# TODO: Add prometheus metrics
# TODO: Add CI/CD pipeline via Github Actions
# TODO: Revisit Logging
# TODO: Lint code
# TODO: Look into making DB operation async
# TODO: Look into making querying rate-limit storage async
# TODO: Possibly add python types
# TODO: Customize Talisman headers
# TODO: Add authentication & authorization
# TODO: Add script to create/bankup/restore db

from app import create_app

app = create_app()

if __name__ == '__main__':
  with app.app_context():
    app.run(debug=True)
