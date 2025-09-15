import secrets
import smtplib
from email.mime.text import MIMEText

from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required

from ..extensions import db
from ..forms import LoginForm, RegistrationForm
from ..models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


def send_verification_email(user: User) -> None:
    """Send a verification email to the user.

    The function attempts to deliver an email containing a verification
    link. Errors during the process are logged but do not interrupt the
    registration flow.
    """

    verify_url = url_for("auth.verify", token=user.verification_token, _external=True)
    msg = MIMEText(f"Please verify your account by visiting: {verify_url}")
    msg["Subject"] = "Verify your account"
    msg["From"] = current_app.config.get("ADMIN_EMAIL", "admin@example.com")
    msg["To"] = user.email

    server = current_app.config.get("MAIL_SERVER", "localhost")
    port = int(current_app.config.get("MAIL_PORT", 25))
    username = current_app.config.get("MAIL_USERNAME")
    password = current_app.config.get("MAIL_PASSWORD")
    try:
        with smtplib.SMTP(server, port) as smtp:
            if username and password:
                smtp.login(username, password)
            smtp.send_message(msg)
    except Exception as exc:  # pragma: no cover - best effort logging
        current_app.logger.error("Failed to send verification email: %s", exc)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_verified:
                flash('Account not verified', 'warning')
            else:
                login_user(user)
                return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        user.set_password(form.password.data)
        user.verification_token = secrets.token_urlsafe(16)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        flash('Registration successful - please verify via email', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@bp.route('/verify/<token>')
def verify(token: str):
    """Verify a user's account via the provided token."""

    user = User.query.filter_by(verification_token=token).first_or_404()
    user.is_verified = True
    user.verification_token = None
    db.session.commit()
    flash('Account verified, you may log in', 'success')
    return redirect(url_for('auth.login'))
