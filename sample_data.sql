USE heart_attack_db;

-- ============================
-- Insert sample patients
-- ============================
INSERT INTO patients (age, gender, result)
VALUES
(63, 1, 'positive'),
(67, 0, 'positive'),
(37, 1, 'negative'),
(41, 0, 'negative'),
(56, 1, 'positive');

-- ============================
-- Insert sample test results
-- ============================
INSERT INTO tests (patient_id, heart_rate, systolic_bp, diastolic_bp, blood_sugar, ck_mb, troponin)
VALUES
<<<<<<< HEAD
(1, 'Normal', 2.3, 2, 0, 'Normal', '2025-10-31'),
(2, 'ST-T abnormality', 1.4, 1, 1, 'Fixed defect', '2025-10-31'),
(3, 'LV hypertrophy', 0.0, 2, 0, 'Normal', '2025-10-31'),
(4, 'Normal', 1.0, 2, 2, 'Reversible defect', '2025-10-31'),
(5, 'ST-T abnormality', 3.4, 3, 0, 'Normal', '2025-10-31');

SET @p_id = LAST_INSERT_ID();

-- Step 2: Update the test to trigger the log
UPDATE tests
SET st_depression = 3.0, slope = 2
WHERE patient_id = @p_id;

-- Step 3: Check logs table
SELECT * FROM logs;
=======
(1, 150, 145, 90, 130, 2.1, 0.020),
(2, 120, 160, 95, 180, 3.5, 0.035),
(3, 187, 130, 85, 140, 1.8, 0.010),
(4, 172, 120, 80, 100, 1.5, 0.008),
(5, 178, 135, 82, 120, 2.3, 0.025);
>>>>>>> db8d970 (Updated database setup and FastAPI CRUD  added logs table, triggers, sample data, and stored procedure)
