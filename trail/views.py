from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import subprocess
import os,shutil
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write,read
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import file
import os.path
import ffmpeg
import numpy as np
import matplotlib.pyplot as plt
import numpy as np


# Create your views here.
def song(request):
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('media/output.wav', fs, myrecording) 
    return render(request,'upload.html');

def home(request):
    return render(request,'index.html');

def upload(request):
    if request.method == 'POST':
        context ={}
        doc = request.FILES
        uploaded_file = doc['d']
        name = uploaded_file.name
        if name.endswith(".mp3") or name.endswith('wav') or name.endswith('.mp4'):
            try:
                os.unlink(os.path.join(os.getcwd(),'media',"a.mp3"))
            except:
                print("No mp3 file in media directory")

            try:
                os.unlink('a.mp3')
            except:
                print("No mp3 file in media directory")
            try:
                os.unlink(os.path.join(os.getcwd(),'media',"combined.wav"))
            except:
                print("No file in media directory")

            fs = FileSystemStorage()
            nn = fs.save('a.mp3',uploaded_file)
            try:
                shutil.copy(os.path.join(os.getcwd(),'media',"a.mp3"), os.getcwd())
            except:
                print("Unable to copy")
            context['url'] = fs.url(nn)
            cmd = "spleeter separate -i a.mp3 -o media/"
            subprocess.check_output(cmd)
            
            return render(request,'show.html',context)
        else:
            print("Upload only .mp3 or .wav files")
    return render(request,'upload.html');

def combine(request):
    if request.method == 'POST':
        context ={}
        doc = request.FILES
        uploaded_file = doc['d']
        name = uploaded_file.name
        if name.endswith(".mp4") or name.endswith('wav') or name.endswith('.mp3'):
            try:
                os.unlink(os.path.join(os.getcwd(),'media',"combined.wav"))
            except:
                print("No file in media directory")
            try:
                os.unlink(os.path.join(os.getcwd(),'media',"sing.wav"))
            except:
                print("No file in media directory")

            fs = FileSystemStorage()
            nn = fs.save('sing.wav',uploaded_file)
            
            context['url'] = fs.url(nn)
            try:
                sound1 = AudioSegment.from_file(os.path.join(os.getcwd(),"media","sing.wav"))
                sound2 = AudioSegment.from_file(os.path.join(os.getcwd(),"media","a","accompaniment.wav"))

                combined = sound1.overlay(sound2)

                combined.export(os.path.join(os.getcwd(),"media","combined.wav"), format='wav')
            except:
                print("Problem in combining")
            return render(request,'comb.html',context)
        else:
            print("Upload only .mp3 or .wav files")
    return render(request,'show.html');

def recorder(request):
    return render(request,'recorder.html');

def save(request):
    if request.method == 'POST':
        current_user = request.user
        dirr = "media/"+str(current_user.id)+"/"
        dirs = "media/"+str(current_user.id)+"/song/"
        dirv = "media/"+str(current_user.id)+"/vocals/"
        dirm = "media/"+str(current_user.id)+"/music/"
        try:
            os.mkdir(dirr)
            os.mkdir(dirs)
            os.mkdir(dirv)
            os.mkdir(dirm)
        except:
            print("unable to create directory")
        try:
           shutil.copy(os.path.join(os.getcwd(),'media',"a.mp3"), os.path.join(os.getcwd(),'media',str(current_user.id),'song'))
        except:
            print("Unable to copy")
        try:
           shutil.copy(os.path.join(os.getcwd(),'media','a',"vocals.wav"), os.path.join(os.getcwd(),'media',str(current_user.id),'vocals'))
        except:
            print("Unable to copy")
        try:
           shutil.copy(os.path.join(os.getcwd(),'media','a',"accompaniment.wav"), os.path.join(os.getcwd(),'media',str(current_user.id),'music'))
        except:
            print("Unable to copy")

        name = request.POST['name']
        namee = name+'.mp3'
        try:
            object = file.objects.filter(name__iexact = name, user_id = current_user.id)
        except:
            object = None
        
        if object:
            return render(request,'save.html');
        else:
            try:
                old_file = os.path.join(os.getcwd(),'media',str(current_user.id),'song','a.mp3')
                new_file = os.path.join(os.getcwd(),'media',str(current_user.id),'song',namee)
                os.rename(old_file, new_file)
            except:
                print("Unable to rename")
            try:
                old_file = os.path.join(os.getcwd(),'media',str(current_user.id),'vocals','vocals.wav')
                new_file = os.path.join(os.getcwd(),'media',str(current_user.id),'vocals',namee)
                os.rename(old_file, new_file)
            except:
                print("Unable to rename")
            try:
                old_file = os.path.join(os.getcwd(),'media',str(current_user.id),'music','accompaniment.wav')
                new_file = os.path.join(os.getcwd(),'media',str(current_user.id),'music',namee)
                os.rename(old_file, new_file)
            except:
                print("Unable to rename")
            song = os.path.join(os.getcwd(),'media',str(current_user.id),'song',namee)
            vocals = os.path.join(os.getcwd(),'media',str(current_user.id),'vocals',namee)
            music = os.path.join(os.getcwd(),'media',str(current_user.id),'music',namee)
            privacy = request.POST['privacy']

            try:
                b = file(name=name, song = song, vocals=vocals, music = music, user = current_user, privacy = privacy)
                b.save()
            except:
                print("Unable to create file")
            return render(request,'show.html')
    else:
        return render(request,'save.html');

