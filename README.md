# A1000Words
### Video Demo:  <URL HERE>

---
### Description:

### Table of Contents
- Introduction
- How to run the web application
- The description of the files
- Discussion

---
### Introduction
My final project is a simple website which in its idea is meant to be a writing challenge and in its functionality is very similar to a blog concept. Registered users can submit posts with their stories, that have been inspired by a photo or an image. The other users then have an opportunity to write their own stories based on the uploaded images. The idea came from the saying ”a picture is worth a 1000 words”, and in this case users have the opportunity to express their own 1000 words, that the image tells them. I have also implemented a very simple photo filter feature, where users can apply a cartoon filter on an uploaded image. The user can then proceed to use the cartoon image in one of the post options.   
As a complete beginner in programming, I am using skills I obtained during the course. The project is built with the Flask framework with Bootstrap (version 4.6) frontend tools. I am using Jinja to render templates. My database is setup with SQLite and I am using my computer (local ssetup) to host the database (db). The chosen programming language is Python and I used VS Code as a text editor.

---
### How to run the web application

To get up and running, enter the following flask commands to the terminal. The first command tells Flask where to find the application. The second command declares the mode to be development.

//TODO: add pre-requisites here...

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
flask init-db
```

---
### The files

I have decided to structre this part based on the folders in the project. The paragraphs are named based on a folder from the project and the subsections of the content are the files contained in the folder.

The size of the title indicates if it is a header, folder or a file. For example:
### Header
#### Folder
##### File
###### References

---
### The Python files

---
#### Flaskr
It is a Python package, that includes the code for the application and most of the necessary files.

---
##### __init__.py

This file has two main purposes. It contains the application factory and it signals to Python, that the project folder flaskr directory should be treated as a package. 
The file begins with the application factory function named `create_app()`. The `instance_relative_config = True` basically lets the app know, that the configuration file can be found in the instance folder.

Next in the code is ` app.jinja_env.filters['number_of_comments'] = number_of_comments`.This is a custom filter, that retrives the number of comments a post has and is applied in the `index.html` file. `Bootstrap(app)` is added to the file to have access to some of the design features from the Bootstrap library via a package called `flask_boostrap`. `Csrf.init_app(app)` is a little security addition, that protect users against CSRF(Cross-Site Request Forgery) attacks. An unique token is created with every submission of a form in this project to make it impossible for an unintended task on the user authenticated web application on the behalf of the someone elses interest. If FlaskForm is used, then it should already include CSRF protection, but as my project is not consistent in its design, I decided for the sake of gaining experince to add it myself aswell. 

The next section in the file is about the configuration settings for developing or testing. The regular configuration of the entire application is applied through ` app.config.from_pyfile('config.py') `, which can be found in the code snippet below. It links to a separate `config.py` file, that includes all the important configurations values, which will replace the defalut settings. The importance of having an instance folder is explained in the **Instance** paragraph below. 

```python
if test_config is None:
  # load the instance config, if it exists, when not testing
  app.config.from_pyfile('config.py', silent=True)

else:
  # load the test config if passed inS
  app.config.from_mapping(test_config)    
```
The `else` section above is dedicated to testing. I have not included the testing folder in this report as the code I was experimenting with was borrowed from the Flask Tutorial and wasn't an original addition. The code below is to check the presence of the instance folder and its path.

```python
try:
  os.makedirs(app.instance_path)
except OSError:
  pass    
