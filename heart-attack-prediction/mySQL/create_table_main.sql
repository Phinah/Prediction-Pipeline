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

--  LOGS TABLE
CREATE TABLE IF NOT EXISTS logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    test_id INT,
    patient_id INT,
    old_st_depression DECIMAL(5,2),
    new_st_depression DECIMAL(5,2),
    old_slope INT,
    new_slope INT,
    action VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE
);

-- ============================================
-- Heart Attack DB (aligned to your CSV)
-- ============================================

DROP DATABASE IF EXISTS heart_attack_db;
CREATE DATABASE heart_attack_db;
USE heart_attack_db;

-- ============ Patients ======================
-- One row per person + final label
CREATE TABLE IF NOT EXISTS patients (
    patient_id   INT AUTO_INCREMENT PRIMARY KEY,
    age          INT NOT NULL,         -- CSV: Age
    gender       TINYINT(1) NOT NULL,  -- CSV: Gender (1/0)
    result       VARCHAR(10),          -- CSV: Result ('positive'/'negative')
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============ Tests =========================
-- Clinical measures that can repeat over time
CREATE TABLE IF NOT EXISTS tests (
    test_id        INT AUTO_INCREMENT PRIMARY KEY,
    patient_id     INT NOT NULL,
    heart_rate     INT,            -- CSV: Heart rate
    systolic_bp    INT,            -- CSV: Systolic blc
    diastolic_bp   INT,            -- CSV: Diastolic b
    blood_sugar    INT,            -- CSV: Blood sugg
    ck_mb          DECIMAL(6,2),   -- CSV: CK-MB
    troponin       DECIMAL(6,3),   -- CSV: Troponin
    recorded_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tests_patient
      FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
      ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============ Logs ==========================
-- Audit table populated by triggers on tests
CREATE TABLE IF NOT EXISTS logs (
    log_id         INT AUTO_INCREMENT PRIMARY KEY,
    patient_id     INT NOT NULL,
    operation      VARCHAR(50) NOT NULL,  -- e.g., 'INSERT on tests'
    operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_logs_patient
      FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
      ON DELETE CASCADE
) ENGINE=InnoDB;

-- Helpful indexes
CREATE INDEX idx_tests_patient ON tests(patient_id);
CREATE INDEX idx_logs_patient  ON logs(patient_id);