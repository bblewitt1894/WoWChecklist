import mysql.connector
import os
import logging
from configs.config import ALLIANCE_FACTIONS, HORDE_FACTIONS
from db.searches import fetch_quests_data, fetch_creature_factions, fetch_object_factions, get_character_guid, get_active_quests, get_completed_quests
from dotenv import load_dotenv
from mysql.connector import Error

logger = logging.getLogger(__name__)


def get_faction_side(reputation_ids: set) -> str:
    has_alliance = any(rep_id in ALLIANCE_FACTIONS for rep_id in reputation_ids)
    has_horde = any(rep_id in HORDE_FACTIONS for rep_id in reputation_ids)

    if has_alliance and not has_horde:
        return "Alliance"
    elif has_horde and not has_alliance:
        return "Horde"
    return "Neutral"


def fetch_quests(faction_filter: str = None):
    load_dotenv()
    wconn = mysql.connector.connect(host=os.getenv('DB_HOST'), port=int(os.getenv('DB_PORT')), user=os.getenv('DB_USER'), password=os.getenv('DB_PASS'), database=os.getenv('DB_WORLDNAME'))
    cursor = wconn.cursor(dictionary=True)
    quests_data = fetch_quests_data(cursor)
    creature_factions = fetch_creature_factions(cursor)
    object_factions = fetch_object_factions(cursor)
    cursor.close()
    wconn.close()

    quests = []
    for q in quests_data:
        qid = q['id']
        rep_ids = set()

        if qid in creature_factions:
            rep_ids.update(fid for fid in creature_factions[qid] if fid is not None)
        if qid in object_factions:
            rep_ids.update(fid for fid in object_factions[qid] if fid is not None)

        side = get_faction_side(rep_ids) if rep_ids else "Neutral"
        q['side'] = side

        if faction_filter is None or side == faction_filter or side == "Neutral":
            quests.append(q)

    return quests


def fetch_character_quests_by_name(char_name):
    cconn = None
    try:
        cconn = mysql.connector.connect(host=os.getenv('DB_HOST'), port=int(os.getenv('DB_PORT')), user=os.getenv('DB_USER'), password=os.getenv('DB_PASS'), database=os.getenv('DB_CHARNAME'))

        cursor = cconn.cursor()

        guid = get_character_guid(cursor, char_name)
        if not guid:
            return set()

        quests = set()

        try:
            quests.update(get_active_quests(cursor, guid))
        except Error:
            pass

        try:
            quests.update(get_completed_quests(cursor, guid))
        except Error:
            pass

        return quests

    except Error as e:
        print(f"MySQL error: {e}")
        return set()
    finally:
        if cconn is not None and cconn.is_connected():
            cconn.close()