```
The last lines of the code are to register the blueprints with the app. Blueprints are a way to organize related code and to avoid having one large file for all of the project.
```python
# authentication
from . import auth
app.register_blueprint(auth.bp)
``` 
###### References

1. https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
2. https://pythonhosted.org/Flask-Bootstrap/forms.html
3. https://portswigger.net/web-security/csrf/tokens
4. https://flask-wtf.readthedocs.io/en/stable/csrf.html

---
##### Auth.py

Is a module, where functions concerning user authentication have been gathered. The files begings with the creation of the Blueprint. 
`bp = Blueprint('auth', __name__, url_prefix='/auth')`
The line includes the name of the Blueprint, which in this case is `auth` and `url_prefix` means that `auth` is added before all views and URLs in the blueprint.  
The file includes register, login, logout, and password change functions. In addition, functions to check if a user is logged in (`login_required`) and fetching data for logged in user(`load_logged_in_user`) have been added. 

`Login_required` is categorized as a decorator, by adding this to other views, it makes sure a user is logged in before giving access to the page. In the case of register and login the function will return a form for the user to fill in. For WTForms classes have been defined on `extensions.py` file. These classes are called in the code lines below and then fed to the the html files for forms. 
```python
form = RegistrationForm(request.form)
form = LoginForm(request.form)
```
When the user submits the data, it will be validated, which ends up as either an error, the registration of a new user or a successful login. In case of successful login, the session dictionary is cleared before saving the recently logged in user id. `User['user_id']` gives access to most features in the web application and is important to make sure it is the correct value. 
```python
if error is None:
  session.clear()
  session['user_id'] = user['user_id']
  return redirect(url_for('index'))
```
The password is stored as a hash for better security. In the case of a password change the user is asked for the username and old password, which will be validated and their new desired password, which will be checked not to be the same as the old password. If the requirements have been fulfilled, the new password will be hashed and added to the db, if one of them fails, the form is loaded again with an error message.
The logout function clears the user id from the session dictionary. 

###### References

1. https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/?highlight=upload%20file

---
##### Blog.py

The second blueprint gathers code concerning a logged in user’s abilities, to perform CRUD operations (create, read, update/edit and delete) on a post. This is the file with most lines in this project.
If the user is logged in, the blueprint begins with index page function, that fetches and shows all the posts from the db. If no user id is present in the session dictionary the program refers the user to the landing page (`about.html`), where they are asked to either Register or Log in.
```python
if g.user is None:
    return render_template('blog/about.html')
