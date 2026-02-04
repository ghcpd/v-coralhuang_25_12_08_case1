# SDG 4 Quality Education System

A Python-based GUI application for managing educational modules related to UN Sustainable Development Goal 4 (Quality Education).

## Features

✅ **User Authentication**
- Create new user accounts with username, email, and password
- Secure login with password hashing (SHA256)
- Account validation and error handling

✅ **Three Educational Modules**
1. **Inclusive Quality Education Framework** - Learn about inclusive and equitable quality education
2. **Building Effective Learning Environments** - Create safe and inclusive learning spaces
3. **Teacher Development and Support** - Professional development strategies for teachers

✅ **Module Management**
- View detailed module content
- Download modules as text files
- Track download statistics
- User-specific download history

✅ **User-Friendly Interface**
- Clean, intuitive Tkinter GUI
- Responsive design with proper layout
- Color-coded buttons and sections
- Scrollable content viewing

## Requirements

- Python 3.7+
- tkinter (usually comes with Python)
- SQLite3 (built-in with Python)

## Installation

1. Clone or download this repository
2. No additional dependencies needed - uses Python standard library

## Usage

Run the application:
```bash
python main.py
```

### First Time Setup
1. Click "Create New Account"
2. Enter username, email, and password
3. Click "Create Account"
4. Login with your credentials

### Using the System
1. After login, you'll see the home page with three modules
2. Click "View Content" to read module materials
3. Click "Download" to save module as text file
4. Click "Logout" to exit (saves session in database)

## File Structure

```
├── main.py              # Application entry point
├── auth.py              # Login and signup GUI
├── home.py              # Home page and modules display
├── database.py          # Database management and user/module data
└── README.md            # This file
```

## Database

The application uses SQLite database (`sdg4_education.db`) which automatically creates tables for:
- **users**: Store user accounts with hashed passwords
- **modules**: Store educational content
- **user_downloads**: Track user download history

## Features Details

### Security
- Passwords are hashed using SHA256
- Username and email uniqueness validation
- Input validation for all forms

### Module Content
Each module includes:
- Comprehensive educational material
- Multiple sections and subtopics
- Implementation strategies
- Case studies and resources

### Download Functionality
- Save modules as text files
- Automatic formatting with headers and metadata
- Download count tracking per module
- User-specific download history

## Future Enhancements

- PDF export functionality
- Search and filter modules
- Category organization
- User progress tracking
- Certificate generation
- Admin panel for module management
- Discussion forums
- Quiz and assessment system

## License

Open source for educational purposes

## Support

For issues or suggestions, please contact the development team.
