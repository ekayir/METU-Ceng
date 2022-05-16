from customer import Customer

import psycopg2

from config import read_config
from messages import *

POSTGRESQL_CONFIG_FILE_NAME = "database.cfg"

"""
    Connects to PostgreSQL database and returns connection object.
"""


def connect_to_db():
    db_conn_params = read_config(filename=POSTGRESQL_CONFIG_FILE_NAME, section="postgresql")
    conn = psycopg2.connect(**db_conn_params)
    conn.autocommit = False
    return conn


"""
    Splits given command string by spaces and trims each token.
    Returns token list.
"""


def tokenize_command(command):
    tokens = command.split(" ")
    return [t.strip() for t in tokens]


"""
    Prints list of available commands of the software.
"""


def help():
    # prints the choices for commands and parameters
    print("\n*** Please enter one of the following commands ***")
    print("> help")
    print("> sign_up <email> <password> <first_name> <last_name> <plan_id>")
    print("> sign_in <email> <password>")
    print("> sign_out")
    print("> show_plans")
    print("> show_subscription")
    print("> subscribe <plan_id>")
    print("> watched_movies <movie_id_1> <movie_id_2> <movie_id_3> ... <movie_id_n>")
    print("> search_for_movies <keyword_1> <keyword_2> <keyword_3> ... <keyword_n>")
    print("> suggest_movies")
    print("> quit")


"""
    Saves customer with given details.
    - Return type is a tuple, 1st element is a boolean and 2nd element is the response message from messages.py.
    - If the operation is successful, commit changes and return tuple (True, CMD_EXECUTION_SUCCESS).
    - If any exception occurs; rollback, do nothing on the database and return tuple (False, CMD_EXECUTION_FAILED).
"""


def sign_up(conn, email, password, first_name, last_name, plan_id):
    # TODO: Implement this function
    try:
        curs = conn.cursor()
        curs.execute("insert into customer (email , password , first_name ,last_name ,session_count ,plan_id) values(%s,%s,%s,%s,0,%s) ", (email, password, first_name, last_name, plan_id))
        conn.commit()
        return True, CMD_EXECUTION_SUCCESS
    except  Exception as e:
        conn.rollback()
        return False, CMD_EXECUTION_FAILED


"""
    Retrieves customer information if email and password is correct and customer's session_count < max_parallel_sessions.
    - Return type is a tuple, 1st element is a customer object and 2nd element is the response message from messages.py.
    - If email or password is wrong, return tuple (None, USER_SIGNIN_FAILED).
    - If session_count < max_parallel_sessions, commit changes (increment session_count) and return tuple (customer, CMD_EXECUTION_SUCCESS).
    - If session_count >= max_parallel_sessions, return tuple (None, USER_ALL_SESSIONS_ARE_USED).
    - If any exception occurs; rollback, do nothing on the database and return tuple (None, USER_SIGNIN_FAILED).
"""


def sign_in(conn, email, password):
    # TODO: Implement this function
    try:
        curs = conn.cursor()
        curs.execute("select c.session_count,p.max_parallel_sessions from customer c, plan p where c.email =%s and c.password=%s and c.plan_id = p.plan_id ", (email,password))
        row = curs.fetchone()
        if row is None:
            return None, USER_SIGNIN_FAILED
        elif row[0] >= row[1] :
            return None, USER_ALL_SESSIONS_ARE_USED
        elif row[0] < row[1] :
            curs.execute("Update customer set session_count = session_count + 1 where email =%s and password=%s", (email,password))
            conn.commit()
            curs.execute("Select * from  customer where email =%s and password=%s", (email,password))
            return (ConvertStringToCustomer(curs.fetchone()), CMD_EXECUTION_SUCCESS)
    except  Exception as e:        
        conn.rollback()
        return None, USER_SIGNIN_FAILED


"""
    Signs out from given customer's account.
    - Return type is a tuple, 1st element is a boolean and 2nd element is the response message from messages.py.
    - Decrement session_count of the customer in the database.
    - If the operation is successful, commit changes and return tuple (True, CMD_EXECUTION_SUCCESS).
    - If any exception occurs; rollback, do nothing on the database and return tuple (False, CMD_EXECUTION_FAILED).
"""


