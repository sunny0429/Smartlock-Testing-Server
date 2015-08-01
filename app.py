from flask import Flask, jsonify, render_template
from flask import abort
from flask import make_response,request
import requests
import json
from pushjack import GCMClient
import sqlite3 as sql

DATABASE = 'SmartlockUser.db'
client = GCMClient(api_key='AIzaSyAG4qhcqNqkJLtBQTmljCI8ijWuBtFY_YM')

app= Flask(__name__)
app.config.from_object(__name__)


app.secret_key = 'my key'


#-------------------------------------------------ANDROID-APP-POST-REQUESTS-------------------------------------------------------------------------

#save details of user into database
@app.route('/smartlock/regis', methods=['POST'])
def create_user():
	
	Username = request.json['Username']
	Password = request.json['Password']
	Regiskey = request.json['Regiskey']
	con = sql.connect("SmartlockUser.db")
	cur = con.cursor()
	cur.execute("INSERT INTO SmartlockUser (Username,Password,Regiskey) VALUES (?,?,?)", (Username,Password,Regiskey))
	con.commit()
	con.close()
	return make_response(jsonify({'success': 'success'}), 200)

	
#seperate method just to post raspkey so that the login is not clubbed with the raspkey
@app.route('/smartlock/raspkey', methods=['POST'])
def add_raspkey():
	Raspkey = request.json['Raspkey']
	con = sql.connect("SmartlockUser.db")
	cur = con.cursor()
	cur.excute("INSERT INTO Raspkey(KEY) VALUES (?)",(Raspkey))
	con.commit()
	con.close()
	return make_response(jsonify({'success': 'success'}), 200)

#post the request to rasp to lock or unlock	
@app.route('/smartlock/action', methods=['POST'])	
def call_rasp():
	Action = request.json('keyword')
	cur.execute('SELECT IP FROM Raspip')
	url = cur.fetchall()[0]
	if url != null:
		headers = {'content-type': 'application/json'}
		r = requests.post(url, data=json.dumps(Action), headers=headers)
	# report user to reset rasp
	else:
		con = sql.connect("SmartlockUser.db")
		cur = con.cursor()
		cur.execute('SELECT Regiskey FROM SmartlockUser')
		regid = cur.fetchall()[0]
		alert = {'message': 'Reset your Raspberry'};
		res = client.send(regid,alert,collapse_key='collapse_key',delay_while_idle=True,time_to_live=604800)
		print(res.responses)

	return make_response(jsonify({'success': 'success'}), 200)


		
#--------------------------------RASBERRY-POST-REQUEST----------------------------------------------------------------------------------------------
		
		
#raspberry pie sends key and matches with key registered by the user from app, then saves it else report to the user		
@app.route('/smartlock/raspkey', methods=['POST'])		
def rasp():
	Key = request.json('key')
	con = sql.connect("SmartlockUser.db")
	cur = con.cursor()
	cur.execute('SELECT KEY FROM Raspkey')
	raspkey = cur.fetchall()[0]
	if Key == raspkey:
		cur.execute("INSERT INTO Raspkey(KEY) VALUES(?)",(Key))
	else:
		alert = {'message':'Rasp key does not match, Kindly Re-enter your key'}
		cur.execute('SELECT Regiskey FROM SmartlockUser')
		regid = cur.fetchall()[0]
		res = client.send(regid,
                  alert,
                  collapse_key='collapse_key',
                  delay_while_idle=True,
                  time_to_live=604800)
		print(res.responses)
	con.close()
	return make_response(jsonify({'success': 'success'}), 200)

#raspberry pie updates the ip address of its network(if changes)
@app.route('/smartlock/IP', methods=['PUT'])
def rasp_ip():
	IP = request.json('ip')
	con = sql.connect("SmartlockUser.db")
	cur = con.cursor()
	cur.execute("INSERT INTO Raspip (IP) VALUES (?)", (IP))
	con.commit
	con.close
	return make_response(jsonify({'success': 'success'}), 200)

	
#raspberry sends the changed status of the lock, message given to user	
@app.route('/smartlock/message', methods=['POST'])
def message():
	message = request.json('message')
	con = sql.connect("SmartlockUser.db")
	cur = con.cursor()
	cur.execute('SELECT Regiskey FROM SmartlockUser')
	regid = cur.fetchall()[0]
	alert = {'message': message};
	res = client.send(regid,
                  alert,
                  collapse_key='collapse_key',
                  delay_while_idle=True,
                  time_to_live=604800)
	print(res.responses)			  
	return make_response(jsonify({'success': 'success'}), 200)
	
if __name__ == '__main__':
	app.run(debug=True)
