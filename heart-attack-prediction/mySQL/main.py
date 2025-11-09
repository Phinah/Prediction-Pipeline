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


# A simple test endpoint 
@app.get("/")
def read_root():
    return {"message": "FastAPI is running and connected to MySQL database heart_attack_db!"}

# UPDATE (PUT) endpoint
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

# CREATE (POST) endpoint
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

# UPDATE (PUT) endpoint
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

        return {"message": f"Test {test_id} updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# GET LATEST ENTRY endpoint for predict.py
@app.get("/api/latest-entry")
def get_latest_entry():
    """
    Fetch the latest test record with patient info for prediction.
    This endpoint combines data from patients and tests tables.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get the latest test with its corresponding patient data
        query = """
            SELECT 
                p.patient_id, p.age, p.gender, p.result,
                t.test_id, t.heart_rate, t.systolic_bp, t.diastolic_bp,
                t.blood_sugar, t.ck_mb, t.troponin, t.recorded_date
            FROM tests t
            JOIN patients p ON t.patient_id = p.patient_id
            ORDER BY t.recorded_date DESC, t.test_id DESC
            LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="No test records found in database")

        # Format response to match MongoDB structure for predict.py compatibility
        response = {
            "patient": {
                "patient_id": result["patient_id"],
                "age": result["age"],
                "gender": result["gender"]
            },
            "medical_record": {
                "heart_rate": result["heart_rate"],
                "systolic_blood_pressure": result["systolic_bp"],
                "diastolic_blood_pressure": result["diastolic_bp"],
                "blood_sugar": result["blood_sugar"]
            },
            "heart_attack_test": {
                "test_id": result["test_id"],
                "ck_mb": float(result["ck_mb"]),
                "troponin": float(result["troponin"]),
                "result": result["result"] if result["result"] else "unknown"
            }
        }

        return response

    except mysql.connector.Error as db_err:
        raise HTTPException(status_code=500, detail=f"Database error: {str(db_err)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)