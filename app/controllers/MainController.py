from flask import render_template, jsonify, Blueprint
from sqlalchemy import func
from app.models import User, Day, Weekend,Holiday
from app import db
import calendar
import datetime as dt

c = calendar.Calendar()

# обработка 404
def err404(e):
    return render_template("404.html"), 404

# главная страница
def index():
    return render_template("index.html")

# получить словарь пользователей формата ( "id": "свойства")
# {
#     1: { prop1: val1, prop2:val2 ... }
# }
def get_users_dict():
    users = User.query.filter(User.disabled != True).all()
    rez = {}
    for u in users: rez[u.as_dict()["id"]] = u.as_dict()  
    return rez

# получить словарь дней формата ( "дата": "объект из базы")
# {
#    ГГГГ-ММ-ДД: объект
# }
def craft_dates_dict(query):
    rez = {}
    for q in query: rez[q.date] = q
    return rez

# получить пользователей как json
def get_users():
    users = get_users_dict()
    return jsonify(users)

# получить диапозон дат за месяц. start=d1, end=dn, month - месяц за который считался период
# weeks:
#     [
#         [d1,...,d7]
#         ...
#         [dn-7,...,dn]
#     ]
def get_month_range(year, month, last=False):
    if last: month = (dt.date(year,month,1) - dt.timedelta(days=1)).month
    weeks = c.monthdatescalendar(int(year),int(month))
    start = weeks[0][0]
    end = weeks[-1][-1]
    return weeks, start, end, month

# получить статистику выходных (weekend=1) и будних (weekend=0) дежурств за период с start по end для каждого пользователя
# (uid, True/False, count)
def get_stat_query(start, end, weekend):
    if start and end: return Day.query\
                            .filter(Day.weekend==weekend, Day.date >= start, Day.date <= end )\
                            .with_entities(Day.uid, Day.weekend,func.count(Day.weekend))\
                            .group_by(Day.uid).all()
    else: return Day.query\
                            .filter(Day.weekend==weekend)\
                            .with_entities(Day.uid, Day.weekend,func.count(Day.weekend))\
                            .group_by(Day.uid).all()

# заполнить weeks из get_month_range словарем со значениями {"date" (str), "uid" (int), "weekend" (True/False), "holiday" (False/ uid)}
def get_month(year, month):
    rez = []
    weeks, start, end, month = get_month_range(year, month)
    days = craft_dates_dict(Day.query.filter(Day.date >= start, Day.date <= end).all())
    weekends = craft_dates_dict(Weekend.query.filter(Weekend.date >= start, Weekend.date <= end).all())
    holidays = craft_dates_dict(Holiday.query.filter(Holiday.date >= start, Holiday.date <= end).all())
    for w in weeks:
        week = []
        for d in w:
            weekend = True if d.weekday() >=5 else False
            holiday = False
            if d in weekends: weekend = weekends[d].weekend
            if d in holidays: holiday = holidays[d].uid
            day = {
                "date": str(d),
                "uid": 0 if d not in days else days[d].uid,
                "weekend": weekend,
                "holiday": holiday
            }
            week.append(day)
        rez.append(week)
    return rez

# получить статистику для каждого пользователя по выходным и будням для указанного и прошлого периода
# {"id": {"weekend": 0, "workday": 0, "last_weekend": 0, "last_workday": 0}}
def get_stat(year, month):
    rez = {}
    weeks, start, end, month = get_month_range(year, month)
    last_weeks, last_start, last_end, last_month = get_month_range(year, month, last=True)
    weekend_stat = get_stat_query(start=start, end=end, weekend=1)
    work_stat = get_stat_query(start=start, end=end, weekend=0)
    last_weekend_stat = get_stat_query(start=last_start, end=last_end, weekend=1)
    last_work_stat = get_stat_query(start=last_start, end=last_end, weekend=0)
    all_weekend_stat = get_stat_query(start=None, end=None, weekend=1)
    all_work_stat = get_stat_query(start=None, end=None, weekend=0)

    users = User.query.all()
    for user in users:
        rez[user.id] = {"weekend": 0, "workday": 0, "last_weekend": 0, "last_workday": 0, "all_weekend": 0, "all_workday": 0, "minutes": user.minutes}

    for stat in weekend_stat: rez[stat[0]]["weekend"] = stat[2]
    for stat in work_stat: rez[stat[0]]["workday"] = stat[2]
    for stat in last_weekend_stat: rez[stat[0]]["last_weekend"] = stat[2]
    for stat in last_work_stat: rez[stat[0]]["last_workday"] = stat[2]
    for stat in all_weekend_stat: rez[stat[0]]["all_weekend"] = stat[2]
    for stat in all_work_stat: rez[stat[0]]["all_workday"] = stat[2]
    return rez, last_month, month

def get_index_data():
    now = dt.datetime.now()
    today = Day.query.filter(Day.date == dt.date.today()).first()
    stat, last_month, month = get_stat(now.year, now.month)
    if now.weekday == 5: last_hour_time = dt.time(16,45,0)
    if now.weekday() == 4: last_hour=17
    if now.weekday() > 4: last_hour=0
    return jsonify({
            "users": get_users_dict(),
            "weeks": get_month(now.year, now.month),
            "stat": stat,
            "statMonth": {"last_month": last_month, "month": month},
            "dutyUser": today.uid if today else 0,
            "user": "uid111",
            "endOfDay": str(dt.datetime.combine(now.date(), dt.time(18,0,0)))
        })

def update_stat(year,month):
    print(year, month)
    stat, last_month, month = get_stat(int(year), int(month))
    print(year, last_month, month)
    return jsonify({
            "stat": stat,
            "statMonth": {"last_month": last_month, "month": month}
        })

def update_month(year, month):
    return jsonify({ "weeks": get_month(year, month) })

def go_home(uid, minutes):
    try:
        user = User.query.get(uid)
        user.minutes = user.minutes + int(minutes)
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Досвидания"})
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})

main_module = Blueprint('main', __name__, url_prefix='')

main_module.errorhandler(404)(err404)
main_module.route('/')(index)
main_module.route('/get_users')(get_users)
main_module.route('/get_index_data')(get_index_data)
main_module.route('/update_month/<year>/<month>')(update_month)
main_module.route('/update_stat/<year>/<month>')(update_stat)
main_module.route('/go_home/<uid>/<minutes>')(go_home)
# main_module.route('/stat')(get_stat)