# CS50BirWri
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
My final project is a simple website which by idea is meant to be a writing challenge and by functionality is very similar to a blog concept. Users are able to submit different types of posts and comment on other users entries. I have also implemented a very simple photo filter feature, where users can apply a cartoon filter on an uploaded image. The user can then proceed to use the cartoon image in one of the post options.   
As a complete beginner in programming, I am using skills I obtained during the course. The project is built with Flask framework with Bootstrap (version 4.6) frontend tools. I am using Jinja to render templates. My database is setup with SQLite and I am using my computer to host the database (db). Programming language is Python and as the text editor I am using VS Code.

---
### How to run the web application

Enter the next flask commands to the terminal. The first command tells Flask where to find the applicatin. The second command declares the mode to be development.
 
1. export FLASK_APP=flaskr
2. export FLASK_ENV=development
3. flask run

---
### The files

I have decided to structre this part based on the folders in the project. The paragraph is named based on a folder from the project and the subsections of the content are the files contained in the folder.

---
### The Python files

---
#### Flaskr
It is a Python package, that includes the code for the application and most of the necessary files.

---
##### __init__.py

The file has two main purposes. It contains the application factory and it signals to Python, that the project folder flaskr directory should be treated as a package. 
The file begings with the application factory function named `create_app()`. The `instance_relative_config = True` basically lets the app know, that configuration file can be found in the instance folder.

Next in the code is ` app.jinja_env.filters['number_of_comments'] = number_of_comments`. It is a custom filter, that retrives the number of comments a post have and is applied in index.html file. `Bootstrap(app)` is added to the file to have access to some of the design features from the Bootstrap library. `Csrf.init_app(app)` is a little security addition, that protect users against CSRF(Cross-Site Request Forgery) attacks. An unique token is created with every submission of a form in this project to make it impossible for an unintended task on the user authenticated web application on the behalf of the someone elses interest. If FlaskForm is used, then it should already include CSRF protection, but as my project is not consistent in its design, I decided for the sake of gaining experince to add it myself aswell. 

The next section in the file is about the configuration settings for developing or testing. The regular configuration of the entire application is applied throught ` app.config.from_pyfile('config.py') `, which can be found in the code snippet below. It links to a separate  `config.py` file, that includes all the important configurations values, which will replace the defalut settings. The importance of having an instance folder is explained in a separate paragraph. 

```ruby
if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)    
```
The else section in the file is dedicated to testing. I have not included the testing folder in this report as the code I was experimenting with was borrowed from the Flask Tutorial and wasn't and original addition. The code below is to check the presence of instance folder and its path.

```ruby
try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    
```
The last lines of the code are to register the blueprints with the app. Blueprints are a way to organize related code and to avoid having one large file for all of the project. Most of the import are identicalexcept for the names of the blueprint, except for the blog.py lines.
```ruby
 # blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
```
It has an addtional line `app.add_url_rule('/', endpoint='index')`, which define the index page to be at `/`. So in theory the views that are connected to the blog blueprint will not have to have a prefix as they do in auth.py (Read little more in auth.py). I have still used blog prefix in every url_for or function reference in my code.  
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
The file includes register, login, logout, and password change functions. In addition, functions to check if a user is logged in (`login_required`) and fetching data for logged in user(`load_logged_in_user`) have been added. `Login_required` is categorized as a decorator, by adding this to other views, it makes sure a user is logged in before giving access to the page. In the case of register and login the function will return a form for the user to fill in. For WTForms classes have been defined on extensions.py file. These classes are called in the code lines below and then fed to the the html files for forms. 
`form = RegistrationForm(request.form)`
`form = LoginForm(request.form)`
When the user submits the data, it will be validated, which ends up as either an error or registration of a new user or successful login. In case of successful login the session dictionary is cleared before saving the recently logged in user id. `User['user_id']` gives access to most of features in the web applicatin and is important to make sure it is the correct value. 
```ruby
if error is None:
    session.clear()
    session['user_id'] = user['user_id']
    return redirect(url_for('index'))
```
The password is stored as a hash for better security.In the case of the password change the user is asked for the username and old password, which will be validated and the new password, which will be checked to not be the same as the old password. If all the requirements have been passed, the new password will be added to the db, if one of them fails, the form is loaded again with an error message. Logout function clears the user id from the session dictionary. 

