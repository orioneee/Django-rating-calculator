from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from polls.models import RatingSubject, RatingRecord


class Subject:
    def __init__(self, subject, credit, enabled):
        print(subject, credit, enabled)
        self.subject = subject
        self.credit = credit,
        self.enabled = enabled


@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        return redirect('/table')
    else:
        return redirect('/login')


@csrf_exempt
def fillSubjects(request):
    RatingSubject.objects.all().delete()
    subjects = [
        Subject("АМС", 5, True),
        Subject("ОТЗП", 5, True),
        Subject("Soft Skills", 4, True),
        Subject("ЕМТ", 3, True),
        Subject("Метрологія", 3, True),
        Subject("ОМ", 5, True),
    ]
    print(subjects)
    for subject in subjects:
        print(subject.subject, subject.credit, subject.enabled)
        RatingSubject.objects.create(subject=subject.subject, credits=subject.credit[0], enabled=subject.enabled)
    return JsonResponse({"status": "ok"})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("fill_rating")
        else:
            return render(request, 'login.html', {"messages": ["Wrong username or password"]})
    else:
        return render(request, 'login.html')

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user is not None:
                return render(request, 'registration_form.html', {"messages": ["User already exists"]})
            else:
                User.objects.create_user(username=username, password=password, first_name=name)
                login(request, user)
                return redirect('/fill_rating')
        except User.DoesNotExist:
            User.objects.create_user(username=username, password=password, first_name=name)
            login(request, User.objects.get(username=username))
            return redirect('/fill_rating')
    return render(request, 'registration_form.html', )

@csrf_exempt
def ratingForm(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        subjects = RatingSubject.objects.all()
        data = []
        for subject in subjects:
            record = RatingRecord.objects.filter(user=request.user, subject=subject)
            if len(record) == 0:
                data.append({
                    "subject": subject.subject,
                    "credits": subject.credits,
                    "value": "",
                    "enabled": subject.enabled,
                })
            else:
                data.append({
                    "subject": subject.subject,
                    "credits": subject.credits,
                    "value": record[0].rating if record[0].rating is not None else "",
                    "enabled": subject.enabled,
                })
        # return JsonResponse(data, safe=False)
        return render(request, 'FillRating.html', {'subjects': data})
    else:
        try:
            RatingRecord.objects.filter(user=request.user).delete()
        except RatingRecord.DoesNotExist:
            pass
        for subject in RatingSubject.objects.all():
            rating = request.POST.get(subject.subject)
            if rating is not None:
                RatingRecord.objects.create(user=request.user, subject=subject, rating=StringToFloat(rating))
            else:
                RatingRecord.objects.create(user=request.user, subject=subject, rating=None)
        return redirect('/table')


@csrf_exempt
def ratingTable(request):
    users = User.objects.all()
    res = []
    for user in users:
        ratingRecords = RatingRecord.objects.filter(user=user)
        t = {}
        t['name'] = user.first_name
        t["records"] = [record.rating for record in ratingRecords]
        if len(t["records"]) < len(RatingSubject.objects.all()):
            for i in range(len(RatingSubject.objects.all()) - len(t["records"])):
                t["records"].append("-")
        for i in range(len(t["records"])):
            if t["records"][i] is None:
                t["records"][i] = "-"

        t['rating'] = calculateRating(ratingRecords)
        res.append(t)

    res.sort(key=lambda x: x['rating'], reverse=True)
    for r in res:
        r['position'] = res.index(r) + 1
    print(res)
    return render(request, 'table.html', {'records': res, 'subjects': RatingSubject.objects.all()})


@csrf_exempt
def calculateRating(ratingRecords):
    sum = 0
    credits = 0
    for record in ratingRecords:
        if record.rating is not None:
            sum += record.rating * record.subject.credits
            credits += record.subject.credits
    if credits == 0:
        return 0
    return sum / credits


def StringToFloat(str):
    try:
        return float(str)
    except ValueError:
        return None
