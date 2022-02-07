# DONE
from logger import Logger
from Flights import Flights
from Airline_Companies import AirlineCompanies
from FacadeBase import FacadeBase
from ExceptioWrongInput import InvalidInput
from ExceptionUnvalidToken import InvalidToken
from ExceptionFlightNotFound import FlightNotFound
from ExceptionWrongLocation import InvalidLocation
from ExceptionAirlineNotFound import AirlineNotFound
from ExceptionNoMoreTickets import NoMoreTicketsLeft
from ExceptionInvalidTime import InvalidTime


class AirlineFacade(FacadeBase):

    def __init__(self, repo, login_token):
        super().__init__(repo)
        self.login_token = login_token
        self.logger = Logger.get_instance()

    def get_flights_by_airline(self, airline):
        self.logger.logger.debug(f'getting flight by airline={airline} >>>')
        if not isinstance(airline, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif self.login_token.role != 'Airline': raise InvalidToken
        elif self.repo.get_by_id(AirlineCompanies, airline) == None: 
            self.logger.logger.error(f'{AirlineNotFound}, airline=[{airline}] wasnt found!')
            raise AirlineNotFound
        else: 
            self.logger.logger.info(f'flights by airline=[{airline}], has been displayed!')
            return self.repo.get_by_column_value(Flights, Flights.airline_company_id, airline)

    def add_flight(self, flight):
        self.logger.logger.debug('adding a flight >>>')
        if not isinstance(flight, Flights): 
            self.logger.logger.error(f'{InvalidInput}, input should be Flight obj!')
            raise InvalidInput('input should be Flight obj!')
        elif self.login_token.role != 'Airline': raise InvalidToken
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
        elif self.login_token.role != 'Airline': raise InvalidToken
        elif super().get_airline_by_id(airline_id) == None: 
            self.logger.logger.error(f'{AirlineNotFound}, airline=[{airline_id}] wasnt found!')
            raise AirlineNotFound
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
        elif self.login_token.role != 'Airline': raise InvalidToken
        elif flight['remaining_tickets'] < 0: 
            self.logger.logger.error(f'{NoMoreTicketsLeft}, remaining tickets cannot be < 0!')
            raise NoMoreTicketsLeft
        elif super().get_flight_by_id(flight_id) == None: 
            self.logger.logger.error(f'{FlightNotFound}, flight=[{flight_id}] wasnt found!')
            raise FlightNotFound 
        else: 
            self.logger.logger.info(f'flight has been updated!')
            self.repo.update_by_id(Flights, Flights.id, flight_id, flight)
            print(f'{flight["remaining_tickets"]} remaining flight tickets ID=[{flight_id}]')

    def remove_flight(self, flight_id):
        self.logger.logger.debug(f'removing flight=[{flight_id}] >>>')
        if not isinstance(flight_id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif self.login_token.role != 'Airline': raise InvalidToken
        elif super().get_flight_by_id(flight_id) == None: 
            self.logger.logger.error(f'{FlightNotFound}, flight=[{flight_id}] wasnt found!')
            raise FlightNotFound
        else: 
            self.repo.delete_by_id(Flights, Flights.id, flight_id)
            self.logger.logger.info(f'flight=[{flight_id}], has been deleted!')

    def __str__(self):
        return f'{super().__init__}'
