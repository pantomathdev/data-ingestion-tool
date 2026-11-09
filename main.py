from Customer import CustomerImport
from Deserializer import CSVDeserializer
deserializer = CSVDeserializer("./dirty_customer_records.csv")
print(deserializer.headers)
print("Valid records:")
for record in deserializer.records:
    print(record.__dict__)
print("Invalid records:")
print(deserializer.invalid_records)