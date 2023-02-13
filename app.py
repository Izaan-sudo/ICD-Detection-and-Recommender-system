from flask import Flask, flash, request, redirect, render_template,url_for
from keras.models import load_model
# from keras.preprocessing import image
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
import os
import pdfkit
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
# path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
# url= "http://127.0.0.1:5000/a"
# config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtmltopdf )
UPLOAD_FOLDER = 'static/uploads/'
model = load_model('pro.h5')

 

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif',"jfif",",mp4"])

def predict_label(img_path):
    # i = image.load_img(img_path, target_size=(150, 150))
    i = load_img(img_path, target_size=(150, 150))
    # i = load_img(img_path, grayscale=True, target_size=(150, 150))
    # i = image.img_to_array(i)
    i = img_to_array(i)
    i = i.reshape(1, 150, 150, 3)
    # i = i.reshape(1, 48, 48, 3)
    i=i.astype("float32")
    i=i/255.0
    p = model.predict(i)
    print(p[0])
    # if p[0]==0:
    #     p="Head"
    # elif p[0]==1:
    #     p="nail"
    # elif p[0]==2:
    #     p="lips"

  
    p="head" if p[0][0] <= 0.5 else "Nail Biting"
    
    return p
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit( '.' , 1)[1].lower() in ALLOWED_EXTENSIONS
     
@app.route('/')
def home():
    return render_template('index.html')

 
@app.route('/a', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if request.method == 'POST':
        # name = request.form.get('name')
        # username = request.form.get('username')
        # return f'{name}, your username is {username}'
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        name = request.form.get('name')
        # username = request.form.get('username')
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        prediction=predict_label(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dataval = ""
        treatment = ""
        
        if prediction == "Nail Biting":
            dataval="NAIL BITING: Onychophagia is characterized as persistent biting of the fingernails, which typically begins in infancy or early adulthood (1–3). More over half of people of school age are thought to bite their nails frequently or at least periodically (4). Few published research have examined the prevalence of this issue in the general population, and those that have mostly focused on children and adolescents. There are between 20% and 29% of children and teenagers that have onychophagia . Rarely has onychophagia been reported in children under the age of 3-6 years. The frequency of this behavior once again declines by the age of 18, but in some individuals, it may continue into adulthood. The destruction of the fingernails may result from onychophagia, which appears to be a form of compulsion. In routine clinical practise, nail biting—which can range in severity from mild to severe—is an under-recognized issue. According to several research, either too much stimulation (from stress or excitement) or not enough stimulation (from boredom or inaction) can lead to nail biting. In an effort to make their fingernails smooth and look ideal or regular, nail biters frequently bite off rough, damaged, or sticking-out portions of their cuticles or fingernails. Additionally, some people who bite their nails appear to feel happy and relaxed when doing so. Some findings indicated a connection between anxiety or OCD and nail-biting."
            treatment = "Some nail biters—especially those whose habit is less severe—can be helped by traditional methods meant expressly to prevent nail biting, such as applying bitter-tasting items to the nails, but people with chronic, compulsive onychophagia typically find these methods less successful. Because they prevent biting and act as physical cues not to bite, barrier-type therapies that prevent contact between the mouth and nails, like gloves, mittens, socks, and bite-plate devices, may be more successful. They might be hard to use regularly or for a long time, though. Professional treatment can be beneficial in more severe cases of onychophagia, particularly if it concentrates on locating triggers and controlling the emotional aspects of nail-biting. Acceptance and commitment therapy (ACT) and cognitive behavioural therapy (CBT) have been demonstrated to be helpful in some BFRB situations, frequently in conjunction with habit-reversal training and/or progressive muscle relaxation. Any effective treatment for onychophagia requires the consent and cooperation of the kid or adult who bites their nails, in addition to encouraging feedback and regular follow-ups."
        
        elif prediction == "head":
            dataval="Hair twirling, also known as coiling your hair around your finger and tugging it in a circle, is a very typical practise. Fidgeting refers to a collection of habits that includes twisting your hair. Children, in particular, may spin their hair to relieve stress, unwind before bed, or just to pass the time when they are bored. Even if the tendency of twisting your hair may just be a nervous behaviour, it occasionally may indicate a serious health issue. Additionally damaging to your hair, twisting it can cause knots, split ends, and hair breakage. From a nervous habit or a child's diversion, hair twirling can develop into a body-focused repetitive behaviour. There’s also a belief that hair twirling habits can lead to trichotillomania. This is a mental health condition that causes an overwhelming urge to pull out your own hair. It's possible that your practise of twisting your hair in adulthood just developed from infancy. It might also be a sign of another ailment. Perhaps you developed the practise of twirling your hair as a young child and never stopped. According to certain research Trusted Source, this kind of conduct is associated with impatience, boredom, annoyance, and unhappiness. When you're feeling sleepy or bored, twirling your hair can help you relax. It might be a habit if you only twirl your hair while you're trying to stay awake in a meeting or when you're watching your favourite show in your pyjamas. And there's no need to worry unless your hair is thinning or damaged."    
            treatment="The method you opt for if you wish to quit twirling your hair will depend on why you do it. As an adult, you can quit twisting your hair by doing the following: Make use of your hands by knitting or crocheting something useful. Rather than twirling your hair, brush it. To lessen the need to pluck your hair, take good care of it. Find other methods of stress alleviation, including mindfulness or meditation. Ask a psychologist if cognitive behavioural treatment (CBT) could be beneficial. Make little objectives for yourself, such as going two hours without twirling your hair, and treat yourself when you achieve them. To stop spinning as you sleep, wear a hoodie, beanie, or baseball cap. Think about taking an anxiety medicine. Reduce your caffeine and sugar intake. Mittens at bedtime. Fidget devices"
        else:
            dataval="new data"
            

        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and predicted below')
        # pdfkit.from_url(url ,output_path = 'webpage.pdf' , configuration = config)
        return render_template('result.html', filename=filename,prediction=prediction,dataval=dataval,treatment=treatment ,name=name )
        
        
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
    # return pdfkit.from_url(url ,output_path = 'webpage.pdf' , configuration = config)
   

    



 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run(debug=True)