def mylist(request):
    if request.method == 'POST':
        id = request.POST['id']
        try:
            obj = file.objects.get(id=id)
        except:
            obj = None
        if obj:
            current_user = request.user
            if obj.user != current_user:
                list = file.objects.filter(user=request.user).values()
                current_user = request.user
                return render(request,'mylist.html',{'list' : list, 'user' : current_user})
        
            else:
                try:
                    os.unlink(os.path.join(os.getcwd(),'media',"a.mp3"))
                except:
                    print("No mp3 file in media directory")

                try:
                    os.unlink(os.path.join(os.getcwd(),'media',"a","vocals.wav"))
                except:
                    print("No vocals wav file in media directory")
                try:
                    os.unlink(os.path.join(os.getcwd(),'media',"a","accompaniment.wav"))
                except:
                    print("No accompaniment wav file in media directory")
                try:
                    shutil.copy(os.path.join(os.getcwd(),'media',str(current_user.id),"song",obj.name+".mp3"), os.path.join(os.getcwd(),'media'))
                except:
                    print("Unable to copy a.mp3")
                try:
                    dirv = "media/"+"a/vocals/"
                    os.mkdir(dirv)
                except:
                    print("Unable to create vocal dir")
                try:
                    shutil.copy(os.path.join(os.getcwd(),'media',str(current_user.id),"vocals",obj.name+".mp3"), os.path.join(os.getcwd(),'media','a','vocals'))
                except:
                    print("Unable to copy")
                try:
                    dirm = "media/"+"a/music/"
                    os.mkdir(dirm)
                except:
                    print("Unable to create music dir")
                try:
                    shutil.copy(os.path.join(os.getcwd(),'media',str(current_user.id),"music",obj.name+".mp3"), os.path.join(os.getcwd(),'media','a','music'))
                except:
                    print("Unable to copy")
                try:
                    old_file = os.path.join(os.getcwd(),'media',obj.name+".mp3")
                    new_file = os.path.join(os.getcwd(),'media',"a.mp3")
                    os.rename(old_file, new_file)
                except:
                    print("Unable to rename")
                try:
                    old_file = os.path.join(os.getcwd(),'media','a','vocals',obj.name+".mp3")
                    new_file = os.path.join(os.getcwd(),'media','a','vocals.wav')
                    os.rename(old_file, new_file)
                except:
                    print("Unable to move")
                try:
                    old_file = os.path.join(os.getcwd(),'media','a','music',obj.name+".mp3")
                    new_file = os.path.join(os.getcwd(),'media','a','accompaniment.wav')
                    os.rename(old_file, new_file)
                except:
                    print("Unable to move")
            
                try:
                    os.rmdir("media/a/vocals")
                except:
                    print("Unable to remove dir")
                try:
                    os.rmdir("media/a/music")
                except:
                    print("Unable to remove dir")
    
                return render(request,'show.html')
        else:
            list = file.objects.filter(user=request.user).values()
            current_user = request.user
            return render(request,'mylist.html',{'list' : list, 'user' : current_user})
    else:
        list = file.objects.filter(user=request.user).values()
        current_user = request.user
    
        return render(request,'mylist.html',{'list' : list, 'user' : current_user})
    

