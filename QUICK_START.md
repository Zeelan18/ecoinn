## 🚀 QUICK START GUIDE

Get EcoVolt AI running in 60 seconds!

### Option 1: Windows (Easiest)

**Step 1:** Double-click `run.bat`

That's it! The application will:
✅ Install dependencies automatically
✅ Initialize database  
✅ Start the server
✅ Open http://localhost:5000

### Option 2: macOS/Linux

```bash
chmod +x run.sh
./run.sh
```

### Option 3: Manual Setup

```bash
# 1. Install Python 3.7+

# 2. Navigate to project
cd EcoVoltAI

# 3. Create virtual environment (optional)
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py
```

## 🔐 Login

Use these demo credentials:
- **Username:** demo
- **Password:** demo123

Or create a new account!

## 🎯 What to Try

1. **Check Real-Time Data**
   - Dashboard shows live energy status
   - Charts update every 5 seconds

2. **Switch Modes**
   - Click "Urban" or "Rural" buttons
   - See demand and costs change

3. **Simulate Outage**
   - Toggle "Simulate Power Cut"
   - Watch system switch to backup battery
   - Notice alerts and warnings

4. **Toggle Theme**
   - Click 🌙 or ☀️ in top right
   - Switch between dark and light themes

5. **View Analytics**
   - Check daily report at bottom
   - View predictions for next 24 hours
   - Read energy saving tips

## 🔗 URLs

- **Dashboard:** http://localhost:5000/dashboard
- **Login:** http://localhost:5000/login
- **Register:** http://localhost:5000/register
- **API Energy Data:** http://localhost:5000/api/energy-data?mode=Urban

## 🐛 Troubleshooting

**"Port 5000 already in use"**
```bash
# Change port in app.py line 121
app.run(port=5001)
```

**"ModuleNotFoundError: No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**"Database locked"**
```bash
# Delete old database and restart
rm database/db.sqlite3
python app.py
```

## 📚 Full Documentation

See README.md for complete information.

---

**Enjoy your Smart Microgrid System!** ⚡🌍
