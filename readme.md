# Task Management System 

A full-stack task management application with user authentication, allowing users to manage tasks securely.

## Features

- User Authentication 
- Create, Read, Update and delete 
- Assign tasks to specific users
- Set deadline and priorities

## Running the project

1. clone the repository
    ```sh
    git clone https://github.com/solangeihirwe03/task_management.git
    ```
2. Setting the environment
    ```sh
    python -m venv env
    ```
3. Activate the environment
    ```sh
    env\Scripts\activate
    ```
4. Install dependencies
    ```sh
    pip install -r requirement.txt
    ```
5. Apply database migration
    ```sh
    python manage.py migrate
    ```
6. Run server
    ```sh
    python manage.py runserver
    ```