```
The second function is about the creation of a post. Firstly, the user is directed to a page, where they must choose their post format, in this case there are 4 templates to choose from, which have been divided into 4 different functions for each type of posts. The 4 types of posts are as follows: 
1. title and body
2. title and image
3. title and cartoonified image
4. title, image and body.

In each case a specific form is shown to the user. 

The post types that include a `body` section use a WYSIWYG (What You See Is What You Get) text editor called TinyMCE text to get the user text input. The received text needs to be cleaned before injecting it to the db, which is done with line `re.compile(‘<.*>’)`, that removes the unnecessary tags from the text. 

The posts with images requires users to choose and upload an image. I have implemented two versions of image storage:
1. The most common is, where uploaded images are directly stored in the `UPLOAD_FOLDER`. The path to the folder can be find in the `config.py` file. 
2. The second version is explained in the `upload.py`, where the uploaded image is stored differently due to additional photo editing step. 

In addition, a list of selected file extensions has been listed to prevent unwelcomed files being uploaded to db. The filename is run through `werkzeug.secure_filename()` to make sure the code doesn’t directly save the `“UPLOAD_FOLDER + filename”` path to the db, so that unwelcomed intruders can’t just send an input named `filename=”../../filename”` as the function takes the file path and converts it to a more secure version, which will be then added to the db. 

The post creation with cartoon images is a different process. The page has a dropdown menu, from where the user can choose images, they have uploaded. 

The next two functions (`update_post(id)` and `update_comment(id)`) are concerning the user’s ability to edit a post or a comment. In both cases the id of a post or a comment is an input to the function, that is used to fetch the specific information from the db. The id is used in the `entry= get_post(id)`, which is fetching the specific data for the enquiry. The `get_post()` function can be found in the `helpers.py` file. 

The reply function (`reply(id)`) gives the users ability to comment on a post. When the function is called, the user is shown the original post followed with all its comments. To be able to perform it, both the post and comments need to be fetched from the db. As a user submit their reply, the inputs are validated, and if no errors are inserted into the db or validation errors are shown to guide them. The user is then redirected to the same page, where they see the original post with all of the comments including theirs.

The last two functions (`delete_post(id)` and `delete_comment(id)`) are dedicated to deleting a post or a comment. These functions require an input, which needs to be the id of the post or comment. The id is used to fetch the correct db entry for deletion. In my code, the action of deleting is separated between the post and comments table. The last step is redirecting the user to the index page with a flash message, letting the user know of the successful deletion of the post/comment. 

###### References

1. https://flask.palletsprojects.com/en/1.1.x/tutorial/views/
2. https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/?highlight=upload%20file

---
##### Db.py

The file includes 5 functions: 
1. First (`get_db()`) is used to establish a connection to the database. The path to the file can be found in the `config.py` under the name `DATABASE`. 
2. Then (`close_db`) is used to check if the connection to the db was successful and to close the connection. 
3. Thirdly, the `init_b` function is called to create all the necessary tables for the db. It can be used to reset the db completely as it deletes and recreates all tables. The list of tables and variables included in the tables can be seen in the file `schema.sql`. 
4. Then the (`init_db_command()`) function utilizes the power of the `init_b` function. At the beginning of the app development flask `init_b` command is ran in the terminal, that creates all the necessary db tables. After successful initiation a *“Initialized the database”* message is printed in the terminal. 
5. The last function (`init_app(app)`) allows the `init_b` command to be registered with the application and be used a flask command. As a result of running the command `flaskr.sqlite` is created into the instance folder.

###### References

1. https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

---
##### Extensions.py

The file was created to try to keep the `__init__.py` file cleaner and more consise. There were several ways to accomplish this and I just chose to have a separate file and import it to the `__init__.py`. It includes a library import necessary to implement the `csrf` token and it also includes a line of code, which is needed to run the system successfully. 

---
##### Forms.py

The file is dedicated to the definition of classes for different types of forms used in the code. There is a class created for registration, login and password change.  `Validators.DataRequired()` makes sure an imput has been submitted by a user. `Validators.Length(min, max)` set a minimum and maximum limitation for the length of the password. During the password change process, the new password and confirm (the same password repeated) is checked by `validators.EqualTo(‘confirm’, …)` to makes sure the same string has been submitted.

###### References

1. https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/ 

---
##### Helpers.py

Helpers is a collection of functions that are mostly called to fetch data from the db. The first function named `allowed_file` is written in connection to uploading a file. It checks if the filename extension is one of the allowed ones. 

The `number_of_comments`  is a custom function that counts the number of comments a post has. The value can be seen on the index page under a post in the parathesis in the button “Comment ()”.  The function needs an input, which is the id of the post. Based on the id, the COUNT command in SQL is used for the task. `Number_of_comments` value after the COUNT needs to be converted to a list and has to be converted to be a string for the filter(read more about the filter in `index.html`) to work properly. The `[1:-1]` is added to remove the square parathesis before the variable is returned. 

The next 4 functions are built the same way to fetch either a single post or a comment, a group of comments or a image. The process begins with establishing connection with the db and follows by the retrieval of the data. In case data wasn’t found, an error message is projected. Otherwise the retrieved data is returned. 

---
##### Schema.py

The file to create tables where user related data is stored and retrieved from. The first lines delete tables one by one. This means all data, which has been saved in the tables will be deleted. The code creates 4 tables: user, post, comments and cartoon. The user table contains the user id, username and password. The post table saves data about created post. The comment table is dedicated to everything related to comments and cartoon save information about the images, that are edited to look like cartoons.  

###### References

1.https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

---
##### Upload.py

This is the third blueprint of the project. Be warned as the file is quite chaotic because I wanted experiment a little. The code is dedicated for uploading an image and applying an image filter using the PIL (PILLOW) library. 

The first part of the uploading process is the same as described in the `blog.py` paragraph. To sum up it quickly: get the image file from a form, check the file before proceeding to add it to the db. The filename is reformed by the `secure_filename` function to hide the path to the upload folder. The file is saved to the upload folder. The location of the original image is saved under the name of `photoPath`. 

I also experimented uploading an image as a BLOB, which is stored in the db. To achieve it, the image needed to be converted to blobdata. After the conversion the blob is inserted into the db with the usual insert into command. 

The image is edited with the `uploaded_file` function. The function uses the stored blob to convert it back to file format and apply the photo editing filter. The image is edited with a filter named quantize. The value 9 defines the number of colors to which the color scale is reduced. The new image is renamed and inserted to the upload folder and the edited cartoon image is shown to the user with `send_from_directory`. It is a secure and quick, but also rough way to show a static file from an upload folder. The user has access to the cartoon images in the process of cartoon image post creation. // TODO: what?

---
### HTML and CSS files

This project uses the Jinja template library to render templates. Jinja is similar to Python. Special delimiters are used to distinguish Jinja syntax from the static data in the template. Anything between `{{` and `}}` is an expression that will be output to the final document. `{% and %}` denotes if and for statements. 

---
#### Static

The static folder is meant to contain all the static files of the project. Images, GIFs and css files used in the design are stored in this folder. It provides the opportunity to reference a file with referenced // TODO: what? with `url_for('static', filename='...')`.

---
##### Base.html

Often named as `layout.html`. The file defines the general layout and style of each of the pages it is extended to. By having `base.html` the developer doensn't have to write the entire html structure in each template. The page begins with the obligatory `<!doctype html>` followed by the `<html>` tag, in which the language of the file is defined to be English. The next tag is the `<head>` tag, that includes all of the links to necessary scrips or libraries to run the design implemented in the application. The linking to css files, scripts files as well as all the other plugins used such as TinyMCE in my project are done here as well. The `<title>` tag allows the developer to name tab in the brower. `{% block title %}` allows to change or add to the title in the browser’s tab and the window title.

The main area of a web application is the body of the page. The definition and styling of it is done within the `<body>` tag. In the tag a JavaScript (JS) function `onload = “SelectFileText()”` has been added to make it possible to see the filename in the form, that is chosen to be uploaded. The first information in the body tag are the link to Bootstrap design library for the version 4.6. The location of the links are intentionally and determined by the Bootstrap library documentation. 

The `<header>` tag defines the top side of the page/section, which usually includes a heading, search, navigation bar, a logo etc. The navigation bar is located in the `<header>` tag. The navbar is divided into two views based on if a user is logged in or not. If the user is logged in they have access to the Home, New post and Cartoonifiy photo options on the left side of the bar and a settings icon on the right. In the settings menu, the username is shown with an icon, change password and a logout button. If the user is not logged in, they are referred to the about page (`about.html`), where on the left side of navbar have a choice between the Register or Login actions.

The `<main>` tag is the section which is mostly changed throughout other html pages.  The first element in the tag and before the content, is the `{% block header %}`, which is similar to title but instead will change the title displayed on the page. Although this block is defined in the project, I personally haven’t used it too much. 

Next is the `get_flashed_messages()`. If the application receives `flash()` signal, which in most cases are either errors or notifications the template loops over each message returned and displays them. The most important block is the `{% block content %}`, which is implemented in all of the other HTML pages in this project.

The last part of the file is dedicated to the `<footer>`. I haven’t design the footer in this project, but if I want to try it in the future, then it is ready to be worked on. The section includes a defined block  `{% block footer %}`, which can be easily extended to other pages. 

---
#### Tinymce

A folde , that needed to be added to be able to implement the TinyMCE editor for the blog. It is a WYSIWYG text editor, that looks good and has good customization options. My setup has been kept at a basic level and the code part of this feature is in the `base.html`.

---
#### Upload

Folder where all of the uploaded images are kept. 

---
##### Style.css

A file, that is a stylesheet and used to format the contents of a webpage. 

---
#### Templates

Templates are files that contain static data as well as placeholders for dynamic data. A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates. Templates render HTML which will display in the user’s browser. 

FI will not write in as much detail on the template files as I did with the blueprints and base.html. I will choose the most important or unique parts or highlights of the code. 

---
#### Auth
##### Login.html, PasswordChange.html and Register.html

If the user doesn’t fill in the required file an error is shown. The  WTForm design for the error was not to my taste and was fixed by using the Bootstrap library to have a nicer look and feel. 
`{% import "bootstrap/wtf.html" as wtf %}`
The code renders a login form with username and password fields. The script below was added to switch off the labels on the WTForm fields.
 
```html
<style>
    .control-label {display: none;}
