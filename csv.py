import csv
import uuid

# Open the CSV file for writing
with open('domains.csv', mode='w', newline='') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)
    
    # Write the header row
    writer.writerow(['Domain Number', 'Domain Name', 'Date Registered'])
    
    # Write some example data to the file
    for i in range(10):
        domain_number = str(uuid.uuid4())
        domain_name = f'domain{i}.com'
        date_registered = '2022-01-01'
        writer.writerow([domain_number, domain_name, date_registered])
