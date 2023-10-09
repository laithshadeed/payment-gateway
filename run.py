# TODO: Implement bank simulator
# TODO: Add API keys so we can map it into marchant ID
# TODO: Derive aquring bank from credit-card information
# TODO: Add table for marchants
# TODO: Add table for API keys
# TODO: Add table for aquiring banks
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
# TODO: Look into hitting bank API async
# TODO: Look into making querying rate-limit storage async
# TODO: Possibly add python types
# TODO: Customize Talisman headers
# TODO: Add script to create/bankup/restore db
# TODO: Look into encrypting sensitive data
# TODO: Look into adding a cache layer for retrieving payments
# TODO: Look into securing the app with TLS
# TODO: Looking into adding a queue for processing payments
# TODO: Look into securing write/read operations to the DB
# TODO: Benchmark the app under high load for cpu/memory/disk/network

from app import create_app

app = create_app()

if __name__ == '__main__':
  with app.app_context():
    app.run(debug=True)
