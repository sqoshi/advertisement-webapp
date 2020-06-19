import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')+'?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

"""
user
{% extends "base.html" %}

{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}"></td>
            <td>
                <h1>User: {{ user.username }}</h1>
                {% if user.about_me %}<p>{{ user.about_me }}</p>{% endif %}
                {% if user.last_seen %}<p>Last seen on: {{ user.last_seen }}</p>{% endif %}
                {% if user == current_user %}
                    <p><a href="{{ url_for('edit_profile') }}">Edit your profile</a></p>
                {% endif %}
            </td>
        </tr>
    </table>
    <hr>
    {% for post in posts %}
        {% include '_announcement.html' %}
    {% endfor %}
{% endblock %}"""