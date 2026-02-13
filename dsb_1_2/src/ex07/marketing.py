import sys

def call_center(clients, recipients):
    return sorted(set(clients) - set(recipients))

def potential_clients(participants, clients):
    return sorted(set(participants) - set(clients))

def loyalty_program(clients, participants):
    return sorted(set(clients) - set(participants))

def main():
    if len(sys.argv) != 2:
        raise Exception("Wrong arguments")
    task = sys.argv[1]
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
               'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    if task == "call_center":
        print(call_center(clients, recipients))
    elif task == "potential_clients":
        print(potential_clients(participants, clients))
    elif task == "loyalty_program":
        print(loyalty_program(clients, participants))
    else:
        raise Exception("Wrong task name")

if __name__ == '__main__':
    main()
