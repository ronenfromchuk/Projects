from DbRepo import DbRepo
from db_config import local_session, create_all_entities

repo = DbRepo(local_session)

create_all_entities()

repo.reset_db()

repo.create_all_sp('sp_file.sql')