</style>
```
To apply the csrf token during post form action. 
```html
 <!-- csrf_token  -->
 <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```
To implement the WTForm and use the classes defines in the `forms.py` file. 
```html
 <dl>
    <div class="container" >
        {{ wtf.form_field(form.username, class='form-control' , placeholder='Username') }}
    </div>
    <div class="container" >
        {{ wtf.form_field(form.password, class='form-control', placeholder='Password') }}
    </div>
    <div class="container" >
         {{ wtf.form_field(form.submit, class="btn btn-primary")  }}
    </div>
              
</dl>
```

---
#### Blog and Upload

The pages or containers in the design have been organized by using the flexbox grid from Bootstrap. The tool is used to build layouts customizable in shape and sizes based on the 12 column system. 

---
##### About.html

The about page is a landing page for users where they can either Regiser or Login.

---
##### Index.html, Post_Selection.html, Replay.html, Title_body.html, Title_cartoon_image.html, Title_image_text.html, Title_image.html, Update_comment.html, Update_post.html, Upload.html, Uploaded.html

These files are made of similar building block, follwing is general overview explaining the structure. Different posts or comments are contained in a card block. A card is a flexible content container. In this project, I mainly used two types of cards: 
1. The most simple one with just the title and body is used as a type of post and as the format for the comments. 
2. The second type is a card with title, image and body. 

The author of the post or a comment has a three dotted menu icon available on the top right. By pressing it a dropdown menu appears with the option to either Edit or Delete the entry. 

If the Edit option is chosen, the user is directed to the update function and view. 

If the Delete option is chosen, a modal opens where additional confirmation is required from the user to delete the post. An example of the modal implementation is as follows:

First there is a button, to activated the modal. Each modal has to have a unique id for it to work. Id originality is acieved by adding `{{ post['post_id']}}` to the href:
```html
<a  href="#confirm-delete-{{ post['post_id']}}" class="nav-link" type="button" data-toggle="modal">
  Delete post
