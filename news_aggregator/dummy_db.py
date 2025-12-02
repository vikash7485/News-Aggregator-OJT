"""
Dummy database backend for Vercel builds where SQLite is not available
"""
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.introspection import BaseDatabaseIntrospection

class DatabaseWrapper(BaseDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.features = type('Features', (), {
            'uses_savepoints': False,
            'can_rollback_ddl': False,
        })()
        self.ops = BaseDatabaseOperations(self)
        self.client = BaseDatabaseClient(self)
        self.introspection = BaseDatabaseIntrospection(self)
    
    def get_connection_params(self):
        return {}
    
    def get_new_connection(self, conn_params):
        return None  # Dummy connection
    
    def ensure_connection(self):
        pass  # No-op
    
    def _close(self):
        pass  # No-op

