from Deserializer import *
class CustomerRecord:
    def __init__(self):
        self.customer_id = ""
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.email = ""
        self.email_domain = ""
        self.city = ""
        self.status = "ACTIVE"
        self.errors = []

class Customer:
    def __init__(self, deserializer):
        self.deserializer = deserializer
        self.valid_customers = []
        self.invalid_customers = []
        self.__validate_data()

    def __validate_data(self):
        for record in self.deserializer.records:
            cust_record = CustomerRecord()
            cust_id_valid, cust_err, cust_id = self.__validate_customer_id(record)
            name_valid, name_err, first_name, middle_name, last_name = self.__validate_name(record)
            email_valid, email_err, email, email_domain = self.__validate_email(record)
            try:
                city = record.city
            except:
                city = ""

            try:
                if "inactive" == record.status.lower():
                    status = "INACTIVE"
                elif "active" == record.status.lower():
                    status = "ACTIVE"
                else:
                    status = "ACTIVE"
            except:
                status = "ACTIVE"

            errors = []
            if not cust_id_valid:
                errors.append(cust_err + "\n")

            if not name_valid:
                errors.append(name_err + "\n")

            if not email_valid:
                errors.append(email_err + "\n")

            cust_record.customer_id = cust_id
            cust_record.first_name = first_name
            cust_record.middle_name = middle_name
            cust_record.last_name = last_name
            cust_record.email = email
            cust_record.email_domain = email_domain
            cust_record.city = city
            cust_record.status = status
            cust_record.errors = errors

            if errors:
                self.invalid_customers.append(cust_record)
            else:
                self.valid_customers.append(cust_record)

    def __validate_customer_id(self, record: Record):
        if not record.customer_id.startswith("CUST-"):
            return False, "Id doesn't start with prefix CUST-", record.customer_id

        cust_id = record.customer_id.split("-")

        if cust_id[1] == "":
            return False, "Expecting Id number after prefix", record.customer_id

        return True, "", record.customer_id

    def __validate_name(self, record: Record):
        if record.name == "":
            return False, "Name is empty", "", "", ""

        name = record.name.split()
        first_name = name[0]
        if len(name) <= 1:
            if not name[0].isalpha():
                return False, "Invalid characters in the name and last name is missing", first_name, "", ""
            return False, "Last name is missing", first_name, "", ""

        last_name = name[-1]
        if len(name) == 2:
            if not first_name.isalpha() or not last_name.isalpha():
                return False, "Invalid characters in the name", first_name, "", last_name
            return True, "", first_name, "", last_name

        middle_name = name[1: -1]
        for part in middle_name:
            if not part.isalpha():
                return False, "Invalid characters in the name", first_name, " ".join(middle_name), last_name
            
        if not first_name.isalpha() or not last_name.isalpha():
            return False, "Invalid characters in the name", first_name, " ".join(middle_name), last_name

        return True, "", first_name, " ".join(middle_name), last_name

    def __validate_email(self, record: Record):
        if record.email == "":
            return False, "email provided is empty", "", ""

        at_count = 0
        for ch in record.email:
            if ch == "@":
                at_count += 1

        if at_count == 0:
            return False, "Invalid email address", record.email, ""

        if at_count > 1:
            return False, "Invalid email address", record.email, ""

        local_part, domain = record.email.split("@")
        allowed_punctuation = "+-_."

        if "." not in domain:
            return False, "Invalid domain", record.email, domain

        if local_part.startswith(tuple(allowed_punctuation)) or local_part.endswith(tuple(allowed_punctuation)) or len(local_part) == 0:
            return False, "Invalid email address", record.email, domain

        for ch in  local_part:
            if ch.isalpha() or ch.isdigit() or ch in allowed_punctuation:
                pass
            else:
                return False, "Invalid character(s) in email address", record.email, domain

        domain_labels = domain.split(".")
        if "" in set(domain_labels):
            return False, "Invalid domain format", record.email, domain

        for label in domain_labels:
            if label.startswith(tuple(allowed_punctuation)) or label.endswith(tuple(allowed_punctuation)):
                return False, "Invalid domain format", record.email, domain

            for ch in label:
                if ch.isalpha() or ch.isdigit() or ch == "-":
                    pass
                else:
                    return False, "Invalid character(s) in domain", record.email, domain

        return True, "", record.email, domain

class CustomerImport:
    @classmethod
    def __validate_schema(cls, deserializer):
        header_set = set(deserializer.headers)

        if len(header_set) == 0:
            raise ValueError("Empty file/Headers are missing.")

        name_missing = False
        custid_missing = False
        email_missing = False

        if "customer_id" not in header_set:
            custid_missing = True

        if "name" not in header_set:
            name_missing = True

        if "email" not in header_set:
            email_missing = True

        if name_missing or custid_missing or email_missing:
            raise ValueError(
                "Missing mandatory fields:" +
                "- customer_id\n" if custid_missing else "" +
                "- name\n" if name_missing else "" +
                "- email\n" if email_missing else ""
            )

    @classmethod
    def from_csv(cls, path: str, sep: str = ","):
        deserializer = CSVDeserializer(path, sep)
        CustomerImport.__validate_schema(deserializer)
        customer = Customer(deserializer)
        return customer