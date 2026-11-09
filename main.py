from Customer import CustomerImport
from Deserializer import CSVDeserializer
deserializer = CSVDeserializer("./dirty_customer_records.csv")
for line, record in deserializer.invalid_records.items():
    print(f"{line}: {record}")