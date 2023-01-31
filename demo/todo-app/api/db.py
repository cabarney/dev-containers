from dataclasses import dataclass
from datetime import date
import psycopg2
import json


class TodoRepository:
    def __init__(self) -> None:
        pass
    
    def _get_connection(self):
        return psycopg2.connect(database="todos",
                                host="db",
                                user="postgres",
                                password="postgres",
                                port="5432")
        
    
    def _query(self, sql, args = None):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, args)
                return cur.fetchall()
        finally:
            conn.close()        
    
    def _execute(self, sql, args = None):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, args)
                conn.commit()
        finally:
            conn.close()
    
    def get_all(self):
        results = self._query('SELECT "Id", "Title", "DueDate", "Completed" FROM "Todo"')
        results = [self._format_todo(row) for row in results]
        return results
            
    def get(self, todo_id):
        results = self._query('SELECT "Id", "Title", "DueDate", "Completed" FROM "Todo" WHERE "Id"=%s', (todo_id,))
        return self._format_todo(results[0])

    def create(self, todo):
        self._execute("""
            INSERT INTO "Todo" ("Title", "DueDate", "Completed")
            VALUES (%s, %s, %s)
            """,
            [todo[field] for field in ["title", "dueDate", "completed"]])
    
    def update(self, todo_id, todo):
        todo["id"] = todo_id
        self._execute("""
            UPDATE "Todo"
            SET "Title"=%s, "DueDate"=%s, "Completed"=%s
            WHERE "Id" = %s
            """,
            [todo[field] for field in ["title", "dueDate", "completed", "id"]])
    
    def delete(self, todo_id):
        self._execute('DELETE FROM "Todo" WHERE "Id"=%s', (todo_id,))
    
    def _format_todo(self, row):
        return {
            "id": row[0],
            "title": row[1],
            "dueDate": row[2].isoformat(),
            "completed": row[3]
        }
