# Announce Web Application
## Table of Contests
1. [ Synopsis ](#Synopsis)
2. [ Code Example ](#Code-Example)
3. [ Motivation ](#Motivation)
4. [ Screenshots ](#Screenshots)
5. [ Installation ](#Installation)
6. [ Launch ](#Launch)
7. [ Tests ](#Tests)
8. [ License ](#License)


## Synopsis

Web announce application that fulfills second Richardson's criteria what makes it a rest-api.
 Application has it's own logging and registration system where users' accounts
are being stored in SQLite database. Application allows to create posts that users can pin to the announce main page.
Each user can search trough announces. The possibilities of this api are huge. It can be used by students to earn some additive money
by posting private lessons services. People can sell items which are not longer needed or look for items that they want to buy.
It can be used to advertise their companies or all kind of services. Each user has his own profile with avatar 
and some simple information like about section, account created that can be updated whenever they want to.
They are allowed to check other users profiles and communicate with them using their emails or phone numbers
Users can also delete their old announces whenever they want.
## Code Example

```python
def add_announcement():
    """
    Adding new announcement in browser by routing to other temp-form
    :return:
    """
    form = AnnouncementForm()
    if form.validate_on_submit():
        u = Announcement(body=form.body.data, name=form.name.data, price=form.price.data, user_id=current_user.id)
        db.session.add(u)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('add_announcement'))
    return render_template('add_announcement.html', title='Add announce',
                           form=form)
```
## Motivation

Application have been created to make place where people can sell their stuff, buy some
new things. To create place where people can advertise their services, companies or even private lessons.

## Screenshots
![Alt text](screen.png?raw=true "Title")

## Installation

Flask and python are only needed to use this app.

## Launch

`python -m flask run`

## Technologies
- Python
- Flask
- SQLite
- SQLAlchemy
- Requests
- Postman
- CSS 3
- HTML 5


## Tests

Application had been tested with Postman.

## License
Open- Source
