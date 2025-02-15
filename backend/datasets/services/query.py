import stardog
from requests import Session

from abc import ABC, abstractmethod

from datasets.services.stardog_api import StardogApi


class QueryExecutionException(Exception):
    pass


class QueryService(ABC):
    @abstractmethod
    def query(self, query: str, limit: int = 10, timeout: int = None, **options) -> dict:
        pass


class LocalQueryService(QueryService):
    database: str

    def __init__(self, database: str):
        self.database = database

    def query(self, query: str, limit: int = 10, timeout: int = None, **options) -> dict:
        try:
            with StardogApi.connection(self.database) as conn:
                if 'LIMIT' in query:
                    limit=None
                output = conn.select(query, limit=limit, timeout=timeout)

            return output
        except stardog.exceptions.StardogException as e:
            raise QueryExecutionException(str(e))


class SPARQLQueryService(QueryService):
    endpoint: str

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def query(self, query: str, limit: int = 10, timeout: int = None, ignore_limit=False, **options) -> dict:
        if 'LIMIT' not in query and not ignore_limit:
            raise QueryExecutionException(f'SPARQL queries must specify a LIMIT')

        with Session() as session:
            response = session.post(
                self.endpoint,
                data=query,
                params={
                    'limit': limit,
                    'timeout': timeout,
                },
                headers={
                    'User-Agent': 'https://github.com/EgorDm/BOLD',
                    'Content-Type': 'application/sparql-query',
                    'Accept': 'application/sparql-results+json',
                },
                timeout=timeout,
                allow_redirects=False
            )

            retry_count = 0
            while response.status_code // 100 == 3 and retry_count < 3:
                request = response.request
                request.url = response.headers.get('Location')
                response = session.send(response.request)
                retry_count += 1

        if response.status_code != 200:
            raise QueryExecutionException(f'{response.status_code} {response.reason}\n{response.text}')

        return response.json()
