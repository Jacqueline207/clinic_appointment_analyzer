import pandas as pd
from database import engine
'''
the entire appointment table can be loaded into a Pandas DataFrame and written out as a CSV file
'''

def main() -> None:
    df= pd.read_sql_table("appointments", con=engine)
    df.to_csv("appointments.csv", index=False)

if __name__ == "__main__":
    main()