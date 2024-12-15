from database.connection import get_db_connection
from models.article import Article
from models.author import Author

class Magazine:
    def __init__(self, id, name = "", category = ""):
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ? LIMIT 1", [id])
        magazine = cursor.fetchone()

        if magazine:
            self._id = magazine['id']
            self._name = magazine['name']
            self._category = magazine['category']
        else:
            # Create an author
            self._id = 0
            self.name = name
            self.category = category
        
            cursor.execute('INSERT INTO authors (magazines) VALUES (?, ?)', (name,category,))
            conn.commit()
            self._id = cursor.lastrowid # Use this to fetch the id of the newly created author

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
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        
        if len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be must be between 2 and 16 characters")
        
        # Update the name
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE magazines SET name = ? WHERE id = ? LIMIT 1", (name, self.id,))
        conn.commit()
        cursor.close()
        
        self._name = name

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):        
        if not isinstance(category, str):
            raise TypeError("Category must be string")
        
        if len(category) < 1:
            raise ValueError("Category must be greater than 0 characters")
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE magazines SET category = ? WHERE id = ? LIMIT 1", (category, self.id,))
        conn.commit()
        cursor.close()
        
        self._category = category

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT author_id FROM articles WHERE magazine_id = ?", [self.id])
        rows = cursor.fetchall()
        conn.close()
        authors = []

        for article in rows:
            temp = Author(article['author_id'])
            authors.append(temp)

        return authors

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM articles WHERE magazine_id = ?", [self.id])
        rows = cursor.fetchall()
        conn.close()
        articles = []

        for article in rows:
            temp = Article(article['id'])
            articles.append(temp)

        return articles
        
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE author_id = ?", self.id)
        rows = cursor.fetchall()
        conn.close()
        articles_titles = []

        if rows.count() == 0:
            return None

        for row in rows:
            articles_titles.append(row["title"])
    
        return articles_titles
    
    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT a.*, count(m.id) as magazine_count
                       FROM authors a
                       JOIN articles ar ON ar.author_id = a.id
                       JOIN magazines m ON m.id = ar.magazine_id
                       GROUP BY m.id
                       HAVING magazine_count > 2 AND ar.author_id = ?
                    ''', [self.id])
        rows = cursor.fetchall()
        conn.close()
        authors = []

        for row in rows:
            authors.append(Author(row["id"]))

        return authors
        
    def __repr__(self):
        return f'<Magazine {self.id}|{self.name}|{self.category}>'
    