# EcoVolt AI - Smart Microgrid System

A production-ready, comprehensive web application for AI-powered energy optimization in rural and urban environments.

## 🚀 Features

- **🔐 Authentication System**: Secure login/register with Flask sessions
- **⚡ Real-time Energy Monitoring**: Live solar, battery, and grid data simulation
- **🧠 AI Optimization Logic**: Intelligent energy source selection using priority algorithms
- **📊 Analytics Dashboard**: Beautiful charts and real-time visualizations with Chart.js
- **🌍 Dual Mode Support**: Urban and Rural energy management modes
- **🔴 Outage Simulation**: Test system resilience with grid outage simulation
- **💰 Cost Tracking**: Monitor savings and energy costs in real-time
- **📈 Predictions**: 24-hour energy demand forecasting
- **🎨 Dark/Light Theme**: Toggle between themes with smooth transitions
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## 📋 System Requirements

- Python 3.7+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 50MB free disk space

## 🔧 Installation Guide

### Step 1: Clone/Download Project

```bash
# Navigate to project directory
cd EcoVoltAI
```

### Step 2: Create Virtual Environment (Optional but Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (Web framework)
- Werkzeug (Security utilities)
- Jinja2 (Template engine)
- And all required supporting libraries

### Step 4: Initialize Database

The database will be automatically created on first run. No manual setup needed!

## ▶️ Running the Application

### Start the Server

```bash
python app.py
```

Expected output:
```
============================================================
EcoVolt AI - Smart Microgrid System
============================================================
Starting Flask application...
Access the application at: http://localhost:5000
============================================================
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

### Demo Credentials

For testing, use:
- **Username**: `demo`
- **Password**: `demo123`

Or create a new account by clicking "Create account" on the login page.

## 📂 Project Structure

```
EcoVoltAI/
├── app.py                 # Main Flask application
├── ai_optimizer.py        # AI optimization logic
├── db_init.py            # Database initialization
├── requirements.txt      # Python dependencies
│
├── /templates
│   ├── login.html        # Login/Register page
│   └── dashboard.html    # Main dashboard
│
├── /static
│   ├── style.css         # Styling with dark/light theme
│   └── script.js         # Dashboard functionality
│
└── /database
    └── db.sqlite3        # SQLite database (created automatically)
```

## 🎯 Key Features Explained

### 1. Authentication System
- Secure password hashing with Werkzeug
- Session-based user authentication
- User registration with validation
- Auto-logout functionality

### 2. Real-time Energy Data
- **Solar Generation**: Time-based simulation (peak at noon)
- **Battery Storage**: Current charge and charging status
- **Grid Supply**: Connection status and availability
- **Demand**: Dynamic load based on mode and time

### 3. AI Optimization Logic
The system uses intelligent algorithms to select the best energy source:

**Priority Order:**
1. **Solar** - When generation > 80% of demand
2. **Battery** - When charged above 20% threshold
3. **Solar + Battery** - Hybrid when both available
4. **Grid** - Fallback when available
5. **Emergency Battery** - During outages

**Decision Factors:**
- Current solar generation
- Battery charge level
- Demand requirements
- Grid availability
- Time of day patterns
- Historical usage data

### 4. Dashboard Features

#### Real-Time Status Cards
- Solar power generation with efficiency
- Battery state of charge and charging status
- Grid connection status
- Current energy demand

#### AI Optimization Display
- Selected energy source with recommendation
- Efficiency percentage
- Hourly cost calculation
- Savings compared to grid

#### Analytics Charts
- **Daily Usage**: Line chart showing 24-hour pattern
- **Source Distribution**: Pie/Doughnut chart breakdown
- **24-Hour Predictions**: Bar chart forecast

#### Energy Reports
- Total energy consumed
- Total cost incurred
- Total savings achieved
- Average hourly demand

#### Smart Alerts
- Battery low warning (< 20%)
- Power outage notification
- Recommendations for optimization

### 5. Mode Selection

**Urban Mode:**
- Higher energy demand (1000-3000W baseline)
- More grid availability
- Solar efficiency: 85%
- Cost: $0.12/kWh

**Rural Mode:**
- Lower energy demand (300-1000W baseline)
- Less grid availability
- Solar efficiency: 75%
- Cost: $0.15/kWh

### 6. Outage Simulation
- Toggle "Simulate Power Cut" to test backup systems
- Grid becomes unavailable
- System automatically switches to battery/solar
- Displays critical alerts
- Shows emergency operations status

## 🧠 AI Optimization Engine

The AI optimizer analyzes multiple factors:

```python
Decision Logic:
├── Solar Available?
│   ├── Yes, > 80% demand → Use Solar
│   └── No → Check Battery
├── Battery Charged?
│   ├── Yes, > 20% → Use Battery
│   └── No → Check Hybrid
├── Can Hybrid Work?
│   ├── Yes → Use Solar+Battery
│   └── No → Check Grid
└── Grid Available?
    ├── Yes → Use Grid
    └── No → Emergency Mode
