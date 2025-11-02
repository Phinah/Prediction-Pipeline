USE heart_attack_db;

-- Remove the procedure if it already exists
DROP PROCEDURE IF EXISTS add_patient_with_test;

DELIMITER $$

CREATE PROCEDURE add_patient_with_test(
    IN p_age INT,
    IN p_gender TINYINT(1),
    IN p_result VARCHAR(10),
    IN t_heart_rate INT,
    IN t_systolic_bp INT,
    IN t_diastolic_bp INT,
    IN t_blood_sugar INT,
    IN t_ck_mb DECIMAL(6,2),
    IN t_troponin DECIMAL(6,3)
)
BEGIN
    -- Step 1: Insert into patients table
    INSERT INTO patients (age, gender, result)
    VALUES (p_age, p_gender, p_result);

    -- Step 2: Get the new patient's ID
    SET @new_patient_id = LAST_INSERT_ID();

    -- Step 3: Insert corresponding test result
    INSERT INTO tests (
        patient_id, heart_rate, systolic_bp, diastolic_bp,
        blood_sugar, ck_mb, troponin
    )
    VALUES (
        @new_patient_id, t_heart_rate, t_systolic_bp, t_diastolic_bp,
        t_blood_sugar, t_ck_mb, t_troponin
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
