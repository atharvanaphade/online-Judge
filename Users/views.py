import datetime
import os
import re
import subprocess
import json

from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse

from Sandbox.views import user_ka_aukaat_check_kar
from .models import Profile, Question, Submissions
from django.shortcuts import redirect

start_time = datetime.datetime.now()
end_time = datetime.datetime.now()

# global variables for path locations
# locations used to store user code and information regarding input-outputs, memory and time limits

USER_CODE_PATH = 'data/users_code/'
STANDARD = 'data/standard/'

# global variables for paths to store number of questions
# used to calculate accuracies at various places in a few functions

NO_OF_QUESTIONS = 6
NO_OF_TEST_CASES = 6


# redirect to question hub page upon entering garbage url
# works only when debug is set to False


def bad_request(request):
    return redirect('question-hub')


def handler404(request):
    return HttpResponseRedirect(reverse("question-hub"))


# function to set timer for the competition

def set_timer(request):
    if request.user.is_superuser:  # url accessible only by admins
        if request.method == 'GET':  # load form on get request
            return render(request, 'Users/timer.html')
        elif request.method == 'POST':
            global start_time
            global end_time
            duration = request.POST.get('duration')  # get duration from front end
            start_time = datetime.datetime.now() + datetime.timedelta(0,
                                                                      15)  # set global start time by adding 15 seconds buffer
            end_time = start_time + datetime.timedelta(0, int(duration))  # set global end time according to duration
            return HttpResponse(" time is set ")
    return HttpResponse("You cannot access this URL.")


def remaining_time(request):
    current_time = datetime.datetime.now()  # get current time
    global end_time
    if current_time < end_time:  # check if time is up
        time_left = end_time - current_time  # if not calculate time left
        return time_left
    else:
        return 0  # return 0 if time is up


# function to register new user to the competition

def register(request):
    if request.user.is_superuser:  # this url is only accessible by admins
        if request.method == 'POST':
            # no special characters allowed, no spaces at start or end of username allowed
            username_regex = '^(?=.{4,20}$)(?:[a-zA-Z\d]+(?:(?:\.|-|_)[a-zA-Z\d])*)+$'

            username = request.POST.get('username')  # get username from front end form
            if User.objects.filter(username=username).exists():  # check if username is taken
                messages.error(request, 'This username already exists. Try another username.')
                return render(request, 'Users/register.html')  # if yes then return to registration form with error
            if not re.search(username_regex, username):  # check if username satisfies requirements (regex)
                messages.error(request, 'Please enter a valid username.')
                return render(request, 'Users/register.html')  # if not return to registration form with error

            # standard email regex
            email_regex = '^((([!#$%&\'*+\-/=?^_`{|}~\w])|([!#$%&\'*+\-/=?^_`{|}~\w][!#$%&\'*+\-/=?^_`{|}~\.\w]{0,}[!#$%&\'*+\-/=?^_`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)$'

            email = request.POST.get('email')  # get email from front end
            if User.objects.filter(email=email).exists():  # check if email is already associated with another username
                messages.error(request, 'This email is already associated with another username.')
                return render(request, 'Users/register.html')  # if yes return to registration form with error
            if not re.search(email_regex, email):  # check if email satisfies requirements (regex)
                messages.error(request, 'Please enter a valid email address.')
                return render(request, 'Users/register.html')  # if not return to registration form with error

            # phone number regex --> not used for now due to country code complications
            # phone_regex = '^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$'

            phone = request.POST.get('phone')  # get phone number form front end (assumed to be indian phone number)
            if (len(str(phone)) != 10 | str(
                    phone).isnumeric() is False):  # check if it satisfies the basic requirements of a phone number i.e. 10 digits long
                messages.error(request, 'Please enter a valid phone number.')
                return render(request, 'Users/register.html')  # if not return to registration form with error
            level = request.POST.get('level')  # get level of user form front end (junior or senior)

            # password must be minimum 8 characters long with 1 capital character, 1 special character and 1 numeric character
            password_regex = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

            password1 = request.POST.get('password1')  # get password from front end
            password2 = request.POST.get('password2')  # get password verification from front end
            if password1 != password2:  # check if both paswords are same
                messages.error(request, 'Passwords don\'t match.')
                return render(request, 'Users/register.html')  # if not return to registration form with error
            if not re.search(password_regex, password1):  # check if passwords satifies requirements (regex)
                messages.error(request,
                               'Password must contain minimum eight characters, at least one letter, one number and one special character.')
                return render(request, 'Users/register.html')  # if not return to regstration from with error
            fname = request.POST.get('fname')  # get first name of user from front end
            lname = request.POST.get('lname')  # get last name of user from front end
            college = request.POST.get('college')  # get college name of user from front end

            # create a new object of type user and assign appropriate values to its attributes from above information
            newUser = User.objects.create_user(username=username, email=email, first_name=fname, last_name=lname,
                                               password=password1)
            newUser.save()  # save the new user in the database

            # create an object of type profile to store additional details of user
            if level == 'Senior':  # check if user is senior or junior and assign values to attributes accordingly
                profile = Profile(user=newUser, phone=phone, college=college, junior=False)
                profile.save()  # save the user profile
            else:
                profile = Profile(user=newUser, phone=phone, college=college)
                profile.save()

            # create new directory for the user in the file structure to store their code
            user_directory = "{}{}/".format(USER_CODE_PATH, username)
            if not os.path.exists(user_directory):
                os.system('mkdir ' + user_directory)

            messages.success(request, 'Your account has been created.')
            return render(request, 'Users/register.html')  # redirect to login page after registration
        elif request.method == 'GET':
            return render(request, 'Users/register.html')  # render registration form in case of get request
        return HttpResponse("Invalid request type.")  # only get and post requests are allowed
    return HttpResponse("You cannot access this URL.")  # no access rights


