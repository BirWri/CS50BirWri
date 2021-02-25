from flaskr.db import get_db
from PIL import ImageFilter


def number_of_comments(post_id):

    print (post_id)

    db = get_db()
    number_of_comments = db.execute(
            'SELECT COUNT (OG_post_id)'
            ' FROM comments'
            ' WHERE OG_post_id = ?',
            (post_id,)
    )

    #https://stackoverflow.com/questions/47716237/python-list-how-to-remove-parenthesis-quotes-and-commas-in-my-list
    # to make the program actually display the int and not show the parenthesis
    number_of_comments = [i[0] for i in number_of_comments]
    #https://stackoverflow.com/questions/13207697/how-to-remove-square-brackets-from-list-in-python
    # trying to remove the []
    number_of_comments = str(number_of_comments)[1:-1]

    print (number_of_comments)
    
    return(number_of_comments)

def blur(file):
        
        file=file.filter(ImageFilter.BLUR)
        return(file)
