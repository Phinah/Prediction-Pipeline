USE heart_attack_db;

-- Drop and recreate for clean reruns
DROP TABLE IF EXISTS logs;

CREATE TABLE IF NOT EXISTS logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    operation VARCHAR(50) NOT NULL,       -- e.g., 'INSERT on tests'
    operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_logs_patient
      FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
      ON DELETE CASCADE
) ENGINE=InnoDB;