# function to login registered user to the competition

def login(request):
    if request.method == 'POST':
        junior = request.POST.get('optradio')  # get user level from front end
        if not junior:  # if no level is selected return to login page with error
            messages.error(request, 'Please select your category.')
            return render(request, 'Users/login.html')

        junior = bool(int(junior))  # convert user level to boolean value for further validations
        timer = remaining_time(request)  # get remaining time
        if timer != 0:  # proceed only if time is not up
            username = request.POST.get('username')  # get username from front end form
            username = str(username)
            username = username.strip()  # strip leading and trailing white spaces if any
            password = request.POST.get('password')  # get password from front end form
            user = auth.authenticate(request, username=username,
                                     password=password)  # authenticate user with given credentials
            # user_profile = Profile.objects.get(user=user.id)
            if user is not None:  # check if user exists
                user_profile = Profile.objects.get(user=user.id)  # if yes get the profile of user to validate level
                if user_profile.junior == junior:  # compare boolean values
                    auth.login(request, user)  # if matched log in user
                    request.session.set_expiry(remaining_time(request).total_seconds())  # set session time out
                    # request.session.set_expiry(timer)
                    return render(request, 'Users/Instructions.html',
                                  context={'username': request.user.username})  # render instructions page
                else:  # if not mathced redirect to login page with error
                    messages.error(request, 'Invalid credentials.')
                    return redirect('login')
            else:  # if not redirect to login page with error
                messages.error(request, 'Invalid credentials.')
                return redirect('login')
        messages.error(request, 'Time is up. You cannot login now')  # if time if up render login page with error
        return render(request, 'Users/login.html')
    elif request.method == 'GET':
        if request.user.is_authenticated:  # check if request is get and user is logged in
            return redirect('question-hub')  # if yes redirect to question hub
        return render(request, 'Users/login.html')  # else render login page
    return HttpResponse("Invalid request type.")  # only get and post requests are allowed


# function to display question hub page

def question_hub(request):
    if request.user.is_authenticated:  # check if user is logged in
        if request.method == 'GET':
            questions = Question.objects.all()  # select all objects from question table
            avg_accuracies = []  # empty list
            for question in questions:  # loop through all questions
                try:
                    accuracy = round(((question.successfulAttempts / question.numberOfAttempts) * 100),
                                     2)  # calculate accuracy of every question as per the iteration
                except ZeroDivisionError:
                    accuracy = 0  # accuracy is 0 if numberOfAttempts is 0
                avg_accuracies.append(accuracy)
            timer = remaining_time(request)  # get reamining time
            if timer != 0:  # proceed only if time is not up
                global end_time
                context = {'group': zip(questions, avg_accuracies),
                           'time': end_time}  # pass question list, accuracy list and end time to front end
                return render(request, 'Users/question_hub.html',
                              context)  # render question hub page with required parameters
            else:  # logout if time is up
                return HttpResponseRedirect(reverse("logout"))
        else:  # only get request is allowed
            return HttpResponse("Invalid request type.")
    messages.error(request, 'You must login to view this page.')  # return to login page if not logged in
    return HttpResponseRedirect(reverse("login"))


