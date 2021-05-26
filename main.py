from flask import render_template, request, redirect, flash
from persistence_layer import *
from app import app


authenticated_user = ''


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if len(authenticated_user) == 0:
            return "need to sign in "
        else:
            town_add = request.form['town']
            address_add = request.form['address']
            title_add = request.form['title']
            id = 0
            try:
                town_search = Town.find(town=town_add)
                if len(town_search) == 0:
                    Town.add(town=town_add)

                address_search = Address.find(town=town_add, address=address_add)
                if len(address_search) == 0:
                    addr = Address.add(town=town_add, address=address_add)
                    id = addr.place_id
                else:
                    addr = address_search
                    for aa in addr:
                        id = aa.place_id

                witness = Witness_accident.add(place_id=id, title=title_add)
                witn_id = witness.witness_id
                Call_911(operator_pass_id=authenticated_user, call_begin=datetime.today(), witness_id=witn_id, call_end=None).add()
                return redirect('/')
            except:
                return 'There was an issue'
    else:
        accidents = Call_911.main_query()
        return render_template('index.html', accidents=accidents)


@app.route('/sign-in/', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        pass_id = request.form['passport']
        authentication = Operator_911.find(operator_pass_id=pass_id)
        if len(authentication) == 0:
            flash("Invalid input. Try again")
            return render_template('sign-in.html')
        else:
            global authenticated_user
            authenticated_user = pass_id
            return redirect('/')
    return render_template('sign-in.html')


@app.route('/delete/<string:operator_pass_id>/<string:call_begin>', methods=('GET', 'POST'))
def delete(operator_pass_id, call_begin):
    call_to_delete = Call_911.find(operator_pass_id=operator_pass_id, call_begin=call_begin)
    try:
        Call_911.delete_self(*call_to_delete)
        return redirect('/')
    except:
        return 'problem in deleting'


@app.route('/update/<string:operator_pass_id>/<string:call_begin>', methods=('GET', 'POST'))
def update(operator_pass_id, call_begin):
    accident = Call_911.main_query(operator_pass_id=operator_pass_id, call_begin=call_begin)
    op_update = list(accident[0])[0]
    witness_id = 0
    if request.method == 'POST':
        for call, witness_accident, addr in accident:
            witness_id = witness_accident.witness_id
        title = request.form['title']
        wit = Witness_accident.find(witness_id=witness_id)[0]
        try:
            if len(authenticated_user) == 0:
                return "Need to sign in"
            else:
                op_update.operator_update(pass_id=authenticated_user)
                wit.title_update(new_title=title)
                return redirect('/')
        except:
            return 'issue updating'
    return render_template('update.html', accidents=accident)


if __name__ == "__main__":
    app.run(debug=False)



