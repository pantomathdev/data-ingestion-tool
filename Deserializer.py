import csv
from copy import deepcopy, copy
class Record:
    pass

class CSVDeserializer:
    def __init__(self, path: str, sep: str = ","):
        if not path.endswith(".csv"):
            raise ValueError("Please supply a CSV file path")

        try:
            with open(path, "r", encoding="utf-8", newline="") as csv_file:
                self.__records = {}
                self.__invalid_records = {}
                lines = csv.reader(csv_file, delimiter=sep, strict=True)
                headers = next(lines)
                self.__headers = [header.strip() for header in headers]

                if not all(self.__headers):
                    raise ValueError("CSV file contains blank header(s)")

                if len(self.__headers) != len(set(self.__headers)):
                    raise ValueError("CSV file contains duplicate headers")
                
                for line in lines:
                    if line:
                        if len(line) == len(self.__headers):
                            record = Record()
                            for attr, val in zip(self.__headers, line):
                                setattr(record, attr, val.strip())
                            self.__records[lines.line_num] = record
                        else:
                            self.__invalid_records[lines.line_num] = line
        except StopIteration:
            raise ValueError("CSV file is empty")
        except csv.Error as e:
            print(f"CSV error at line {lines.line_num}: {e}")
            raise
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at the path {path} does not exist.")
        except PermissionError:
            raise PermissionError(f"The file at the path {path} does not have sufficient read permission.")

    @property
    def records(self):
        return deepcopy(self.__records)

    @property
    def invalid_records(self):
        return deepcopy(self.__invalid_records)

    @property
    def headers(self):
        return copy(self.__headers)