###### References

1. https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/?highlight=upload%20file

---
##### Blog.py

The second blueprint gathers code concerning logged in user’s abilities, to create, delete, edit a post. This is the file with most lines in this project.
If the user is logged in, the blueprint begins with index page function, that fetches and shows all the posts from the db. If no user id is present in the session dictionary the program refers the user to the landing page (`about.html`), where they are asked to either Register or Log in.
```ruby
if g.user is None:
    return render_template('blog/about.html')
```
The second function is about post creation. Firstly, the user is directed to a page, where they must choose their post format. In this case there are 4 templates to choose from. The next four functions deal with the 4 types of posts. The 4 types of posts are as follows: title and body, title and image, title and cartoonified image, and last, but not least title, image and body. In all the cases some form of a form is shown to the user. The post types, that include body section have TinyMCE text editor called to get the user text input. The received text needs to be cleaned before injecting it to the db, which is done with line `re.compile(‘<.*>’)`, that removes the unnecessary tags from the text. 
Post types with image requires users to upload an image to the database. I have implemented two versions of image storage. The most common is, where uploaded images are directly stored in the `UPLOAD_FOLDER`. The path to the folder can be find in the `config.py` file. The second version is explained in the `upload.py`, where the uploaded image is stored differently due to additional photo editing step. In addition, a list of selected file extensions has been listed to prevent unwelcomed files being uploaded to db. The filename is run through `werkzeug.secure_filename()` to make sure the code doesn’t directly save the `“UPLOAD_FOLDER + filename”` path to the db, so that unwelcomed intruders can’t just send an input named `filename=”../../filename”` as the function takes the file path and converts it to a more secure version, which will be then added to the db. 
The post creation with cartoon images is a different process. The page has a dropdown menu, from where the user can choose images, they have uploaded.   
The next two functions are concerning the user’s ability to edit a post or a comment. In both cases the id of a post or a comment is an input to the function, that is used to fetch the specific information from the db.  The id is used in the `entry= get_post(id)`, which is fetching the specific data for the inquiry. The `get_post()` function can be found in the `helpers.py` file. 
The reply function gives the users ability to comment on a post. When the function is activated, the user is shown the original post followed with all its comments. To be able to perform it, both the post and comments need to be fetched from the db. As the user submits its reply, the process requesting inputs, validating the input or flashing an error and inserting information into db. The user is redirected to the same page, where they see the original post with all of the comments including theirs.
The two last functions are dedicated to deleting a post or a comment. These functions require an input, which needs to be the id of the post or comment. The id is used to fetch the correct db entry for deletion. In my code the action of deleting is separated between the post and comments table. The last step is redirecting the user to the index page with a flash message, letting the user know of the successful deletion. 

###### References

1. https://flask.palletsprojects.com/en/1.1.x/tutorial/views/
2. https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/?highlight=upload%20file

---
##### Db.py

The file includes 5 functions. The first one is to establish connection to the db file. The path to the file can be found in the `config.py` under the name `DATABASE`. The second function is to check if the connection to the db was successful and to close the connection. The third function `init_b` is a function, that is called to create all the necessary tables for the db. It can be used to reset the db completely as it deletes and recreates all the tables.  The list of the tables and the variables included in the tables can be seen in the file schema.sql. The next function is to utilize the power of the `init_b` function. In the beginning of the app development flask `init_b` commandment is ran in the terminal, that creates all the necessary db tables. After successful initiation message “ Initialized the database” is printed in the terminal. The last function allows the `init_b` commandent to be registered with the application and be used a flask command. As a result of running command flaskr.sqlite is created into the instance folder.

###### References

1. https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

---
##### Extensions.py

The file was created to try to keep the `__init__.py` file cleaner looking. There were several ways to accomplish this and I just chose to have a separate file and import it to the `__init__.py`. It includes an library import necessary to implement the csrf token and it also includes a line of code, which is needed to run the system successfully. 

---
##### Forms.py

The file is dedicated to the definition of classes for different types of forms used in the code. There is a class created for registration, login and password change.  `Validators.DataRequired()` makes sure an imput has been submitted by a user. `Validators.Length(min, max)` set a minimum and maximum limitation for the length of the password. During password change process the new password and confirm is checked by `validators.EqualTo(‘confirm’, …)` to makes sure the same string has been submitted.

