import tables.Countries
import tables.Administrators
from DbRepo import DbRepo
from db_config import local_session, create_all_entities

repo = DbRepo(local_session)

create_all_entities()

repo.reset_db()

repo.create_all_sp('sp_file.sql')

'''
repo.delete_table('countries')
repo.delete_table('administrators')
repo.delete_table('users')
repo.delete_table('flights')
repo.delete_table('airline_companies')
repo.delete_table('tickets')
repo.delete_table('customers')
repo.delete_table('user_roles')
'''

#repo.add(tables.Countries.Countries(name='argentina'))
#repo.add(tables.Countries.Countries(name='irland'))

#repo.add(tables.Administrators.Administrators(first_name='bobby', last_name='charlton', user_id=3))
