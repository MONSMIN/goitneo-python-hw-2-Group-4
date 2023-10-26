from faker import Faker
from classes import AddressBook, Record, Name, Phone

fake = Faker()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Not enough params. Print help"
        except KeyError:
            return "Contact not found."

    return inner


@input_error
def parse_input(user_input):
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


@input_error
def add_contact(args, contacts):
    name, *phones = args
    new_record = Record(name)
    for phone in phones:
        new_record.add_phones(phone)
    contacts.add_record(new_record)
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, new_phone = args
    record = contacts.find(name)
    if record:
        record.edit_phone(new_phone)
        return f"Contact {name} updated phone: {new_phone}"
    else:
        return "Contact not found."


@input_error
def show_phone(args, contacts):
    name, *_phones = args
    record = contacts.find(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        return f"Phones: {phones}, contact {name}!"
    else:
        return "Contact not found."


@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts found."
    result = "\n".join([str(record) for record in contacts.values()])
    return result


def main():
    contacts = AddressBook()

    for _ in range(10):
        name = fake.first_name()
        phone = str(fake.random_int(min=1000000000, max=9999999999))
        new_record = Record(name)
        new_record.add_phones(phone)
        contacts.add_record(new_record)

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
