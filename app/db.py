"""
Database Connection Management
============================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: Database connection pooling and management for SQL Server
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module provides connection pooling functionality to efficiently manage
database connections and improve application performance.
"""

import pyodbc
import logging
from app.config import SQLSERVER_DSN, DB_POOL_SIZE
from contextlib import contextmanager
import threading

logger = logging.getLogger(__name__)

# Simple connection pool
class ConnectionPool:
    def __init__(self, dsn, max_connections=10):
        self.dsn = dsn
        self.max_connections = max_connections
        self._pool = []
        self._lock = threading.Lock()
        self._created_connections = 0
    
    def get_connection(self):
        """Get a connection from the pool or create a new one"""
        with self._lock:
            if self._pool:
                # Return existing connection from pool
                connection = self._pool.pop()
                logger.debug("Reusing connection from pool")
                return connection
            elif self._created_connections < self.max_connections:
                # Create new connection
                try:
                    connection = pyodbc.connect(self.dsn)
                    self._created_connections += 1
                    logger.debug(f"Created new connection. Pool size: {self._created_connections}")
                    return connection
                except pyodbc.Error as e:
                    logger.error(f"Failed to create new connection: {e}")
                    raise
            else:
                # Pool is full, wait for a connection to be returned
                logger.warning("Connection pool is full, waiting for available connection")
                raise Exception("Connection pool exhausted")
    
    def return_connection(self, connection):
        """Return a connection to the pool"""
        try:
            # Check if connection is still valid
            if connection and not connection.closed:
                with self._lock:
                    if len(self._pool) < self.max_connections:
                        self._pool.append(connection)
                        logger.debug(f"Connection returned to pool. Pool size: {len(self._pool)}")
                    else:
                        # Pool is full, close the connection
                        connection.close()
                        self._created_connections -= 1
                        logger.debug("Pool full, connection closed")
            else:
                # Connection is invalid, don't return it
                self._created_connections -= 1
                logger.debug("Invalid connection, not returned to pool")
        except Exception as e:
            logger.error(f"Error returning connection to pool: {e}")
            self._created_connections -= 1

# Global connection pool instance
_connection_pool = None

def get_connection_pool():
    """Get or create the global connection pool"""
    global _connection_pool
    if _connection_pool is None:
        if not SQLSERVER_DSN:
            raise ValueError("SQLSERVER_DSN environment variable is not set")
        _connection_pool = ConnectionPool(SQLSERVER_DSN, max_connections=DB_POOL_SIZE)
        logger.info(f"Connection pool initialized with {DB_POOL_SIZE} max connections")
    return _connection_pool

@contextmanager
def get_connection():
    """Get database connection with automatic transaction management and cleanup"""
    pool = get_connection_pool()
    connection = None
    try:
        connection = pool.get_connection()
        logger.debug("Database connection obtained from pool")
        yield connection
        # Se arriviamo qui senza eccezioni, esegui commit
        if connection and not connection.closed:
            connection.commit()
            logger.debug("Transaction committed successfully")
    except pyodbc.Error as e:
        # Errore database: esegui rollback
        if connection and not connection.closed:
            try:
                connection.rollback()
                logger.warning(f"Transaction rolled back due to database error: {e}")
            except Exception as rollback_error:
                logger.error(f"Failed to rollback transaction: {rollback_error}")
        logger.error(f"Database connection failed: {e}")
        raise
    except Exception as e:
        # Errore generico: esegui rollback
        if connection and not connection.closed:
            try:
                connection.rollback()
                logger.warning(f"Transaction rolled back due to error: {e}")
            except Exception as rollback_error:
                logger.error(f"Failed to rollback transaction: {rollback_error}")
        logger.error(f"Unexpected error during database connection: {e}")
        raise
    finally:
        # Restituisci sempre la connessione al pool
        if connection:
            pool.return_connection(connection)
