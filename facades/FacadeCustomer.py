# DONE
from logger import Logger
from FacadeBase import FacadeBase
from tables.Tickets import Tickets
from tables.Flights import Flights
from tables.Customers import Customers
from exceptions.ExceptionUnvalidToken import InvalidToken
from exceptions.ExceptioWrongInput import InvalidInput
from exceptions.ExceptionNoMoreTickets import NoMoreTicketsLeft
from exceptions.ExceptionFlightNotFound import FlightNotFound
from exceptions.ExceptionTicketNotFound import TicketNotFound
from exceptions.ExceptionCustomerNotFound import CustomerNotFound

class CustomerFacade(FacadeBase):

    def __init__(self, repo, config, login_token):
        super().__init__(repo, config)
        self.login_token = login_token
        self.logger = Logger.get_instance()

    def update_customer(self, customer, customer_id):
        self.logger.logger.debug(f'updating customer=[{customer_id}] >>>')
        if not isinstance(customer_id, int): 
            self.logger.logger.error(f'{InvalidInput} , input should be int!')
            raise InvalidInput('input should be integer!')
        elif not isinstance(customer, dict): 
            self.logger.logger.error(f'{InvalidInput}, input should be dict!')
            raise InvalidInput('input should be dictionary!')
        elif self.repo.get_by_id(Customers, customer_id) == None: 
            self.logger.logger.error(f'{CustomerNotFound}, customer=[{customer_id}] wasnt found!')
            raise CustomerNotFound
        else: 
            customer_check = self.repo.get_by_id(Customers, customer_id)
            if self.login_token.id != customer_check.user_id:
                self.logger.logger.error(f'{InvalidToken}, you cant edit customers!')
                raise InvalidToken
            else: 
                self.logger.logger.info(f'customer=[{customer_id}], has been updated!')
                self.repo.update_by_id(Customers, Customers.id, customer_id, customer)

    def add_ticket(self, ticket):
        self.logger.logger.debug(f'adding ticket >>>')
        if not isinstance(ticket, Tickets): 
            self.logger.logger.error(f'{InvalidInput}, input should be [Tiekcts] object!')
            raise InvalidInput('input should be [Tiekcts] object!')
        flight = super().get_flight_by_id(ticket.flight_id)
        if flight == None: 
            self.logger.logger.error(f'{FlightNotFound}, flight=[{ticket.flight_id}] wasnt found!')
            raise FlightNotFound
        elif flight.remaining_tickets == 0:
            self.logger.logger.error(f'{NoMoreTicketsLeft}, no seats are available, ticket has been canceled!')
            raise NoMoreTicketsLeft
        else:
            customer_check = self.repo.get_by_id(Customers, ticket.customer_id)
            if self.login_token.id != customer_check.user_id:
                self.logger.logger.error(f'{InvalidToken}, you cant edit customers!')
                raise InvalidToken
            else:
                self.repo.add(ticket)
                self.repo.update_by_id(Flights, Flights.id, ticket.flight_id, {'remaining_tickets': flight.remaining_tickets - 1})
                self.logger.logger.info(f'ticket has been created!')

    def remove_ticket(self, ticket):
        self.logger.logger.debug(f'removing ticket=[{ticket}] >>>')
        if not isinstance(ticket, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be integer!')
        elif self.repo.get_by_id(Tickets, ticket) == None: 
            self.logger.logger.error(f'{TicketNotFound}, ticket=[{ticket}] wasnt found!')
            raise TicketNotFound
        else: 
            ticket_delete = self.repo.get_by_id(Tickets, ticket)
            customer = self.repo.get_by_id(Customers, ticket_delete.customer_id)
            if self.login_token.id != customer.user_id:
                self.logger.logger.error(f'{InvalidToken}, you cant edit customers!')
                raise InvalidToken
            else:
                flight = self.get_flight_by_id(ticket_delete.flight_id) 
                self.repo.update_by_id(Flights, Flights.id, flight.id, {'remaining_tickets': flight.remaining_tickets + 1})
                self.repo.delete_by_id(Tickets, Tickets.id, ticket)
                self.logger.logger.info(f'ticket=[{ticket}], has been deleted!')

    def get_ticket_by_customer(self, customer):
        self.logger.logger.debug(f'getting ticket by customer=[{customer}] >>>')
        if not isinstance(customer, int): 
            self.logger.logger.error(f'{InvalidInput}, inout should be int!')
            raise InvalidInput('inout should be integer!')
        elif self.repo.get_by_id(Customers, customer) == None: 
            self.logger.logger.error(f'{CustomerNotFound}, customer=[{customer}] wadnt found!')
            raise CustomerNotFound
        else: 
            customer_check = self.repo.get_by_id(Customers, customer)
            if self.login_token.id != customer_check.user_id:
                self.logger.logger.error(f'{InvalidToken}, you cant edit customers!')
                raise InvalidToken
            else:
                self.logger.logger.info(f'ticket/s by customer=[{customer}], has been displayed!')
                return self.repo.get_by_column_value(Tickets, Tickets.customer_id, customer)

    def __str__(self):
        return f'facade_customer: {self.logger}... token id={self.login_token.id} \n name={self.login_token.name}, role={self.login_token.role}'