# function to add sandbox rules and filters to user's code

def modify_file_contents(code, extension, code_file_path):
    if extension != 'py':  # for c or cpp code
        sandbox_header = '#include"../../../include/sandbox.h"\n'  # relative path to sandbox rules in file structure
        try:
            before_main = code.split('main')[0] + 'main'  # split user's code at main function
            # add line install_filters(); as the first line in main function
            after_main = code.split('main')[1]
            index = after_main.find('{') + 1
            main = before_main + after_main[:index] + 'install_filters();' + after_main[
                                                                             index:]  # reconstruct main function
            with open(code_file_path, 'w+') as f:
                f.write(sandbox_header)  # add sandbox header
                f.write(main)  # add modified main function
                f.close()  # save
        except IndexError:
            with open(code_file_path, 'w+') as f:
                f.write(code)
                f.close()
    else:  # for python
        with open(code_file_path, 'w+') as f:
            f.write('import temp\n')  # import files which have sandbox rules
            f.write(code)  # append code
            f.close()  # save


# function to load previous or latest submission of the user for a question

def load_buffer(request):
    if not request.user.is_authenticated:  # check if user is logged in
        messages.error(request, 'You must login first.')
        return HttpResponseRedirect(reverse("login"))
    if not request.is_ajax:  # only ajax request is allowed
        return HttpResponse("Invalid request type.")
    if request.user.is_authenticated and request.is_ajax():
        # get question number and selected extension of front end editor
        question_number = request.POST.get('qno')
        ext = request.POST.get('ext')
        question = Question.objects.get(pk=question_number)  # select appropriate question from database
        txt = ""  # empty string
        submissions = Submissions.objects.filter(userID=request.user.id, quesID=question.id, language=ext).order_by(
            '-attempt').first()  # get latest submission of selected question and extension of front end editor
        if submissions:  # if submission exists
            # get file path for the saved user code
            code_file = USER_CODE_PATH + '{}/question{}/code{}.{}'.format(request.user.username, question_number,
                                                                          submissions.attempt, submissions.language)
            f = open(code_file, "r")
            txt = f.read()  # append user's code to empty string
            f.close()
        response_data = {'txt': txt}
        return JsonResponse(response_data)  # return code string


# function to get output for custom input by user

