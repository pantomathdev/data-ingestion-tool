from Customer import CustomerImport
from Deserializer import CSVDeserializer
deserializer = CSVDeserializer.deserialize("./dirty_customer_records.csv")
for key, record in deserializer.records.items():
    print(key, record.__name)