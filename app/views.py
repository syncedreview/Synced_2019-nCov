from django.shortcuts import render
from django.http import JsonResponse
from app.tools import strtime_to_timestamp_10, timestamp_to_strtime
from apscheduler.scheduler import Scheduler
import json, requests

# Create your views here.

sched = Scheduler()


@sched.interval_schedule(hours=1)
def fetch():
    url = 'https://lab.isaaclin.cn/nCoV/api/overall?latest=0'
    try:
        content = requests.get(url)
        content = json.loads(content.text)
        data = []
        for idx, val in enumerate(content['results']):
            temp = {}
            temp['confirmedCount'] = val['confirmedCount']
            temp['suspectedCount'] = val['suspectedCount']
            temp['curedCount'] = val['curedCount']
            temp['deadCount'] = val['deadCount']
            temp['updateTime'] = val['updateTime']
            try:
                temp['seriousCount'] = val['seriousCount']
            except:
                temp['seriousCount'] = 'NULL'
            try:
                temp['suspectedIncr'] = val['suspectedIncr']
            except:
                temp['suspectedIncr'] = 'NULL'
            try:
                temp['confirmedIncr'] = val['confirmedIncr']
            except:
                temp['confirmedIncr'] = 'NULL'
            try:
                temp['curedIncr'] = val['curedIncr']
            except:
                temp['curedIncr'] = 'NULL'
            try:
                temp['deadIncr'] = val['deadIncr']
            except:
                temp['deadIncr'] = 'NULL'
            try:
                temp['seriousIncr'] = val['seriousIncr']
            except:
                temp['seriousIncr'] = 'NULL'
            try:
                temp['currentConfirmedCount'] = val['currentConfirmedCount']
            except:
                temp['currentConfirmedCount'] = 'NULL'
            try:
                temp['currentConfirmedIncr'] = val['currentConfirmedIncr']
            except:
                temp['currentConfirmedIncr'] = 'NULL'
            data.append(temp)

        with open('data.json', 'w') as f:
            json.dump(data, f)
    except:
        print('Fetch Data Error...')

fetch()
sched.start()


def show(request):
    date = request.GET.get('date')
    hour = request.GET.get('hour')
    local_str_time = date + ' ' + hour + ':00:00'
    timestamp = strtime_to_timestamp_10(local_str_time)
    with open('data.json', 'r') as f:
        content = json.load(f)
    delta = [abs(timestamp - int(str(i['updateTime'])[:-3])) for i in content]
    target = content[delta.index(min(delta))] 
    data = {
        "confirmed_case": target['confirmedCount'],
        "suspected_case": target['suspectedCount'],
        "cured_case": target['curedCount'],
        "death_case": target['deadCount'],
        "serious_case": target['seriousCount'],
        "current_confirmed_case": target['currentConfirmedCount'],
        "confirmedIncr": target['confirmedIncr'],
        "suspectedIncr": target['suspectedIncr'],
        "curedIncr": target['curedIncr'],
        "deadIncr": target['deadIncr'],
        "seriousIncr": target['deadIncr'],
        "currentConfirmedIncr": target['currentConfirmedIncr'],
        "time": timestamp_to_strtime(target['updateTime'])[:-7]
    }
    return render(request, 'index.html', data)


def api(request):
    date = request.GET.get('date')
    hour = request.GET.get('hour')
    local_str_time = date + ' ' + hour + ':00:00'
    timestamp = strtime_to_timestamp_10(local_str_time)
    with open('data.json', 'r') as f:
        content = json.load(f)
    delta = [abs(timestamp - int(str(i['updateTime'])[:-3])) for i in content]
    target = content[delta.index(min(delta))] 
    data = {
        "confirmed_case": target['confirmedCount'],
        "suspected_case": target['suspectedCount'],
        "cured_case": target['curedCount'],
        "death_case": target['deadCount'],
        "serious_case": target['seriousCount'],
        "current_confirmed_case": target['currentConfirmedCount'],
        "confirmedIncr": target['confirmedIncr'],
        "suspectedIncr": target['suspectedIncr'],
        "curedIncr": target['curedIncr'],
        "deadIncr": target['deadIncr'],
        "seriousIncr": target['deadIncr'],
        "currentConfirmedIncr": target['currentConfirmedIncr'],
        "time": timestamp_to_strtime(target['updateTime'])[:-7]
    }
    return JsonResponse(data)