</a>
```
Below is the actual code for the modal:
```html
<div class="modal fade" 
     id="confirm-delete-{{ post['post_id'] }}" 
     tabindex="-1" 
     aria-labelledby="exampleModalLabel" 
     aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="myModalLabel">Delete post</h5>
        <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        Are you sure you want to delete "{{post['post_title']}}" post?
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <form action="{{ url_for('blog.delete_post', id=post['post_id']) }}" method="post">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
          <button type="submit" class="btn btn-primary">Save changes</button>
        </form>
      </div>
    </div>
  </div>
</div>
```

In addtion, the `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>` had to be added to the modal to work. The cancel button refreshes the page. It is done with a small JS code shown down.

```html
<script>
function refreshpage() {
  window.location.reload();
}
</script>
```
In `index.html` the implementation of a custom filter, that retrieves the number of comments a post contains has been implemented as `|number_of_comments` in the code below:
```html
<form action="{{ url_for('blog.reply', id=post.post_id) }}">
  <button type="submit" style="margin-top:10px;" class="btn btn-primary"> 
    Comment (  {{post['post_id']|number_of_comments}} )
  </button>
</form>
```
Several JS functions have been implemented in `title_image_text.html`. The first is named `pr`. The purpose of it is to remove everything else except the filename in the form fields when uploading a file.  `SelectFileText` is written to fill the form field with text “Select image…”. The preview function shows a preview of the uploaded image. 
```javascript
function pr() {
  var path = document.getElementById('image').value;
  var filename = path.replace(/^.*\\/, "");
  document.getElementById("result").innerHTML = filename;
};

  // if no file has been chosen, then have a Select file line.
  // "result" canbe found inthe base.html file
function SelectFileText() {
  document.getElementById("result").innerHTML = "Select image...";
}

function preview() {
  frame.src=URL.createObjectURL(event.target.files[0]);
}
```
Most of the HTML files have been built using the same building blocks but have been rearranged a little. Above are a few highlights chosen by me.

---
##### .gitignore

A file for version control, that instructs `git` to ignore all files and folders that fit the naming when committing and pushing to the repository.

---
##### License.md

A license file to make my project open source, and hence free to use elsewhere.

---
##### README.md

Information on the project and important documentation regarding it. (You are currently reading this).

---
##### Setup.py

This file describes the projects and files that belong to it. The variable packages calls a function `find_packages`, which finds the package directories automatically. The configuration `include_package_data = True` allows to include static and template files to the application. These additional files are stored in `MANIFEST.in`. The file tells Python to copy everything in the static, templates and `schema.sql` files and to ignore all bytecode files. 

---
#### Instance

The instance folder has been included in the `.gitignore` file, which means it won't be added to the GitHub repositry. Anything sensitive can be added to this folder as it stays on the local device. The folder includes the file with the SECRET_KEY, the configurations file and the database of the web application. I have now isolated my configurations to a separate file and pull the SECRET_KEY from an environment variable (`.env`).

---
##### .env

A local file, that includes the project's `SECRET_KEY`.

---
##### config.py

The configurations for the web applications. It is a very basic and simple setup. Python-dotenv (`environ.get`) is used access the .env file where the SECRET_KEY is stored and any other environment variables (if needs be). 
```python
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = True
DEBUG = True
FLASK_ENV='development'
SECRET_KEY = environ.get('SECRET_KEY')
DATABASE=path.join(basedir, 'flaskr.sqlite') 

