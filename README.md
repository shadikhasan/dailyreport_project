
# Daily Report Project

A web application built with Django and Bootstrap to submit and manage daily reports efficiently.

---

## Overview

This project is a simple and intuitive daily report management system that allows users to submit daily work reports through a clean web interface. It is designed to help teams and individuals keep track of their daily tasks and progress in an organized way.

---

## Features

- User-friendly form to submit daily reports  
- Report listing and management  
- Responsive UI using Bootstrap 5  
- Easy to customize and extend  
- REST API endpoints (if applicable)  

---

## Technologies Used

- Python 3.x  
- Django 4.x  
- Bootstrap 5  
- SQLite (default, can be changed to PostgreSQL or others)  
- HTML, CSS, JavaScript  

---

## Installation & Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/shadikhasan/dailyreport_project.git
    cd dailyreport_project
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6. **Open your browser and navigate to:**
    ```
    http://127.0.0.1:8000/
    ```

---

## Usage

- Navigate to the daily report submission page.
- Fill out the report form with your daily tasks.
- Submit the form to save the report.
- View or manage existing reports (depending on implemented features).

---

## Project Structure

```
dailyreport_project/
├── dailyreport/           # Django app: models, views, templates, static files
├── dailyreport_project/   # Project settings and configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

---

## License

This project is licensed under the MIT License.

---

## Contact

Created by **Shadik Hasan**  
- GitHub: [shadikhasan](https://github.com/shadikhasan)  