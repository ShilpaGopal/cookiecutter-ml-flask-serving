from config.config import SERVICE_CONFIG


loglevel = 'info'
bind = '0.0.0.0:' + str(SERVICE_CONFIG['port'])
timeout = 2 * 60  # 2 minutes
workers = SERVICE_CONFIG['workers']
