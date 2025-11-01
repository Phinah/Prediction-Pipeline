# --- FastAPI + MySQL Connection Setup ---
from fastapi import FastAPI, HTTPException
import mysql.connector

# Create the FastAPI app
app = FastAPI(title="Heart Attack API", version="1.0")

# Database connection function
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",          # keep this if you're using MySQL locally
        user="root",               # your MySQL username
        password="admin123",       # ✅ your real MySQL password
        database="heart_attack_db" # ✅ your confirmed database name
    )
    return connection


# --- A simple test endpoint ---
@app.get("/")
def read_root():
    return {"message": "✅ FastAPI is running and connected to MySQL database heart_attack_db!"}


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
            raise HTTPException(status_code=404, detail=f"⚠️ No patient found with ID {patient_id}")

        return {"message": f"✅ Patient {patient_id} updated successfully"}

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
            raise HTTPException(status_code=404, detail=f"⚠️ No patient found with ID {patient_id}")

        return {"message": f"🗑️ Patient {patient_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
