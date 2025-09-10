from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Application
from . import db
from .scrapers.scrape_karriere import scrape_karriere, get_cached_postings

main = Blueprint("main", __name__)

@main.route("/")
def list_applications():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)
    status_filter = request.args.get("status", "", type=str)

    query = Application.query

    # Apply search filter
    if search:
        query = query.filter(
            db.or_(
                Application.firm.ilike(f"%{search}%"),
                Application.position.ilike(f"%{search}%")
            )
        )

    # Apply status filter
    if status_filter:
        query = query.filter_by(status=status_filter)

    # Pagination: 10 per page
    pagination = query.order_by(Application.created_at.desc()).paginate(page=page, per_page=10)
    applications = pagination.items

    # History counts per application
    history_counts = {}
    for app in applications:
        count = Application.query.filter(
            Application.firm == app.firm,
            Application.id != app.id
        ).count()
        history_counts[app.id] = count

    return render_template(
        "applications.html",
        applications=applications,
        history_counts=history_counts,
        pagination=pagination,
        search=search,
        status_filter=status_filter,
        title="Applications"
    )


@main.route("/add", methods=["POST"])
def add_application():
    firm = request.form.get("firm")
    position = request.form.get("position")
    note = request.form.get("note")

    if firm and position:
        new_app = Application(firm=firm, position=position, note=note)
        db.session.add(new_app)
        db.session.commit()
        flash("Application added!", "success")
    else:
        flash("Both firm and position are required.", "danger")
    return redirect(url_for("main.list_applications"))


@main.route("/update_status/<int:id>/<string:status>")
def update_status(id, status):
    app = Application.query.get_or_404(id)
    app.status = status
    db.session.commit()
    flash("Status updated!", "info")
    return redirect(url_for("main.list_applications"))


@main.route("/delete/<int:id>")
def delete_application(id):
    app = Application.query.get_or_404(id)
    db.session.delete(app)
    db.session.commit()
    flash("Application deleted.", "warning")
    return redirect(url_for("main.list_applications"))


@main.route("/update_note/<int:application_id>", methods=["POST"])
def update_note(application_id):
    app = Application.query.get_or_404(application_id)
    app.note = request.form.get("note")
    db.session.commit()
    flash("Note updated!", "info")
    return redirect(url_for("main.list_applications"))


@main.route("/history/<string:firm>")
def firm_history(firm):
    # Get all applications for this firm, newest first
    applications = Application.query.filter_by(firm=firm).order_by(Application.created_at.desc()).all()
    return render_template("history.html", applications=applications, firm=firm, title=f"{firm} History")


@main.route("/jobs")
def jobs():
    cache = get_cached_postings()
    postings = cache["postings"]
    last_refreshed = cache["last_refreshed"]
    return render_template("jobs.html", postings=postings, last_refreshed=last_refreshed,)

@main.route("/jobs/refresh")
def refresh_jobs():
    scrape_karriere()
    return redirect(url_for("main.jobs"))