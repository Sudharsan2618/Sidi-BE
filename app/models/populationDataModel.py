from psycopg2.extras import RealDictCursor

def get_population_data(conn, country_name):
    query = """
        SELECT 
            population.country_id, 
            population.year, 
            c.country_name, 
            population.yearly_percentage_change, 
            population.country_global_rank 
        FROM 
            sidi_population_master.population_historical_master AS population
        JOIN 
            sidi_population_master.country_master AS c 
        ON 
            c.country_id = population.country_id
        WHERE 
            TRIM(REGEXP_REPLACE(LOWER(c.country_name), '\s+', ' ', 'g')) = 
            TRIM(REGEXP_REPLACE(LOWER(%s), '\s+', ' ', 'g'))
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, (country_name,))
        return cursor.fetchall()
