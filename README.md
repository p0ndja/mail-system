# Mail System
This is a python mail sender system which is used as a backend on communicating with SMTP server.
It's use `stmplib` for SMTP connection with SSL security.

Mainly code are in PondJaMail.
It use method `sendMail()` to send email with required parameters:
- sender(str) -> sender information, need to specify in pattern : name;email;password
- receiver(str) -> receiver information, only email.
- subject(str) -> title of the email.
- mail(str) -> source to be email template. If you have any variable to replace, be sure that it's in "{{variable}}" format
- variable(str) -> any variable that being to replace from email template. Can't be empty but can send empty json ("{}").

You can import PondJaMail for sending email purpose, as a demo in `database-to-mail.py` example.