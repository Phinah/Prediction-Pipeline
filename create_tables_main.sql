-- CREATE MAIN TABLES FOR HEART ATTACK DATABASE
DROP DATABASE IF EXISTS heart_attack_db;
CREATE DATABASE heart_attack_db;
USE heart_attack_db;

--  PATIENTS TABLE
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    resting_bp INT,
    cholesterol INT,
    fasting_bs BOOLEAN,
    max_heart_rate INT,
    exercise_angina BOOLEAN,
    target BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

--  TESTS TABLE
CREATE TABLE IF NOT EXISTS tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    ecg_result VARCHAR(50),
    st_depression DECIMAL(5,2),
    slope INT,
    num_major_vessels INT,
    thalassemia VARCHAR(20),
    recorded_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
) ENGINE=InnoDB;
