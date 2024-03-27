DataWhisperer: Chat with your MySQL Database
This Streamlit application allows you to interact with your MySQL database using natural language! Ask questions about your data and get clear explanations alongside the corresponding SQL queries.

Features

Natural Language Interface: Interact with your database using plain English questions.
AI-Powered Query Generation: Leverage large language models to generate SQL queries based on your questions.
Natural Language Response: Receive explanations of the data retrieved from the database in an easy-to-understand format.
Streamlit Integration: Enjoy a user-friendly interface for seamless interaction with your data.
Getting Started

Prerequisites:
Python 3.6 or later
Streamlit
LangChain libraries (langchain-core, langchain-openai, langchain-community)
A MySQL database
Clone the repository:
Bash
git clone https://github.com/your-username/datawhisperer.git
Use code with caution.
Install dependencies:
Bash
pip install -r requirements.txt
Use code with caution.
Create a .env file:

Create a file named .env in the project root directory. Add your database connection details to this file following the format:

HOST=your_database_host
PORT=your_database_port
USER=your_database_username
PASSWORD=your_database_password
DATABASE=your_database_name
Run the application:

Bash
streamlit run app.py
Use code with caution.
How to Use

Open http://localhost:8501/ in your web browser (Streamlit default port).
Connect to your database by entering the details in the sidebar and clicking the "Connect" button.
Type your questions in the chat input box at the bottom and press Enter.
The application will generate the corresponding SQL query, execute it on your database, and provide a natural language explanation of the results.
Example Questions

How many orders were placed in January?
Show me the top 5 products by units sold.
List all transactions above $500.
Which product category is the most profitable?
Compare this month's revenue to the same month last year.
Further Enhancements

This code provides a solid foundation for a user-friendly database exploration tool. Consider exploring features like:

Customizable dashboards
Interactive data visualizations
Scheduled queries and data alerts
Data export options