def publicsongs(request):
    if request.method == 'POST':
        
        id = request.POST['id']
        try:
            obj = file.objects.get(id=id)
        except:
            obj = None
        if obj:
            if obj.privacy != True:
        
                try:
                    os.unlink(os.path.join(os.getcwd(),'media',"a.mp3"))
                except:
                    print("No mp3 file in media directory")

                try:
                    os.unlink(os.path.join(os.getcwd(),'media',"a","vocals.wav"))
                except:
                    print("No vocals wav file in media directory")
                try:
                    os.unlink(os.path.join(os.getcwd(),'media',"a","accompaniment.wav"))
                except:
                    print("No accompaniment wav file in media directory")
                try:
                    shutil.copy(os.path.join(os.getcwd(),'media',str(obj.user_id),"song",obj.name+".mp3"), os.path.join(os.getcwd(),'media'))
                except:
                    print("Unable to copy a.mp3")
                try:
                    dirv = "media/"+"a/vocals/"
                    os.mkdir(dirv)
                except:
                    print("Unable to create vocal dir")
                try:
                    shutil.copy(os.path.join(os.getcwd(),'media',str(obj.user_id),"vocals",obj.name+".mp3"), os.path.join(os.getcwd(),'media','a','vocals'))
                except:
                    print("Unable to copy")
                try:
                    dirm = "media/"+"a/music/"
                    os.mkdir(dirm)
                except:
                    print("Unable to create music dir")
                try:
                    shutil.copy(os.path.join(os.getcwd(),'media',str(obj.user_id),"music",obj.name+".mp3"), os.path.join(os.getcwd(),'media','a','music'))
                except:
                    print("Unable to copy")
                try:
                    old_file = os.path.join(os.getcwd(),'media',obj.name+".mp3")
                    new_file = os.path.join(os.getcwd(),'media',"a.mp3")
                    os.rename(old_file, new_file)
                except:
                    print("Unable to rename")
                try:
                    old_file = os.path.join(os.getcwd(),'media','a','vocals',obj.name+".mp3")
                    new_file = os.path.join(os.getcwd(),'media','a','vocals.wav')
                    os.rename(old_file, new_file)
                except:
                    print("Unable to move")
                try:
                    old_file = os.path.join(os.getcwd(),'media','a','music',obj.name+".mp3")
                    new_file = os.path.join(os.getcwd(),'media','a','accompaniment.wav')
                    os.rename(old_file, new_file)
                except:
                    print("Unable to move")
            
                try:
                    os.rmdir("media/a/vocals")
                except:
                    print("Unable to remove dir")
                try:
                    os.rmdir("media/a/music")
                except:
                    print("Unable to remove dir")
    
                return render(request,'show.html')
            else:
                list = file.objects.filter(privacy='False').values()
                return render(request,'publicsongs.html',{'list':list})
        else:
            list = file.objects.filter(privacy='False').values()
            return render(request,'publicsongs.html',{'list':list})
    
    else:
        list = file.objects.filter(privacy='False').values()
        return render(request,'publicsongs.html',{'list':list})

def searchpublicsong(request):
    search = request.POST['search']
    match = file.objects.filter(Q(name__icontains = search) | Q(id__icontains = search))
    match = match.exclude(privacy=True)
    return render(request,'publicsongs.html',{'list':match})

def searchmylist(request):
    search = request.POST['search']
    match = file.objects.filter(Q(name__icontains = search) | Q(id__icontains = search)).filter(user = request.user)
    return render(request,'mylist.html',{'list':match})

