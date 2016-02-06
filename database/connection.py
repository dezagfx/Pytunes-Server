from sqlalchemy import create_engine
from database import config

connection_string = str(
                'mysql+pymysql://' + config.db_user + ':' +
                config.db_pass + '@' + config.db_host + '/' +
                config.db_name
                    )
engine = create_engine(connection_string, echo=False)
connection = engine.connect()
