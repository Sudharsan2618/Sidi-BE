from psycopg2.extras import RealDictCursor
from datetime import datetime

def get_population_data_for_current_year(conn):
    current_year = datetime.now().year
    query = """
     
SELECT 
    cc.country_name, 
    cc.country_iso_code, 
    COALESCE(phm.country_share_of_world_population, 0) AS country_share_of_world_population
FROM 
    sidi_population_master.country_code AS cc
LEFT JOIN 
    sidi_population_master.country_master AS cm 
ON 
    cm.country_name = cc.country_name
LEFT JOIN 
    sidi_population_master.population_historical_master AS phm 
ON 
    phm.country_id = cm.country_id 
    AND phm.year = 2024;
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, (current_year,))
        return cursor.fetchall()