def get_output(request):
    if not request.user.is_authenticated:  # check if user is logged in
        messages.error(request, 'You must login first.')
        return HttpResponseRedirect(reverse("login"))  # return to login page with error if not
    if not request.is_ajax:  # only ajax request is allowed
        return HttpResponse("Invalid request type.")
    if request.user.is_authenticated and request.is_ajax():
        response_data = {}  # empty dictionary
        # get question number and user's input from front end
        ques_no = request.POST.get('question_no')
        i = request.POST.get('ip')
        i = str(i)
        # run executable using user's input
        ans = subprocess.Popen("data/standard/executable/question{}/a.out".format(ques_no),
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (out, err) = ans.communicate(input=i.encode())
        response_data["out"] = out.decode()  # pass output of executable as json response
        return JsonResponse(response_data)


def coding_page(request, pk):  # pass question id via url
    if request.user.is_authenticated:
        global end_time
        timer = remaining_time(request)
        if request.method == 'GET':
            # get all required information on coding page
            que = Question.objects.get(pk=pk)
            user_profile = Profile.objects.get(user=request.user)
            user = request.user
            if timer != 0:
                context = {'question': que, 'user': user,
                           'time': end_time,
                           'total_score': user_profile.totalScore,
                           'question_id': pk,
                           'junior': user_profile.junior}
                return render(request, 'Users/coding_page.html', context)  # load only if time is not up
            else:
                return HttpResponseRedirect(reverse("logout"))
        elif request.method == 'POST':
            if timer != 0:
                username = request.user.username
                current_question = Question.objects.get(pk=pk)
                ext = request.POST['ext']  # get editor language
                code = request.POST['code']  # get user code
                if Submissions.objects.filter(userID=request.user.id,
                                              quesID=current_question).exists():  # check if previously submitted
                    submissions = Submissions.objects.filter(userID=request.user.id, quesID=current_question.pk)
                    submission = submissions.order_by('-attempt').first()
                    attempt = submission.attempt + 1  # get appropriate attempt number
                else:
                    attempt = 1  # attempt = 1 by default
                user_question_path = '{}{}/question{}/'.format(USER_CODE_PATH, username,
                                                               pk)  # path to store user's code
                if not os.path.exists(user_question_path):
                    os.system('mkdir ' + user_question_path)  # create directories if not present
                code_file = user_question_path + "code{}.{}".format(attempt, ext)
                code = str(code)
                modify_file_contents(code, ext, code_file)  # modify code file contents to run in sandbox
                testcase_values = user_ka_aukaat_check_kar(username=username, question_number=pk, attempts=attempt,
                                                           ext=ext)  # run code and get result
                code_f = open(code_file, 'w+')
                code_f.seek(0)
                code_f.write(code)  # save unmodified code
                code_f.close()

                # get current submission time in required format to store in database
                # save time duration of submission after the start of competition

                time = datetime.datetime.now()
                global start_time
                submission_time = time - start_time
                days, second = submission_time.days, submission_time.seconds
                hours = str(days * 24 + second // 3600)
                minutes = str((second % 3600) // 60)
                seconds = str(second % 60)
                if int(hours) < 10:
                    hours = "0" + hours
                if int(minutes) < 10:
                    minutes = "0" + minutes
                if int(seconds) < 10:
                    seconds = "0" + seconds
                final_submission_time = '{}:{}:{}'.format(hours, minutes, seconds)  # time is in string format

                # check if error file is generated by sandbox

                error_text = ""
                epath = USER_CODE_PATH + '/{}/question{}/error.txt'.format(username, pk)
                if os.path.exists(epath):
                    ef = open(epath, 'r')
                    error_text = ef.read()
                    # if yes format it properly
                    error_text = re.sub('/.*?:', '', error_text)  # regular expression
                    ef.close()
                if error_text == "":
                    error_text = "Compiled successfully."

                no_of_pass = 0
                for i in testcase_values:
                    if i == 'AC':
                        no_of_pass += 1  # check passed test cases
                current_accuracy = round(((no_of_pass / NO_OF_TEST_CASES) * 100), 2)  # calculate accuracy
                status = 'PASS' if no_of_pass == NO_OF_TEST_CASES else 'FAIL'  # set overall status as pass only if all test cases have been passed
                new_submission = Submissions(quesID=current_question, userID=request.user, language=ext,
                                             code=code, attempt=attempt, submission_time=final_submission_time,
                                             accuracy=current_accuracy, status=status)  # create new submission entry
                # update user profile table according to accuracy and user level
                user_profile = Profile.objects.get(user=request.user)

                # 4 possibilities:
                # 1. user --> senior, status --> pass
                # 2. user --> senior, status --> fail
                # 3. user --> junior, status --> pass
                # 4. user --> junior, status --> fail

                if status == 'PASS' and not user_profile.junior:  # case 1
                    if Submissions.objects.filter(userID=request.user.id,
                                                  quesID=pk):  # check if previous submissions exist
                        submissions = Submissions.objects.filter(userID=request.user.id, quesID=pk)
                        submission = submissions.order_by('-score').first()
                        if submission.score != 100:  # check if any submission has 100 marks
                            user_profile.totalScore += 100  # if not update user's profile else don't
                            user_profile.correctly_answered += 1
                        current_question.successfulAttempts += 1  # question data is modified at every submission for accuracy calculations
                        current_question.numberOfAttempts += 1
                    else:  # in case first submission is correct itself
                        user_profile.totalScore += 100
                        user_profile.correctly_answered += 1
                        current_question.successfulAttempts += 1
                        current_question.numberOfAttempts += 1
                    current_question.save()
                    user_profile.save()
                    new_submission.score = 100
                    new_submission.save()
                elif user_profile.junior and status == 'PASS':  # case 3
                    if Submissions.objects.filter(userID=request.user.id,
                                                  quesID=pk):  # check if previous submissions exist
                        submissions = Submissions.objects.filter(userID=request.user.id, quesID=pk)
                        submission = submissions.order_by('-score').first()
                        if submission.score < 100:  # check if max score from previous submissions is less than 100
                            user_profile.totalScore -= submission.score  # if yes, subtract previous max and add 100
                            user_profile.totalScore += 100  # update user profile
                            user_profile.correctly_answered += 1
                        current_question.successfulAttempts += 1  # update question data
                        current_question.numberOfAttempts += 1
                    else:  # in case first submission is correct itself
                        user_profile.totalScore += 100
                        user_profile.correctly_answered += 1
                        current_question.successfulAttempts += 1
                        current_question.numberOfAttempts += 1
                    current_question.save()
                    user_profile.save()
                    new_submission.score = 100
                    new_submission.save()
                elif status == 'FAIL' and user_profile.junior:  # case 4
                    currentScore = (
                                           no_of_pass * 100) / NO_OF_TEST_CASES  # calculate current score according to decided logic
                    if Submissions.objects.filter(userID=request.user.id,
                                                  quesID=pk):  # check if previous submissions exist
                        submissions = Submissions.objects.filter(userID=request.user.id, quesID=pk)
                        submission = submissions.order_by('-score').first()
                        if submission.score < currentScore:  # check if max score from previous submissions is less than current score
                            user_profile.totalScore -= submission.score  # if yes subtract previous max and add current max score
                            user_profile.totalScore += currentScore
                        current_question.numberOfAttempts += 1  # update question model
                    else:  # in case of first submission
                        user_profile.totalScore += currentScore
                        current_question.numberOfAttempts += 1
                    current_question.save()
                    user_profile.save()
                    new_submission.score = currentScore
                    new_submission.save()
                else:  # case 2
                    current_question.numberOfAttempts += 1
                    current_question.save()
                    new_submission.score = 0
                    new_submission.save()
                data = {
                    'testcases': testcase_values,
                    'error': error_text,
                    'status': status,
                    'score': new_submission.score,
                    'time': end_time,
                    'question_id': pk,
                }
                return render(request, "Users/test_cases.html", data)  # load test cases page with required parameters
            else:
                return HttpResponseRedirect(reverse("logout"))  # logout if time is up
        else:
            return HttpResponse("Invalid request type.")  # only get and post request allowed
    messages.error(request, 'You must login to view this page.')
    return HttpResponseRedirect(reverse("login"))  # redirect to login page with error


# function to display the leaderboard

def leaderboard(request):
    if request.user.is_authenticated:  # check if user is logged in
        if request.method == 'GET':
            timer = remaining_time(request)  # get remaining time
            if timer != 0:  # proceed only if time is not up
                questions = Question.objects.all()
                current_user = request.user.username
                current_score = request.user.profile.totalScore
                leaderboard = {}  # format --> key (username): value (score of all questions and total score)
                # loop through all user profiles according to required order
                for profile in Profile.objects.order_by('-totalScore', 'latestSubTime'):
                    question_scores = [0 for _ in questions]  # set initial score as 0 for all questions
                    user_submissions = Submissions.objects.filter(
                        userID=profile.user.id)  # get all submissions of iterating user
                    if user_submissions:
                        # loop for total number of questions if user submissions exist
                        for question in questions:
                            question_submission = user_submissions.filter(
                                quesID=question.id)  # get all submissions of iterating question
                            if question_submission:
                                # if submissions for question exist then select highest score for it
                                question_score = question_submission.order_by('-score').first()
                                question_scores[
                                    question.id - 1] += question_score.score  # append to question score list at appropriate index
                    question_scores.append(profile.totalScore)  # append user's total score to the list
                    leaderboard[
                        profile.user.username] = question_scores  # set key: value according to above mentioned format
                rank = list(leaderboard.keys()).index(current_user)  # find position of current user in dictionary

                paginator = Paginator(tuple(leaderboard.items()), 10)  # Show 10 users per page.
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                page_range = paginator.page_range

                # collect or calculate other information required on leaderboard page
                user_accuracy = round(((request.user.profile.correctly_answered / len(questions)) * 100), 2)
                fname = request.user.first_name
                lname = request.user.last_name
                initials = fname[0].upper() + lname[0].upper()
                global end_time
                context = {'questions': questions, 'page_obj': page_obj, 'current_user': current_user,
                           'current_user_score': current_score, 'current_user_rank': rank + 1, 'page_range': page_range,
                           'user_accuracy': user_accuracy, 'initials': initials, 'time': end_time}
                return render(request, 'Users/leaderboard.html', context)  # load leaderboard page
            else:
                return HttpResponseRedirect(reverse("logout"))  # if time is up logout
        else:  # only get request is allowed
            return HttpResponse("Invalid request type.")
    messages.error(request, 'You must login to view this page.')
    return HttpResponseRedirect(reverse("login"))  # load login page with error


# function to view all submissions by a user

def submission_page(request):
    if request.user.is_authenticated:
        global end_time
        timer = remaining_time(request)
        if request.method == 'GET':
            if timer != 0:
                pk = 1  # load submissions of question 1 by default
                submissions = Submissions.objects.filter(userID=request.user.id, quesID=pk)
                context = {'submissions': submissions, 'question_number': pk, 'time': end_time}
                return render(request, "Users/submissions.html", context)
            else:
                return HttpResponseRedirect(reverse("logout"))
        elif request.method == 'POST':
            if timer != 0:
                pk = request.POST.get('selected')  # get question from front end
                question = Question.objects.get(pk=pk)  # select appropriate question
                submissions = Submissions.objects.filter(userID=request.user.id, quesID=question.id)
                context = {'submissions': submissions, 'question_number': pk, 'time': end_time}
                return render(request, 'Users/submissions.html', context)  # load submission page of selected question
            else:
                return HttpResponseRedirect(reverse("logout"))
        else:
            return HttpResponse("Invalid request type.")
    messages.error(request, 'You must login to view this page.')
    return HttpResponseRedirect(reverse("login"))


# function to view a particular submission code

def view_submission(request, submission_id):  # pass submission id via url
    if request.user.is_authenticated:
        if request.method == 'GET':
            timer = remaining_time(request)
            if timer != 0:
                # select appropriate user and submission
                user_profile = Profile.objects.get(user=request.user)
                submission = Submissions.objects.get(id=submission_id)
                # get code in json format
                code = json.dumps(submission.code, ensure_ascii=False)
                question = Question.objects.get(pk=submission.quesID.pk)
                user = request.user
                global end_time
                context = {'question': question, 'user': user, 'time': end_time,
                           'total_score': user_profile.totalScore, 'question_id': submission.quesID.pk,
                           'code': code}
                return render(request, 'Users/coding_page.html', context)  # load coding page with modified parameters
            else:
                return HttpResponseRedirect(reverse("logout"))
        else:
            return HttpResponse("Invalid request type.")
    messages.error(request, 'You must login to view this page.')
    return HttpResponseRedirect(reverse("login"))


def logout(request):
    if request.user.is_authenticated:  # check if logged in

        # leaderboard code but for first 6 ranks only

        questions = Question.objects.all()
        current_user = request.user.username
        current_score = request.user.profile.totalScore
        leaderboard = {}
        for profile in Profile.objects.order_by('-totalScore', 'latestSubTime'):
            leaderboard[profile.user.username] = profile.totalScore
        rank = list(leaderboard.keys()).index(current_user)

        # process user profile for displaying additional information on result page

        current_user_profile = Profile.objects.get(user=request.user)
        correct = current_user_profile.correctly_answered
        attempted = 0
        for question in questions:
            if Submissions.objects.filter(userID=request.user.id, quesID=question.pk).exists():
                attempted += 1
        fname = request.user.first_name
        lname = request.user.last_name
        initials = fname[0].upper() + lname[0].upper()
        context = {'leaderboard': leaderboard, 'username': current_user, 'rank': rank + 1, 'score': current_score,
                   'questions_solved': correct, 'questions_attempted': attempted, 'initials': initials}
        auth.logout(request)
        return render(request, 'Users/result rc.html', context)  # load result page
    return redirect('login')


# additional function to manage tab switching feature --> discarded

def cheat(request):
    data = {'cheatcounter': request.user.profile.chances}
    if request.method == 'POST':
        request.user.profile.chances -= 1
        request.user.profile.save()
        return JsonResponse(data)
    elif request.method == 'GET':
        return JsonResponse(data)
