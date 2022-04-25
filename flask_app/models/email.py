from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Email:
    db = "email_validation"
    def __init__(self, email_data):
        self.id = email_data['id']
        self.email_address = email_data['email_address']
        self.created_at = email_data['created_at']
        self.updated_at = email_data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"

        email_results = connectToMySQL("email_validation").query_db(
            query
        )
        emails = []
        for email in email_results:
            emails.append(cls(email))
        return emails

    @classmethod
    def save(cls, data):
        query = "INSERT INTO emails (email_address) VALUES (%(email_address)s);"
        return connectToMySQL("email_validation").query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM emails WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_email(email):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # is_valid = False
        query = "SELECT * FROM emails WHERE email_address = %(email_address)s;"
        results = connectToMySQL(Email.db).query_db(query, email)
        if len(results) >= 1:
            flash("Email already taken!")
            return False
        elif not EMAIL_REGEX.match(email['email_address']):
            flash("Invalid Email Address!")
            return False
        return True
