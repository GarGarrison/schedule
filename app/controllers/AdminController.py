from flask import Blueprint, request, render_template, jsonify
from app import db
from app.models import User, Day, Weekend, Holiday
import datetime as dt
def admin():
    return render_template("admin.html")

def get_user(uid):
    try:
        return jsonify(User.query.get(uid).as_dict())
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})

def add_user():
    try:
        data = request.get_json()
        user = User(data)
        db.session.add(user)
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Успешно добавлено"})
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})

def edit_user():
    try:
        data = request.get_json()
        user = User.query.get(data.get("id"))
        user.update_dict(data)
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Успешно изменено"})
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})

def disable_user(uid):
    try:
        user = User.query.get(uid)
        user.disabled = True
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Успешно удален"})
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})

def create_day():
    try:
        data = request.get_json()
        day = Day(data)
        db.session.add(day)
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Успешно добавлено"})
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})

def update_day():
    try:
        data = request.get_json()
        d = dt.datetime.strptime(data.get("date"), "%Y-%m-%d")
        day = Day.query.get(d)
        day.update_dict(data)
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Успешно изменено"})
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})

def toggleWeekend():
    try:
        data = request.get_json()
        d = dt.datetime.strptime(data.get("date"), "%Y-%m-%d")
        weekend = Weekend.query.get(d)
        day = Day.query.get(d)
        if day: day.weekend = not day.weekend
        if weekend: weekend.update_dict(data)
        else:
            weekend = Weekend(data)
            db.session.add(weekend)
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Успешно добавлено"})
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})

def addHolidays():
    try:
        days = []
        data = request.get_json()
        uid = data.get("uid")
        from_d = dt.datetime.strptime(data.get("from").split("T")[0], "%Y-%m-%d")
        till_d = dt.datetime.strptime(data.get("till").split("T")[0], "%Y-%m-%d")
        while from_d <= till_d:
            holiday = Holiday({"uid": uid, "date": from_d})
            days.append(holiday)
            from_d = from_d + dt.timedelta(days=1)
        db.session.bulk_save_objects(days)
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Успешно добавлено"})
    except Exception as e:
        raise(e)
        return jsonify ({
            "status": "err",
            "msg": str(e)})
def delHoliday():
    try:
        data = request.get_json()
        holiday_deleted = Holiday.query.filter(
            Holiday.date == data.get("date"),
            Holiday.uid == data.get("uid")).delete()
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": "Успешно удалено"})
    except Exception as e:
        return jsonify ({
            "status": "err",
            "msg": str(e)})


def edit_hours():
    try:
        data = request.get_json()
        user = User.query.get(data.get("id"))
        old_minutes = user.minutes
        delta_minutes = int(data.get("count")) * 60
        action = data.get("action")
        msg = "Успешно добавлено"
        if action == "+": user.minutes = old_minutes + delta_minutes
        elif old_minutes < delta_minutes: msg = "Недостаточно часов"
        else: user.minutes = old_minutes - delta_minutes
        db.session.commit()
        return jsonify ({
            "status": "ok",
            "msg": msg})
    except Exception as e:
        raise e
        return jsonify ({
            "status": "err",
            "msg": str(e)})

admin_module = Blueprint('admin', __name__, url_prefix='/admin')

admin_module.route('/', methods=['GET'])(admin)
admin_module.route('/get_user/<uid>', methods=['GET'])(get_user)
admin_module.route('/add_user', methods=['POST'])(add_user)
admin_module.route('/edit_user', methods=['POST'])(edit_user)
admin_module.route('/disable_user/<uid>', methods=['GET'])(disable_user)
admin_module.route('/create_day', methods=['POST'])(create_day)
admin_module.route('/update_day', methods=['POST'])(update_day)
admin_module.route('/toggle_weekend', methods=['POST'])(toggleWeekend)
admin_module.route('/add_holiday', methods=['POST'])(addHolidays)
admin_module.route('/del_holiday', methods=['POST'])(delHoliday)
admin_module.route('/edit_hours', methods=['POST'])(edit_hours)