def deletemylist(request):
    if request.method == 'POST':
        id = request.POST['id']
        try:
            obj = file.objects.get(id=id)
        except:
            obj = None
        if obj:
            current_user = request.user
            if obj.user != current_user:
                list = file.objects.filter(user=request.user).values()
                current_user = request.user
                return render(request,'mylist.html',{'list' : list, 'user' : current_user})
        
            else:
                try:
                    os.remove(os.path.join(os.getcwd(),'media',str(obj.user_id),'song',obj.name+'.mp3'))
                except:
                    print("No such music file")
                try:
                    os.remove(os.path.join(os.getcwd(),'media',str(obj.user_id),'vocals',obj.name+'.mp3'))
                except:
                    print("No such vocals file")
                try:
                    os.remove(os.path.join(os.getcwd(),'media',str(obj.user_id),'music',obj.name+'.mp3'))
                except:
                    print("No such music file")
                file.objects.filter(id=id).delete()
                list = file.objects.filter(user=request.user).values()
                current_user = request.user
                return render(request,'mylist.html',{'list' : list, 'user' : current_user})
        else:
            list = file.objects.filter(user=request.user).values()
            current_user = request.user
            return render(request,'mylist.html',{'list' : list, 'user' : current_user})
    else:
        list = file.objects.filter(user=request.user).values()
        current_user = request.user
    
        return render(request,'mylist.html',{'list' : list, 'user' : current_user})

def compaare(request):
    
    try:
        samplerate, data = read(os.path.join(os.getcwd(),'media',"a",'vocals.wav'))
        duration = len(data)/samplerate
        time = np.arange(0,duration,1/samplerate)
        plt.plot(time,data,color='c')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('Original')
        plt.savefig('media/f1.png')
        plt.clf()
        samplerate1, data1 = read(os.path.join(os.getcwd(),'media','sing.wav'))
        duration1 = len(data1)/samplerate1
        time1 = np.arange(0,duration1,1/samplerate1)
        plt.plot(time1,data1,color='k')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('Recorded')
        plt.savefig('media/f2.png')
        plt.clf()
        plt.plot(time,data,"c",time1,data1,"k")
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('Original vs Recorded')
        plt.savefig('media/f3.png')
        plt.clf()
        plt.plot(time1,data1,"k",time,data,"c")
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('Original vs Recorded')
        plt.savefig('media/f4.png')
        plt.clf()
        return render(request,'compaare.html')
    except:
        return render(request,'compaare.html')


def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username = username, password = password)
		print(user)

		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			messages.error(request, 'Invalid Credentials. Please check and try again.')
			return redirect('login')

	else:
		return render(request, 'login.html')

def signup(request):

	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']

		if User.objects.filter(username = username).exists():
			messages.error(request, 'Username already taken. Try different one')
			return redirect('signup')

		elif User.objects.filter(email = email).exists():
			messages.error(request, 'Email already taken')
			return redirect('signup')


		else:
			user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, 
				password = password, email = email)
			user.save()
			return redirect('login')
	
	else:
		return render(request, 'signup.html')

def logout(request):
	auth.logout(request)
	return redirect('/')
def singlebarvisualizer(request):
    return render(request, 'singlebarvisualizer.html')
def circlevisualizer(request):
    return render(request, 'circlevisualizer.html')
def normalvisualizer(request):
    return render(request, 'normalvisualizer.html')
def combinedvisualizer(request):
    return render(request, 'combinedvisualization.html')
def publicsongvisualizer(request):
    if request.method == 'POST':
        
        id = request.POST['id']
        try:
            obj = file.objects.get(id=id)
        except:
            obj = None
        if obj:
            if obj.privacy != True:
                userid = obj.user_id
                song = obj.name
                return render(request, 'publicsongvisualizer.html',{'userid':userid,'song':song})
            else:
                list = file.objects.filter(privacy='False').values()
                return render(request,'publicsongs.html',{'list':list})
        else:
            list = file.objects.filter(privacy='False').values()
            return render(request,'publicsongs.html',{'list':list})
    
    else:
        list = file.objects.filter(privacy='False').values()
        return render(request,'publicsongs.html',{'list':list})
def mylistvisualizer(request):
    if request.method == 'POST':
        id = request.POST['id']
        try:
            obj = file.objects.get(id=id)
        except:
            obj = None
        if obj:
            current_user = request.user
            if obj.user != current_user:
                list = file.objects.filter(user=request.user).values()
                current_user = request.user
                return render(request,'mylist.html',{'list' : list, 'user' : current_user})
        
            else:
                userid = obj.user_id
                song = obj.name
                return render(request, 'mylistvisualizer.html',{'userid':userid,'song':song})
        else:
            list = file.objects.filter(user=request.user).values()
            current_user = request.user
            return render(request,'mylist.html',{'list' : list, 'user' : current_user})
    else:
        list = file.objects.filter(user=request.user).values()
        current_user = request.user

