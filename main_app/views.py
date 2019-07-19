from django.shortcuts import render, redirect
from main_app.forms import UserForm
from main_app.models import saveLaunch
from .forms import searchForm
from .models import launchEnt
import requests


# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    print("main")
    data = requests.get("https://launchlibrary.net/1.4/launch/next/5").json()
    lone = launchEnt(data['launches'][0])
    lset = [launchEnt(data['launches'][1]),launchEnt(data['launches'][2]),launchEnt(data['launches'][3]),launchEnt(data['launches'][4])]
    print(lone)
    return render(request, 'main_app/index.html',{'lone':lone,'lset':lset})

def search(request):
    print("search")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("its post")
        # create a form instance and populate it with data from the request:
        form = searchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            date_start = form['date_start'].data
            date_end = form['date_end'].data
            data = requests.get(f"https://launchlibrary.net/1.4/launch/{date_start}/{date_end}?limit=100").json()
            listLaunch = []
            ccc = {}
            for ent in data['launches']:
                l = launchEnt(ent)
                listLaunch.append(l)
                if l.locationCC in ccc:
                    ccc[l.locationCC] += 1
                else:
                    ccc[l.locationCC] = 1


            #calc count of country codes

            print(ccc)
            return render(request, 'main_app/search/search_result.html',{"list":listLaunch,'date':[date_start,date_end],'ccc':ccc})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = searchForm()

    return render(request, 'main_app/search/main.html',{'form': form})




@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)

        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()


    return render(request,'main_app/registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'main_app/login.html', {})


@login_required
def saved_launches(request):

    userid = request.user.id
    listLaunch = []
    query = saveLaunch.objects.filter(userid=userid)
    for item in query:
        data = requests.get(f"https://launchlibrary.net/1.4/launch/{item.rocketid}").json()
        lone = launchEnt(data['launches'][0])
        listLaunch.append(lone)

    # TODO needs refactoring out as repeated
    ccc = {}
    for ent in listLaunch:
        if ent.locationCC in ccc:
            ccc[ent.locationCC] += 1
        else:
            ccc[ent.locationCC] = 1

    return render(request, 'main_app/search/search_result.html',{"list":listLaunch,'ccc':ccc,'savedpage':True})



@login_required
def remove_launch(request):
    print("remove")
    userid = request.POST.get('userid')
    rocketid = request.POST.get('launchid')
    try:
        saveLaunch.objects.get(userid=userid,rocketid=rocketid).delete()
    except:
        print("already removed")

    return redirect('/main_app/saved_launches/')



@login_required
def save_launch(request):
    print("save")
    userid = request.POST.get('userid')
    rocketid = request.POST.get('launchid')
    print(userid)
    print(rocketid)
    #print(type(userid))

    #print(type(int(userid)))

    ent = saveLaunch(userid=userid, rocketid=rocketid)
    try:
        ent.save()
    except:
        print("already saved")


