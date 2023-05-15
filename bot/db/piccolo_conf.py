from piccolo.engine.postgres import PostgresEngine


DB = PostgresEngine(config={
    'host': 'localhost',
    'port': 5432,
    'database': 'bot.db',
    'user': 'postgres',
    'password': ''
})