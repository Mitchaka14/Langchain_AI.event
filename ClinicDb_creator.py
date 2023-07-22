import sqlite3
from sqlite3 import Error
from datetime import datetime


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_patient(conn, patient):
    # Ensure the dob is not in the future
    dob = datetime.strptime(patient[2], "%m-%d-%Y")
    if dob.date() > datetime.now().date():
        print(f"Error: Date of birth for patient {patient[1]} is in the future.")
        return

    sql = """ INSERT OR ABORT INTO patients(id, name, dob, address, insurance_info)
              VALUES(?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, patient)
    return cur.lastrowid


def create_appointment(conn, appointment):
    sql = """ INSERT OR ABORT INTO appointments(patient_id, appointment_date, appointment_type, employee_id)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, appointment)


def create_appointment_type(conn, appointment_type):
    sql = """ INSERT OR ABORT INTO appointment_types(type)
              VALUES(?) """
    cur = conn.cursor()
    cur.execute(sql, appointment_type)


def create_billing(conn, billing):
    sql = """ INSERT OR ABORT INTO billing(patient_id, amount_due)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, billing)


def create_prescription(conn, prescription):
    sql = """ INSERT OR ABORT INTO prescriptions(patient_id, medication)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, prescription)


def create_test(conn, test):
    sql = """ INSERT OR ABORT INTO tests(patient_id, test_results)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, test)


def create_complaint(conn, complaint):
    sql = """ INSERT OR ABORT INTO complaints(patient_id, complaint_text)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, complaint)


def create_referral(conn, referral):
    sql = """ INSERT OR ABORT INTO referrals(patient_id, referral_text)
              VALUES(?,?) """
    cur = conn.cursor()
    cur.execute(sql, referral)


def create_employee(conn, employee):
    sql = """ INSERT OR ABORT INTO employees(name)
              VALUES(?) """
    cur = conn.cursor()
    cur.execute(sql, employee)
    return cur.lastrowid


def create_employee_availability(conn, availability):
    sql = """ INSERT OR ABORT INTO employee_availability(employee_id, day, start_time, end_time)
              VALUES(?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, availability)


def create_interaction(conn, interaction):
    sql = """ INSERT OR ABORT INTO interactions(patient_id, employee_id, interaction_date)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, interaction)


