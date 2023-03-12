from flask_principal import Permission, RoleNeed, Need
from functools import partial
# Needs
be_admin = RoleNeed('Admin')
be_student = RoleNeed('Student')
be_instructor = RoleNeed('Instructor')

# Permissions
admin = Permission(be_admin)
admin.description = "Admin's permissions"
student = Permission(be_student)
student.description = "Student's permission"
instructor = Permission(be_instructor)
instructor.description = "Instructor's permissions"

AdminAccessNeed = partial(Need, 'access')
class AdminAccessPermission(Permission):
    def __init__(self, admin_id):
        need = AdminAccessNeed(admin_id)
        super(AdminAccessPermission, self).__init__(need)