def sign_out(conn, customer):
    # TODO: Implement this function
    try:
        curs = conn.cursor()
        customer_id = customer.customer_id        
        curs.execute("Update customer set session_count = session_count - 1 where session_count > 0 and customer_id =%s ", [customer_id])
        conn.commit()
        return True, CMD_EXECUTION_SUCCESS
    except  Exception as e:
        conn.rollback()
        return False, CMD_EXECUTION_FAILED


"""
    Quits from program.
    - Return type is a tuple, 1st element is a boolean and 2nd element is the response message from messages.py.
    - Remember to sign authenticated user out first.
    - If the operation is successful, commit changes and return tuple (True, CMD_EXECUTION_SUCCESS).
    - If any exception occurs; rollback, do nothing on the database and return tuple (False, CMD_EXECUTION_FAILED).
"""


def quit(conn, customer):
    # TODO: Implement this function
    try:
        if customer is None : 
            return (True, CMD_EXECUTION_SUCCESS)
        elif conn is None : 
            return (True, CMD_EXECUTION_SUCCESS)

        return sign_out(conn, customer)        
    except  Exception as e:
        return False, CMD_EXECUTION_FAILED



"""
    Retrieves all available plans and prints them.
    - Return type is a tuple, 1st element is a boolean and 2nd element is the response message from messages.py.
    - If the operation is successful; print available plans and return tuple (True, CMD_EXECUTION_SUCCESS).
    - If any exception occurs; return tuple (False, CMD_EXECUTION_FAILED).

    Output should be like:
    #|Name|Resolution|Max Sessions|Monthly Fee
    1|Basic|720P|2|30
    2|Advanced|1080P|4|50
    3|Premium|4K|10|90
"""


def show_plans(conn):
    # TODO: Implement this function
    try:
        curs = conn.cursor()
        curs.execute("select plan_id||'|'||plan_name||'|'||resolution||'|'||max_parallel_sessions||'|'||monthly_fee as result from plan order by plan_id")
        rows = curs.fetchall()
        if(curs.rowcount > 0) : print("#|Name|Resolution|Max Sessions|Monthly Fee")
        for row in rows:
            print(row[0])
        curs.close()
        return True, CMD_EXECUTION_SUCCESS
    except  Exception as e:
        conn.rollback()
        return False, CMD_EXECUTION_FAILED


"""
    Retrieves authenticated user's plan and prints it. 
    - Return type is a tuple, 1st element is a boolean and 2nd element is the response message from messages.py.
    - If the operation is successful; print the authenticated customer's plan and return tuple (True, CMD_EXECUTION_SUCCESS).
    - If any exception occurs; return tuple (False, CMD_EXECUTION_FAILED).

    Output should be like:
    #|Name|Resolution|Max Sessions|Monthly Fee
    1|Basic|720P|2|30
"""


def show_subscription(conn, customer):
    # TODO: Implement this function
    try:
        customer_id = customer.customer_id
        curs = conn.cursor()
        curs.execute("select plan_id||'|'||plan_name||'|'||resolution||'|'||max_parallel_sessions||'|'||monthly_fee as result from plan where plan_id = (select c2.plan_id from customer c2 where customer_id =%s)",[customer_id])
        row = curs.fetchone()
        print("#|Name|Resolution|Max Sessions|Monthly Fee")
        print(row[0])
        curs.close()
        return True, CMD_EXECUTION_SUCCESS
    except  Exception as e:
        conn.rollback()
        return False, CMD_EXECUTION_FAILED

"""
    Insert customer-movie relationships to Watched table if not exists in Watched table.
    - Return type is a tuple, 1st element is a boolean and 2nd element is the response message from messages.py.
    - If a customer-movie relationship already exists, do nothing on the database and return (True, CMD_EXECUTION_SUCCESS).
    - If the operation is successful, commit changes and return tuple (True, CMD_EXECUTION_SUCCESS).
    - If any one of the movie ids is incorrect; rollback, do nothing on the database and return tuple (False, CMD_EXECUTION_FAILED).
    - If any exception occurs; rollback, do nothing on the database and return tuple (False, CMD_EXECUTION_FAILED).
"""


