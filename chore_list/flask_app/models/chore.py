from lib2to3.pytree import _Results
from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Chore:
    db = 'chores'
    def __init__(self,data):
        self.id = data['id']
        self.chore = data['chore']
        self.description = data['description']
        self.completed = data['date_last_completed']
        self.notes = data['notes']
        self.recurring_date = data['recurring_date']
        self.completed_by = data['completed_by']
        self.user_id = data['user_id']
        self.user = []
        self.user_chore = []

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO chores
        (chore, 
        description,
        date_last_completed,
        notes, 
        recurring_date,
        completed_by,
        user_id)
        VALUES(
            %(chore)s,
            %(description)s,
            %(date_last_completed)s,
            %(notes)s,
            %(recurring_date)s,
            %(completed_by)s,
            %(user_id)s
        )
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = """
        SELECT * 
        FROM chores
        JOIN users
        ON chores.user_id=users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_chores = []
        if not results:
            return results
        for this_chore in results:
            new_chore = cls(this_chore)
            this_user = {
                'id':this_chore['users.id'],
                'first_name':this_chore['first_name'],
                'last_name':this_chore['last_name'],
                'email':this_chore['email'],
                'password':this_chore['password'],
                'created_at':this_chore['created_at'],
                'updated_at':this_chore['updated_at'],
            }
            new_chore.user=user.User(this_user)
            all_chores.append(new_chore)
        return all_chores