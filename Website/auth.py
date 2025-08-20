from flask import *

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    db = current_app.get_db()  # ✅ get a fresh connection
    my_cursor = db.cursor()  # ✅ create cursor from that connection
    my_cursor.execute("SELECT username, password FROM login_info")
    users = my_cursor.fetchall()

    if request.method == "POST":
        usernames = request.form.get('username')
        password = request.form.get('password')
        print(usernames, password)

        if (usernames, password) in users:
            session['logged_in'] = True
            my_cursor.execute("SELECT privileges FROM login_info WHERE username = %s", (usernames,))
            privi = my_cursor.fetchall()
            if privi == [(0,)]:
                session['privilege'] = 0
            else:
                session['privilege'] = 1
            return redirect(url_for('views.protected_page_general'))
        else:
            session['logged_in'] = False
            return render_template("Login_page.html", error="Incorrect Password/Username", username=usernames,
                                   password=password)

    return render_template("Login_page.html")


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))