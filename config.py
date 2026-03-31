"""
EcoVolt AI Configuration
Project setup and verification utilities
"""

import os
import sys
import sqlite3
from pathlib import Path

class ProjectConfig:
    """Project configuration and verification"""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent
    TEMPLATES_DIR = PROJECT_ROOT / 'templates'
    STATIC_DIR = PROJECT_ROOT / 'static'
    DATABASE_DIR = PROJECT_ROOT / 'database'
    
    # Required files
    REQUIRED_FILES = {
        'Python': ['app.py', 'ai_optimizer.py', 'db_init.py'],
        'Templates': ['templates/login.html', 'templates/dashboard.html'],
        'Static': ['static/style.css', 'static/script.js'],
        'Config': ['requirements.txt', 'README.md']
    }
    
    # Python dependencies
    DEPENDENCIES = {
        'Flask': '2.3.2',
        'Werkzeug': '2.3.6',
        'Jinja2': '3.1.2',
    }
    
    @classmethod
    def verify_structure(cls):
        """Verify project structure"""
        print("Verifying project structure...")
        print("-" * 60)
        
        missing = []
        found = []
        
        for category, files in cls.REQUIRED_FILES.items():
            print(f"\n{category}:")
            for file in files:
                filepath = cls.PROJECT_ROOT / file
                if filepath.exists():
                    print(f"  ✓ {file}")
                    found.append(file)
                else:
                    print(f"  ✗ {file} [MISSING]")
                    missing.append(file)
        
        print("\n" + "-" * 60)
        print(f"Summary: {len(found)} files found, {len(missing)} missing")
        
        if missing:
            print(f"\nMissing files: {', '.join(missing)}")
            return False
        
        return True
    
    @classmethod
    def verify_database(cls):
        """Verify database setup"""
        print("\nVerifying database...")
        print("-" * 60)
        
        db_path = cls.DATABASE_DIR / 'db.sqlite3'
        
        if db_path.exists():
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                
                # Check for required tables
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table'
                """)
                tables = [row[0] for row in cursor.fetchall()]
                
                required_tables = ['users', 'energy_usage', 'alerts', 'daily_reports']
                
                print(f"\nDatabase tables ({len(tables)}):")
                for table in tables:
                    status = "✓" if table in required_tables else "•"
                    print(f"  {status} {table}")
                
                conn.close()
                return True
            except Exception as e:
                print(f"  ✗ Database error: {e}")
                return False
        else:
            print(f"  ✗ Database not found (will be created on first run)")
            return False
    
    @classmethod
    def verify_dependencies(cls):
        """Verify Python dependencies"""
        print("\nVerifying dependencies...")
        print("-" * 60)
        
        missing_deps = []
        
        for package, version in cls.DEPENDENCIES.items():
            try:
                __import__(package.lower() if package != 'Werkzeug' else 'werkzeug')
                print(f"  ✓ {package} {version}")
            except ImportError:
                print(f"  ✗ {package} {version} [NOT INSTALLED]")
                missing_deps.append(package)
        
        if missing_deps:
            print(f"\nMissing dependencies: {', '.join(missing_deps)}")
            print("Run: pip install -r requirements.txt")
            return False
        
        return True
    
    @classmethod
    def run_all_checks(cls):
        """Run all verification checks"""
        print("\n" + "=" * 60)
        print("  EcoVolt AI - System Verification")
        print("=" * 60)
        
        results = {
            'Structure': cls.verify_structure(),
            'Database': cls.verify_database(),
            'Dependencies': cls.verify_dependencies(),
        }
        
        print("\n" + "=" * 60)
        print("  Verification Summary")
        print("=" * 60)
        
        for check, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {check}: {status}")
        
        all_passed = all(results.values())
        
        print("\n" + "=" * 60)
        if all_passed:
            print("  ✓ All checks passed! Ready to run.")
            print("  Run: python app.py")
        else:
            print("  ✗ Some checks failed. See above for details.")
        print("=" * 60 + "\n")
        
        return all_passed


if __name__ == '__main__':
    # Run verification
    success = ProjectConfig.run_all_checks()
    sys.exit(0 if success else 1)
