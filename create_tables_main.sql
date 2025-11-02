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
