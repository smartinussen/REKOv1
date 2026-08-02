import json
import sqlite3

from models import Farm


def create_farm_table():
    conn = sqlite3.connect("reko.db")
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS farms
                 (
                     id                 INTEGER PRIMARY KEY,
                     farm_name          TEXT    NOT NULL,
                     farm_manager       TEXT    NOT NULL,
                     address            TEXT    NOT NULL,
                     city               TEXT    NOT NULL,
                     postal_code        TEXT    NOT NULL,
                     latitude           REAL,
                     longitude          REAL,
                     phone_no           TEXT    NOT NULL,
                     email              TEXT    NOT NULL,
                     website            TEXT,
                     description        TEXT,
                     certifications     TEXT,
                     produce_categories TEXT,
                     reko_markets       TEXT,
                     is_active          INTEGER NOT NULL,
                     created_at         TEXT DEFAULT CURRENT_TIMESTAMP,
                     updated_at         TEXT DEFAULT CURRENT_TIMESTAMP
                 )
    """)
    conn.commit()
    conn.close()


def insert_farm(farm: Farm):
    conn = sqlite3.connect("reko.db")
    cursor = conn.execute(
        """
        INSERT INTO farms (farm_name, farm_manager, address, city, postal_code,
                            latitude, longitude, phone_no, email, website,
                            description, certifications, produce_categories,
                            reko_markets, is_active)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            farm.farm_name,
            farm.farm_manager,
            farm.address,
            farm.city,
            farm.postal_code,
            farm.latitude,
            farm.longitude,
            farm.phone_no,
            farm.email,
            str(farm.website) if farm.website else None,
            farm.description,
            json.dumps(farm.certifications),
            json.dumps(farm.produce_categories),
            json.dumps(farm.reko_markets),
            int(farm.is_active),
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def deserialize_farm(farm):
    farm["certifications"] = json.loads(farm["certifications"])
    farm["produce_categories"] = json.loads(farm["produce_categories"])
    farm["reko_markets"] = json.loads(farm["reko_markets"])
    farm["is_active"] = bool(farm["is_active"])
    return farm


def get_farms():
    conn = sqlite3.connect("reko.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT * FROM farms")
    rows = cursor.fetchall()
    conn.close()
    farms = [dict(row) for row in rows]
    for row in farms:
        deserialize_farm(row)
    return farms


def get_farm_by_id(farm_id: int):
    conn = sqlite3.connect("reko.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT * FROM farms WHERE id = ?", (farm_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    farm = dict(row)
    deserialize_farm(farm)
    return farm


def update_farm(farm_id: int, updates: dict):
    conn = sqlite3.connect("reko.db")
    fields = ", ".join(f"{key} = ?" for key in updates)
    sql = f"UPDATE farms SET {fields}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    converted = {}
    for key, value in updates.items():
        if isinstance(value, (list, dict)):
            value = json.dumps(value)
        elif key == "website":
            value = str(value)
        elif key == "is_active":
            value = int(value)
        converted[key] = value
    values = list(converted.values())
    values.append(farm_id)
    cursor = conn.execute(sql, values)
    conn.commit()
    conn.close()
    return cursor.rowcount != 0
