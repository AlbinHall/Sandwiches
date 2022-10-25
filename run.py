import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')
data = sales.get_all_values()


def get_sales_data():
    """
    get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    inside try converts string values into integers.
    raises ValueError if data value cannot be converted into
    integers or dont match instructions
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, You provided {len(values)}'
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
        return False
    return True


def update_sales_worksheet(data):
    """
    update sales worksheet, add new row with the list data provided
    """
    print(f'Updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print(f"sales data update completed!\n")


def update_surplus_worksheet(data):
    """
    update surplus worksheet
    """
    print(f'updating surplus worksheet..\n')
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print(f'Update completed\n')


def calculate_surplus_data(sales_row):
    """
    compares sales and stock and gives the surplus
    """
    print(f"Calculating surplus data \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
        
    return surplus_data


def get_last_five_records():
    """
    collecting the last 5 sales entry for the specifik sandwiches, getting sales of sale into list
    """
    sales = SHEET.worksheet("sales")


    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns 


def calculate_stock_data(data):
    """
    calculate the average stock for each sandwich
    """
    print("calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        stock_num = round(stock_num)
        new_stock_data.append(stock_num)

    return new_stock_data


def main():
    """
    Run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)
    sales_columns = get_last_five_records()
    stock_data = calculate_stock_data(sales_columns)


print("Welcome to the sandwich data calculation")
main()