def watched_movies(conn, customer, movie_ids):
    # TODO: Implement this function
    try:
        distinctMovieIds = set(movie_ids)
        t = tuple(distinctMovieIds)
        curs = conn.cursor()
        sql = "select count(*) from movies m where movie_id  in {}".format(t)
        if(len(t) < 2) : 
            sql = sql[:-2] 
            sql+=")"
        curs.execute(sql)
        tupleLen = len(t)
        databaseLen = curs.fetchone()[0]
        if (tupleLen != databaseLen) :
            return False, CMD_EXECUTION_FAILED
        insertStatement = "insert into watched  select * from ("
        for i in t:
            ss = "select customerIdValue as customer_id,'movieIdValue' as movie_id union ".replace("customerIdValue",str(customer.customer_id)).replace("movieIdValue",str(i))
            insertStatement+=ss
        insertStatement+=" select null,null) t where not exists (select 1 from watched w2 where w2.customer_id = t.customer_id and w2.movie_id = t.movie_id) and t.customer_id is not null"
        curs.execute(insertStatement)
        conn.commit()
        return True, CMD_EXECUTION_SUCCESS
    except  Exception as e:
        conn.rollback()
        return False, CMD_EXECUTION_FAILED


"""
    Subscribe authenticated customer to new plan.
    - Return type is a tuple, 1st element is a customer object and 2nd element is the response message from messages.py.
    - If target plan does not exist on the database, return tuple (None, SUBSCRIBE_PLAN_NOT_FOUND).
    - If the new plan's max_parallel_sessions < current plan's max_parallel_sessions, return tuple (None, SUBSCRIBE_MAX_PARALLEL_SESSIONS_UNAVAILABLE).
    - If the operation is successful, commit changes and return tuple (customer, CMD_EXECUTION_SUCCESS).
    - If any exception occurs; rollback, do nothing on the database and return tuple (None, CMD_EXECUTION_FAILED).
"""


def subscribe(conn, customer, plan_id):
    # TODO: Implement this function
    try:
        curs = conn.cursor()
        curs.execute("select max_parallel_sessions from plan where plan_id=%s",[plan_id])
        newPlan = curs.fetchone()
        if newPlan is None:
            return None, SUBSCRIBE_PLAN_NOT_FOUND

        curs.execute("select max_parallel_sessions from plan where plan_id = (select c2.plan_id from customer c2 where customer_id =%s)", [customer.customer_id])
        oldPlan = curs.fetchone()       
        if newPlan[0] < oldPlan[0] : 
            return None, SUBSCRIBE_MAX_PARALLEL_SESSIONS_UNAVAILABLE


        customer_id = customer.customer_id
        curs.execute("Update customer set plan_id=%s where customer_id =%s ", [plan_id ,customer_id])
        conn.commit()
        curs.execute("select * from customer where customer_id=%s", [customer_id])
        return (ConvertStringToCustomer(curs.fetchone()), CMD_EXECUTION_SUCCESS)
    except  Exception as e:
        conn.rollback()
        return False, CMD_EXECUTION_FAILED
    

"""
    Searches for movies with given search_text.
    - Return type is a tuple, 1st element is a boolean and 2nd element is the response message from messages.py.
    - Print all movies whose titles contain given search_text IN CASE-INSENSITIVE MANNER.
    - If the operation is successful; print movies found and return tuple (True, CMD_EXECUTION_SUCCESS).
    - If any exception occurs; return tuple (False, CMD_EXECUTION_FAILED).

    Output should be like:
    Id|Title|Year|Rating|Votes|Watched
    "tt0147505"|"Sinbad: The Battle of the Dark Knights"|1998|2.2|149|0
    "tt0468569"|"The Dark Knight"|2008|9.0|2021237|1
    "tt1345836"|"The Dark Knight Rises"|2012|8.4|1362116|0
    "tt3153806"|"Masterpiece: Frank Millers The Dark Knight Returns"|2013|7.8|28|0
    "tt4430982"|"Batman: The Dark Knight Beyond"|0|0.0|0|0
    "tt4494606"|"The Dark Knight: Not So Serious"|2009|0.0|0|0
    "tt4498364"|"The Dark Knight: Knightfall - Part One"|2014|0.0|0|0
    "tt4504426"|"The Dark Knight: Knightfall - Part Two"|2014|0.0|0|0
    "tt4504908"|"The Dark Knight: Knightfall - Part Three"|2014|0.0|0|0
    "tt4653714"|"The Dark Knight Falls"|2015|5.4|8|0
    "tt6274696"|"The Dark Knight Returns: An Epic Fan Film"|2016|6.7|38|0
"""


