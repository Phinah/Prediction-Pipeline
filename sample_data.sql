USE heart_attack_db;

-- Insert sample patients
INSERT INTO patients (age, gender, resting_bp, cholesterol, fasting_bs, max_heart_rate, exercise_angina, target)
VALUES
(63, 'M', 145, 233, TRUE, 150, FALSE, TRUE),
(67, 'F', 160, 286, TRUE, 108, TRUE, TRUE),
(37, 'M', 130, 250, FALSE, 187, FALSE, FALSE),
(41, 'F', 130, 204, FALSE, 172, FALSE, FALSE),
(56, 'M', 120, 236, TRUE, 178, FALSE, TRUE);

-- Insert sample test results
INSERT INTO tests (patient_id, ecg_result, st_depression, slope, num_major_vessels, thalassemia, recorded_date)
VALUES
(1, 'Normal', 2.3, 2, 0, 'Normal', '2025-10-31'),
(2, 'ST-T abnormality', 1.4, 1, 1, 'Fixed defect', '2025-10-31'),
(3, 'LV hypertrophy', 0.0, 2, 0, 'Normal', '2025-10-31'),
(4, 'Normal', 1.0, 2, 2, 'Reversible defect', '2025-10-31'),
(5, 'ST-T abnormality', 3.4, 3, 0, 'Normal', '2025-10-31');
