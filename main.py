# --- FastAPI + MySQL Connection Setup ---
from fastapi import FastAPI, HTTPException
import mysql.connector
import Request

# Create the FastAPI app
app = FastAPI(title="Heart Attack Prediction API", version="2.0")

# --- Database connection ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",        # ✅ your MySQL password
        database="heart_attack_db"  # ✅ your database
    )

# --- Root endpoint ---
@app.get("/")
def root():
    return {"message": "✅ FastAPI is running and connected to heart_attack_db!"}

# --- CREATE (POST) ---
@app.post("/patients")
def add_patient(age: int, gender: int, result: str,
                heart_rate: int, systolic_bp: int, diastolic_bp: int,
                blood_sugar: int, ck_mb: float, troponin: float):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert patient
        cursor.execute(
            "INSERT INTO patients (age, gender, result) VALUES (%s, %s, %s)",
            (age, gender, result)
        )
        patient_id = cursor.lastrowid

        # Insert test
        cursor.execute("""
            INSERT INTO tests (patient_id, heart_rate, systolic_bp, diastolic_bp,
                               blood_sugar, ck_mb, troponin)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (patient_id, heart_rate, systolic_bp, diastolic_bp, blood_sugar, ck_mb, troponin))

        conn.commit()
        return {"message": f"✅ Added patient {patient_id} successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# --- READ (GET) ---
@app.get("/patients")
def get_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# --- UPDATE (PUT) ---
@app.put("/tests/{test_id}")
def update_test(test_id: int,
                heart_rate: int, systolic_bp: int, diastolic_bp: int,
                blood_sugar: int, ck_mb: float, troponin: float):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        update_query = """
            UPDATE tests
            SET heart_rate = %s,
                systolic_bp = %s,
                diastolic_bp = %s,
                blood_sugar = %s,
                ck_mb = %s,
                troponin = %s
            WHERE test_id = %s
        """
        cursor.execute(update_query, (heart_rate, systolic_bp, diastolic_bp, blood_sugar, ck_mb, troponin, test_id))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"⚠️ No test found with ID {test_id}")

        return {"message": f"🧾 Test {test_id} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# --- DELETE (DELETE) ---
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"⚠️ No patient found with ID {patient_id}")

        return {"message": f"🗑️ Patient {patient_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# --- EXTRA: Fetch Latest Test Entry (Task 3 preparation) ---
@app.get("/tests/latest")
def get_latest_test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tests ORDER BY recorded_date DESC LIMIT 1")
        latest = cursor.fetchone()
        if not latest:
            raise HTTPException(status_code=404, detail="No test records found")
        return latest
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@app.post("/patients/")
def create_patient(request: Request):
    try:
        data = request.json()  # read JSON body

        conn = get_db_connection()
        cursor = conn.cursor()

        # Call stored procedure
        cursor.callproc('add_patient_with_test', (
            data["age"], data["gender"], data["resting_bp"], data["cholesterol"],
            data["fasting_bs"], data["max_heart_rate"], data["exercise_angina"],
            data["target"], data["ecg_result"], data["st_depression"], data["slope"],
            data["num_major_vessels"], data["thalassemia"], data["recorded_date"]
        ))
        conn.commit()

        return {"message": "✅ Patient and test record added successfully"}

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
            raise HTTPException(status_code=404, detail=f"⚠️ Patient ID {patient_id} not found")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
