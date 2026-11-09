class Record:
    pass

class CSVDeserializer:
    def __init__(self, path: str, sep: str = ","):
        if not path.endswith(".csv"):
            raise ValueError("Please supply a CSV file path")

        try:
            with open(path, encoding="utf-8") as csv_file:
                self.records = []
                self.invalid_records = []
                header = csv_file.readline()
                self.headers = header.strip().split(sep)
                for line in csv_file:
                    line_data = line.strip()
                    if line_data != "":
                        data = line_data.split(sep)
                        if len(data) == len(self.headers):
                            record = Record()
                            for i in range(len(self.headers)):
                                setattr(record, self.headers[i], data[i].strip())
                            self.records.append(record)
                        else:
                            self.invalid_records.append(line_data)

        except FileNotFoundError:
            raise FileNotFoundError(f"The file at the path {path} does not exist.")
        except PermissionError:
            raise PermissionError(f"The file at the path {path} does not have sufficient read permission.")