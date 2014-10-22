from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from penntext.models import User, FlatPrice, UserProfile
from penntext.forms import UserForm, UserProfileForm, FlatPriceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random
from django.core.mail import EmailMessage
from django.http import HttpRequest

def addurl(subject_list):
    for subject in subject_list:
        subject.url = subject.name.replace(' ', '_')

def index(request):
    context = RequestContext(request)
    return render_to_response('penntext/index.html', {}, context)

def about(request):
    context= RequestContext(request)
    return render_to_response('penntext/about.html', {'mymessage': "Work in progress."}, context)


def joblist(request, job_name_url):
    context = RequestContext(request)
    if request.user.is_authenticated():
        current_user = User.objects.get(id = request.user.id)
        job_type = FlatPrice.objects.filter(job = job_name_url).exclude(name= current_user.username)
    else:
        job_type = FlatPrice.objects.filter(job = job_name_url)
    job_list = job_type.order_by('-timeposted')
    return render_to_response('penntext/job_list.html', {'job_list': job_list,
                                                         'job_name_url': job_name_url}, context)


@login_required
def add_job(request, job_name_url):
    context = RequestContext(request)
    if request.method == 'POST':
        form = FlatPriceForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            profile = request.user.get_profile()
            job.name = request.user.get_username()
    
            if not (job.contact):
                job.contact = profile.phone
            
            if not (job.location):
                job.location = profile.location

            if not (job.typeofpay):
                job.typeofpay = 0
            job.email = request.user.email
            job.userid = (request.user).id
            job.job = job_name_url.replace('_', ' ')

            job.url = (job.title).replace(' ', '_')
            if 'picture' in request.FILES:
                job.picture = request.FILES['picture']
            form.save()
            return my_job(request)
        else:
            print form.errors
    else:
        form = FlatPriceForm()
    return render_to_response('penntext/add_job.html', {'form': form,
                                                        'job_name_url': job_name_url,
                                                        }, context)
        



def accept_job(request, theid, job_url, job_name_url):
    context = RequestContext(request)
    title = job_url.replace('_', ' ')
    thejob = FlatPrice.objects.get(id = theid)
    user = User.objects.get(username=thejob.name)
    current_user = User.objects.get(id = request.user.id)
    current_user_prof = request.user.get_profile()
    endjob = (str(random.randint(0, 9999999)) + str(request.user.id))            
    thejob.acceptedby = current_user.username
    thejob.completioncode = int(endjob)
    thejob.save()
    email_subject = 'Job Acceptance of: ' + thejob.title + ' by ' + current_user.username
    email_body = 'Contact info of the person who accepted the job: \n' + current_user.email + '\n' + str(current_user_prof.phone)
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()
    new_email_subject = 'Job Code: ' + endjob
    new_email_body = 'This email is proof that you have accepted the job ' + thejob.title + ' by ' + current_user.username + '. Upon completion of the payment, give this code (in the subject) to the job poster so he may declared the job as over. This email acts as proof that you are required to complete the job and that you must be paid after the job is over'
    new_email_body = new_email_body + '\n \n The contact info of the job poster: ' + thejob.email + '\n' + thejob.location + '\n' + thejob.contact
    new_email = EmailMessage(new_email_subject, new_email_body, to=[current_user.email])
    new_email.send()
    go = '/localquaker/' + job_name_url + '/job'
    return HttpResponseRedirect(go)
    

@login_required
def my_job(request):
    context = RequestContext(request)
    current_user = request.user.id
    myJobs = FlatPrice.objects.filter(userid=current_user)
    return render_to_response('penntext/my_job.html', {'myJobs': myJobs
                                                        }, context)


def my_accepted(request):
    context= RequestContext(request)
    current_user = User.objects.get(id = request.user.id)
    myJobs = FlatPrice.objects.filter(acceptedby=current_user.username)
    return render_to_response('penntext/my_accepted.html', {'myJobs': myJobs
                                                        }, context)




@login_required
def del_flatprice(request, sell_id):
    context= RequestContext(request)
    todel= FlatPrice.objects.get(id = sell_id)
    if (todel.acceptedby):
        theuser = User.objects.get(username = todel.acceptedby)
        if (int(todel.completioncode) == int(request.REQUEST["code"])):
            todel.picture.delete()
            todel.delete()
            return HttpResponseRedirect('/localquaker/my_job/')
        else:
            current_user = request.user.id
            myJobs = FlatPrice.objects.filter(userid=current_user)
            return render_to_response('penntext/my_job.html', {'myJobs': myJobs,
                                                               'error' :'Wrong Completion Code'
                                                        }, context)

    todel.picture.delete()
    todel.delete()
    return HttpResponseRedirect('/localquaker/my_job/')


def register(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/localquaker/')
    
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data= request.POST)
        if user_form.is_valid() and profile_form.is_valid:
            user = user_form.save()


            user.set_password(user.password)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit= False)

            profile.user=user
                            
            profile.activation_key = (str(random.randint(0, 9999999)) + str(user.id))
            email_subject = 'LocalQuaker Confirmation'
            email_body = "To activate your account, click this link: \n\n http://127.0.0.1:8000/localquaker/confirm/%s" % (
                profile.activation_key)
            email = EmailMessage(email_subject, email_body, to=[user.email])
            email.send()
            profile.save()
            registered = True
            
        else:
            print user_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'penntext/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)



def confirm(request, activation_key):
    userprofile = UserProfile.objects.get(activation_key=activation_key)
    userprofile.user.is_active = True
    userprofile.user.save()
    userprofile.save()

    return HttpResponseRedirect('/localquaker/login/')


def user_login(request):
    context= RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/localquaker/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/localquaker/')
            else:
                context_dict = {'error' :'An inactive account was used.'}
                return render_to_response('penntext/login.html', context_dict, context)

        else:
            print "Invalid login details: {0}, {1}".format(username, password)            
            context_dict = {'error' :  'Wrong username or password.'}
            return render_to_response('penntext/login.html', context_dict, context)
    
    else:
        return render_to_response('penntext/login.html',{}, context)
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/localquaker/')
