from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main_old():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()


    '''
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implmentation.
    '''

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models

    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    print("\nAuthors:")
    for author in authors:
        print(Author(author["id"], author["name"]))

    print("\nArticles:")
    for article in articles:
        print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))


def add_magazine():
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")

    try:
        Magazine(0, magazine_name, magazine_category)
        print("Magazine successfully added")
    except Exception as e:
        print(e)

def magazine_choices(author):
    while True:
        print(f"\t1. List {author.name} articles")
        print(f"\t2. List {author.name} magazines")
        print(f"\t3. Add new magazines")
        print(f"\t4. Select magazines")
        print(f"\t-1. Go back")

        choice = int(input("Enter choice: "))

        if choice == -1:
            break

        if choice == 1:
            articles = author.articles()

            if articles is None:
                print("No articles found for this author")
                continue
            
            print("*" * 20)
            for article in articles:
                print(f"{article.title}")
                print("-" * len(article.title))
                print(f"{article.content}")

            print("*" * 20)
            print("\n")

        if choice == 2:
            magazines = author.magazines()

            if magazines is None:
                print("No magazines found for this author")
                continue
            
            print("*" * 20)
            for magazine in magazines:
                print(f"{magazine.name} - {magazine.category}")

            print("*" * 20)
            print("\n")




def main():
    # Initialize the database and create tables
    create_tables()

    # Get all authors as an entry point to our app
    # Connect to the database
    print("Welcome!!")
    
    while True:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        cursor.close()
        magazine_ids = []

        print("Choose magazine")
        for row in rows:
            magazine_id.append(row["id"])
            print(f"\t{row['id']}: {row['name']}")

        print("\t0: add new magazine")
        print("\t-1: exit")

        magazine_id = int(input("Enter choice: "))

        if magazine_id == -1:
            break

        if magazine_id == 0:
            # Create method for adding new magazine
            add_magazine()
            continue

        if magazine_id not in magazine_ids:
            print("Invalid choice, try again\n")
            continue

        # Valid magazine prommpt other
        magazine_choices(Magazine(magazine_id))
        continue


if __name__ == "__main__":
    main()

