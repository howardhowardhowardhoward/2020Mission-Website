import csv
import io

#Form retrieval functions
def info_retrieve(form) -> dict:
    LCYL, LSPH, LAxis, LADD = form.get("cyl_left"), form.get("sph_left"), form.get("axis_left"), form.get("add_left")
    RCYL, RSPH, RAxis, RADD = form.get("cyl_right"), form.get("sph_right"), form.get("axis_right"), form.get(
        "add_right")
    bridge, gender, description = form.get("bridge size"), form.get("gender"), form.get("description")
    return  {'lsph' :LSPH, 'lcyl':LCYL, 'laxis': LAxis, 'ladd':LADD, 'rsph':RSPH, 'rcyl': RCYL, 'raxis': RAxis,
             'radd': RADD, 'bridge':bridge, 'gender': gender, 'description': description}

#DATABASE MODIFIER FUNCTIONS
def add_to_database(ids: int, details: dict, cursor) -> bool:
    """
    Adds one eyeglass to the database based off given values
    Returns True iff operation is successful
    Precondition: ids, lsph, rsph, bridge, gender, cursor are given
    """
    my_cursor = cursor
    id = ids
    lsph, lcyl, laxis, ladd = details['lsph'], details['lcyl'], details['laxis'], details['ladd']
    rsph, rcyl, raxis, radd = details['rsph'], details['rcyl'], details['raxis'], details['radd']
    bridge, gender, description = details['bridge'], details['gender'], details['description']

    try:
        if not description or description == '':
            my_cursor.execute("INSERT INTO Frame (id, bridge_size, gender) VALUES (%s, %s, %s)", (id, bridge, gender))
        else:
            my_cursor.execute("INSERT INTO Frame (id, bridge_size, gender, description) VALUES (%s, %s, %s, %s)", (id, bridge, gender, description))

        spot1 = "id, eye, SPH"
        spot2 = "id, eye, SPH"
        value1 = [id, 'L', lsph]
        value2 = [id, 'R', rsph]

        if lcyl and lcyl != "":
            value1.append(lcyl)
            spot1 += ", CYL"
        if laxis and laxis != "":
            value1.append(laxis)
            spot1 += ", Axis"
        if ladd and ladd != "":
            value1.append(ladd)
            spot1 += ", `ADD`"

        if rcyl and rcyl != "":
            value2.append(rcyl)
            spot2 += ', CYL'
        if raxis and raxis != "":
            value2.append(raxis)
            spot2 += ", Axis"
        if radd and radd != "":
            value2.append(radd)
            spot2 += ", `ADD`"

        placeholders1 = ", ".join(["%s"] * len(value1))
        query1 = f"INSERT INTO Lens ({spot1}) VALUES ({placeholders1})"
        my_cursor.execute(query1, value1)

        placeholders2 = ", ".join(["%s"] * len(value2))
        query2 = f"INSERT INTO Lens ({spot2}) VALUES ({placeholders2})"
        my_cursor.execute(query2, value2)
        return True
    except:
        return False

def delete_from_database(ids: int, cursor) -> bool:
    """
    Deletes one eyeglass from database based on given id
    Returns True iff operation is successful
    """
    my_cursor = cursor
    id = ids
    my_cursor.execute('SELECT * FROM FRAME WHERE id = %s', (id,))
    glass = my_cursor.fetchall()
    if glass:
        my_cursor.execute('DELETE FROM Frame WHERE id = %s', (id,))
        my_cursor.execute('DELETE FROM LENS WHERE id = %s', (id,))
        return True
    else:
        return False

def csv_to_list(cv)-> list:
    """
    Returns CSV file as a list
    """
    cv.seek(0)
    csv_text = io.TextIOWrapper(cv, encoding='utf-8')
    return list(csv.reader(csv_text))


#DATABASE SEARCH FUNCTIONS
def search_by_id(id: int, my_cursor) -> list:
    """
    Returns the details of the eyeglass with the specified id in the form of a list
    """
    query = """
    SELECT Frame.id, Frame.bridge_size, Frame.gender, Frame.description,
           l1.sph, l1.cyl, l1.axis, l1.add,
           l2.sph, l2.cyl, l2.axis, l2.add
    FROM Frame
    JOIN Lens l1 ON Frame.id = l1.id AND l1.Eye = 'L'
    JOIN Lens l2 ON Frame.id = l2.id AND l2.Eye = 'R'
    WHERE Frame.id = %s
    """
    my_cursor.execute(query, (id,))
    glasses_desc = my_cursor.fetchall()
    return glasses_desc

def search_by_attributes(cursor, details: dict, sph_range = None, cyl_range = None, axis_range = None) -> list:
    """
    Returns the details of the eyeglasses which meet the specified criteria
    """
    lsph, lcyl, laxis, ladd = details['lsph'], details['lcyl'], details['laxis'], details['ladd']
    rsph, rcyl, raxis, radd = details['rsph'], details['rcyl'], details['raxis'], details['radd']
    bridge, gender, description = details['bridge'], details['gender'], details['description']
    try:
        my_cursor = cursor
        query_call = """
        SELECT Frame.id, Frame.bridge_size, Frame.gender, Frame.description,
               l1.sph, l1.cyl, l1.axis, l1.add,
               l2.sph, l2.cyl, l2.axis, l2.add
                FROM Frame JOIN Lens l1 ON Frame.id = l1.id AND l1.Eye = 'L'
            JOIN Lens l2 ON Frame.id = l2.id AND l2.Eye = 'R'
            WHERE"""
        if lsph:
            query_call += ' l1.sph BETWEEN ' + str(float(lsph) - sph_range) + ' AND ' + str(float(lsph) + sph_range) + ' AND'
        if lcyl:
            query_call += " l1.cyl BETWEEN " + str(float(lcyl) - cyl_range) + ' AND ' + str(float(lcyl) + cyl_range) + ' AND'
        if laxis:
            query_call += ' l1.axis BETWEEN ' + str(float(laxis) - axis_range) + ' AND ' + str(float(laxis) + axis_range) + ' AND'
        if ladd:
            query_call += ' l1.add = ' + ladd + ' AND'

        if rsph:
            query_call += ' l2.sph BETWEEN ' + str(float(rsph) - sph_range) + ' AND ' + str(float(rsph) + sph_range) + ' AND'
        if rcyl:
            query_call += " l2.cyl BETWEEN " + str(float(rcyl) - cyl_range) + ' AND ' + str(float(rcyl) + cyl_range) + ' AND'
        if raxis:
            query_call += ' l2.axis BETWEEN ' + str(float(raxis) - axis_range) + ' AND ' + str(float(raxis) + axis_range) + ' AND'
        if radd:
            query_call += ' l2.add = ' + radd + ' AND'

        if bridge:
            query_call += ' Frame.bridge_size = ' + bridge + ' AND'
        if gender:
            query_call += " (Frame.gender = '" + gender + "' OR Frame.gender = 'MF') AND"
        if description:
            query_call += " Frame.description = '" + description + "' AND"

        if (not lcyl and not lsph and not laxis and not rcyl and not rsph
                and not raxis and not bridge and not gender
                and not radd and not ladd and not description):
            query_call = query_call[:-5] + " LIMIT 10 OFFSET 0"
        else:
            query_call = query_call[:-3] + " LIMIT 10 OFFSET 0"

        my_cursor.execute(query_call)
        result = my_cursor.fetchall()
        return result
    except:
        return []