###### References

1. https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/ 

---
##### Helpers.py

Helpers is a collection of functions that are mostly called to fetch data from db. The first function named `allowed_file` is written in connection to uploading a file. It checks if the filename extension is one of the allowed ones. The `number_of_comments`  is a custom function that counts the number of comments a post has. The value can be seen on the index page under a post in the parathesis in the button “Comment ()”.  The function needs an input, which is the id of the post. Based on the id, the COUNT command in SQL is used for the task. `Number_of_comments` value after the COUNT needs to be converted to a list and has to be converted to be a string for the filter(read more about the filter in `index.html`) to work properly. The `[1:-1]` is added to remove the square parathesis before the variable is returned. The next 4 functions are built the same way to fetch either a single post or a comment, a group of comments or a image. The process begins with establishing connection with the db and follows by the retrieval of the data. In case data wasn’t found, an error message is projected. Otherwise the retrieved data is returned. 

---
##### Schema.py

File to create tables where user related data is stored and retrieved from. The first lines delete tables one by one. This means all data, which has been saved in the tables will be deleted. The code creates 4 tables: user, post, comments and cartoon. The user table contains the user id, username and password. The post table saves data about created post. Comment table is dedicated to everything related to comments and cartoon save information about the images, that are edit to look like cartoons.  

###### References

1.https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

---
##### Upload.py

Is the third blueprint of the project. Be warned as the file is quite chaotic as I wanted experiment a little. The code is dedicated for uploading an image and applying an image filter from PIL (PILLOW ) library. The first part of the uploading process is the same as described in `blog.py` paragraph. To sum up it quickly: get the image file from a form, check the file before proceeding to add it to the db. The filename is reformed by `secure_filename` function to hide the path to the upload folder. The file is saved to the upload folder. The location of the original image is saved under the name of `photoPath`.  I also experimented uploading an image as a BLOB, which is stored in the db. To achieve it, the image needed to be converted to blobdata. After the conversion the blob is plopped into the db with the usual insert into commandment. The image is edited with the `uploaded_file` function. The function uses the stored blob to convert it back to file format and apply the photo editing filter. The image is edited with a filter named quantize. The value 9 defines the number of colors to which the color scale is reduced. The new image is renamed and inserted to the upload folder and the edited cartoon image is shown to the user with send_from_directory. It is a secure and quick, but a rough way to show a static file from an upload folder. The user has access to the cartoon images in the process of cartoon image post creation. 

---
### HTML and CSS files

This project uses Jinja template library to render templates. Jinja is similar to Python. Special delimiters are used to distinguish Jinja syntax from the static data in the template. Anything between {{ and }} is an expression that will be output to the final document. {% and %} denotes an if and for statements. 

---
#### Static

Static folder is meant to contain all the static files of the project. In this folder the images, GIFs and css files used in the design are stored. It provides an opportunity to reference a file with referenced with `url_for('static', filename='...')`.

---
##### Base.html

Often named as `layout.html`. The file defines the general layout and style of each of the pages it is extended to. By having `base.html` the developer doensnt have to write the entire html structure in each template. The page begins with the obligatory `<!doctype html>` followed by the `<html>` tag, in which the language of the file is defined to be English. The next up is the `<head>` tag, that includes all of the links to necessary scrips or libraries to run the design implemented in the application. The linking to css files, scripts files as well as all the other plug ins used such as TinyMCE in my project are done here as well. The `<title>` tag allowes the developer to name tab in the brower. `{% block title %}` allows to change or add to the title in the browser’s tab and the window title.

