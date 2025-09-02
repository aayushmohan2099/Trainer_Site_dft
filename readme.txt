UPSRLM Training site Draft #1  By Ayush M Srivastava
-----------------------------------------------------

- Installed Git
- Installed Repo
- Installed venv
- Installed Django


Project Start
--------------

- Installed accounts app

- Target,
----------

User Registration Page

User Login Page

Basic Home Page (only visible after login)

- Pages to build,
------------------

1) Beneficiary Registration + Login
    - Full registration form (all fields from URS).
    - After login → redirect to Beneficiary Homepage.

2) Beneficiary Homepage (Dashboard)
    - Simple welcome message.
    - Display SHG info, membership details, demographics, etc.

3) Master Trainer Login + Homepage (for demo)
    - Separate login for Master Trainers.
    - Trainer homepage showing qualifications, expertise, and availability (from URS dataset).

- Problems Faced,
------------------

1) Import/Export not appearinmg in the admin Page
2) Foreign key Problems
3) The imported users have no password so no way of login
4) They have no first and last name

- New Model Needed!
-----------------------

VO (Village Organizer model to supervise and create overview of beneficiaries to reset their uname and pass)

