const express = require('express');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');
const path = require('path');

const app = express();
// Isko paste karein (Ab folder ki zaroorat nahi, files baahar hongi toh bhi chalega)
app.use(express.static(__dirname));
app.use('/css', express.static(path.join(__dirname, 'css')));



// YAHAN PAR PASTE KARNA HAI (Updated Config)
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'MyWebsiteDB', 
  password: 'admin123', 
  port: 5432,
});

// 1. REGISTER ROUTE
app.post('/api/register', async (req, res) => {
  const { username, email, mobile, password } = req.body;
  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    await pool.query(
      'INSERT INTO users (username, email, mobile, password) VALUES ($1, $2, $3, $4)',
      [username, email, mobile, hashedPassword]
    );
    res.status(201).json({ message: "User registered successfully!" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Email/Mobile already exists or server error." });
  }
});

// 2. LOGIN ROUTE
app.post('/api/login', async (req, res) => {
  const { identifier, password } = req.body;
  try {
    const result = await pool.query(
      'SELECT * FROM users WHERE email = $1 OR mobile = $1', 
      [identifier]
    );

    if (result.rows.length === 0) {
      return res.status(400).json({ error: "User not found with this Email/Mobile!" });
    }

    const user = result.rows[0];
    const validPassword = await bcrypt.compare(password, user.password).catch(() => password === user.password);
    
    if (!validPassword) {
      return res.status(400).json({ error: "Invalid password!" });
    }

    res.json({ message: "Login successful", username: user.username });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error during login." });
  }
});

// 3. FORGOT PASSWORD ROUTE
app.post('/api/forgot-password', async (req, res) => {
  const { identifier, newPassword } = req.body;
  try {
    const hashedNewPassword = await bcrypt.hash(newPassword, 10);
    const result = await pool.query(
      'UPDATE users SET password = $1 WHERE email = $2 OR mobile = $2', 
      [hashedNewPassword, identifier]
    );
    
    if (result.rowCount === 0) {
      return res.status(404).json({ error: "No user found with this Email/Mobile!" });
    }
    res.json({ message: "Password updated successfully!" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error during password reset." });
  }
});

// Server Start
app.listen(3000, () => {
  console.log("Server chal raha hai: http://localhost:3000");
});
