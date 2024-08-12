from pymongo import MongoClient

def setup_db(config):
    client = MongoClient(config['db_uri'])
    shows_db = client.get_default_database("shows")

    raw_coll = shows_db.raw
    raw_coll.create_index("id", unique=True)
    raw_coll.create_index("last_update")

    enriched_coll = shows_db.enriched
    enriched_coll.create_index("id", unique=True)
    enriched_coll.create_index("last_update")