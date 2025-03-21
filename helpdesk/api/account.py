import dontmanage
from dontmanage.core.doctype.user.user import test_password_strength

"""
	Signup for customer portal only (TODO: agent signups)
"""


@dontmanage.whitelist(allow_guest=True)
def signup(email, first_name, last_name):
    dontmanage.utils.validate_email_address(email, True)

    current_user = dontmanage.session.user
    dontmanage.set_user("Administrator")

    email = email.strip().lower()

    if not dontmanage.db.exists("User", email):
        user = dontmanage.get_doc(
            {
                "doctype": "User",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "send_welcome_email": "0"
                # "role_profile_name": "Helpdesk Contact"	TODO: add this role profile and then un-comment this part
            }
        ).insert()

        dontmanage.get_doc(
            {
                "doctype": "HD Desk Account Request",
                "email": email,
                "user": user.name,
            }
        ).insert()

        dontmanage.set_user(current_user)
    else:
        dontmanage.set_user(current_user)
        dontmanage.throw("User already exists, please try loggin in using this email")


@dontmanage.whitelist(allow_guest=True)
def verify_and_create_account(request_key, email, password):
    account_request = dontmanage.get_doc("HD Desk Account Request", {"email": email})
    if account_request:
        if account_request.request_key == request_key:
            current_user = dontmanage.session.user
            dontmanage.set_user("Administrator")

            user = dontmanage.get_doc("User", account_request.user)
            user.new_password = password
            user.save()

            dontmanage.set_user(current_user)
        else:
            dontmanage.throw("Ivalid request key")
    else:
        dontmanage.throw(f"Account request for {email} not found, please signup first")


@dontmanage.whitelist(allow_guest=True)
def validate_password(password, first_name, last_name, email):
    available = True

    user_data = (first_name, last_name, email)
    result = test_password_strength(password, "", None, user_data)
    feedback = result.get("feedback")

    if feedback and not feedback.get("password_policy_validation_passed", False):
        available = False

    return available
