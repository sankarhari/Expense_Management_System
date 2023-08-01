from django.shortcuts import render
import json
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from email_validator import validate_email, EmailNotValidError
from django.contrib import messages

def register(request):
    if request.method == "GET":
        return render(request, "authentication/register.html", context = {})
    elif request.method == "POST":
        context = {
            "fieldValues" : request.POST
        }
        # print(json.dumps(request.POST))
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        errors = []

        username_validate_result = username_validate(username)
        if not "username_valid" in username_validate_result:
            errors.append(username_validate_result["username_error"])
        
        email_validate_result = email_validate(email)
        if not "useremail_valid" in email_validate_result:
            errors.append(email_validate_result["useremail_error"])

        password_validate_result = password_validate(password, repassword)
        print(password_validate_result)
        if not "userpassword_valid" in password_validate_result:
            errors.append(password_validate_result["userpassword_error"])

        print(errors)

        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
        else:
            new_user = User.objects.create_user(username = username, email = email)
            new_user.set_password(password)
            new_user.save()
            messages.success(request, "User created successfully")

        return render(request, "authentication/register.html", context = context)

def username_validate(username: str) -> dict:
    if not str(username).isalnum():
        return {'username_error':'Username only should contain alphanumberic'}
    if User.objects.filter(username = username).exists():
        return {'username_error':'Username already in user. Please try different one.'}
    return {"username_valid":True}
    
@csrf_exempt
def username_validation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        validate_result = username_validate(username)
        status_code = 400
        if "username_valid" in validate_result:
            status_code = 200
        return JsonResponse(validate_result, status = status_code)
    raise Http404("Page does not exist")

def email_validate(email: str) -> dict:
    try:
        email_info = validate_email(email)
        if User.objects.filter(email = email).exists():
            return {'useremail_error':'Given email ID is already registered.'}
    except EmailNotValidError as e:
        return {'useremail_error': str(e)}
    return {'useremail_valid':True}

@csrf_exempt
def email_validation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"]
        validate_result = email_validate(email)
        status_code = 400
        if "useremail_valid" in validate_result:
            status_code = 200
        return JsonResponse(validate_result, status = status_code)
    raise Http404("Page does not exist")

def password_validate(password: str, repassword: str) -> dict:
    if not password == repassword: 
        return {'userpassword_error':'Password and Re-enter Password missmatch.'}
    elif len(password) <= 8:
        return {'userpassword_error':'Password should have more than 8 Characters.'}
    elif password.isalnum():
        return {'userpassword_error':'Password must contain atleast one special charater.'}
    return {'userpassword_valid':True}

@csrf_exempt
def password_validation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        password = data["password"]
        repassword = data["repassword"]
        
        validate_result = password_validate(password, repassword)
        status_code = 400
        if "userpassword_valid" in validate_result:
            status_code = 200
        return JsonResponse(validate_result, status = status_code)

    raise Http404("Page does not exist")