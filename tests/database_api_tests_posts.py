'''
Created on 20.02.2018


Database interface testing for all posts related methods.

A post object is a dictionary which contains the following keys:
    -    post_id: (int) id of the post
    -    timestamp: UNIX timestamp (long integer) that specifies when the
                    post was created.
    -    sender_id: (int) id of the owner of the post.
    -    receiver_id: (int) id of the receiver of the post.
    -    reply_to: (int) id of the parent post.
    -    post_text: post's text.
    -    rating: (int) represents the rating of the post
    -    anonymous: (int) shows the anonymity of the post.
                    0 is False, 1 is True
    -    public: (int) shows the anonymity of the post.
                    0 is False, 1 is True

A posts' list has the following format:
[   {'post_id':'', 'timestamp':'', 'receiver_id':'', 'reply_to':'',
     'post_text':'', 'rating':'', 'anonymous':'', 'public':''},
    {'post_id':'', 'timestamp':'', 'receiver_id':'', 'reply_to':'',
     'post_text':'', 'rating':'', 'anonymous':'', 'public':''},
     ...  ]

@author: Mina
REFERENCEs:
-   Programmable Web Projects, Exercise 1, database_api_tests_messages.py
'''
#   importing the important modules
import sqlite3, unittest

#   load the database
from app import database 

#   path to the database file.
DB_PATH = 'db/critique_test.db'
ENGINE = database.Engine(DB_PATH)

#   stating some test subjects and test results
POST0_ID = 0

POST0 = {   'post_id':0,
            'timestamp':1362017481,
            'sender_id':1,
            'receiver_id': 2,
            'reply_to': NULL,
            'post_text': 'She is scary and used to love me in highscool.',
            'rating': 3,
            'anonymous': 0,
            'public': 1}

POST1_ID = 1

POST1 =  {  'post_id':2,
            'timestamp':1362017281,
            'sender_id':1,
            'receiver_id': 4,
            'reply_to': NULL,
            'post_text': 'This dude is good at video games!',
            'rating': 4,
            'anonymous': 0,
            'public': 1}

WRONG_POST_ID = 200

INITIAL_SIZE = 12


class PostDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the posts
    '''

    @classmethod
    def setUpClass(cls):
        '''
            Creates the database structure. Removes
            first any pre-existing database files.
        '''
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''
            Remove the testing database
        '''
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        '''
            Populates the database
        '''
        try:
          #This method load the initial values from critique_data_dump.sql
            ENGINE.populate_tables()
          #Creates a Connection instance to use the API
            self.connection = ENGINE.connect()
        except Exception as e: 
        #For instance if there is an error while populating the tables
            ENGINE.clear()

    def tearDown(self):
        '''
            Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()

    #---------------------------------------------------#
    def test_posts_table_created(self):
        '''
        Checks that the table initially contains 5 posts
        (check critique_data_dump.sql).

        NOTE: NOT used with Connection instance but called
            directly by SQL
        '''
        print('('+ self.test_posts_table_created.__name__ +')',\
                    self.test_posts_table_created.__doc__)
        #   Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM posts'
        #   Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #   Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #   Provide support for foreign keys
            cur.execute(keys_on)
            #   Execute main SQL Statement
            cur.execute(query)
            users = cur.fetchall()
            #   Assert
            self.assertEqual(len(users), INITIAL_SIZE)

    def test_create_post_object(self):
        '''
        Check that the method _create_post_object works return adequate
        values for the first database row. 
        
        NOTE: Do not use Connection instace
            to extract data from database but call directly SQL.
        '''
        print('('+self.test_create_post_object.__name__+')', \
                self.test_create_post_object.__doc__)
        
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM posts WHERE post_id = 0'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            #Extrac the row
            row = cur.fetchone()
        #Test the method
        post = self.connection._create_post_object(row)
        self.assertDictContainsSubset(post, POST0)

    def test_get_post(self):
        '''
        Test get_post with id 0 and 10
        '''
        print('('+self.test_get_post.__name__+')', \
              self.test_get_post.__doc__)
        #Test with an existing message
        post = self.connection.get_post(POST0_ID)
        self.assertDictContainsSubset(post, POST0)
        post = self.connection.get_message(POST1_ID)
        self.assertDictContainsSubset(post, POST1)
        
    # TODO : make test for malformed post_id after implementing the format of the post (post-#######)

    def test_get_posts(self):
        '''
        Test that get_posts work correctly
        '''
        print('('+self.test_get_posts.__name__+')', self.test_get_posts.__doc__)
        posts = self.connection.get_posts()
        #Check that the size is correct
        self.assertEqual(len(posts), INITIAL_SIZE)
        #Iterate through posts and check if the posts with POST0_ID and
        #POST1_ID are correct:
        for post in posts:
            if post['post_id'] == POST0_ID:
                self.assertEqual(len(post), 8)
                self.assertDictContainsSubset(post, POST0)
            elif post['post_id'] == POST1_ID:
                self.assertEqual(len(post), 8)
                self.assertDictContainsSubset(post, POST1)


if __name__ == '__main__':
    print('Start running posts tests...')
    unittest.main()