UPLOAD_FOLDER = '/Users/dotdj/Desktop/web-projects/CS50BirWri/flaskr/static/upload/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
```

---
##### flaskr.sqlite

The db file for the web application.

---
### Discussion

This is my first programming project ever. I believe I have committed all the beginner crimes when it comes to programming. So here are few most of the important and vivid lessons learnt during my final project. 

Although I tried to take time to think through the design and architecture of my web application, it didn’t last for long as I didn’t have much to go on and wasn’t knowledgeable enough to properly evaluate different options found during research. My goal of a smart design quite quickly escalated to gaining as much experience as possible and to try to get my functions to work first. I am looking forward to my next larger project and it's planning phase as I feel I have a little more insight as to what to expect.  

My lack of experience was evident in my overly complicated webpage idea, which I had to simplify and refactor the code on multiple occasions. I really learnt the hard way, that a eemingly simple idea can be quite complicated to build as an application. Complexity estimation can only be done based on previous experience.

I began my project without any structuring whatsoever and it quickly became a confusing mess. The main file of the main application was, as I now know, the worst kind of spaghetti code example. I had to completely reorganize the project folder and files. I decided to get guidance on the structure of the project from a Flask Tutorial, which I think is a great introduction.

“The biggest lie a person can say to themselves is, that I won't have to write it down now as I will remember it tomorrow”. This seems to be the lesson I must relearn on a yearly basis. Documentation and comments in the code needs to be kept up from the very first day of the project. I began the project with undervaluing comments in code. I did not include enough information about the functions I added to the code and wasted quite a bit of time figuring them out later. I can now appreciate when a comment has been added and can imagine the value of comments for other developers working with unfamiliar code.  

I wrote my configurations, including the SECRET_KEY, directly into the source code and uploaded it to GitHub. It took me quite a long time to understand the gravity of my mistake. I am glad for the lesson as it made me look a little more indepth about the security of my application and made me aware of it in the future.  

In my future programming projects, I will try to keep uniformity of the syntax from the get-go (by following common conventions). I noticed later in the project, that for example, I have written my db execution lines in different styles. By the time I became aware of it, it was too time consuming for me to go through the whole program to change it. 

I would like to practice writing code, where I write more helper functions compared to having many lines in my blueprints. I believe it would result in easier error detection and I can reuse functions instead repeating them in my code. 

Lastly, I did not properly organize my CSS code. I have some in `style.css` and some in the HTML files, which is now a nightmare to work with. In addition, I have made the mistake of adding `print()` function in my code, that says "CHECK HERE", but doesnt say where the "here" is... Making it hard to find the line from my source code fast. In the future I will add more information on where I place my `print()` function, so i can successfully remove them if needed. 

I noticed the addition of backing up project version on GitHub in the 2021 class. This is a great habit to learn from the get go, as I am from the 2020 class. I lost the first version of my final project due to a mysterious glitch. My loss lead me to use git and store my repository on GitHub. I have found a really easy to use git GUI called GitKraken and I will never stop using it. 

I experienced great frustration as a result of unknowingly implementing different versions of Bootstrap, which didn't want to properly work together. I mixed versions of 3.4, 4.6 and 5.0. I eventually decided to use 4.6.

The last lesson is concerning naming and the messages of my commits on GitHub. The importance of clear and precise naming of variables and functions saves so much time. A silly name for a variable can turn into a nightmare to track down or to know what it does.



