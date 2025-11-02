# --- FastAPI + MySQL Connection Setup ---
from fastapi import FastAPI, HTTPException, Request, Body
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

# Create the FastAPI app
app = FastAPI(title="Heart Attack API", version="1.0")
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST","localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

    return connection


# --- A simple test endpoint ---
@app.get("/")
def read_root():
    return {"message": "FastAPI is running and connected to MySQL database heart_attack_db!"}


# --- UPDATE (PUT) endpoint ---
@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: int,
    age: int,
    gender: str,
    resting_bp: int,
    cholesterol: int,
    fasting_bs: int,
    max_heart_rate: int,
    exercise_angina: int,
    target: int
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        update_query = """
            UPDATE Patients
            SET age = %s,
                gender = %s,
                resting_bp = %s,
                cholesterol = %s,
                fasting_bs = %s,
                max_heart_rate = %s,
                exercise_angina = %s,
                target = %s
            WHERE patient_id = %s
        """
        cursor.execute(update_query, (
            age, gender, resting_bp, cholesterol, fasting_bs,
            max_heart_rate, exercise_angina, target, patient_id
        ))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"No patient found with ID {patient_id}")

        return {"message": f"Patient {patient_id} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


#  Delete (DELETE) endpoint for removing patients

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        delete_query = "DELETE FROM Patients WHERE patient_id = %s"
        cursor.execute(delete_query, (patient_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"No patient found with ID {patient_id}")

        return {"message": f"🗑️ Patient {patient_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

# --- CREATE (POST) endpoint ---
@app.post("/patients/")
def create_patient(
    age: int = Body(...),
    gender: str = Body(...),
    resting_bp: int = Body(...),
    cholesterol: int = Body(...),
    fasting_bs: int = Body(...),
    max_heart_rate: int = Body(...),
    exercise_angina: int = Body(...),
    target: int = Body(...)
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO patients (
                age, gender, resting_bp, cholesterol, fasting_bs,
                max_heart_rate, exercise_angina, target
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            age, gender, resting_bp, cholesterol, fasting_bs,
            max_heart_rate, exercise_angina, target
        ))
        conn.commit()

        new_id = cursor.lastrowid

        return {
            "message": "Patient record created successfully",
            "patient_id": new_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@app.get("/patients/{patient_id}")
def read_patient(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT p.*, t.*
            FROM patients p
            LEFT JOIN tests t ON p.patient_id = t.patient_id
            WHERE p.patient_id = %s
        """
        cursor.execute(query, (patient_id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail=f"Patient ID {patient_id} not found")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@app.get("/patients")
def get_all_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Retrieve all patients, optionally joined with test info
        query = """
            SELECT 
                p.patient_id, p.age, p.gender, p.resting_bp, p.cholesterol,
                p.fasting_bs, p.max_heart_rate, p.exercise_angina, p.target,
                p.created_at,
                t.test_id, t.ecg_result, t.st_depression, t.slope,
                t.num_major_vessels, t.thalassemia, t.recorded_date
            FROM patients p
            LEFT JOIN tests t ON p.patient_id = t.patient_id
            ORDER BY p.patient_id ASC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return {"message": "No patients found in the database."}

        return {"total_patients": len(results), "data": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
