from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Job:
    db = 'chores'
    def __init__(self,data):
        self.id = data['id']
        self.job = data['job']
        self.description = data['description']
        self.location = data['location']
        self.user_id = data['user_id']
        self.user = []
        self.user_job = []

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO chores
        (job, 
        description,
        location,
        user_id)
        VALUES(
            %(job)s,
            %(description)s,
            %(location)s,
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
        all_jobs = []
        if not results:
            return results
        for this_job in results:
            new_job = cls(this_chore)
            this_user = {
                'id':this_job['users.id'],
                'first_name':this_job['first_name'],
                'last_name':this_job['last_name'],
                'email':this_job['email'],
                'password':this_job['password'],
                'created_at':this_job['created_at'],
                'updated_at':this_job['updated_at'],
            }
            new_job.user=user.User(this_user)
            all_jobs.append(new_job)
        return all_jobs

    @classmethod
    def get_one(cls,data):
        query = """
        SELECT *
        FROM chores
        WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])