#from app.models.common import UserRole, User, DoctorPatient, UserRelation

"""
admin_permission = Permission(RoleNeed(UserRole.ADMIN))
user_permission = Permission(RoleNeed(UserRole.USER))
patient_permission = Permission(RoleNeed(UserRole.PATIENT))
doctor_permission = Permission(RoleNeed(UserRole.DOCTOR))



# has permission to view patient resource
# patient himself, his doctors, his guardians
# this is used for web request

# usage: must be used before another decorator that expects a function taking patient_user_id as parameter
# example:
# @node.route('/patient/<patient_user_id>', methods=('GET', ))
# @hasPermissionPatientResource
# def view_patient_info(patient_user, role):
def hasPermissionPatientResource(f):
    @wraps(f)
    def decorator(patient_user_id):
        try:
            patient_user_id = int(patient_user_id)
        except Exception, e:
            abort(404)

        if current_user.role.value == UserRole.DOCTOR:
            patient_doctor = current_user.doctor.getPatientAssociationById(patient_user_id)
            if patient_doctor is None:
                abort(403)
            patient_user = patient_doctor.patient.user
            role = 'doctor'
        else:
            if current_user.id == patient_user_id:
                patient_user = current_user
                role = 'patient'
            else:
                # check guardian permission
                relation = current_user.guardian_relations.filter(
                    UserRelation.user_id == patient_user_id,
                    UserRelation.status == UserRelation.STATUS_ACTIVE
                ).first()
                if relation is None:
                    abort(403)
                patient_user = relation.user
                role = 'guardian'
        return f(patient_user=patient_user, role=role)
    return decorator


# check if the current user has expired
def checkExpiry(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.is_expired:
            return render_template('common/expired.html')
        return f(*args, **kwargs)
    return decorator


# check if the user hasDevice
def hasDevice(f):
    @wraps(f)
    def decorator():
        user_devices = current_user.user_devices
        if user_devices.count() == 0:
            abort(403)
        return f(user_devices=user_devices)
    return decorator


def getDoctor(f):
    @wraps(f)
    def decorator(doctor_user_id):
        try:
            doctor_user_id = int(doctor_user_id)
        except Exception, e:
            abort(404)

        doctor_user = User.query.get(doctor_user_id)

        if not doctor_user or\
            doctor_user.role.value != UserRole.DOCTOR:
            abort(404)

        return f(doctor_user=doctor_user)
    return decorator


def premiumAccountPermission(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.is_patient:
            if current_user.patient.is_premium:
                return f(*args, **kwargs)
            return render_template('common/_upgrade_account.html')
        return f(*args, **kwargs)
    return decorator



# they are used together with @api function
# to check permission of patient/doctor

def doctorPermission(handler):
    def validated(*args, **kwargs):
        user = kwargs.get('user')
        data = kwargs.get('data')
        patient = data.get('patient_id')

        if not user.is_doctor:
            raise ApiError(gettext('Permission denied.'),
                status=ResponseStatus.VALIDATION)

        if patient:
            relation = user.doctor.getPatientAssociationById(patient.user_id)
            if relation is None:
                raise ApiError(gettext('Permission denied.'),
                    status=ResponseStatus.VALIDATION)
        return handler(*args, **kwargs)
    return validated

def patientPermission(handler):
    def validated(*args, **kwargs):
        user = kwargs.get('user')
        if not user.is_patient:
            raise ApiError(gettext('Permission denied.'),
                status=ResponseStatus.VALIDATION)
        return handler(*args, **kwargs)
    return validated

def patientResourcePermission(handler):
    def validated(*args, **kwargs):
        user = kwargs.get('user')
        data = kwargs.get('data')
        patient = data.get('patient_id')

        if user.is_patient:
            patient = user.patient
        elif user.is_doctor:
            if patient:
                relation = user.doctor.getPatientAssociationById(patient.user_id)
                if relation is None:
                    raise ApiError(gettext('Permission denied.'))
            else:
                raise ApiError("Missing required field: patient_id")
        else:
            # guardian
            relation = user.guardian_relations.filter(
                UserRelation.user_id == patient.user_id,
                UserRelation.status == UserRelation.STATUS_ACTIVE
            ).first()
            if relation is None:
                raise ApiError(gettext("Permission denied."))

        kwargs['patient'] = patient
        return handler(*args, **kwargs)
    return validated
"""