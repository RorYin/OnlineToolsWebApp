from email import message
from flask import Flask,render_template,request,redirect
from cryptography.fernet import Fernet
#For Encryption 
key = "P0mpAZyn3WGpj88GFGewWwmY4OI4JxZyxeJ3-UKUH6A="
crypter = Fernet(key)


app=Flask(__name__)
app.url_map.strict_slashes=False

@app.route('/',methods=['GET', 'POST'])
def home():
    
    return render_template("index.html")

@app.route('/gen',methods=['GET', 'POST'])
def display():
    # enc = bytes(request.get_data(),'utf-8')
    # decurl =str(crypter.decrypt(enc),'utf8')
    # print(decurl)
    # return decurl

    
    if (request.method=="POST"):
        data=request.form
        # print(data)
        name=data['name']
        celebrant=data['celebrant']
        imgurl=data['imgurl']

        # print(name,celebrant,imgurl)
        data=bytes(name+"|"+celebrant+"|"+imgurl, 'utf-8')
        enc=crypter.encrypt(data)
        # print(enc)
        decurl =str(crypter.decrypt(enc),'utf8')
        # print(decurl)
        return redirect(f"./happybirthday?enc={enc}")
        
        
        return render_template("main.html",celebrant=celebrant,name=name,imgurl=imgurl)
        
@app.route("/happybirthday",methods=['GET', 'POST'])
def wish():
    
    encurl=request.args.get('enc')
    encurl=encurl.strip("b'")
    encurl=encurl.strip("'")
    enc = bytes(encurl, 'utf-8')  
    decurl =str(crypter.decrypt(enc),'utf-8') 
    # print(type(encurl))
    # print(encurl)
    # print(decurl)
    
    name=(decurl.split("|"))[0]
    celebrant=(decurl.split("|"))[1]
    imgurl=(decurl.split("|"))[-1]

    return render_template("main.html",celebrant=celebrant,name=name,imgurl=imgurl)
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
