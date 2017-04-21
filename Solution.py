"""
A script that will take one or more stock symbols as input, and provide the 3 following files, in CSV format, with the header line as described:
 
1)         Symbol-YYYYMMDD-summary:                Previous Close, Open, Bid, Ask, 1y Target Estimate, Beta, Earnings Date, Day’s Range, 52 week Range, Volume, Average Volume (3 months), Market Cap, P/E, EPS, Dividend & Yield.
 
2)         Symbol-YYYYMMDD-calls:                        For *ALL* the options available that day, provide the following information, one option per line:  Option Expiration Date, Strike Price, Contract Name, Previous Close, Open, Bid, Ask, Day’s Range, Volume, Open Interest
 
3)         Symbol-YYYYMMDD-puts:             For *ALL* the options available that day, provide the following information, one option per line:  Option Expiration Date, Strike Price, Contract Name, Previous Close, Open, Bid, Ask, Day’s Range, Volume, Open Interest
 

"""





from bs4 import BeautifulSoup as bs4
from bs4 import BeautifulSoup
import csv, time, requests,urllib2


stockdetail = []			# list to store symbols

ch = 'y'
while (ch == 'y'):  		#loop for getting symbols as input
    Symbol = raw_input("Enter Symbol: ")
    stockdetail.append(Symbol)
    ch = raw_input("Want to add more Symbols('y' or 'n'): ")

for i in stockdetail:
    values = []  #list to store Row Values
   Heading = [] #list to store Column Headings
 
    r = requests.get("http://finance.yahoo.com/q?uhb=uh3_finance_vert&fr=&type=2button&s=" + i)
    data = r.text

    soup = BeautifulSoup(data, "html.parser")  #parsing data
    today = time.strftime('%Y%m%d')

    a = i + "-" + today + "-summary"
    Heading.append(a) # heading row prepared
    for r in range(1, 15):
        if r > 0:
            Heading.append("")

    for k in range(15):
        values.append(((soup.select('td[class="yfnc_tabledata1"]'))[k]).text)			#	rows populated



    rowlabel = ['Previous_Close', 'Open', 'Bid', 'Ask', '1y_Target_Est', 'Beta', 'Next_Earnings_Date', 'Day\'s_Range',
                '52wk_range', 'Volume', 'Avg_Vol(3m)', 'Market_Cap', 'P/E(ttm)', 'EPS(ttm)', 'Div_&_Yield']

	#function to write data into file
	def csv_writer(data, path):

		with open(path, "a") as csv_file:
		    writer = csv.writer(csv_file)

		    writer.writerow("")
		    writer.writerow(Heading)
		    writer.writerow(rowlabel)
		    writer.writerow(data)


    csv_writer(values, 'STOCK_Summary.csv') #--------------------->      #ENTER PATH


#LOOP ENDS

heading1 = ["Strike", "Contract_Name", "Last", "Bid", "Ask", "Change", "%Change", "Volume", "Open_Interest",
           "Implied_Volatility"]
for i in stockdetail:

    Heading1 = []
    Heading2 = []
 
    today1 = time.strftime('%Y%m%d')
    a = i + "-" + today1 + "-Calls"

    Heading1.append(a)
    for r in range(1, 10):
        if r > 0:
            Heading1.append("")


    today1 = time.strftime('%Y%m%d')

    a = i + "-" + today1 + "-Puts"
    Heading2.append(a)
    for r in range(1, 10):
        if r > 0:
            Heading2.append("")


    html_file = urllib2.urlopen("http://finance.yahoo.com/q/op?s=" + i + "+Options")
    soup = bs4(html_file)

# write data to csv files
    with open("STOCK_Calls.csv", "a") as csv_file: #--------------------->      #ENTER PATH
        writer = csv.writer(csv_file)
        writer.writerow(Heading1)
        writer.writerow(heading1)

    with open("STOCK_Puts.csv", "a") as csv_file: #--------------------->      #ENTER PATH
        writer = csv.writer(csv_file)
        writer.writerow(Heading2)
        writer.writerow(heading1)


    calls = []    # list to hold values of stock price

 
    for count in range(80):
        for price in soup.findAll(attrs={'data-row': "" + str(count)}):
            calls.append(price.text)  


        p = ""
        calls1 = str(calls)
        calls2 = []

        for i in calls1:
            if i == "\\" or i == "n":
                calls2.append(p)
                p = ""

            else:
                p += i


        list2 = []  # combined values are stored in this list
        for j in calls2:
            if j == "":
                print "",
            else:
                list2.append(j)

# splitting the list2 in two parts
        list12 = list2[1:11]   
        list22 = list2[12:22]

        calls = []  #emptying the list to be used in the next iteration
		
		#function to write data into files
        def csv_writer(data, path):

            with open(path, "a") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow("")
                writer.writerow(data)


        csv_writer(list12, 'STOCK_Calls.csv')          #--------------------->      #ENTER PATH
        csv_writer(list22, 'STOCK_Puts.csv')           #--------------------->      #ENTER PATH
