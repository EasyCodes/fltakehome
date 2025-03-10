import os

import psycopg2


PG_HOST = os.getenv('POSTGRES_HOST', 'localhost')
PG_USER = os.getenv('POSTGRES_USER', 'user')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
PG_DB = os.getenv('POSTGRES_DB', 'events')
PG_BATCH_SIZE = os.getenv('POSTGRES_BATCH_SIZE', '1000')


def get_postgres_conn():
    return psycopg2.connect(host=PG_HOST, user=PG_USER, password=PG_PASSWORD, dbname=PG_DB)


def record_results(journey_mappings: list):
    if not journey_mappings:
        return

    # TODO batching
    # if len(journy_mappings) > PG_BATCH_SIZE: ...

    with get_postgres_conn() as conn:
        with conn.cursor() as cursor:
            for journey_map in journey_mappings:
                cursor.executemany(
                    'INSERT INTO mapped_journeys (journey_id, route_id) VALUES (%s, %s)',
                    journey_map
                )
                conn.commit()

