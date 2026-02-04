"""
Database module for managing user accounts and module data
"""
import sqlite3
import hashlib
import os
from datetime import datetime

class Database:
    def __init__(self, db_name='sdg4_education.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with users and modules tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create modules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                content TEXT,
                download_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_downloads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                module_id INTEGER,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(module_id) REFERENCES modules(id)
            )
        ''')
        
        conn.commit()
        
        # Add sample modules if they don't exist
        self.add_sample_modules()
        
        conn.close()
    
    def add_sample_modules(self):
        """Add sample modules for SDG 4"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check if modules exist
        cursor.execute('SELECT COUNT(*) FROM modules')
        if cursor.fetchone()[0] == 0:
            modules = [
                {
                    'title': 'Inclusive Quality Education Framework',
                    'description': 'Learn about inclusive and equitable quality education for all learners',
                    'content': '''
MODULE 1: INCLUSIVE QUALITY EDUCATION FRAMEWORK

1. Introduction to SDG 4
   - Ensuring inclusive and equitable quality education
   - Promoting lifelong learning opportunities for all

2. Key Principles
   - Accessibility for all learners
   - Equity in educational opportunities
   - Quality standards and outcomes

3. Implementation Strategies
   - Remove barriers to education
   - Support for disadvantaged groups
   - Teacher training and capacity building

4. Success Metrics
   - Enrollment rates
   - Completion rates
   - Learning outcomes assessment
   - Gender parity in education

5. Resources
   - UNESCO Guidelines for Inclusive Education
   - World Bank Education Reports
   - NGO Partnership Programs
'''
                },
                {
                    'title': 'Building Effective Learning Environments',
                    'description': 'Create safe, inclusive, and effective learning spaces for quality education',
                    'content': '''
MODULE 2: BUILDING EFFECTIVE LEARNING ENVIRONMENTS

1. Physical Infrastructure Requirements
   - Safe school buildings
   - Adequate classroom facilities
   - Sanitation and hygiene facilities
   - Technology access (computers, internet)

2. Inclusive Teaching Methods
   - Differentiated instruction
   - Accessibility for students with disabilities
   - Mother-tongue instruction
   - Interactive learning techniques

3. Curriculum Development
   - Relevant and quality curriculum
   - 21st-century skills integration
   - Assessment methods
   - Teacher support materials

4. Creating Inclusive Policies
   - Anti-discrimination policies
   - Gender equality measures
   - Support for vulnerable learners
   - Community involvement

5. Case Studies
   - Successful implementations worldwide
   - Lessons learned
   - Best practices
   - Challenges and solutions

6. Action Items for Implementation
   - Resource allocation
   - Training programs
   - Monitoring and evaluation
   - Continuous improvement
'''
                },
                {
                    'title': 'Teacher Development and Support',
                    'description': 'Professional development strategies for teachers in quality education',
                    'content': '''
MODULE 3: TEACHER DEVELOPMENT AND SUPPORT

1. Teacher Training Standards
   - Minimum qualifications
   - Continuous professional development
   - Subject matter expertise
   - Pedagogical skills

2. Professional Development Programs
   - In-service training
   - Mentoring and coaching
   - Workshops and seminars
   - Online learning platforms

3. Supporting Teacher Wellbeing
   - Work-life balance
   - Mental health support
   - Fair compensation
   - Career advancement opportunities

4. Teaching Methods Enhancement
   - Student-centered learning
   - Critical thinking development
   - Problem-solving approaches
   - Technology integration

5. Assessment and Performance
   - Regular evaluation methods
   - Feedback mechanisms
   - Performance incentives
   - Recognition programs

6. Building Learning Communities
   - Teacher collaboration
   - Knowledge sharing
   - Professional networks
   - Research and innovation

7. Resources for Teachers
   - Curriculum materials
   - Professional journals
   - Training resources
   - Support organizations
'''
                }
            ]
            
            for module in modules:
                cursor.execute('''
                    INSERT INTO modules (title, description, content)
                    VALUES (?, ?, ?)
                ''', (module['title'], module['description'], module['content']))
            
            conn.commit()
        
        conn.close()
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            
            conn.commit()
            conn.close()
            return True, "Account created successfully!"
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return False, "Username already exists!"
            else:
                return False, "Email already registered!"
    
    def login_user(self, username, password):
        """Verify user login credentials"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, username FROM users WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, user
        else:
            return False, None
    
    def get_all_modules(self):
        """Retrieve all available modules"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, title, description FROM modules')
        modules = cursor.fetchall()
        
        conn.close()
        return modules
    
    def get_module_content(self, module_id):
        """Get full content of a specific module"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT title, description, content FROM modules WHERE id = ?', (module_id,))
        module = cursor.fetchone()
        
        conn.close()
        return module
    
    def record_download(self, user_id, module_id):
        """Record a module download"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_downloads (user_id, module_id)
            VALUES (?, ?)
        ''', (user_id, module_id))
        
        cursor.execute('''
            UPDATE modules SET download_count = download_count + 1
            WHERE id = ?
        ''', (module_id,))
        
        conn.commit()
        conn.close()
