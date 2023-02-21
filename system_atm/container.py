from adapters.outbound.repositories.customer_adapter_repository import customer_adapter_repository


# INSIDE_PORTS
from application.ports.inside.customer.account_generator_inside_port import account_generator_inside_port
from application.ports.inside.customer.create_new_customer_inside_port import create_new_customer_inside_port
from application.ports.inside.customer.get_account_inside_port import get_account_inside_port
from application.ports.inside.customer.execute_transfer_inside_port import execute_transfer_inside_port

# SERVICE
from application.services.customer.account_generator_service import account_generator_service
from application.services.customer.create_new_customer_service import create_new_customer_service
from application.services.customer.get_account_service import get_account_service

# VALIDATION
from application.validation.account_validation import account_validation

# OUTSIDE_PORTS
from application.ports.outside.customer.costumer_repository_outside_port import costumer_repository_outside_port
from application.ports.outside.customer.get_account_outside_port import get_account_outside_port
from application.ports.outside.customer.account_exists_outside_port import account_exists_outside_port


def container(repository: dict) -> tuple:

    customer_adapter = customer_adapter_repository(repository)

    account_generator_injector = account_generator_inside_port(
        account_generator_service(
            account_exists_outside_port(customer_adapter)))

    create_new_customer_injector = create_new_customer_inside_port(
        create_new_customer_service(account_validation(),
                                    costumer_repository_outside_port(customer_adapter)))

    get_account_inside_injector = get_account_inside_port(
        get_account_service(
            get_account_outside_port(customer_adapter)))

    execute_transfer_injector = execute_transfer_inside_port(
        customer_adapter)

    return account_generator_injector, \
        create_new_customer_injector, \
        get_account_inside_injector, \
        execute_transfer_injector