The main area of a web application is the body of the page. The definition and styling of it is done within the `<body>` tag. In the tag a JS function `onload = “SelectFileText()”` has been added to make it possible to see the filename in the form, that is chosen to be uploaded. The first information in the body tag are the link to Bootstrap design library for the version 4.6. The location of the links are intentionally and determined by the Bootstrap library documentation. 
The `<header>` tag defines the top side of the page/section, which usually includes a heading, search, navigation bar, a logo etc. The navigation bar is located in the `<header>` tag. The navbar is divided into two views based on if a user is logged in or not. If the user is logged in they have access to the Home, New post and Cartoonifiy photo options on the left side of the bar and a settings icon on the right. In the settings menu, the username is shown with an icon, change password and a logout button. If the user is not logged in, they are referred to the about page (`about.html`), where on the left side of navbar have a choice between Register or Login. 
The `<main>` tag is the sections which is mostly changed throughout other html pages.  The first element in the tag and before the content, is the `{% block header %}`, which is similar to title but instead will change the title displayed on the page. Although this block is defined in the project, I personally haven’t used it too much. Next is the `get_flashed_messages()`. If the application receives `flash()` signal, which in most cases are either errors or notifications the template loops over each message returned and  displays them. The most important block is the `{% block content %}`, which is implemented in all of the other Html pages in this project.
Last part of the file is dedicated to the `<footer>`. I haven’t design the footer in this project, but if I want to try it in the future, then it is ready for the future. The section includes a defined block  {% block footer %}, which can be easily extended to other pages. 

---
#### Tinymce

A folder , that needed to be added to be able to implement TinyMCE feature for the blog. It is a text editor, that looks good and has good customization options. My setup has been kept at a basic level and the code part of this feature is in the `base.html`.

---
#### Upload

Folder where all of the uploaded images are kept. 

---
##### Style.css

A file, that is a style sheet and used to format the contents of a webpage. 

---
#### Templates

Templates are files that contain static data as well as placeholders for dynamic data. A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates. Templates render HTML which will display in the user’s browser. 
For the templates I will not write in detail about all the files as I did with the blueprints and base.html. I will choose the most important or highlights and unique parts of the code. 

---
#### Auth
##### Login.html, PasswordChange.html and Register.html

If the user doesn’t fill in the required file an error is shown. The  WTForm design for the error was not to my taste and was fixed by using Bootstrap extension to have a nicer looking design. 
`{% import "bootstrap/wtf.html" as wtf %}`
The code renders a login form with username and password field. The script below was added to switch off the labels on the WTForm fields.
 
```ruby
<style>
    .control-label {display: none;}
</style>
```
To apply the csrf token during post form action. 
```ruby
 <!-- csrf_token  -->
 <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```
To implement the WTForm and use the classes defines in the forms.py file. 
```ruby
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

Is a landing page for user either to Regiser or Login.

---
##### Index.html, Post_Selection.html, Replay.html, Title_body.html, Title_cartoon_image.html, Title_image_text.html, Title_image.html, Update_comment.html, Update_post.html, Upload.html, Uploaded.html

Are made of similar building block, which I will make a general overview. Different posts, comments are contained in a card. A card is a flexible content container. In this project simple two types of cards are mainly used. The most simple one with just the title and body is used as a type of a post and as the format for the comments. The second type is a card with title, image and body. 
The author of the post or a comment has a three dots menu icon available. By pressing it a dropdown menu appears with the option of either Edit or Delete the entry. If Edit is chosen the user is directed to the update function and view. The delete button opens a modal, where additional confirmation is asked from the user to delete the post. An example of the modal implementation is as follows.
First there is a button, to activated the modal. Each modal has to have a unique id for it to work. Id originality is acieved by adding `{{ post['post_id']}}` to the href.
```ruby
<a  href="#confirm-delete-{{ post['post_id']}}" class="nav-link" type="button" data-toggle="modal">Delete post</a>
```
The actual code for the modal.
```ruby
 <div class="modal fade" id="confirm-delete-{{ post['post_id'] }}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="myModalLabel">Delete post</h5>
                  <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  Are you sure you want to delete "{{post['post_title']}}"" post?
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

