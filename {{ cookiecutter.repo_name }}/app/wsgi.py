import app as service
from config.config import SERVICE_CONFIG

if __name__ == "__main__":
    service.run(port=SERVICE_CONFIG['port'])
