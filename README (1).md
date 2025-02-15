# Face Recognition Voting System

## Overview

This project is a face recognition-based voting system developed using Python. It leverages modern computer vision techniques to identify and authenticate voters based on their facial features. This system aims to provide a secure, efficient, and user-friendly alternative to traditional voting methods.

## Features

- **Face Detection and Recognition**: Utilizes deep learning models to detect and recognize faces.
- **Voter Authentication**: Ensures that only registered voters can cast their votes.
- **Real-time Processing**: Processes facial recognition in real-time for a seamless user experience.
- **Secure Voting**: Implements security measures to prevent fraudulent activities.
- **User-friendly Interface**: Provides an intuitive interface for voters and administrators.

## Technologies Used

- **Programming Language**: Python
- **Libraries**: OpenCV, dlib, face_recognition, Flask
- **Database**: SQLite for storing voter information and votes
- **Web Framework**: Flask for developing the web interface

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Dharanya004/face-recognition-voting-system.git
    cd face-recognition-voting-system
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**:
    ```bash
    flask run
    ```

## Usage

1. **Register Voters**:
    - Register voter details along with their facial images using the admin interface.
    
2. **Voting Process**:
    - Voters can log in using their face and cast their votes securely.

3. **Admin Interface**:
    - Admins can manage voter registrations, monitor voting processes, and tally votes.

## Folder Structure

```
face-recognition-voting-system/
│
├── app.py              # Main application file
├── models.py           # Database models
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Contributing

Contributions are welcome! Please fork the repository and open a pull request to contribute.

## License

This project is licensed under the MIT License.

## Contact

- **Email**: [dharanya004@example.com](mailto:dharanya004@example.com)
- **LinkedIn**: [Dharanya's LinkedIn](https://www.linkedin.com/in/dharanya004)

---

✨ _This project was developed by Dharanya004_ ✨

```` ▋