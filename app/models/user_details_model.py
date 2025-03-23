from psycopg2.extras import RealDictCursor

def get_user_details_with_badges_and_courses(conn, user_id):
    query = """
SELECT 
    u.user_id,
    -- User details aggregated as a single JSON object
    jsonb_build_object(
        'user_id', u.user_id,
        'full_name', u.full_name,
        'phone_number', u.phone_number,
        'age', u.age,
        'gender', u.gender,
        'country', u.country,
        'preferred_language', u.preferred_language,
        'investment_experience_level', u.investment_experience_level,
        'areas_of_interest', u.areas_of_interest,
        'annual_income_range', u.annual_income_range,
        'risk_tolerance', u.risk_tolerance,
        'preferred_investment_duration', u.preferred_investment_duration
    ) AS user_details
FROM 
    user_details AS u
WHERE 
    u.user_id = %s
GROUP BY 
    u.user_id, 
    u.full_name, 
    u.phone_number, 
    u.age, 
    u.gender, 
    u.country, 
    u.preferred_language, 
    u.investment_experience_level, 
    u.areas_of_interest, 
    u.annual_income_range, 
    u.risk_tolerance, 
    u.preferred_investment_duration;
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, (user_id,))
        return cursor.fetchone()





def update_user_details(conn, data):
    with conn.cursor() as cursor:
        # Step 1: Delete the existing user record
        delete_query = """
        DELETE FROM user_details
        WHERE user_id = %(user_id)s
        """
        cursor.execute(delete_query, {'user_id': data['user_id']})

        # Step 2: Insert the new user record
        insert_query = """
        INSERT INTO user_details (
            user_id,
            full_name,
            phone_number,
            age,
            gender,
            country,
            preferred_language,
            investment_experience_level,
            areas_of_interest,
            annual_income_range,
            risk_tolerance,
            preferred_investment_duration
        ) VALUES (
            %(user_id)s,
            %(full_name)s,
            %(phone_number)s,
            %(age)s,
            %(gender)s,
            %(country)s,
            %(preferred_language)s,
            %(investment_experience_level)s,
            %(areas_of_interest)s,
            %(annual_income_range)s,
            %(risk_tolerance)s,
            %(preferred_investment_duration)s
        )
        """
        cursor.execute(insert_query, data)

        # Commit the transaction
        conn.commit()
        return cursor.rowcount > 0
