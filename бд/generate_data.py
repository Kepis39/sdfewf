import psycopg2
import time
from faker import Faker
import random

# Initialize Faker with Russian locale
fake = Faker('ru_RU')

def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            conn = psycopg2.connect(
                dbname="mydb",
                user="myuser",
                password="mypassword",
                host="db",
                port="5432"
            )
            return conn
        except psycopg2.OperationalError:
            print("Database not ready yet, waiting...")
            time.sleep(2)
            retries -= 1
    raise Exception("Could not connect to the database")

def main():
    conn = wait_for_db()
    cursor = conn.cursor()
    
    print("Generating 1001 records...")
    
    for _ in range(1001):
        # Generate gender-specific data to keep names consistent
        gender_code = random.choice(['male', 'female'])
        if gender_code == 'male':
            gender = 'Мужской'
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
            middle_name = fake.middle_name_male()
        else:
            gender = 'Женский'
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()
            middle_name = fake.middle_name_female()
            
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        mobile_phone = fake.phone_number()
        home_phone = fake.phone_number()
        email = fake.ascii_free_email()
        
        # Insert into users
        cursor.execute(
            """
            INSERT INTO users (last_name, first_name, middle_name, mobile_phone, home_phone, birth_date, gender, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (last_name, first_name, middle_name, mobile_phone, home_phone, birth_date, gender, email)
        )
        user_id = cursor.fetchone()[0]
        
        # Generate passport details
        passport_series_number = f"{random.randint(10, 99)} {random.randint(10, 99)} {random.randint(100000, 999999)}"
        issue_date = fake.date_between(start_date=birth_date, end_date='now')
        department_code = f"{random.randint(100, 999)}-{random.randint(100, 999)}"
        issued_by = f"УМВД РОССИИ ПО {fake.region().upper()}"
        birth_address = fake.address()
        actual_address = fake.address()
        has_foreign_passport = random.choice([True, False])
        
        # Insert into passports
        cursor.execute(
            """
            INSERT INTO passports (user_id, passport_series_number, last_name, first_name, middle_name, birth_date, issue_date, department_code, issued_by, birth_address, actual_address, has_foreign_passport)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (user_id, passport_series_number, last_name, first_name, middle_name, birth_date, issue_date, department_code, issued_by, birth_address, actual_address, has_foreign_passport)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Successfully populated 1001 records!")

if __name__ == '__main__':
    main()
