# Разработка защищённых приложений

## Task I

Implement a GUI application that satisfies
the following requirements:
- The application authenticates the user.
- Each user of the program must belong to some
a group of users (roles) whose members have access to various
functionality of the program.
- The program must accept some input from the user and,
perhaps, after some processing, display them.
- При этом должна осуществляться защита от как минимум 4-х типов
возможных атак на приложение:
    1. Buffer overflow attack.
    2. SQL injection attack.
    3. An attack exploiting canonicalization errors.
    4. Attack "XSS" (cross-site coding).
    5. The principle of minimizing privileges.
    6. DoS attack (denial of service).


Implement an installer application that allows you to install on
user's computer application implemented in the previous paragraph
tasks.

## Task II

Implement an installer application that allows you to install on
user's computer application implemented in the previous paragraph
tasks.

Application requirements:
- Installer application together with the application to be installed must provide
protection software unauthorized reproduction.
- The installer application must be protected from possible attacks on
him.

### **Watch info about pyinstaller and NSIS**

## Task III
Test the correct operation of the protection systems developed
applications through the implementation of test attacks of the selected 4 types.