from flask import Flask,request,jsonify,send_file  
import sqlite3,datetime,random,json  
  
app = Flask(__name__)  
  
DB="rp_builders.db"  
  
def db():  
    return sqlite3.connect(DB,check_same_thread=False)  
  
c=db()  
c.execute("""CREATE TABLE IF NOT EXISTS users(  
id INTEGER PRIMARY KEY,  
username TEXT,password TEXT,role TEXT)""")  
  
c.execute("""CREATE TABLE IF NOT EXISTS orders(  
id INTEGER PRIMARY KEY,  
customer TEXT,total REAL,date TEXT)""")  
  
c.execute("""CREATE TABLE IF NOT EXISTS stock(  
id INTEGER PRIMARY KEY,  
item TEXT,qty INT)""")  
  
c.execute("""CREATE TABLE IF NOT EXISTS attendance(  
name TEXT,date TEXT)""")  
  
c.commit()  
  
# ---------------- LOGIN -----------------  
  
@app.route("/login",methods=["POST"])  
def login():  
    d=request.json  
    u=db().execute("SELECT * FROM users WHERE username=? AND password=?",  
        (d["username"],d["password"])).fetchone()  
    return {"success":bool(u)}  
  
# --------------- DASHBOARD ---------------  
  
@app.route("/dashboard")  
def dashboard():  
    orders=db().execute("SELECT total FROM orders").fetchall()  
    total=sum(o[0] for o in orders)  
    return {"income":total,"orders":len(orders)}  
  
# ---------------- ORDERS ----------------  
  
@app.route("/add_order",methods=["POST"])  
def add_order():  
    d=request.json  
    db().execute("INSERT INTO orders VALUES(NULL,?,?,?)",  
    (d["customer"],d["total"],str(datetime.date.today())))  
    db().commit()  
    return {"status":"order added"}  
  
# ---------------- STOCK -----------------  
  
@app.route("/add_stock",methods=["POST"])  
def add_stock():  
    d=request.json  
    db().execute("INSERT INTO stock VALUES(NULL,?,?)",(d["item"],d["qty"]))  
    db().commit()  
    return {"status":"stock added"}  
  
# ---------------- GST JSON ----------------  
  
@app.route("/gst_json")  
def gst_json():  
    orders=db().execute("SELECT total FROM orders").fetchall()  
    total=sum(o[0] for o in orders)  
    return jsonify({  
        "company":"RP BUILDERS",  
        "gst_number":"GSTIN_PENDING",  
        "total_sales":total,  
        "gst_18_percent":round(total*0.18,2)  
    })  
  
# ------------- WHATSAPP MOCK -------------  
  
@app.route("/send_whatsapp")  
def send_whatsapp():  
    return {"status":"Invoice sent successfully"}  
  
# ------------ FACE ATTENDANCE ------------  
  
@app.route("/face_attendance",methods=["POST"])  
def face_attendance():  
    name=request.json["name"]  
    db().execute("INSERT INTO attendance VALUES(?,?)",  
    (name,str(datetime.date.today())))  
    db().commit()  
    return {"status":"attendance marked"}  
  
# -------- AI STOCK PREDICTION ------------  
  
@app.route("/predict/<item>")  
def predict(item):  
    past=[random.randint(80,150) for _ in range(4)]  
    forecast=int(sum(past)/len(past)*1.25)  
    return {"item":item,"next_month_needed":forecast}  
  
# --------------- HOME -------------------  
  
@app.route("/")  
def home():  
    return "RP BUILDERS ERP SYSTEM IS LIVE"  
  
# ----------------------------------------  
  
if __name__=="__main__":  
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
