"""
AI Optimizer Module - Energy optimization using rule-based logic and simple ML
"""

import random
from datetime import datetime
from collections import defaultdict

class EnergyOptimizer:
    """Energy optimization engine with AI logic"""
    
    def __init__(self):
        self.priority_order = ['Solar', 'Battery', 'Grid']
        self.min_battery_threshold = 0.2  # 20%
        self.max_battery_threshold = 0.9  # 90%
        
    def optimize(self, solar, battery_current, battery_capacity, grid_available, 
                 demand, mode='Urban', history=None, outage_simulated=False):
        """
        Main optimization function
        Returns: {source, efficiency, cost, savings, recommendation, alert}
        """
        
        battery_percent = battery_current / battery_capacity if battery_capacity > 0 else 0
        alert = None
        
        # Check for critical alerts
        if battery_percent < self.min_battery_threshold and solar == 0:
            alert = {
                'type': 'critical',
                'message': '⚠️ Battery low and no solar available!',
                'severity': 'high'
            }
        
        if not grid_available and solar == 0 and battery_percent < 0.3:
            alert = {
                'type': 'critical',
                'message': '🚨 Power outage! Battery critically low!',
                'severity': 'critical'
            }
        
        # Decision logic with priorities
        decision = self._make_decision(
            solar=solar,
            battery_current=battery_current,
            battery_capacity=battery_capacity,
            battery_percent=battery_percent,
            grid_available=grid_available,
            demand=demand,
            mode=mode,
            outage_simulated=outage_simulated
        )
        
        # Calculate costs and efficiency
        costs = self._calculate_costs(decision['source'], mode, demand)
        efficiency = self._calculate_efficiency(decision['source'], solar, battery_percent)
        
        # Predict savings
        savings = self._calculate_savings(decision['source'], demand, mode)
        
        return {
            'source': decision['source'],
            'efficiency': round(efficiency, 2),
            'cost': round(costs['cost'], 4),
            'savings': round(savings, 2),
            'recommendation': decision['recommendation'],
            'alert': alert
        }
    
    def _make_decision(self, solar, battery_current, battery_capacity, battery_percent,
                      grid_available, demand, mode, outage_simulated):
        """
        Decision making logic based on energy availability and demand
        """
        
        # Priorities based on availability
        available_sources = []
        
        # 1. Solar - Use if available and sufficient
        if solar >= demand * 0.8:
            return {
                'source': 'Solar',
                'recommendation': 'Using solar energy - Maximum efficiency!'
            }
        
        # 2. Battery - Use if available and above min threshold
        if battery_current >= demand and battery_percent > self.min_battery_threshold:
            return {
                'source': 'Battery',
                'recommendation': 'Using stored battery energy - Cost effective!'
            }
        
        # 3. Hybrid Solar + Battery
        if solar >= demand * 0.5 and battery_current >= demand * 0.5:
            # Use solar + battery
            if battery_percent > self.max_battery_threshold:
                # Charge battery instead
                return {
                    'source': 'Charging Battery',
                    'recommendation': 'Storing excess solar energy for later use'
                }
            else:
                return {
                    'source': 'Solar+Battery',
                    'recommendation': 'Using hybrid source - Optimal efficiency!'
                }
        
        # 4. Solar + Grid fallback
        if solar >= demand * 0.3:
            return {
                'source': 'Solar',
                'recommendation': f'Supplementing with solar + {("Grid" if grid_available and not outage_simulated else "Battery")}'
            }
        
        # 5. Grid - Use if available
        if grid_available and not outage_simulated:
            return {
                'source': 'Grid',
                'recommendation': 'Using grid supply - Reliable backup'
            }
        
        # 6. Outage scenario - Use battery only
        if outage_simulated or not grid_available:
            if battery_current >= demand:
                return {
                    'source': 'Battery',
                    'recommendation': '🔋 Power outage activated - Using backup battery!'
                }
            elif solar > 0:
                return {
                    'source': 'Solar',
                    'recommendation': '☀️ Power outage activated - Using solar + Battery!'
                }
            else:
                return {
                    'source': 'Emergency Battery',
                    'recommendation': '⚠️ LIMITED POWER - Battery backup active!'
                }
        
        # Default - Battery
        return {
            'source': 'Battery',
            'recommendation': 'Using battery backup'
        }
    
    def _calculate_costs(self, source, mode, demand):
        """Calculate energy costs based on source"""
        kwh_demand = demand / 1000  # Convert W to kWh
        
        if source == 'Grid':
            rate = 0.12 if mode == 'Urban' else 0.15
            cost = kwh_demand * rate
        elif source in ['Solar', 'Battery', 'Charging Battery', 'Solar+Battery', 'Emergency Battery']:
            cost = kwh_demand * 0.05  # Maintenance cost
        else:
            cost = kwh_demand * 0.08
        
        return {'cost': cost, 'source': source}
    
    def _calculate_efficiency(self, source, solar, battery_percent):
        """Calculate efficiency percentage"""
        base_efficiency = {
            'Solar': 85,
            'Battery': 90,
            'Grid': 95,
            'Solar+Battery': 92,
            'Charging Battery': 88,
            'Emergency Battery': 70
        }
        
        efficiency = base_efficiency.get(source, 80)
        
        # Adjust based on solar availability
        if source == 'Solar' and solar > 0:
            efficiency = min(95, efficiency + 5)
        
        # Adjust based on battery state
        if 'Battery' in source:
            if battery_percent > 0.8:
                efficiency += 3
            elif battery_percent < 0.3:
                efficiency -= 5
        
        return max(50, min(100, efficiency))
    
    def _calculate_savings(self, source, demand, mode):
        """Calculate money saved by using renewable sources"""
        kwh_demand = demand / 1000
        grid_rate = 0.12 if mode == 'Urban' else 0.15
        
        if source == 'Solar':
            savings = kwh_demand * grid_rate * 0.95
        elif source == 'Battery':
            savings = kwh_demand * grid_rate * 0.90
        elif source == 'Solar+Battery':
            savings = kwh_demand * grid_rate * 0.92
        else:
            savings = 0
        
        return savings
    
    def predict_usage(self, history, hours=24):
        """
        Predict energy usage for next N hours using simple ML
        Uses historical patterns and time-based logic
        """
        
        if not history:
            # Default predictions if no history
            return self._default_predictions(hours)
        
        # Parse historical data
        hourly_usage = defaultdict(list)
        for record in history:
            # record format: (timestamp, source, amount, mode)
            try:
                timestamp = datetime.fromisoformat(record[0]) if isinstance(record[0], str) else record[0]
                amount = float(record[2])
                hourly_usage[timestamp.hour].append(amount)
            except:
                continue
        
        # Calculate average usage per hour
        avg_usage = {}
        for hour, values in hourly_usage.items():
            avg_usage[hour] = sum(values) / len(values) if values else 0
        
        # Generate predictions
        predictions = []
        current_hour = datetime.now().hour
        
        for i in range(hours):
            predict_hour = (current_hour + i) % 24
            
            # Get base prediction from history
            base_value = avg_usage.get(predict_hour, 1500)
            
            # Add randomness (±10%)
            variance = base_value * (random.uniform(-0.1, 0.1))
            predicted_value = max(100, base_value + variance)
            
            # Apply time-based patterns
            if 18 <= predict_hour <= 21:  # Evening peak
                predicted_value *= 1.4
            elif 6 <= predict_hour < 9:  # Morning peak
                predicted_value *= 1.2
            elif 2 <= predict_hour < 6:  # Night low
                predicted_value *= 0.6
            
            predictions.append({
                'hour': predict_hour,
                'predicted_demand': round(predicted_value, 2),
                'confidence': round(0.75 + (len(history) / 1000), 2)
            })
        
        return predictions
    
    def _default_predictions(self, hours):
        """Generate default predictions when no history available"""
        predictions = []
        current_hour = datetime.now().hour
        
        for i in range(hours):
            predict_hour = (current_hour + i) % 24
            
            # Default pattern (kWh)
            if 18 <= predict_hour <= 21:  # Evening peak
                demand = random.uniform(2200, 3000)
            elif 6 <= predict_hour < 9:  # Morning
                demand = random.uniform(1500, 2000)
            elif 2 <= predict_hour < 6:  # Night
                demand = random.uniform(600, 1000)
            else:  # Day
                demand = random.uniform(800, 1500)
            
            predictions.append({
                'hour': predict_hour,
                'predicted_demand': round(demand, 2),
                'confidence': 0.70
            })
        
        return predictions

# Create global instance
optimizer = EnergyOptimizer()
