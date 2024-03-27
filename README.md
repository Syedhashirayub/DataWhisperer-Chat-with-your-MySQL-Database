# DataWhisperer: Chat with your MySQL Database

DataWhisperer is an innovative Streamlit application designed to bridge the gap between complex SQL queries and users at all levels of SQL proficiency. By enabling both natural language and direct SQL queries, DataWhisperer makes database insights accessible and interactive.

## Features

- **Natural Language Interface**: Ask questions in plain English to retrieve data from your MySQL database.
- **AI-Powered Query Generation:**: Leverage large language models to generate SQL queries based on your questions.
- **Natural Language Response**: Receive explanations of the data retrieved from the database in an easy-to-understand format..
- **Customizable Database Connections**: Easily configure the application to connect to different MySQL databases.
- **User-Friendly Documentation**: Get started quickly with comprehensive documentation and examples.

## Installation

Ensure Python and pip are installed on your machine. Follow these steps to set up DataWhisperer:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Syedhashirayub/DataWhisperer.git
   cd DataWhisperer

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Create a .env file**:
   Create a file named .env in the project root directory. Add your Open AI key details to this file following the format
   ```bash
   OPENAI_API_KEY= sk-

4. **Run the application**:
   ```bash
   streamlit run app.py

