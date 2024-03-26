# PassBank 4.0

PassBank 4.0 is a simple yet secure password manager written in Python. It allows users to store their passwords securely and access them with ease whenever needed.

## Features

- **Secure Password Storage**: PassBank encrypts passwords using industry-standard encryption techniques to ensure they are securely stored.
- **User-Friendly Interface**: The user interface is designed to be intuitive and easy to use, making it suitable for both novice and experienced users.
- **Password Generator**: PassBank includes a built-in password generator that can create strong and unique passwords.
- **Cross-Platform Compatibility**: PassBank is compatible with Windows, macOS, and Linux operating systems.
- **Import/Export Functionality**: Users can import existing password data or export their stored passwords for backup purposes.
- **Auto-Locking**: PassBank automatically locks after a period of inactivity to prevent unauthorized access.

## Installation

To use PassBank 4.0, follow these steps:

1. Clone the PassBank repository to your local machine:

   ```bash
   git clone https://github.com/ErickOliveiraT/PassBank-4.0.git
2. Install requirements
    ```bash
   pip install -r requirements.txt
3. Run this command
    ```bash
   python src/gui.py
4. If you want to generate a .exe file, run this command:
    ```bash
    python -m PyInstaller src/gui.py --onefile --noconsole