from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine

class Author:
    def __init__(self, id, name = ""):
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ? LIMIT 1", [id])
        author = cursor.fetchone()

        if author:
            self._id = author['id']
            self._name = author['name']
        else:
            # Create an author
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
            conn.commit()
            self._id = cursor.lastrowid # Use this to fetch the id of the newly created author
            self._name = name
        
        cursor.close()    

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if hasattr(self, "id"):
            raise ValueError("ID already set")
        
        if not isinstance(id, int):
            raise TypeError("ID must be int")
            
        self._id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if hasattr(self, "name"):
            raise ValueError("Name already set")
        
        if not isinstance(id, str):
            raise TypeError("Name must be string")
        
        if len(name) == 0:
            raise ValueError("Name must be greater than 0 characters")
        
        self._name = name

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM articles WHERE author_id = ?", [self.id])
        rows = cursor.fetchall()
        conn.close()
        articles = []

        for article in rows:
            temp = Article(article['id'])
            articles.append(temp)

        return articles

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT m.id 
                       FROM magazines m
                       JOIN articles a ON a.magazine_id = m.id 
                       WHERE a.author_id = ? 
                       LIMIT 1
                       ''', [self.id])
        rows = cursor.fetchall()
        conn.close()
        magazines = []

        for magazine in rows:
            temp = Magazine(magazine['id'])
            magazines.append(temp)

        return magazines
    
    def __repr__(self):
        return f'<Author {self.id}|{self.name}>'
