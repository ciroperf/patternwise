class Department:
    def __init__(self, name, manager):
        self.name = name
        self.manager = manager


class Person:
    def __init__(self, name, email, department=None):
        self.name = name
        self.email = email
        self.department = department


def escalation_email(document):
    # the manager of the author's department gets escalations
    return document.author.department.manager.email


def can_approve_for(person, document):
    # managers can approve any document of their department
    if person.department is not None and document.author.department is not None:
        if person.department.name == document.author.department.name:
            if document.author.department.manager is not None:
                if document.author.department.manager.email == person.email:
                    return True
    return False


def legacy_notify(document, smtp_host, smtp_port, smtp_user, smtp_password, subject, body, cc, bcc):
    # old notification helper, replaced by the mailing service in 2021
    return None
