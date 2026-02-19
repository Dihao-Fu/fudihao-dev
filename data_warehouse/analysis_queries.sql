-- 1. 设备健康状况分析
SELECT 
    d.device_name,
    d.device_type,
    d.location,
    COUNT(s.timestamp) as reading_count,
    ROUND(AVG(s.temperature), 2) as avg_temp,
    ROUND(MAX(s.temperature), 2) as max_temp,
    ROUND(AVG(s.vibration), 4) as avg_vibration,
    SUM(CASE WHEN s.status = 'WARNING' THEN 1 ELSE 0 END) as warning_count
FROM device_dimension d
JOIN sensor_fact s ON d.device_id = s.device_id
GROUP BY d.device_id, d.device_name, d.device_type, d.location
ORDER BY warning_count DESC;

-- 2. 产品质量分析（按批次）
SELECT 
    batch_id,
    COUNT(*) as total_products,
    SUM(CASE WHEN test_result = 'PASS' THEN 1 ELSE 0 END) as pass_count,
    ROUND(SUM(CASE WHEN test_result = 'PASS' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pass_rate,
    ROUND(AVG(read_speed), 2) as avg_read_speed,
    ROUND(AVG(write_speed), 2) as avg_write_speed
FROM product_quality
GROUP BY batch_id
ORDER BY pass_rate DESC;

-- 3. 预警分析：哪些设备需要维护？
SELECT 
    d.device_name,
    d.location,
    COUNT(CASE WHEN s.temp_category = '危险' THEN 1 END) as danger_temp_count,
    COUNT(CASE WHEN s.vib_category = '严重' THEN 1 END) as severe_vib_count,
    COUNT(CASE WHEN s.status = 'WARNING' THEN 1 END) as total_warnings
FROM device_dimension d
JOIN sensor_fact s ON d.device_id = s.device_id
GROUP BY d.device_id, d.device_name, d.location
HAVING total_warnings > 0
ORDER BY total_warnings DESC;
