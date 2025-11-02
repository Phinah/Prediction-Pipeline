USE heart_attack_db;

DELIMITER //

CREATE TRIGGER log_test_insert
AFTER INSERT ON tests
FOR EACH ROW
BEGIN
  INSERT INTO logs (patient_id, operation)
  VALUES (NEW.patient_id, 'INSERT on tests');
END //

CREATE TRIGGER log_test_update
AFTER UPDATE ON tests
FOR EACH ROW
BEGIN
  INSERT INTO logs (patient_id, operation)
  VALUES (NEW.patient_id, 'UPDATE on tests');
END //

CREATE TRIGGER log_test_delete
AFTER DELETE ON tests
FOR EACH ROW
BEGIN
  INSERT INTO logs (patient_id, operation)
  VALUES (OLD.patient_id, 'DELETE on tests');
END //

DELIMITER ;