def main():
    database = "ClinicDb.db"

    sql_create_patients_table = """ CREATE TABLE IF NOT EXISTS patients (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        dob text NOT NULL,
                                        address text NOT NULL,
                                        insurance_info text UNIQUE
                                    ); """

    sql_create_appointment_types_table = """ CREATE TABLE IF NOT EXISTS appointment_types (
                                                id integer PRIMARY KEY,
                                                type text NOT NULL UNIQUE
                                            ); """

    sql_create_employees_table = """ CREATE TABLE IF NOT EXISTS employees (
                                         id integer PRIMARY KEY,
                                         name text NOT NULL
                                     ); """

    sql_create_employee_availability_table = """ CREATE TABLE IF NOT EXISTS employee_availability (
                                                     id integer PRIMARY KEY,
                                                     employee_id integer NOT NULL,
                                                     day text NOT NULL,
                                                     start_time text NOT NULL,
                                                     end_time text NOT NULL,
                                                     FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE
                                                 ); """

    sql_create_appointments_table = """ CREATE TABLE IF NOT EXISTS appointments (
                                            id integer PRIMARY KEY,
                                            patient_id integer NOT NULL,
                                            appointment_date text NOT NULL,
                                            appointment_type integer,
                                            employee_id integer,
                                            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE,
                                            FOREIGN KEY (appointment_type) REFERENCES appointment_types (id) ON DELETE SET NULL,
                                            FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE SET NULL
                                        ); """

    sql_create_billing_table = """ CREATE TABLE IF NOT EXISTS billing (
                                        id integer PRIMARY KEY,
                                        patient_id integer NOT NULL,
                                        amount_due real NOT NULL CHECK (amount_due >= 0),
                                        FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                                    ); """

    sql_create_prescriptions_table = """ CREATE TABLE IF NOT EXISTS prescriptions (
                                            id integer PRIMARY KEY,
                                            patient_id integer NOT NULL,
                                            medication text NOT NULL,
                                            FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                                        ); """

    sql_create_tests_table = """ CREATE TABLE IF NOT EXISTS tests (
                                    id integer PRIMARY KEY,
                                    patient_id integer NOT NULL,
                                    test_results text,
                                    FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                                ); """

    sql_create_complaints_table = """ CREATE TABLE IF NOT EXISTS complaints (
                                        id integer PRIMARY KEY,
                                        patient_id integer NOT NULL,
                                        complaint_text text NOT NULL,
                                        FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                                    ); """

    sql_create_referrals_table = """ CREATE TABLE IF NOT EXISTS referrals (
                                        id integer PRIMARY KEY,
                                        patient_id integer NOT NULL,
                                        referral_text text NOT NULL,
                                        FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                                    ); """

    sql_create_interactions_table = """ CREATE TABLE IF NOT EXISTS interactions (
                                           id integer PRIMARY KEY,
                                           patient_id integer NOT NULL,
                                           employee_id integer NOT NULL,
                                           interaction_date text NOT NULL,
                                           FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE,
                                           FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE
                                       ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_patients_table)
        create_table(conn, sql_create_appointment_types_table)
        create_table(conn, sql_create_employees_table)
        create_table(conn, sql_create_employee_availability_table)
        create_table(conn, sql_create_appointments_table)
        create_table(conn, sql_create_billing_table)
        create_table(conn, sql_create_prescriptions_table)
        create_table(conn, sql_create_tests_table)
        create_table(conn, sql_create_complaints_table)
        create_table(conn, sql_create_referrals_table)
        create_table(conn, sql_create_interactions_table)
    else:
        print("Error! Cannot create the database connection.")

    with conn:
        # create employees
        employees = [
            ("Dr. John Doe",),
            ("Dr. Jane Doe",),
            ("Nurse James Smith",),
            ("Nurse Mary Johnson",),
        ]

        for employee in employees:
            employee_id = create_employee(conn, employee)

            # create related data for each employee
            # 10am to 5pm from Monday to Friday
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                create_employee_availability(conn, (employee_id, day, "10:00", "17:00"))

        # create patients
        patients = [
            (1, "Naruto Uzumaki", "10-10-1980", "Konoha", "Insurance1"),
            (2, "Sasuke Uchiha", "07-23-1981", "Konoha", "Insurance2"),
            (3, "Monkey D. Luffy", "05-05-1982", "Grand Line", "Insurance3"),
            (4, "John Doe", "01-01-1983", "Address4", "Insurance4"),
            (5, "Jane Doe", "02-02-1984", "Address5", "Insurance5"),
            (6, "Tom Cruise", "07-03-1962", "Hollywood", "Insurance6"),
            (7, "Elon Musk", "06-28-1971", "Los Angeles", "Insurance7"),
            (8, "Taylor Swift", "12-13-1989", "Nashville", "Insurance8"),
            (9, "LeBron James", "12-30-1984", "Los Angeles", "Insurance9"),
            (10, "Oprah Winfrey", "01-29-1954", "Chicago", "Insurance10"),
        ]

        for patient in patients:
            patient_id = create_patient(conn, patient)

            # create related data for each patient
            # for simplicity, assume all patients are seen by the first employee (Dr. John Doe)
            create_appointment(conn, (patient_id, "2023-12-01", 1, 1))
            create_billing(conn, (patient_id, 100.00))
            create_prescription(conn, (patient_id, "Medication1"))
            create_test(conn, (patient_id, "Test results"))
            create_complaint(conn, (patient_id, "Complaint1"))
            create_referral(conn, (patient_id, "Referral1"))

            # create an interaction record
            create_interaction(conn, (patient_id, 1, "2023-12-01"))


if __name__ == "__main__":
    main()
