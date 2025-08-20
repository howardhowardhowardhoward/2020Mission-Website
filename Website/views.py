from flask import *
from .functions import *

views = Blueprint('views', __name__)

@views.route('/info', methods=['GET', 'POST'])
def protected_page_general():
    if not session['logged_in']:
        return redirect(url_for("auth.login"))
    db = current_app.get_db()           # ✅ get db connection
    my_cursor = db.cursor()

    if request.method == "POST":
        form = request.form
        the_button = form.get('submit_button')
        if the_button == 'id':
            ide = form.get('id')
            result = search_by_id(ide, my_cursor)
            if not result:
                session['id'] = ''
                return render_template('General_lookup.html', id_result='Glasses Not Found', attribute_result=session['attributes'], previous_search=session['last search'])
            session['id'] = result
            return render_template('General_lookup.html', id_result=session['id'], attribute_result=session['attributes'], previous_search=session['last search'])
        elif the_button == "attributes":
            details = info_retrieve(form)
            session['last search'] = details
            search_type = request.form.get('search-type')
            if search_type == 'exact':
                glasses_desc = search_by_attributes(cursor=my_cursor, details=details, sph_range=0, cyl_range=0, axis_range=0)
            elif search_type == 'general':
                glasses_desc = search_by_attributes(cursor=my_cursor, details=details, sph_range=0.50, cyl_range=0.50, axis_range=30)
            elif search_type == 'advanced':
                glasses_desc = search_by_attributes(cursor=my_cursor, details=details, sph_range=0.75, cyl_range=0.75, axis_range=60)

            if not glasses_desc:
                session['attributes'] = ''
                return render_template('General_lookup.html', attribute_result='Glasses Not Found', id_result=session['id'], previous_search=session['last search'])

            session['attributes'] = glasses_desc
            return render_template('General_lookup.html', attribute_result=session['attributes'], id_result=session['id'], previous_search=session['last search'])

    return render_template('General_lookup.html', attribute_result=session['attributes'], id_result=session['id'], previous_search=session['last search'])

@views.route('/admin', methods=['GET', 'POST'])
def protected_page_admin():
    if not session['logged_in']:
        return redirect(url_for("auth.login"))
    if session['privilege'] == 1:
        return redirect(url_for('views.protected_page_general'))
    session['id'] = ''
    session['attributes'] = ''
    db = current_app.get_db()           # ✅ get db connection
    my_cursor = db.cursor()

    if request.method == 'POST':
        value = request.form.get('submit_button')
        if value == 'id':
            id = request.form.get("id")
            val = delete_from_database(id, my_cursor)
            if val:
                db.commit()             # ✅ commit on this connection
                return render_template('Admin_page.html', result1='SUCCESS')
            else:
                return render_template('Admin_page.html', result1='ID NOT FOUND')

        elif value == "attributes":
            form = request.form
            details = info_retrieve(form)
            if details['lsph'] and details['rsph'] and details['bridge'] and details['gender']:
                my_cursor.execute("SELECT MAX(id) From Frame")
                ide = my_cursor.fetchall()[0][0] + 1
                val = add_to_database(ids=ide, details=details, cursor=my_cursor)
                if val:
                    db.commit()         # ✅ commit here too
                    return render_template('Admin_page.html', result2="SUCCESS: ID " + str(ide) + " ADDED")
                else:
                    return render_template('Admin_page.html', result2="INVALID INPUTS")
            else:
                return render_template('Admin_page.html', result2='MISSING REQUIRED VALUES')

        elif value == "bulk":
            frame_csv = request.files.get("frame_csv_file")
            lens_csv = request.files.get("lens_csv_file")
            frame_reader = csv_to_list(frame_csv)
            lens_reader = csv_to_list(lens_csv)

            if 2 * len(frame_reader) - 1 == len(lens_reader):
                for i in range(1, len(frame_reader)):
                    if frame_reader[i][0] == lens_reader[2*i][0] and lens_reader[2*i][0] == lens_reader[2*i-1][0] and\
                            lens_reader[2*i-1][1].strip() == 'R' and lens_reader[2*i][1].strip() == 'L':
                        details = {
                            'lsph': lens_reader[2*i][2], 'lcyl': lens_reader[2*i][3], 'laxis': lens_reader[2*i][4], 'ladd': lens_reader[2*i][5],
                            'rsph': lens_reader[2*i - 1][2], 'rcyl': lens_reader[2*i-1][3], 'raxis': lens_reader[2*i-1][4], 'radd': lens_reader[2*i-1][5],
                            'bridge': frame_reader[i][1], 'gender': frame_reader[i][2], 'description': frame_reader[i][3]
                        }
                        val = add_to_database(ids=int(frame_reader[i][0]), details=details, cursor=my_cursor)
                        if not val:
                            return render_template('Admin_page.html', result_3="INVALID INPUTS AT ROW " + str(i))
                    else:
                        return render_template('Admin_page.html', result_3="MISMATCH AT ROW " + str(i))
                db.commit()             # ✅ commit after bulk insert
                return render_template('Admin_page.html', result_3="SUCCESS")
            else:
                return render_template('Admin_page.html', result_3="FAILURE")

    return render_template('Admin_page.html')