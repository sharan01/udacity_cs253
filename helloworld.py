import webapp2
import codecs
import re

form =""" 
<form method="post" action="/rot13">
	<textarea name="text">%(text)s</textarea>
	<input type="submit" />
</form>

"""

validation = """ 
<form method="post" action="user">
	<input type=text name="username" value="{username}" />{uerror}<br>
	<input type=text name="password" />{perror}<br>
	<input type=text name="verify" />{verror}<br>
	<input type=text name="email" value="{email}" />{eerror}<br>
	<input type="submit"><br>


</form>


"""
class Form:
	def username(self,username):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		return USER_RE.match(username)
	def password(self,password):
		PASSWORD_RE = re.compile("^.{3,20}$")
		return PASSWORD_RE.match(password)
	def email(self,email):
		EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")
		return EMAIL_RE.match(email)

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(form)


class ROT13(webapp2.RequestHandler):
	def write_form(self,text=""):
		self.response.out.write(form%{"text":text})

	def get(self):
		self.write_form("")
	def post(self):
		user_string = self.request.get('text')
		rot13_string = codecs.encode(user_string,'rot_13')
		self.write_form(rot13_string)
class User(webapp2.RequestHandler):
	def write_form(self,un="",em="",eun="",ep="",evp="",eem=""):
		self.response.out.write(validation.format(	username=un,
													email=em,
													uerror=eun,
													perror=ep,
													verror=evp,
													eerror=eem))
	def get(self):
		#self.response.out.write("ghhghj")
		self.write_form("hgf")
	def post(self):
		f = Form()
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		un = f.username(username)
		p = f.password(password)
		v = f.password(verify)
		if email=="":
			em = True 
		else:
			em = f.email(email)
		
		uerror = "" if un else "invalid username"
		perror = "" if p else "invalid passord"
		verror = "" if password==verify else "passwords do not match"
		eerror = "" if em else "invalid"
		if un and p and v and em :
			#uname = self.request.get("username")
			#self.response.out.write("welcome " + uname)
			self.redirect("/welcome?username="+username)
		else:

			self.write_form(username,email,uerror,perror,verror,eerror)

class Welcome(webapp2.RequestHandler):
	def get(self):
		f= Form()
		uname = self.request.get("username")
		if f.username(uname):
			self.response.out.write("welcome " + uname)
		else:
			self.redirect('/user')
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', ROT13),
    ('/user',User),
    ('/welcome',Welcome)
], debug=True)

