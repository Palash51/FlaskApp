from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from bs4 import BeautifulSoup																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																		
import dryscrape

app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'soup'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()




@app.route("/")
def main():
	return render_template('interface.html')


@app.route('/interface',methods=['POST'])
def interface():
 
    # read the posted values from the UI
    search_item = request.form['inputid']
    try:
    	cursor.execute("select {0} from cars;".format(search_item))
    	data = cursor.fetchall()
    except Exception as e:
    	cursor.execute("alter table cars add({0} varchar(250) CHARSET=utf8)".format(search_item))    
    session = dryscrape.Session()
    session.visit("https://www.google.co.in/?gfe_rd=cr&ei=ja7vV4aWHITy8Af784CQAg#q={0}".format(search_item))
    response = session.body()
    soup = BeautifulSoup(response)
    a = soup.find_all("h3", class_="r")
    for tag in a:
    	child_tg = tag.find("a")
    	q=""
    	for i in child_tg.text:
    		if i.isalpha():
        		q = "".join([q,i])
    	cursor.execute("insert into cars values(\"{0}\")".format(q.encode('utf-8')))

    
    
 



if __name__ == "__main__":
	app.run(debug=True)	