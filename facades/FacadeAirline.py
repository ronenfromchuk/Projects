from logger import Logger
from tables.Flights import Flights
from tables.Airline_Companies import AirlineCompanies
from FacadeBase import FacadeBase
from exceptions.ExceptioWrongInput import InvalidInput
from exceptions.ExceptionUnvalidToken import InvalidToken
from exceptions.ExceptionFlightNotFound import FlightNotFound
from exceptions.ExceptionWrongLocation import InvalidLocation
from exceptions.ExceptionAirlineNotFound import AirlineNotFound
from exceptions.ExceptionNoMoreTickets import NoMoreTicketsLeft
from exceptions.ExceptionInvalidTime import InvalidTime


class AirlineFacade(FacadeBase):

    def __init__(self, repo, config, login_token):
        super().__init__(repo, config)
        self.login_token = login_token
        self.logger = Logger.get_instance()
        self.ticket_limit = self.config["limits"]["ticket_limit"]

    def get_flights_by_airline(self, airline):
        self.logger.logger.debug(f'getting flight by airline={airline} >>>')
        if not isinstance(airline, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif self.repo.get_by_id(AirlineCompanies, airline) == None: 
            self.logger.logger.error(f'{AirlineNotFound}, airline=[{airline}] wasnt found!')
            raise AirlineNotFound
        else: 
            airline_check = self.repo.get_by_id(AirlineCompanies, airline)
            if self.login_token.id != airline_check.user_id:
                self.logger.logger.error(f'{InvalidToken}, you cant edit the ariline!')
                raise InvalidToken
            else:
                self.logger.logger.info(f'flights by=[{airline}], has been displayed!')
                return self.repo.get_by_column_value(Flights, Flights.airline_company_id, airline)

    def add_flight(self, flight):
        self.logger.logger.debug('adding a flight >>>')
        if not isinstance(flight, Flights): 
            self.logger.logger.error(f'{InvalidInput}, input should be Flight obj!')
            raise InvalidInput('input should be Flight obj!')
        elif flight.departure_time > flight.landing_time: 
            self.logger.logger.error(f'{InvalidTime}, departure must be before landing time!')
            raise InvalidTime
        elif flight.remaining_tickets < 0: 
            self.logger.logger.error(f'{NoMoreTicketsLeft}, remaining tickets cant be < 0!')
            raise NoMoreTicketsLeft
        elif flight.origin_country_id == flight.destination_country_id: 
            self.logger.logger.error(f'{InvalidLocation}, destination must be different than origin country!')
            raise InvalidLocation
        else: 
            airline_check = self.repo.get_by_id(AirlineCompanies, flight.airline_company_id)
            if self.login_token.id != airline_check.user_id:
                self.logger.logger.error(f'{InvalidToken}, you cant edit the ariline!')
                raise InvalidToken
            else:
                self.logger.logger.info(f'flight has been created!')
                self.repo.add(flight)

    def update_airline(self, airline, airline_id):
        self.logger.logger.debug(f'updating airline=[{airline_id}] >>>')
        if not isinstance(airline_id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif not isinstance(airline, dict): 
            self.logger.logger.error(f'{InvalidInput}, input should be dict!')
            raise InvalidInput('input should be dictionary!')
        elif super().get_airline_by_id(airline_id) == None: 
            self.logger.logger.error(f'{AirlineNotFound}, airline=[{airline_id}] wasnt found!')
            raise AirlineNotFound
        else:
            airline_check = self.repo.get_by_id(AirlineCompanies, airline_id)
            if self.login_token.id != airline_check.user_id:
                self.logger.logger.error(f'{InvalidToken}, you cant edit the ariline!')
                raise InvalidToken
            else:
                self.logger.logger.info(f'airline has been updated!')
                self.repo.update_by_id(AirlineCompanies, AirlineCompanies.id, airline_id, airline)

    def update_flight(self, flight, flight_id):
        self.logger.logger.debug(f'updating flight=[{flight_id}] >>>')
        if not isinstance(flight_id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('Input must be an integer!')
        elif not isinstance(flight, dict): 
            self.logger.logger.error(f'{InvalidInput}, input shout be dict!')
            raise InvalidInput('input shout be dictionary!')
        elif flight['remaining_tickets'] < 0: 
            self.logger.logger.error(f'{NoMoreTicketsLeft}, remaining tickets cannot be < 0!')
            raise NoMoreTicketsLeft
        elif super().get_flight_by_id(flight_id) == None: 
            self.logger.logger.error(f'{FlightNotFound}, flight=[{flight_id}] wasnt found!')
            raise FlightNotFound 
        else: 
            current_tickets = self.repo.get_by_id(Flights, flight_id).remaining_tickets
            self.repo.update_by_id(Flights, Flights.id, flight_id, flight)
            updated_tickets = self.repo.get_by_id(Flights, flight_id).remaining_tickets
            if updated_tickets < int(self.ticket_limit):
                self.repo.update_by_id(Flights, Flights.id, flight_id, {'remaining_tickets':current_tickets})
                self.logger.logger.error(f'{NoMoreTicketsLeft}, theres no more tickets left!')
                raise NoMoreTicketsLeft
            else:
                flight_check = self.repo.get_by_id(Flights, flight_id)
                airline_check = self.repo.get_by_id(AirlineCompanies, flight_check.airline_company_id)
                if self.login_token.id != airline_check.user_id:
                    self.logger.logger.error(f'{InvalidToken} - you cannot edit for other airline!')
                    raise InvalidToken
                else:
                    self.logger.logger.info(f'flight has been updated!')
                    print(f'{updated_tickets} remaining tickets on flight=[{flight_id}]')

    def remove_flight(self, flight_id):
        self.logger.logger.debug(f'removing flight=[{flight_id}] >>>')
        if not isinstance(flight_id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif super().get_flight_by_id(flight_id) == None: 
            self.logger.logger.error(f'{FlightNotFound}, flight=[{flight_id}] wasnt found!')
            raise FlightNotFound
        else: 
            flight_check = self.repo.get_by_id(Flights, flight_id)
            airline_check = self.repo.get_by_id(AirlineCompanies, flight_check.airline_company_id)
            if self.login_token.id != airline_check.user_id:
                self.logger.logger.error(f'{InvalidToken}, you cant edit the airline!')
                raise InvalidToken
            else:
                self.repo.delete_by_id(Flights, Flights.id, flight_id)
                self.logger.logger.info(f'flight=[{flight_id}], has been deleted!')

    def __str__(self):
        return f'facade_airline: {self.logger}... token id={self.login_token.id}\n name={self.login_token.name}, role={self.login_token.role}'
