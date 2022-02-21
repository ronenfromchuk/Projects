from logger import Logger
from abc import ABC, abstractmethod
from datetime import datetime
from exceptions.ExceptionShortPassword import WrongPassword
from exceptions.ExceptionAirlineNotFound import AirlineNotFound
from exceptions.ExceptionFlightNotFound import FlightNotFound
from exceptions.ExceptioWrongInput import InvalidInput
from exceptions.ExceptionWrongCountry import InvalidCountry
from tables.Flights import Flights
from tables.Users import Users
from tables.Airline_Companies import AirlineCompanies
from tables.Countries import Countries


class FacadeBase(ABC):

    @abstractmethod
    def __init__(self, repo, config):
        self.repo = repo
        self.config = config
        self.logger = Logger.get_instance()

    def get_all_flights(self):
        self.logger.logger.info(f'displaying flights!')
        return self.repo.get_all(Flights)

    def get_flight_by_id(self, id):
        self.logger.logger.debug(f'reaching flight id={id} >>>')
        if not isinstance(id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif self.repo.get_by_id(Flights, id) == None: 
            self.logger.logger.error(f'{FlightNotFound}, flight=[{id}] wasnt found!')
            raise FlightNotFound
        else: 
            self.logger.logger.info(f'displaying flight!')
            return self.repo.get_by_id(Flights, id)

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        self.logger.logger.debug(f'reaching flights by parameters >>>')
        if not isinstance(origin_country_id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif not isinstance(destination_country_id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif not isinstance(date, datetime):  
            self.logger.logger.error(f'{InvalidInput}, input should be datetime obj!')
            raise InvalidInput('input should be datetime obj!')
        elif self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.origin_country_id == origin_country_id, Flights.destination_country_id == destination_country_id, Flights.departure_time == date)) == []: 
            self.logger.logger.error(f'{FlightNotFound}, flight wasnt found!')
            raise FlightNotFound
        else: 
            self.logger.logger.info(f'displaying flight!')
            return self.repo.get_by_condition(Flights, lambda query: query.filter(Flights.origin_country_id == origin_country_id, Flights.destination_country_id == destination_country_id, Flights.departure_time == date))

    def get_all_airlines(self):
        self.logger.logger.info(f'Airlines displayed!')
        return self.repo.get_all(AirlineCompanies)

    def get_airline_by_id(self, id):
        self.logger.logger.debug(f'getting airline by id=[{id}] >>>')
        if not isinstance(id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif self.repo.get_by_id(AirlineCompanies, id) == None: 
            self.logger.logger.error(f'{AirlineNotFound}, airline wasnt found!')
            raise AirlineNotFound
        else: 
            self.logger.logger.info(f'displaying ariline!')
            return self.repo.get_by_id(AirlineCompanies, id)

    def get_all_countries(self):
        self.logger.logger.info(f'displaying all countries!')
        return self.repo.get_all(Countries)

    def get_country_by_id(self, id):
        if not isinstance(id, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be int!')
            raise InvalidInput('input should be int!')
        elif self.repo.get_by_id(Countries, id) == None: 
            self.logger.logger.error(f'{InvalidCountry}, country=[{id}] wasnt found!')
            raise InvalidCountry
        else: 
            self.logger.logger.info(f'displaying country!')
            return self.repo.get_by_id(Countries, id)

    def create_user(self, user):
        if not isinstance(user, Users): 
            self.logger.logger.error(f'{InvalidInput}, input should be Users obj!')
            raise InvalidInput('input should be Users obj!')
        elif len(user.password) < 6: 
            self.logger.logger.error(f'{WrongPassword}, password must be at least 6 chars!')
            raise WrongPassword
        else: 
            self.logger.logger.info(f'User=[{user.username}], has been created!')
            self.repo.add(user)

    def __str__(self):
        return f'facade_base_repo: {self.repo}'