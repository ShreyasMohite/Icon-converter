from flask import Flask,render_template,redirect,url_for,request,send_file,send_from_directory
from flask_uploads import UploadSet,configure_uploads,IMAGES
import os
import time
import imageio
import random
import io
import shutil

app=Flask(__name__)

photos=UploadSet('photos',IMAGES)  

app.config['UPLOADED_PHOTOS_DEST']='getsome'  #directory where images is going to stored


configure_uploads(app,photos)     #configuring in app

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'logos.ico',mimetype='image/vnd.microsoft.icon')



@app.route("/")
def home():
    return render_template("home.html",title="Icon Converter")



@app.route("/upload",methods=['GET','POST'])
def upload():
    if request.method=="POST":

        os.makedirs("getsome", exist_ok=True)  #make directory if not exits
        filename=photos.save(request.files['photo'])  #get the image from inputs
        name=request.files['photo'].filename    #to get image name

        img = imageio.imread(f"getsome/{name}")   #reading the image from file which is created
        ra=random.randint(1,1111)
        logoname=f'logo{ra}.ico'             #giving file a name
        imgs=imageio.imwrite(logoname, img)   #creating icon
        time.sleep(3)                       #time takes to sleep

        with open(logoname,'rb') as file:   #opening that icon image which is created using temporery memory
            return_data = io.BytesIO(file.read())  #reading the file and storing in memory
        return_data.seek(0)              #allocating data in memory

        os.remove(f"getsome/{name}")  #removing the file which we have created 
        os.remove(logoname)            #removing the folder which we have created in starting
        shutil.rmtree("getsome")        #removing the file logoname 
        ran=random.randint(1,100)        
        return send_file(return_data,as_attachment=True,mimetype='image/ico',attachment_filename=f"icon{ran}.ico") #sending file 


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404



port = int(os.environ.get('PORT', 5000))
if __name__=="__main__":
    app.run()


