USE heart_attack_db;

-- Remove the procedure if it already exists
DROP PROCEDURE IF EXISTS add_patient_with_test;

DELIMITER $$

CREATE PROCEDURE add_patient_with_test(
    IN p_age INT,
    IN p_gender VARCHAR(10),
    IN p_resting_bp INT,
    IN p_cholesterol INT,
    IN p_fasting_bs BOOLEAN,
    IN p_max_heart_rate INT,
    IN p_exercise_angina BOOLEAN,
    IN p_target BOOLEAN,
    IN t_ecg_result VARCHAR(50),
    IN t_st_depression DECIMAL(5,2),
    IN t_slope INT,
    IN t_num_major_vessels INT,
    IN t_thalassemia VARCHAR(20),
    IN t_recorded_date DATE
)
BEGIN
    -- Step 1: Insert into patients table
    INSERT INTO patients (
        age, gender, resting_bp, cholesterol,
        fasting_bs, max_heart_rate, exercise_angina, target
    )
    VALUES (
        p_age, p_gender, p_resting_bp, p_cholesterol,
        p_fasting_bs, p_max_heart_rate, p_exercise_angina, p_target
    );

    -- Step 2: Get the new patient's ID
    SET @new_patient_id = LAST_INSERT_ID();

    -- Step 3: Insert corresponding test result
    INSERT INTO tests (
        patient_id, ecg_result, st_depression, slope,
        num_major_vessels, thalassemia, recorded_date
    )
    VALUES (
        @new_patient_id, t_ecg_result, t_st_depression, t_slope,
        t_num_major_vessels, t_thalassemia, t_recorded_date
    );
END$$

DELIMITER ;

DELIMITER $$

DROP TRIGGER IF EXISTS after_tests_update $$

CREATE TRIGGER after_tests_update
AFTER UPDATE ON tests
FOR EACH ROW
BEGIN
    -- Only log if st_depression or slope actually changed
    IF OLD.st_depression <> NEW.st_depression OR OLD.slope <> NEW.slope THEN
        INSERT INTO logs (
            test_id,
            patient_id,
            old_st_depression,
            new_st_depression,
            old_slope,
            new_slope,
            action
        )
        VALUES (
            OLD.test_id,
            OLD.patient_id,
            OLD.st_depression,
            NEW.st_depression,
            OLD.slope,
            NEW.slope,
            'UPDATED TEST'
        );
    END IF;
END$$

DELIMITER ;
