import subprocess
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='migration.log')

def show_menu():
    print("************")
    print("* 1. Migrate Transaction Table *")
    print("* 2. Migrate Balance Table *")
    print("* 3. Migrate Account Table *")
    print("************")

def get_user_choice():
    try:
        choice = int(input("Enter the number corresponding to your choice: "))
        return choice
    except ValueError:
        logging.error("Invalid input. Please enter a valid number.")
        return get_user_choice()

def get_time_frame():
    try:
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        return start_date, end_date
    except Exception as e:
        logging.error(f"Error while getting time frame: {e}")
        raise

def print_instructions(table_name, pid_sqlplus, pid_tokenize):
    print(f"\n{table_name} migration commands executed successfully.")
    print(f"\nTo check the status of SQL Plus migration:")
    print(f"    - Execute: ps aux | grep {pid_sqlplus}")
    print(f"To check the status of Tokenize JAR execution:")
    print(f"    - Execute: ps aux | grep {pid_tokenize}")

def migrate_table(table_name, script_file, output_file):
    try:
        logging.info(f"--- Migrating {table_name} Table ---")
        start_date, end_date = get_time_frame()
        
        # Execute SQL Plus in the background
        sql_command = f"nohup sqlplus username/password@database @{script_file} {table_name} {start_date} {end_date} > {output_file} 2>&1 &"
        sqlplus_process = subprocess.Popen(sql_command, shell=True)
        pid_sqlplus = sqlplus_process.pid

        # Execute Tokenize JAR in the background
        tokenize_command = f"nohup java -jar tokenize_file.jar {output_file} {table_name}_tokenized_output.txt > {table_name}_tokenize_output.log 2>&1 &"
        tokenize_process = subprocess.Popen(tokenize_command, shell=True)
        pid_tokenize = tokenize_process.pid

        print_instructions(table_name, pid_sqlplus, pid_tokenize)

    except KeyboardInterrupt:
        logging.info("Migration process interrupted by user.")
    except Exception as e:
        logging.error(f"Error during {table_name} migration: {e}")
        raise

# Main script
if __name__ == "__main__":
    try:
        show_menu()
        choice = get_user_choice()

        if choice == 1:
            migrate_table("Transaction", "transaction_migration_script.sql", "transaction_output.log")
        elif choice == 2:
            migrate_table("Balance", "balance_migration_script.sql", "balance_output.log")
        elif choice == 3:
            migrate_table("Account", "account_migration_script.sql", "account_output.log")
        else:
            logging.error("Invalid choice. Please choose a valid option.")
    except Exception as e:
        logging.error(f"Error in main script: {e}")
