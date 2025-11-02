-- 1. DROP EXISTING COMPONENTS TO AVOID ERRORS (Safe Cleanup)
-- Drop trigger and function before dropping the table it uses (Vitals)
DROP TRIGGER IF EXISTS heart_rate_update_trigger ON Vitals;
DROP FUNCTION IF EXISTS log_vitals_changes();
DROP FUNCTION IF EXISTS get_full_patient_profile(p_id INT);

-- Drop tables in dependency order (children first)
DROP TABLE IF EXISTS Labs;
DROP TABLE IF EXISTS Vitals;
DROP TABLE IF EXISTS Audit_Log;
DROP TABLE IF EXISTS Patients; 

-- A. Implement the Schema (4 Tables)

-- 1. Create the core PATIENTS table 
CREATE TABLE Patients (
    patient_id SERIAL PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    result VARCHAR(50) 
);

-- 2. Create the VITALS table
CREATE TABLE Vitals (
    vitals_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    heart_rate INT,
    systolic_blood_pressure INT,
    diastolic_blood_pressure INT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

-- 3. Create the LABS table
CREATE TABLE Labs (
    lab_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    blood_sugar NUMERIC(5, 2),
    ck_mb NUMERIC(5, 2),
    troponin NUMERIC(5, 3),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

-- 4. Create the required Audit Log table for the trigger
CREATE TABLE Audit_Log (
    log_id SERIAL PRIMARY KEY,
    patient_id INT,
    old_hr INT,
    new_hr INT,
    changed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- B. Create One Stored Procedure (Function)
-- Retrieves a patient's full medical profile
CREATE OR REPLACE FUNCTION get_full_patient_profile(p_id INT)
RETURNS TABLE (
    patient_age INT,
    patient_gender VARCHAR,
    hr INT,
    sbp INT,
    dbp INT,
    sugar NUMERIC,
    ckmb NUMERIC,
    troponin NUMERIC,
    ml_result VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.age, p.gender, v.heart_rate, v.systolic_blood_pressure, v.diastolic_blood_pressure,
        l.blood_sugar, l.ck_mb, l.troponin, p.result
    FROM
        Patients p
    LEFT JOIN
        Vitals v ON p.patient_id = v.patient_id
    LEFT JOIN
        Labs l ON p.patient_id = l.patient_id
    WHERE
        p.patient_id = p_id;
END;
$$ LANGUAGE plpgsql;


-- C. Create One Trigger (Logging Changes)

-- 1. Create the Trigger Function (The action to perform)
CREATE OR REPLACE FUNCTION log_vitals_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- This condition logs a change ONLY if the heart_rate value is different
    IF OLD.heart_rate IS DISTINCT FROM NEW.heart_rate THEN
        INSERT INTO Audit_Log (patient_id, old_hr, new_hr)
        VALUES (OLD.patient_id, OLD.heart_rate, NEW.heart_rate);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Create the Trigger itself (The rule that fires the action)
CREATE TRIGGER heart_rate_update_trigger
AFTER UPDATE ON Vitals -- Fires AFTER an UPDATE operation
FOR EACH ROW -- Fires once for every row affected
EXECUTE FUNCTION log_vitals_changes();