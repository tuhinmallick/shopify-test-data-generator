import shopify
from faker import Factory
from pyactiveresource.connection import ResourceNotFound

from stdg import config


class Customers(object):
    def __init__(self):

        return

    def create(self, number_customers):

        customers_created = []

        for counter in range(number_customers):

            print("Generating Customer: {0}".format(str(counter+1)))

            new_customer = shopify.Customer().create(self.generate_data())

            if new_customer.errors:
                # something went wrong!
                # TODO: we need to loop over our error messages and print them
                for message in new_customer.errors.full_messages():
                    print(message)
                return

            customers_created.append(str(new_customer.id))

        with open('stdg-customers.csv', mode='a', encoding='utf-8') as customers_file:
            customers_file.write('\n'.join(customers_created) + '\n')

        return

    @staticmethod
    def generate_data():

        settings = config.settings['customers']

        # We're forcing US locale since it contains the most complete providers for the Faker package.
        fake = Factory.create(settings['LOCALE'])

        first_name = fake.first_name()
        last_name = fake.last_name()

        customer = {
            'first_name': first_name,
            'last_name': last_name,
            'addresses': [
                {
                    'address1': fake.street_address(),
                    'city': fake.city(),
                    'province': fake.state(),
                    'phone': fake.phone_number(),
                    'zip': fake.postcode(),
                    'last_name': first_name,
                    'first_name': last_name,
                    'country': 'US'
                }
            ],
        }

        return customer

    def delete(self, customers=None):

        if customers is None:
            # delete all orders
            with open('stdg-customers.csv') as customer_file:
                customers_delete = customer_file.read().splitlines()

            for customer_id in customers_delete:

                try:
                    customer = shopify.Customer.find(int(customer_id))
                    customer.destroy()
                    print("[DELETED] Customer #{0}".format(customer_id))
                except ResourceNotFound:
                    print("[WARNING]: Customer #{0} not found.".format(customer_id))
                except:
                    print("Customer #: {0} has existing orders maybe?".format(customer_id))

        return
