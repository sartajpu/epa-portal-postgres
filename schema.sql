CREATE TABLE web_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    mobile VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    profile_pic VARCHAR(255),
    target_post VARCHAR(100),
    batch_time VARCHAR(50),
    student_height VARCHAR(20),
    student_chest VARCHAR(20),
    running_1600m VARCHAR(20),
    admission_date VARCHAR(50),
    attendance_percent VARCHAR(10)
);