```

### Prediction Model
Uses historical data to forecast:
- Next 24 hours demand patterns
- Peak usage times
- Optimal charging windows
- Seasonal adjustments

## 📱 Responsive Design

The application is fully responsive:

**Desktop (1024px+)**
- Full dashboard with sidebar
- Multi-column layouts
- Expanded charts

**Tablet (768px-1023px)**
- Stacked layouts
- Mobile-optimized menus
- Touch-friendly buttons

**Mobile (< 768px)**
- Single column layout
- Compact cards
- Simplified navigation

## 🎨 Theme System

### Dark Theme
- Eye-friendly for night usage
- Reduced blue light
- Better battery life on OLED

### Light Theme
- High contrast for daytime
- Professional appearance
- Better readability in sunlight

Theme persists using localStorage.

## 🔌 API Endpoints

### Authentication
- `GET /` - Redirect to login/dashboard
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /register` - Register page
- `POST /register` - Create account
- `GET /logout` - Logout user

### Dashboard
- `GET /dashboard` - Main dashboard (requires login)

### API Endpoints
- `GET /api/energy-data` - Real-time energy data
- `POST /api/optimize` - AI optimization decision
- `GET /api/daily-report` - Daily statistics
- `GET /api/tips` - Energy saving tips
- `GET /api/predictions` - 24-hour predictions
- `GET /api/health-check` - System health status

## 🔒 Security Features

- Secure password hashing with Werkzeug
- CSRF protection via Flask sessions
- SQL injection prevention with parameterized queries
- XSS protection through Jinja2 templating
- Session timeout on logout
- Secure cookie handling

## 📊 Database Schema

### Tables Created Automatically

**users**
- id, username, email, password_hash
- Stores user credentials and metadata

**energy_usage**
- id, user_id, source, amount, mode, timestamp
- Records every energy decision and usage

**alerts**
- id, user_id, alert_type, message, severity
- Stores system alerts and notifications

**daily_reports**
- id, user_id, date, total_energy, total_cost, total_savings
- Aggregated daily statistics

**system_config**
- id, user_id, solar_max, battery_capacity, etc.
- User preferences and system settings

**predictions**
- id, user_id, hour, predicted_demand, confidence
- Energy forecasts

## 🚀 Performance

- Auto-refresh every 5 seconds
- Lazy loading of charts
- Optimized SQL queries with indexes
- Responsive rendering with CSS animations
- Efficient data compression

## 🧪 Testing the System

### Test Scenarios

1. **Normal Operation**
   - Login with demo credentials
   - Observe real-time energy flow
   - Check AI recommendations

2. **Power Outage**
   - Enable "Simulate Power Cut"
   - Watch system switch to battery
   - Observe alerts and warnings

3. **Mode Switching**
   - Toggle between Urban and Rural
   - Notice demand/cost changes
   - Compare efficiency

4. **Theme Toggle**
   - Click moon icon
   - Observe dark theme activation
   - Switch back to light

5. **Data Analysis**
   - Monitor daily report
   - Review prediction accuracy
   - Check savings calculations

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
```bash
# Change port in app.py
# Find line: app.run(port=5000, ...)
# Change to: app.run(port=5001, ...)
```

### Issue: Database locked
```bash
# Delete database and restart
rm database/db.sqlite3
python app.py
```

### Issue: Module not found
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: Charts not rendering
```bash
# Clear browser cache (Ctrl+Shift+Delete)
# Refresh page (Ctrl+F5)
```

## 📈 Optimization Tips

1. **For Better Predictions**: System learns from historical data - use for 7+ days
2. **For High Efficiency**: Keep battery between 20-90% charge
3. **For Cost Savings**: Shift loads to peak solar hours (10 AM - 4 PM)
4. **For Reliability**: Maintain battery health and regular maintenance

## 🔄 Updates & Maintenance

The application automatically:
- Initializes database on first run
- Creates demo user account
- Manages session cleanup
- Logs all operations for debugging

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review console logs (browser F12)
3. Check server terminal output
4. Verify all files are in correct locations

## 📄 License

This project is provided as-is for educational and commercial use.

## 🎓 Learning Resources

### Built With
- **Flask**: Lightweight Python web framework
- **SQLite**: Embedded relational database
- **Chart.js**: Beautiful charting library
- **CSS3**: Modern styling with variables and animations
- **Vanilla JavaScript**: No external dependencies

### Key Concepts Implemented
- MVC Architecture
- RESTful API design
- Database normalization
- Session management
- Responsive web design
- Progressive enhancement
- Error handling

## 🌱 Future Enhancements

Potential additions:
- Real hardware integration (Raspberry Pi)
- Machine learning with TensorFlow
- Weather API integration
- Mobile app (React Native)
- Real IoT device support
- Advanced analytics with pandas
- Email notifications
- Export to PDF/Excel

## ✅ Verification Checklist

Before deployment, verify:
- [ ] All files present in correct directories
- [ ] requirements.txt has all dependencies
- [ ] Database initializes without errors
- [ ] Login/Register functionality works
- [ ] Dashboard loads with data
- [ ] Charts render correctly
- [ ] Theme toggle works
- [ ] Mode selection updates UI
- [ ] Outage simulation activates
- [ ] API endpoints respond with JSON
- [ ] Auto-refresh works every 5 seconds
- [ ] Error handling displays gracefully

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅

Enjoy your Smart Microgrid System! ⚡🌍
