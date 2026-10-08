"""Seed data: subjects/topics and the question bank.

Questions reference topics by their position (1-based) in the seeded topic list,
which is resolved to real database ids at insert time, so ids never need to match.
"""
from app.database.connection import SessionLocal
from app.models import Question, Subject, Topic

SUBJECTS = {
    "C Programming": (
        "Assess your C programming fundamentals and problem-solving skills.",
        ["Basics", "Variables and Data Types", "Operators", "Conditional Statements", "Loops",
         "Functions", "Arrays", "Strings", "Pointers", "Structures", "File Handling"],
    ),
    "Java": (
        "Assess Java programming and object-oriented programming skills.",
        ["Java Basics", "Classes and Objects", "OOP", "Inheritance", "Polymorphism", "Abstraction",
         "Encapsulation", "Exception Handling", "Collections", "Multithreading", "JDBC"],
    ),
    "DBMS": (
        "Assess database concepts, SQL and database programming skills.",
        ["DBMS Basics", "ER Model", "Relational Model", "SQL", "Joins", "Subqueries",
         "Normalization", "Transactions", "Concurrency Control", "Indexing", "PL/SQL"],
    ),
}


def make_question(question_text, option_a, option_b, option_c, option_d,
                  correct_answer, difficulty, topic_id):
    return Question(
        question_text=question_text, option_a=option_a, option_b=option_b,
        option_c=option_c, option_d=option_d, correct_answer=correct_answer,
        difficulty=difficulty, topic_id=topic_id,
    )


