# Ristorante ilcapo Desktop Application

Prerequisites

- 	Visual Studio Code
-  	Python Extension for VS Code
-  	Git
-  	Python 3.9
-  	MySQL: The MySQL database server must be running. filess.io

1. Installation and Deployment

Launch VSCode and install the "Python" extension published by Microsoft. After creating the 'Restaurant Bureau' folder, open an integrated terminal in VS Code to clone the repository and execute the following commands:

  	« git clone https://github.com/VitorPinto1/ristoranteBureau.git »
  	« cd Restaurant Bureau »
   
2. Environment Configuration

Activate the Python virtual environment in the terminal:

  	« source env/bin/activate »  # Unix ou MacOS
  	« env\Scripts\activate »    # Windows

If the virtual environment does not exist yet, you can create it with:

  	« python -m venv env » 

3. Install Dependencies

Install the necessary packages from the requirements.txt file, if available:

  	« pip install -r requirements.txt »

4. Launching the Application

Run the application in the terminal:

  	« python main.py »

5. Accessing the Application

By following these steps, you should be able to deploy the desktop application locally and test its functionalities.

# File Information 

- database.py : Manages interactions with the database.
- reservation.py : Contains the application logic for managing reservations.
- main.py : Main file to start the application and manage the user interface.


