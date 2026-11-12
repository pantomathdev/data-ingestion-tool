import csv
from copy import deepcopy

class Record:
    def __init__(self, row):
        if any(val is None for val in row.values()):
            raise SchemaError("Missing field in the row")
        
        if any(key is None for key in row.keys()):
            raise SchemaError("Extra field in the row")
        
        for key, val in row.items():
            setattr(self, key.strip(), val.strip())

class RecordCollection:
    def __init__(self):
        self.__records = {}
        self.__invalid_records = {}
        self.__headers = []

    @property
    def headers(self):
        return deepcopy(self.__headers)

    @property
    def records(self):
        return deepcopy(self.__records)

    @property
    def invalid_records(self):
        return deepcopy(self.__invalid_records)

    def add_record(self, line_num: int, record: Record):
        self.__records[line_num] = record

    def add_invalid_record(self, line_num: int, err_msg: str):
        self.__invalid_records[line_num] = err_msg

    def set_headers(self, headers: list[str]):
        self.__headers = headers

class SchemaError(ValueError):
    pass

class CSVDeserializer:
    @classmethod
    def deserialize(cls, path: str, sep: str = ","):
        if not path.endswith(".csv"):
            raise ValueError("Please supply a CSV file path")

        try:
            with open(path, "r", encoding="utf-8", newline="") as csv_file:
                dict_reader = csv.DictReader(csv_file,delimiter= sep, strict= True)

                if not dict_reader.fieldnames:
                    raise ValueError("File is empty")

                headers = [header.strip().lower() for header in dict_reader.fieldnames]

                if not all(headers):
                    raise ValueError("CSV file contains blank header(s)")

                if len(headers) != len(set(headers)):
                    raise ValueError("CSV file contains duplicate headers")
                
                container = RecordCollection()
                headers = [header.strip() for header in dict_reader.fieldnames]
                container.set_headers(headers)

                for row in dict_reader:
                    try:
                        record = Record(row)
                    except SchemaError as s:
                        container.add_invalid_record(dict_reader.line_num, str(s))
                        continue

                    container.add_record(dict_reader.line_num, record)

                return container
                
        except ValueError as v:
            print(str(v))
            raise
        except csv.Error as e:
            print(f"CSV error at line {dict_reader.line_num}: {e}")
            raise
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at the path {path} does not exist.")
        except PermissionError:
            raise PermissionError(f"The file at the path {path} does not have sufficient read permission.")