import csv

# Open the CSV file for reading
with open('domains.csv', mode='r') as csv_file:
    # Create a CSV reader object
    reader = csv.reader(csv_file)
    
    # Skip the header row
    next(reader)
    
    # Search for the row containing the desired domain name
    for row in reader:
        if row[1] == 'domain5.com':
            domain_number = row[0]
            break
    
    # Print the domain number
    print(f"The domain number for domain5.com is {domain_number}")
