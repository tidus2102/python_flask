from flask.ext.wtf import Form as WTForm
from wtforms.fields import TextField, PasswordField, DateField, RadioField,\
     BooleanField, TextAreaField, FileField, SelectField
from wtforms.validators import Email, InputRequired, ValidationError, Length, \
     Optional, ValidationError
from flask.ext.babelex import gettext, ngettext
from flask.ext.babelex import lazy_gettext
from app.models.user import User
from sqlalchemy import or_
from urlparse import urlparse
import phonenumbers
from datetime import datetime


"""
class FormTranslations(object):
    def gettext(self, string):
        return lazy_gettext(string)

    # FIX: What to use here? There's no lazy version of ngettext
    def ngettext(self, singular, plural, n):
        return ngettext(singular, plural, n)


class Form(WTForm):
    def _get_translations(self):
        return FormTranslations()


class LoginForm(Form):
    email = TextField(lazy_gettext('Email or Phone'), validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])

    def validate(self):
        Form.validate(self)
        if self.email.errors or self.password.errors:
            return False

        user = User.query.filter(
            or_(
                User.email == self.email.data,
                User.phone == self.email.data
            )).first()

        if user is None:
            self.email.errors.append(gettext('Invalid login'))
            return False

        if not user.is_valid_password(self.password.data):
            self.password.errors.append(gettext('Invalid login'))
            return False

        if user.status != User.STATUS_ACTIVE:
            self.email.errors.append(gettext('Your account is not active yet.'))
            return False

        self.user = user
        return True


class RegistrationForm(Form):
    email = TextField(validators=[Email()])
    password = PasswordField(validators=[InputRequired()])
    full_name = TextField(lazy_gettext('Full name'), validators=[InputRequired()])


    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        user = User.query.filter(User.email == self.email.data).first()
        if user:
            # Check duplicate email
            # 1. when creating new user (self.user = None)
            # 2. when updating existing user
            if self.user is None or self.user.id != user.id:
                self.email.errors.append(gettext('Email already exists.'))
                return False

        if self.invitation:
            # check if the email matches with the invite_code
            if self.invitation.invitee_email != self.email.data:
                self.email.errors.append(gettext('Invalid email'))
                return False
        return True


class DoctorRegistrationForm(RegistrationForm):
    #birthday = DateField(lazy_gettext('Birthday'), format='%d-%m-%Y')
    #gender = RadioField(lazy_gettext('Gender'), coerce=int, choices=User.getGenderOptions())

    identity_id = TextField(lazy_gettext('Identity ID'), validators=[InputRequired()])
    license_id = TextField(lazy_gettext('License ID'), validators=[InputRequired()])
    specialist = TextField(lazy_gettext('Specialist'))
    experience = TextField(lazy_gettext('Experience'))
    workplace = TextField(lazy_gettext('Workplace'))
    address = TextField(lazy_gettext('Address'))

    phone = TextField(validators=[InputRequired()])
    invite_code = TextField(lazy_gettext('Invite code'))

    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        user = User.query.filter(User.phone == self.phone.data).first()
        if self.user is None and user:
            self.phone.errors.append(gettext('Phone already exists.'))
            return False
        return True


class UserInfoForm(Form):
    full_name = TextField(lazy_gettext('Full name'), validators=[InputRequired()])
    birthday = DateField(lazy_gettext('Birthday'), format='%d-%m-%Y')
    gender = RadioField(lazy_gettext('Gender'), coerce=int, choices=User.getGenderOptions())
    address = TextField(lazy_gettext('Address'))
    phone = TextField(lazy_gettext('Phone number'))
    email = TextField(validators=[Email(), Optional()])

    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        if not self.email.data and not self.phone.data:
            self.email.errors.append(gettext('Both phone number and email cannot be empty.'))
            return False

        # if user already has data, don't allow to change
        if self.user.phone and self.user.phone != self.phone.data:
            self.phone.errors.append(gettext('Don\'t allow to change phone number'))
            return False
        if self.user.email and self.user.email != self.email.data:
            self.email.errors.append(gettext('Don\'t allow to change email'))
            return False

        check = True
        user = User.query.filter(
                User.id != self.user.id,
                User.phone == self.phone.data).first()
        if user:
            self.email.errors.append(gettext('Phone number already exists.'))
            check = False

        user = User.query.filter(
                User.id != self.user.id,
                User.email == self.email.data).first()
        if user:
            self.email.errors.append(gettext('Email already exists.'))
            check = False
        return check


class ChangePwdForm(Form):
    current_password = PasswordField(lazy_gettext('Current'), validators=[InputRequired()])
    new_password = PasswordField(lazy_gettext('New'), validators=[InputRequired()])
    confirm_password = PasswordField(lazy_gettext('Confirm'), validators=[InputRequired()])

    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        check = True
        if not self.user.is_valid_password(self.current_password.data):
            self.current_password.errors.append(gettext('Wrong password'))
            check = False

        if self.new_password.data != self.confirm_password.data:
            self.confirm_password.errors.append(gettext('Confirmed password must be the same as new password'))
            check = False

        if self.new_password.data == self.current_password.data:
            self.new_password.errors.append(gettext('New password must be different than the old one'))
            check = False
        return check


class ResetPwdForm(Form):
    new_password = PasswordField(lazy_gettext('New password'), validators=[InputRequired()])
    confirm_password = PasswordField(lazy_gettext('Confirm Password'), validators=[InputRequired()])

    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        if self.new_password.data != self.confirm_password.data:
            self.confirm_password.errors.append(gettext('Confirm Password must be the same with New Password'))
            return False
        return True


class UserSettingForm(Form):
    phone_notification = BooleanField(lazy_gettext('Receive notifications via Phone'))
    email_notification = BooleanField(lazy_gettext('Receive notifications via Email'))
    receive_news = BooleanField(lazy_gettext('Receive news via Email'))


class DoctorInfoForm(Form):
    title = TextField(lazy_gettext('Title'), validators=[InputRequired()])
    license_id = TextField(lazy_gettext('Certification'), validators=[InputRequired()])
    #specialist = TextField(lazy_gettext('Specialties'), validators=[InputRequired()])
    #experience_year = TextField(lazy_gettext('Experience'), validators=[InputRequired()])

    specialty_id = TextField(lazy_gettext('Specialties'), validators=[InputRequired()])

    experience_year = SelectField(
        lazy_gettext('Experience'), coerce=int,
        choices=[(i,i) for i in range(1, 11)])

    workplace = TextField(lazy_gettext('Work Places'), validators=[InputRequired()])
    clinic = TextField(lazy_gettext('Personal Clinic'))


class DoctorVideoForm(Form):
    video_uri = TextField(lazy_gettext('Youtube URL'), validators=[InputRequired()])

    def validate_video_uri(self, field):
        if not field.data:
            return True

        # urlparse does not work if the link is missing http scheme
        if not field.data.startswith('http'):
            field.data = '%s%s' % ('http://', field.data)
        parse_value = urlparse(field.data)
        if parse_value.hostname not in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            raise ValidationError(gettext('Unsupported video link.'))


class DoctorExpInfoForm(Form):
    from_date = TextField(lazy_gettext('From (Begin Time)'), validators=[InputRequired()])
    to_date = TextField(lazy_gettext('To (End Time)'), validators=[InputRequired()])

    position = TextField(lazy_gettext('Position/Job Title'), validators=[InputRequired()])
    work_place = TextField(lazy_gettext('Work Place'), validators=[InputRequired()])
    description = TextAreaField(lazy_gettext('Details'))

    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        # from_date.data has format mm/yyyy
        # convert it to date object
        try:
            self.from_date.data = datetime.strptime(self.from_date.data, '%m/%Y')
        except Exception, e:
            self.from_date.errors.append(gettext('Invalid format'))
            return False

        try:
            self.to_date.data = datetime.strptime(self.to_date.data, '%m/%Y')
        except Exception, e:
            self.to_date.errors.append(gettext('Invalid format'))
            return False

        if self.from_date.data > self.to_date.data:
            self.from_date.errors.append(gettext('This field must be smaller than End_Time'))
            return False
        return True


class InvitationForm(Form):
    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        # check if invite_method is defined
        # invite_method is only defined for doctor and patient invitation
        if getattr(self, 'invite_method', None) is None or self.invite_method.data == 0: # invite by email
            if not self.invitee_email.data:
                self.invitee_email.errors.append(gettext('This field is required.'))
                return False
            user = User.query.filter(User.email == self.invitee_email.data).first()
            if user:
                self.invitee_email.errors.append(gettext('Email already exists.'))
                return False
        elif getattr(self, 'invitee_phone', None):
            # invite by sms only for doctor and patient
            if not self.invitee_phone.data:
                self.invitee_phone.errors.append(gettext('This field is required.'))
                return False

            try:
                phone = phonenumbers.parse(self.invitee_phone.data, 'VN')
                assert phonenumbers.is_valid_number(phone)
            except Exception, e:
                self.invitee_phone.errors.append(gettext('Invalid phone number'))
                return False

            user = User.query.filter(User.phone == self.invitee_phone.data).first()
            if user:
                self.invitee_phone.errors.append(gettext('Phone number already exist.'))
                return False
        return True


class UserInvitationForm(InvitationForm):
    invitee_name = TextField(lazy_gettext('Name'), validators=[InputRequired()])
    invitee_email = TextField(lazy_gettext('Email'), validators=[Email(), Optional()])
    invite_text = TextAreaField(lazy_gettext('Invite Text (Optional)'))


# this form can be used for doctor invitation and patient invitation
class DoctorInvitationForm(InvitationForm):
    invite_method = RadioField(lazy_gettext('Invite By'), coerce=int,
            choices=[(0, lazy_gettext('Email')), (1, lazy_gettext('SMS'))],
            default=0)
    invitee_name = TextField(lazy_gettext('Name'), validators=[InputRequired()])
    invitee_email = TextField(lazy_gettext('Email'), validators=[Email(), Optional()])
    invitee_phone = TextField(lazy_gettext('Phone'))
    invite_text = TextAreaField(lazy_gettext('Invite Text'))


class GuardianInvitationForm(InvitationForm):
    invitee_name = TextField(lazy_gettext('Guardian Name'), validators=[InputRequired()])
    invitee_email = TextField(lazy_gettext('Guardian Email'), validators=[Email(), Optional()])
    invitee_phone = TextField(lazy_gettext('Guardian Phone'))
    relationship = SelectField(lazy_gettext('Relation'), choices=UserRelation.getRelationList())
    invite_text = TextAreaField(lazy_gettext('Invite Text'))


class DeliveryForm(Form):
    full_name = TextField(lazy_gettext('Full name'), validators=[InputRequired()])
    email = TextField(lazy_gettext('Email'), validators=[Email(), InputRequired()])
    phone = TextField(lazy_gettext('Phone'), validators=[InputRequired()])
    city = SelectField(lazy_gettext('Choose Province/City'), choices=UserOrder.getCityList(), validators=[InputRequired()])
    address = TextAreaField(lazy_gettext('Address'), validators=[InputRequired()])
    note = TextAreaField(lazy_gettext('Note'))

    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        try:
            phone = phonenumbers.parse(self.phone.data, 'VN')
            assert phonenumbers.is_valid_number(phone)
        except Exception, e:
            self.phone.errors.append(gettext('Invalid phone number'))
            return False
        return True


class AddUserForm(Form):
    full_name = TextField(lazy_gettext('Full name'), validators=[InputRequired()])
    phone = TextField(lazy_gettext('Phone'), validators=[InputRequired()])
    email = TextField(lazy_gettext('Email'), validators=[Email(), Optional()])

    def validate(self):
        Form.validate(self)
        if self.errors:
            return False

        try:
            phone = phonenumbers.parse(self.phone.data, 'VN')
            assert phonenumbers.is_valid_number(phone)
        except Exception, e:
            self.phone.errors.append(gettext('Invalid phone number'))
            return False

        user = User.query.filter(User.email == self.email.data).first()
        if user:
            self.email.errors.append(gettext('Email already exists.'))
            return False

        user = User.query.filter(User.phone == self.phone.data).first()
        if user:
            self.phone.errors.append(gettext('Phone number already exist.'))
            return False
        return True
"""