def _build_questions():
    return [

        # =========================================================
        # C PROGRAMMING - EASY
        # =========================================================

        make_question(
            "Which symbol is used to end a statement in C?",
            ".", ";", ":", ",",
            "B", "Easy", 1
        ),

        make_question(
            "Which function is used to print output in C?",
            "scanf()", "print()", "printf()", "display()",
            "C", "Easy", 1
        ),

        make_question(
            "Which header file is required for printf() and scanf()?",
            "string.h", "stdio.h", "stdlib.h", "math.h",
            "B", "Easy", 1
        ),

        make_question(
            "Which function is the entry point of a C program?",
            "start()", "main()", "begin()", "run()",
            "B", "Easy", 1
        ),

        make_question(
            "Which data type is used to store a single character?",
            "char", "string", "text", "character",
            "A", "Easy", 2
        ),

        make_question(
            "Which data type is commonly used to store decimal values?",
            "int", "char", "float", "void",
            "C", "Easy", 2
        ),

        make_question(
            "Which keyword is used to declare a constant in C?",
            "constant", "const", "fixed", "immutable",
            "B", "Easy", 2
        ),

        make_question(
            "Which operator is used for logical AND in C?",
            "||", "&&", "!", "&",
            "B", "Easy", 3
        ),

        make_question(
            "Which operator gives the remainder after division?",
            "/", "%", "//", "mod",
            "B", "Easy", 3
        ),

        make_question(
            "Which loop executes its body at least once?",
            "for", "while", "do-while", "nested",
            "C", "Easy", 5
        ),

        # =========================================================
        # C PROGRAMMING - MEDIUM
        # =========================================================

        make_question(
            "What is the value of 10 % 3 in C?",
            "0", "1", "2", "3",
            "C", "Medium", 3
        ),

        make_question(
            "Which operator is used to compare two values for equality?",
            "=", "==", "!=", "=>",
            "B", "Medium", 3
        ),

        make_question(
            "What is the output of printf(\"%d\", 5 + 3 * 2);?",
            "16", "11", "13", "10",
            "B", "Medium", 3
        ),

        make_question(
            "Which keyword is used to exit a loop immediately?",
            "stop", "exit", "break", "continue",
            "C", "Medium", 5
        ),

        make_question(
            "Which statement skips the remaining statements of the current loop iteration?",
            "break", "continue", "skip", "pass",
            "B", "Medium", 5
        ),

        make_question(
            "What is the index of the first element in a C array?",
            "0", "1", "-1", "Depends on array",
            "A", "Medium", 2
        ),

        make_question(
            "Which format specifier is used for an integer in printf()?",
            "%f", "%c", "%d", "%s",
            "C", "Medium", 2
        ),

        make_question(
            "What is the output of: int x = 5; x++; printf(\"%d\", x);",
            "4", "5", "6", "7",
            "C", "Medium", 2
        ),

        make_question(
            "Which operator is used to access the address of a variable?",
            "*", "&", "->", "%",
            "B", "Medium", 2
        ),

        make_question(
            "Which operator is used to dereference a pointer?",
            "&", "*", "->", "#",
            "B", "Medium", 2
        ),

        # =========================================================
        # C PROGRAMMING - HARD
        # =========================================================

        make_question(
            "What is the output of printf(\"%d\", 10 / 3);?",
            "3", "3.33", "4", "10",
            "A", "Hard", 1
        ),

        make_question(
            "What is the output of int x = 2; printf(\"%d\", x++ * ++x);?",
            "6", "8", "Undefined behavior", "4",
            "C", "Hard", 3
        ),

        make_question(
            "Which storage class makes a local variable retain its value between function calls?",
            "auto", "static", "register", "extern",
            "B", "Hard", 1
        ),

        make_question(
            "Which function is used to dynamically allocate memory in C?",
            "alloc()", "malloc()", "create()", "new()",
            "B", "Hard", 2
        ),

        make_question(
            "Which function is used to release dynamically allocated memory?",
            "delete()", "remove()", "free()", "clear()",
            "C", "Hard", 2
        ),

        make_question(
            "Which operator has higher precedence in C?",
            "*", "+", "=", "||",
            "A", "Hard", 3
        ),

        make_question(
            "What is recursion?",
            "Calling a variable repeatedly",
            "A function calling itself",
            "Using multiple loops",
            "Using multiple arrays",
            "B", "Hard", 5
        ),

        make_question(
            "What must a recursive function generally contain to stop recursion?",
            "Pointer", "Loop", "Base case", "Array",
            "C", "Hard", 5
        ),

        make_question(
            "Which declaration correctly creates a pointer to an integer?",
            "int p", "int *p", "pointer int p", "int &p",
            "B", "Hard", 2
        ),

        make_question(
            "What does a NULL pointer indicate?",
            "It points to the first memory location",
            "It points to no valid object",
            "It points to an integer",
            "It points to a character",
            "B", "Hard", 2
        ),

        # =========================================================
        # JAVA - EASY
        # =========================================================

        make_question(
            "Which keyword is used to create a class in Java?",
            "class", "Class", "new", "object",
            "A", "Easy", 12
        ),

        make_question(
            "Which method is the entry point of a Java program?",
            "start()", "run()", "main()", "execute()",
            "C", "Easy", 12
        ),

        make_question(
            "Which keyword is used to create an object?",
            "class", "object", "new", "create",
            "C", "Easy", 12
        ),

        make_question(
            "Which keyword is used to inherit a class in Java?",
            "implements", "inherits", "extends", "super",
            "C", "Easy", 15
        ),

        make_question(
            "Which concept allows a class to acquire properties of another class?",
            "Encapsulation", "Inheritance", "Abstraction", "Compilation",
            "B", "Easy", 15
        ),

        make_question(
            "Which keyword refers to the parent class object?",
            "this", "parent", "super", "base",
            "C", "Easy", 15
        ),

        make_question(
            "Which collection does not allow duplicate elements?",
            "List", "Set", "ArrayList", "Vector",
            "B", "Easy", 20
        ),

        make_question(
            "Which collection maintains insertion order and allows duplicates?",
            "Set", "List", "Map", "TreeSet",
            "B", "Easy", 20
        ),

        make_question(
            "Which class is commonly used to store a dynamic list of elements?",
            "ArrayList", "HashSet", "HashMap", "TreeMap",
            "A", "Easy", 20
        ),

        make_question(
            "Which keyword is used to define a constant in Java?",
            "constant", "static", "final", "const",
            "C", "Easy", 12
        ),

        # =========================================================
        # JAVA - MEDIUM
        # =========================================================

        make_question(
            "Which keyword is used when a class implements an interface?",
            "extends", "implements", "inherits", "interface",
            "B", "Medium", 15
        ),

        make_question(
            "Which type of inheritance is directly supported through classes in Java?",
            "Multiple", "Multilevel", "Hybrid", "Multiple class inheritance",
            "B", "Medium", 15
        ),

        make_question(
            "What is method overloading?",
            "Same method name with different parameters",
            "Different method names with same parameters",
            "Overriding a parent class",
            "Creating multiple classes",
            "A", "Medium", 15
        ),

        make_question(
            "What is method overriding?",
            "Changing variable names",
            "Redefining a parent method in a child class",
            "Creating a constructor",
            "Creating overloaded methods",
            "B", "Medium", 15
        ),

        make_question(
            "Which keyword is used to prevent method overriding?",
            "static", "private", "final", "protected",
            "C", "Medium", 15
        ),

        make_question(
            "Which collection stores key-value pairs?",
            "List", "Set", "Map", "Queue",
            "C", "Medium", 20
        ),

        make_question(
            "Which Map implementation generally allows one null key?",
            "HashMap", "TreeMap", "Hashtable", "EnumMap",
            "A", "Medium", 20
        ),

        make_question(
            "Which Set implementation stores elements in sorted order?",
            "HashSet", "LinkedHashSet", "TreeSet", "ArraySet",
            "C", "Medium", 20
        ),

        make_question(
            "Which interface is the root of the Java collection hierarchy?",
            "Collection", "Collections", "IterableOnly", "Container",
            "A", "Medium", 20
        ),

        make_question(
            "Which keyword is used to call the current class constructor?",
            "super", "this", "self", "current",
            "B", "Medium", 12
        ),

        # =========================================================
        # JAVA - HARD
        # =========================================================

        make_question(
            "Which principle allows the same interface to have different implementations?",
            "Encapsulation", "Polymorphism", "Compilation", "Serialization",
            "B", "Hard", 15
        ),

        make_question(
            "Which access modifier allows access only inside the same class?",
            "public", "protected", "private", "default",
            "C", "Hard", 15
        ),

        make_question(
            "Which keyword can be used to invoke a superclass constructor?",
            "this", "super", "parent", "base",
            "B", "Hard", 15
        ),

        make_question(
            "What happens when a superclass reference refers to a subclass object?",
            "Only subclass variables can be accessed",
            "Runtime polymorphism can occur",
            "Compilation always fails",
            "The object becomes a superclass object",
            "B", "Hard", 15
        ),

        make_question(
            "Which collection provides average constant-time lookup by key?",
            "ArrayList", "HashMap", "TreeMap", "LinkedList",
            "B", "Hard", 20
        ),

        make_question(
            "What is the average time complexity of searching for a key in a HashMap?",
            "O(1)", "O(n)", "O(log n)", "O(n log n)",
            "A", "Hard", 20
        ),

        make_question(
            "Which collection maintains insertion order while storing unique elements?",
            "HashSet", "LinkedHashSet", "TreeSet", "PriorityQueue",
            "B", "Hard", 20
        ),

        make_question(
            "Which collection stores elements in natural sorted order?",
            "HashSet", "TreeSet", "LinkedHashSet", "ArrayList",
            "B", "Hard", 20
        ),

        make_question(
            "Which OOP concept hides implementation details from the user?",
            "Inheritance", "Abstraction", "Polymorphism", "Overloading",
            "B", "Hard", 15
        ),

        make_question(
            "Which mechanism allows one object to take many forms?",
            "Inheritance", "Polymorphism", "Encapsulation", "Constructor",
            "B", "Hard", 15
        ),

        # =========================================================
        # DBMS - EASY
        # =========================================================

        make_question(
            "What does DBMS stand for?",
            "Database Management System",
            "Data Backup Management System",
            "Database Memory System",
            "Data Management Software",
            "A", "Easy", 23
        ),

        make_question(
            "Which key uniquely identifies a row in a table?",
            "Foreign Key", "Primary Key", "Candidate Key", "Secondary Key",
            "B", "Easy", 23
        ),

        make_question(
            "What is a database?",
            "A collection of related data",
            "A programming language",
            "A computer network",
            "An operating system",
            "A", "Easy", 23
        ),

        make_question(
            "Which key is used to reference a primary key in another table?",
            "Candidate Key", "Foreign Key", "Super Key", "Alternate Key",
            "B", "Easy", 24
        ),

        make_question(
            "What does an entity represent in an ER model?",
            "A real-world object",
            "A SQL command",
            "A database server",
            "A table column only",
            "A", "Easy", 24
        ),

        make_question(
            "Which SQL command is used to retrieve data?",
            "GET", "FETCH", "SELECT", "READ",
            "C", "Easy", 26
        ),

        make_question(
            "Which SQL command is used to add a new row?",
            "ADD", "INSERT", "CREATE", "UPDATE",
            "B", "Easy", 26
        ),

        make_question(
            "Which JOIN returns matching rows from both tables?",
            "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN",
            "A", "Easy", 27
        ),

        make_question(
            "Which normal form removes repeating groups?",
            "1NF", "2NF", "3NF", "BCNF",
            "A", "Easy", 29
        ),

        make_question(
            "Which normal form removes partial dependency?",
            "1NF", "2NF", "3NF", "BCNF",
            "B", "Easy", 29
        ),

        # =========================================================
        # DBMS - MEDIUM
        # =========================================================

        make_question(
            "Which SQL command is used to modify existing data?",
            "CHANGE", "UPDATE", "MODIFY", "ALTER",
            "B", "Medium", 26
        ),

        make_question(
            "Which SQL command removes rows from a table?",
            "REMOVE", "DELETE", "DROP", "CLEAR",
            "B", "Medium", 26
        ),

        make_question(
            "Which clause is used to filter rows in a SELECT query?",
            "GROUP BY", "WHERE", "ORDER BY", "HAVING",
            "B", "Medium", 26
        ),

        make_question(
            "Which clause is used to sort query results?",
            "SORT BY", "ORDER BY", "ARRANGE BY", "GROUP BY",
            "B", "Medium", 26
        ),

        make_question(
            "Which JOIN returns all rows from the left table and matching rows from the right table?",
            "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN",
            "B", "Medium", 27
        ),

        make_question(
            "Which JOIN returns all rows from the right table?",
            "LEFT JOIN", "INNER JOIN", "RIGHT JOIN", "SELF JOIN",
            "C", "Medium", 27
        ),

        make_question(
            "Which normal form removes transitive dependency?",
            "1NF", "2NF", "3NF", "BCNF",
            "C", "Medium", 29
        ),

        make_question(
            "What is a relationship in an ER model?",
            "Association between entities",
            "A table attribute",
            "A SQL statement",
            "A primary key",
            "A", "Medium", 24
        ),

        make_question(
            "What is cardinality in an ER model?",
            "Number of relationships between entities",
            "Number of columns only",
            "Number of databases",
            "Number of SQL queries",
            "A", "Medium", 24
        ),

        make_question(
            "Which key can uniquely identify a tuple and may contain more attributes than necessary?",
            "Foreign Key", "Super Key", "Primary Key", "Composite Key only",
            "B", "Medium", 23
        ),

        # =========================================================
        # DBMS - HARD
        # =========================================================

        make_question(
            "Which normal form requires every non-key attribute to depend only on the key?",
            "1NF", "2NF", "3NF", "4NF",
            "C", "Hard", 29
        ),

        make_question(
            "Which normal form deals with multivalued dependencies?",
            "2NF", "3NF", "4NF", "BCNF",
            "C", "Hard", 29
        ),

        make_question(
            "Which normal form is stricter than 3NF?",
            "1NF", "2NF", "BCNF", "4NF only",
            "C", "Hard", 29
        ),

        make_question(
            "What does a transaction represent in a DBMS?",
            "A logical unit of work",
            "A database table",
            "A type of key",
            "A query result",
            "A", "Hard", 23
        ),

        make_question(
            "Which ACID property ensures that a transaction is treated as one unit?",
            "Consistency", "Isolation", "Atomicity", "Durability",
            "C", "Hard", 23
        ),

        make_question(
            "Which ACID property ensures committed data survives system failure?",
            "Atomicity", "Consistency", "Isolation", "Durability",
            "D", "Hard", 23
        ),

        make_question(
            "Which SQL operation combines rows from two or more tables based on a related column?",
            "UNION only", "JOIN", "GROUP", "ORDER",
            "B", "Hard", 27
        ),

        make_question(
            "Which JOIN can produce the Cartesian product of two tables?",
            "INNER JOIN", "LEFT JOIN", "CROSS JOIN", "RIGHT JOIN",
            "C", "Hard", 27
        ),

        make_question(
            "Which SQL feature is commonly used to group rows having the same values?",
            "WHERE", "GROUP BY", "ORDER BY", "JOIN",
            "B", "Hard", 26
        ),

        make_question(
            "Which clause is used to filter grouped results?",
            "WHERE", "HAVING", "GROUP BY", "ORDER BY",
            "B", "Hard", 26
        ),

        # =========================================================
        # ADDITIONAL EASY QUESTIONS
        # =========================================================

        # C Programming
        make_question(
            "Which keyword is used to declare an integer variable in C?",
            "integer",
            "int",
            "number",
            "var",
            "B",
            "Easy",
            2
        ),

        # DBMS
        make_question(
            "Which command is used to create a new table in SQL?",
            "MAKE",
            "BUILD",
            "CREATE",
            "NEW",
            "C",
            "Easy",
            26
        ),

        make_question(
            "Which SQL command is used to remove a table completely?",
            "DELETE",
            "REMOVE",
            "DROP",
            "CLEAR",
            "C",
            "Easy",
            26
        ),

        # Java
        make_question(
            "Which keyword is used to declare an integer variable in Java?",
            "integer",
            "int",
            "number",
            "var",
            "B",
            "Easy",
            12
        )
    ]



def seed_questions(db=None) -> int:
    """Insert any questions that are not already in the database. Returns the number inserted."""
    own = db is None
    db = db or SessionLocal()
    try:
        ordered_topics = (
            db.query(Topic).join(Subject).order_by(Subject.id, Topic.id).all()
        )
        if not ordered_topics:
            return 0
        topic_ids = [t.id for t in ordered_topics]

        existing = {text for (text,) in db.query(Question.question_text).all()}
        new = []
        for q in _build_questions():
            if q.question_text in existing:
                continue
            q.topic_id = topic_ids[q.topic_id - 1]
            new.append(q)
        if new:
            db.add_all(new)
            db.commit()
        return len(new)
    finally:
        if own:
            db.close()