def search_for_movies(conn, customer, search_text):
    # TODO: Implement this function
    try:
        curs = conn.cursor()
        stringSearchValue = ""
        for letter in search_text :
            stringSearchValue+=letter
        
        
        stringSearchValue.replace("'","''")

        selectStatement = "select '\"'||movie_id||'\"|'||'\"'||title||'\"|'||movie_year||'|'||trim(case when to_char(rating,'99D9') = '   .0' then '0.0' else to_char(rating,'99D9') end)||'|'||votes||'|'||(select count(1) from watched w2 where w2.movie_id =m.movie_id)\
                            from movies m where lower(title) like '%'||lower('searchValue')||'%' order by movie_id "
        selectStatement = selectStatement.replace("searchValue",stringSearchValue)
        
        curs.execute(selectStatement)
        rows = curs.fetchall()
        if(curs.rowcount > 0) : print("Id|Title|Year|Rating|Votes|Watched")
        for row in rows:
            print(row[0])
        curs.close()
        return True, CMD_EXECUTION_SUCCESS
    except  Exception as e:
        return False, CMD_EXECUTION_FAILED


"""
    Suggests combination of these movies:
        1- Find customer's genres. For each genre, find movies with most number of votes among the movies that the customer didn't watch.

        2- Find top 10 movies with most number of votes and highest rating, such that these movies are released 
           after 2010 ( [2010, today) ) and the customer didn't watch these movies.
           (descending order for votes, descending order for rating)

        3- Find top 10 movies with votes higher than the average number of votes of movies that the customer watched.
           Disregard the movies that the customer didn't watch.
           (descending order for votes)

    - Return type is a tuple, 1st element is a boolean and 2nd element is the response message from messages.py.    
    - Output format and return format are same with search_for_movies.
    - Order these movies by their movie id, in ascending order at the end.
    - If the operation is successful; print movies suggested and return tuple (True, CMD_EXECUTION_SUCCESS).
    - If any exception occurs; return tuple (False, CMD_EXECUTION_FAILED).
"""


def suggest_movies(conn, customer):
    # TODO: Implement this function
    try:
        curs = conn.cursor()
        selectStatement = "select '\"'||movie_id||'\"|'||'\"'||title||'\"|'||movie_year||'|'\
                            ||trim(case when to_char(rating,'99D9') = '   .0' then '0.0' else to_char(rating,'99D9') end)||'|'||votes\
                            from (\
                            select m2.* from movies m2 , genres g3,(select g.genre_name , max(m.votes)maxVotes from movies m , genres g where m.movie_id =g.movie_id \
                            and m.movie_id not in (select w.movie_id from watched w where w.customer_id =customerIdValue)\
                            and g.genre_name in (select g2.genre_name from watched w2, genres g2 where w2.customer_id =customerIdValue and w2.movie_id = g2.movie_id )\
                            group by g.genre_name )t\
                            where m2.movie_id =g3.movie_id and m2.votes=t.maxVotes and g3.genre_name =t.genre_name\
                            union\
                            (select m.* from movies m where m.movie_id not in (select w.movie_id from watched w where w.customer_id =customerIdValue)\
                            and m.movie_year >=2010\
                            order by m.votes desc, m.rating desc \
                            limit 10)\
                            union\
                            (select m.* from movies m where m.movie_id not in (select w.movie_id from watched w where w.customer_id =customerIdValue)\
                            and m.votes > (select avg(m.votes ) from watched w , movies m where w.customer_id =customerIdValue and w.movie_id =m.movie_id)\
                            order by m.votes desc limit 10 \
                            ))h\
                            order by movie_id"
        selectStatement = selectStatement.replace("customerIdValue",str(customer.customer_id))
        curs.execute(selectStatement)
        rows = curs.fetchall()
        if(curs.rowcount > 0) : print("Id|Title|Year|Rating|Votes")
        for row in rows:
            print(row[0])
        curs.close()
        return True, CMD_EXECUTION_SUCCESS
    except  Exception as e:
        return False, CMD_EXECUTION_FAILED

def ConvertStringToCustomer(fetchedRow):
    return Customer(fetchedRow[0],fetchedRow[1],fetchedRow[3],fetchedRow[4],fetchedRow[5],fetchedRow[6])
