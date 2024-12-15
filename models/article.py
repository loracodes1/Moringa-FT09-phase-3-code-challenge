from database.connection import get_db_connection

class Article:
    def __init__(self, id, title = "", content = "", author_id = 0, magazine_id = 0):
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ? LIMIT 1", [id])
        article = cursor.fetchone()

        if article:
            self._id = article['id']
            self._title = article['title']
            self._content = article['content']
            self._author_id = article['author_id']
            self._magazine_id = article['magazine_id']
        else:
            # Create an article
            self._id = 0
            self.title = title
            self.magazine_id = magazine_id
            self.author_id = author_id
            self.content = content
        
            cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                           (title,content,author_id,magazine_id,))
            self._id = cursor.lastrowid # Use this to fetch the id of the newly created author
            conn.commit()

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
    def author_id(self):
        return self._author_id
    
    @author_id.setter
    def author_id(self, author_id):
        if hasattr(self, "author_id"):
            raise ValueError("Author ID already set")
        
        if not isinstance(author_id, int):
            raise TypeError("Author ID must be int")
        
        self._author_id = author_id

    @property
    def magazine_id(self):
        return self._magazine_id
    
    @magazine_id.setter
    def magazine_id(self, magazine_id):
        if hasattr(self, "magazine_id"):
            raise ValueError("Magazine ID already set")
        
        if not isinstance(magazine_id, int):
            raise TypeError("Magazine ID must be int")
            
        self._magazine_id = magazine_id

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if hasattr(self, "title"):
            raise ValueError("Title already set")
        
        if not isinstance(title, str):
            raise TypeError("Title must be string")
        
        if len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be between 5 and 50 characters")
        
        self._title = title

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, content):        
        if not isinstance(content, str):
            raise TypeError("Content must be string")
        
        if len(content) > 5000:
            raise ValueError("Content must be less than 5000 characters")
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE articles SET content = ? WHERE id = ? LIMIT 1", (content, self.id,))
        conn.commit()
        cursor.close()

        self._content = content

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM authors WHERE id = ? LIMIT 1", [self.author_id])
        author = cursor.fetchone()
        conn.close()

        if not author:
            return None

        return Author(author['id'])
    
    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM magazines WHERE id = ? LIMIT 1", [self.magazine_id])
        magazine = cursor.fetchone()
        conn.close()

        if not magazine:
            return None
        
        return Magazine(magazine["id"])


    def __repr__(self):
        return f'<Article {self.id}|{self.title}|{self.author_id}|{self.magazine_id}|{self.content}>'
