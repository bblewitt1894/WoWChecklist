def fetch_quests_data(cursor):
    cursor.execute("""
        SELECT 
            q.entry AS id,
            q.Title AS name,
            q.QuestLevel,
            q.ZoneOrSort AS zone_id,
            a.name AS zone_name,
            q.RequiredClasses
        FROM quest_template q
        LEFT JOIN area_template a ON q.ZoneOrSort = a.entry
        WHERE q.Title NOT LIKE '%<UNUSED>%'
          AND q.Title NOT LIKE '%<TXT>%'
          AND q.Title NOT LIKE '%<NYI>%'
          AND q.Title NOT LIKE '%<TEST>%'
    """)
    return cursor.fetchall()


def fetch_creature_factions(cursor):
    cursor.execute("""
        SELECT q.entry AS quest_id, ft.faction_id
        FROM quest_template q
        JOIN creature_questrelation cqr ON q.entry = cqr.quest
        JOIN creature_template ct ON cqr.id = ct.entry
        LEFT JOIN faction_template ft ON ct.faction = ft.ID
    """)
    creature_factions = { }
    for row in cursor.fetchall():
        qid = row['quest_id']
        fid = row['faction_id']
        creature_factions.setdefault(qid, set()).add(fid)
    return creature_factions


def fetch_object_factions(cursor):
    cursor.execute("""
        SELECT q.entry AS quest_id, ft.faction_id
        FROM quest_template q
        JOIN gameobject_questrelation gqr ON q.entry = gqr.quest
        JOIN gameobject_template gt ON gqr.id = gt.entry
        LEFT JOIN faction_template ft ON gt.faction = ft.ID
    """)
    object_factions = { }
    for row in cursor.fetchall():
        qid = row['quest_id']
        fid = row['faction_id']
        object_factions.setdefault(qid, set()).add(fid)
    return object_factions