from test_project.models.TestUserModel import TestUserModel

user = "testpigpeppa@gmail.com"
password = "Testpassword2017"
client_id = "355336847962-7v5qhecc1l3p0hpcnmke9hjgpvgru97j.apps.googleusercontent.com"
client_secret = "a4rSMhaHOpY9-LhhMkWn8lz3"
client = TestUserModel(email=user,
                       password=password,
                       client_id=client_id,
                       client_secret=client_secret)

user_second = "testpigpeppa@gmail.com"
password_second = "Testpassword2017"
client_id_second = "803647386337-jj1s383m0mlt3l4ho65neou156n5m32p.apps.googleusercontent.com"
client_secret_second = "uTGwS9XwwGy88ozgcrIn0nc6"
client_second = TestUserModel(email=user_second,
                              password=password_second,
                              client_id=client_id_second,
                              client_secret=client_secret_second)

base_url = r"https://accounts.google.com/o/oauth2/"

scope_calendar = (r"https://mail.google.com/" +
                  r" https://www.googleapis.com/auth/calendar")

scope_mail = (r" https://www.googleapis.com/auth/gmail.modify" +
              r" https://www.googleapis.com/auth/gmail.readonly" +
              r" https://www.googleapis.com/auth/gmail.insert" +
              r" https://www.googleapis.com/auth/gmail.compose" +
              r" https://www.googleapis.com/auth/gmail.send" +
              r" https://mail.google.com/"
              )

scope_gmail_drafts = (r" https://www.googleapis.com/auth/gmail.modify" +
                      r" https://www.googleapis.com/auth/gmail.compose" +
                      r" https://www.googleapis.com/auth/gmail.readonly" +
                      r" https://mail.google.com/"
                      )

scope_gmail_setting = (r" https://www.googleapis.com/auth/gmail.modify" +
                       r" https://www.googleapis.com/auth/gmail.compose" +
                       r" https://www.googleapis.com/auth/gmail.readonly" +
                       r" https://www.googleapis.com/auth/gmail.settings.basic" +
                       r" https://www.googleapis.com/auth/gmail.settings.sharing" +
                       r" https://mail.google.com/"
                       )

scope_labels = (r" https://mail.google.com/" +
                r" https://www.googleapis.com/auth/gmail.modify" +
                r" https://www.googleapis.com/auth/gmail.labels"
                )

scope_gmail_settings = (r" https://mail.google.com/" +
                        r" https://www.googleapis.com/auth/gmail.settings.basic" +
                        r" https://www.googleapis.com/auth/gmail.settings.sharing"
                        )

scope_settings_forwarding = (r" https://www.googleapis.com/auth/gmail.settings.basic" +
                             r" https://www.googleapis.com/auth/gmail.settings.sharing" +
                             r" https://mail.google.com/")

# Need to method settings.filters.get/settings.filters.list
scope_gmail_settings_filters_least_one = ("https://mail.google.com/" +
                                          "https://www.googleapis.com/auth/gmail.modify" +
                                          "https://www.googleapis.com/auth/gmail.readonly" +
                                          "https://www.googleapis.com/auth/gmail.settings.basic")
# Need to method settings.filters.create/settings.filters.delete
scope_gmail_settings_filters = "https://www.googleapis.com/auth/gmail.settings.basic"
