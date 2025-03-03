import csv
import pandas as pd
from pprint import pprint


# df = pd.read_csv('successful.csv')
# row = pd.DataFrame({'Dates': ['Current date: 12/11/2024'],
#                     'Cryptics' : ['Meal Uncle John cooked containing zero joules'],
#                     'Wins' :[0]})

# print(row)

# df = pd.concat([df, row], ignore_index=True)

# print(df)

# alist = ['Ruler presiding over nothern region', 
#     'Enchanting woman follows opening of stock exchange', 
#     'Meal Uncle John cooked containing zero joules',
#     ]

# blist = ['Current date: 12/09/2024', 'Current date: 12/10/2024', 'Current date: 12/11/2024']
# df = pd.DataFrame()
# df['Dates'] = blist
# df['Cryptics'] = alist
# df['Cryptics'] = [1,1,0]

# # pprint( df )

# print( list(df['Dates'])[-1] )
# df.to_csv('successful.csv', index=False)

# #  'Current date: 12/11/2024,Meal Uncle John cooked containing zero joules,0'

def add_to_wins(dateline, crypt, win):
    df = pd.read_csv('successful.csv')
    if list(df['Dates'])[-1] == dateline:
        return 0
    else:
        row = pd.DataFrame({'Dates': [dateline],
                    'Cryptics' : [crypt],
                    'Wins' :[win]})
        df = pd.concat([df, row], ignore_index=True)

        df.to_csv('successful.csv', index=False)
        
def main():
    df = pd.read_csv('successful.csv')
    total = df['Wins'].sum()
    length = len(df)
    success_rate = (total/length)*100
    print()
    print(f'Since 12/09/2024, this program has been used {length} times and guessed the answer {success_rate}% of the time')
    
if __name__ == "__main__":
    main()