```ruby
<script>

function refreshpage() {
  window.location.reload();

}

</script>
```
In `index.html` the implementation of a custom filter, that retrieves the number of comments a post has, is done as `|number_of_comments` in the code below:
```ruby
<form action="{{ url_for('blog.reply', id=post.post_id) }}">
        <button type="submit" style="margin-top:10px;" class="btn btn-primary"> Comment (  {{post['post_id']|number_of_comments}} )</button>
      </form>
```
Several JS functions have been implemented in `title_image_text.html`, etc. The first is named `pr`. The purpose of it is to remove everything else except the filename in the form fiels, when uploading a file.  `SelectFileText` is written to fill the form field with text “Select image…”. Preview function shows a preview of the uploaded image. 
```ruby
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
Most of the html files have been built using the same building blocks just rearranged a little different. Above as just few highlight chosen by me.

---
##### .gitignore

A file for version control, that instructs the included files, that are generated while running your project, to be ignored.

---
##### License.md

WHAT TO WRITE HERE???!!

---
##### README.md

Documentation and You are here inside it at the moment.

---
##### Setup.py

File, which describes the projects and files, that belong to it. Variable packages calls a function `find_packages`, which finds package directories automatically. The configuration `include_package_data = True` allows to include static and template files to the application. These additional files are stored in `MANIFEST.in`. The file tells Python to copy everything in the static, templates and `schema.sql` files and to ignore all bytecode files. 

---
#### Instance

Instance folder has been included in the `.gitignore` file, which means it wont be added to the Github repositry. Anything sensitive can be added to this folder as it stays on the local device. The folder includes the file with the SECRET_KEY, the configurations file and the database of the web application. I have now isolated my configurations to a separate file and pull SECRET_KEY from an environment variable (`.env`).

---
##### .env

A local file, that includes the projects `SECRET_KEY`.

---
##### config.py

The configurations for the web applications. It is a very basic and simple setup. Python-dotenv (`environ.get`) helps to retrieve .env for the SECRET_KEY. 
```ruby
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

This is my first programming project ever. I believe I have committed all the beginner crimes when it comes to programming. So here are few most important and vivid lessons learnt during my final project. 

Although I tried to take time to think through the design and architecture of my web application, it didn’t last for long as I didn’t have much to go on and wasn’t knowledgeable enough to properly evaluate different options found during research. My goal of smart design quite quickly updated to gaining experience as much as possible and just trying to figure out how to make my functions work first. I am looking forward to my next larger project and its planning phase as I feel I have little more insight as to what to expect.  

My lack of experience was evident in my overly complicated webpage idea, which I had to simplify and rewrite the code on many occasions. I really learnt the hard way, that seemingly simple idea can be quite complicated to build as an application. Complexity estimation can only be done based on previous experience.

I began my project without any structuring whatsoever and it quickly became a confusing mess. The main file of the main application was, as I now know, the worst kind of spaghetti code example. I had to completely reorganize the project folder and files. I decided to get guidance on the structure of the project from a Flask Tutorial, which I think is a great introduction.

“The biggest lie a person can say to themselves is, that I wont have to writing down as I will remember it tomorrow” seems to be the lesson I must relearn on a yearly basis. Documentation and comments in the code needs to be kept up from the very first day of the project. I began the project with undervaluing comments in the code. I did not include enough information about the functions I added to the code and wasted quite a bit of time figuring them out later. I can now appreciate when a comment has been added and can imagine the value of comments for other developers working with unfamiliar code.  

I wrote my configurations, including the SECRET_KEY, directly into the source code and uploaded it to Github. It took me quite a long time to understand the gravity of my mistake. I am glad for the lesson as it made me look a little more indepth about the security of my application and make me mindful of it in the future.  

In my future programming projects, I will try to keep uniformity of the syntax from the get-go. I noticed later in the project, that for example I have written my db execution lines in different styles. By the time I became aware of it, it was too time consuming for me to go through the whole program to change it. I would like to practice writing code, where I write more helper functions compared to having many lines in my blueprints. I believe it would result in easier error detection and I can reuse functions instead repeating them in my code. Lastly, I did not properly organize my CSS code. I have some in style.css and some in the html files.

I noticed the addition of backing up project version on gitup in 2021 class. This is a great habit to learn from early on, as I am from 2020 class and I lost the first version of my final project due to a mysterious glitch. My loss lead me to GitKraken and I will never stop using it. 

I experienced great frustration as a result of unknowgly implementing different versions of Bootstrap, which didnt want to properly work together. I mixed versions of 3.4, 4.6 and 5.0. I eventually decided to use 4.6.

The last lesson is concerning naming and in version descriptions on GitKraken. The importance of clear and precise naming of variables and functions saves so much time. A silly name for a variable can turn into a nightmare to track down. 



