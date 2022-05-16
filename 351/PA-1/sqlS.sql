1.
Create table author(
author_id int,
author_name varchar(60),
primary key(author_id)
);

Create table publisher(
publisher_id int,
publisher_name varchar(50),
primary key(publisher_id)
);

Create table book(
isbn char(13),
book_name varchar(120),
publisher_id int,
first_publish_year char(4),
page_count int,
category varchar(25),
rating float,
primary key(isbn),
foreign key (publisher_id) references publisher(publisher_id)
);


Create table author_of(
isbn char(13),
author_id int,
primary key(isbn,author_id),
foreign key (isbn) references book(isbn),
foreign key (author_id) references author(author_id)
);


Create table phw1(
isbn char(13),
book_name varchar(120),
rating float,
primary key(isbn)
);

2.
INSERT INTO author(author_id,author_name) VALUES(authors[i].getAuthor_id(),authors[i].getAuthor_name());
INSERT INTO book(isbn,book_name,publisher_id,first_publish_year,page_count,category,rating) 
	VALUES(book[i].getIsbn(),book[i].getBook_name(),book[i].getPublisher_id(),book[i].getFirst_publish_year()
		,book[i].getPage_count(),book[i].getCategory(),book[i].getRating());
INSERT INTO publisher(publisher_id,publisher_name) VALUES(publishers[i].getPublisher_id(),publishers[i].getPublisher_name());
INSERT INTO author_of(isbn,author_id) VALUES(author_ofs[i].getIsbn(),author_ofs[i].getAuthor_id());

3.

SELECT DISTINCT
    b.isbn, b.first_publish_year, b.page_count, p.publisher_name
FROM
    book b,
    publisher p
WHERE
    b.page_count = (SELECT 
            MAX(b1.page_count)
        FROM
            book b1)
        AND p.publisher_id = b.publisher_id
ORDER BY b.isbn;

4.

SELECT DISTINCT
    b1.publisher_id,
    (SELECT 
            AVG(b2.page_count)
        FROM
            book b2
        WHERE
            b2.publisher_id = b1.publisher_id) avgPageCount
FROM
    author_of a1,
    book b1
WHERE
    a1.author_id = author_id1
        AND EXISTS( SELECT 
            1
        FROM
            author_of a2
        WHERE
            a2.author_id = author_id2 AND a2.isbn = a1.isbn)
        AND b1.isbn = a1.isbn
		ORDER BY b1.publisher_id;


5.

SELECT DISTINCT
    b1.book_name, b1.category, b1.first_publish_year
FROM
    book b1,author_of ao2
WHERE
     b1.isbn =ao2.isbn and
    (b1.first_publish_year,ao2.author_id ) in (SELECT 
            MIN(b2.first_publish_year),a.author_id
        FROM
            book b2,
            author a,
            author_of ao
        WHERE
            a.author_id = ao.author_id
                AND ao.isbn = b2.isbn
                AND a.author_name = ?
                group by a.author_id)
        AND b1.isbn IN (SELECT 
            b3.isbn
        FROM
            book b3,
            author a1,
            author_of ao1
        WHERE
            a1.author_id = ao1.author_id
                AND ao1.isbn = b3.isbn
                AND a1.author_name = ?)                
order by   b1.book_name, b1.category, b1.first_publish_year;

6.

SELECT DISTINCT
    bb.publisher_id, bb.category
FROM
    book bb
WHERE
    bb.publisher_id IN (SELECT 
            p.publisher_id
        FROM
            publisher p,
            book b
        WHERE
            ((LENGTH(p.publisher_name)) - LENGTH(REPLACE(p.publisher_name, ' ', '')) + 1) > 2
                AND p.publisher_id = b.publisher_id
        GROUP BY p.publisher_id
        HAVING COUNT(1) >= 3 AND AVG(b.rating) > 3)
ORDER BY bb.publisher_id , bb.category;


7.


SELECT DISTINCT
    A.*
FROM
    (SELECT 
        a.author_id, a.author_name
    FROM
        author_of ao, author a, book b
    WHERE
        ao.author_id = a.author_id
            AND ao.isbn = b.isbn
            AND b.publisher_id IN (SELECT DISTINCT
                b1.publisher_id
            FROM
                author_of ao1, book b1
            WHERE
                ao1.author_id = ?
                    AND b1.isbn = ao1.isbn)
    GROUP BY a.author_id , a.author_name
    HAVING COUNT(1) = (SELECT 
            COUNT(DISTINCT b1.publisher_id)
        FROM
            author_of ao1, book b1
        WHERE
            ao1.author_id = ?
                AND b1.isbn = ao1.isbn)) A
ORDER BY A.author_id;

8.

 Select distinct ao1.author_id,b1.isbn from book b1,author_of ao1 where ao1.isbn=b1.isbn
 and ao1.author_id in(
 select  ao.author_id from book b, author_of ao where 
 b.publisher_id in ( SELECT p.publisher_id from publisher p
 where (Select Count(distinct ao.author_id) from book b, author_of ao
 where b.publisher_id = p.publisher_id and b.isbn = ao.isbn)=1)
 and ao.isbn = b.isbn)
 order by 1,2;

9.

SELECT DISTINCT
    p.publisher_id, p.publisher_name
FROM
    book b,
    publisher p
WHERE
    b.publisher_id = p.publisher_id
        AND b.category = 'Roman'
        AND EXISTS( SELECT 
            1
        FROM
            book b1,
            publisher p1
        WHERE
            b1.publisher_id = p1.publisher_id
                AND p1.publisher_id = p.publisher_id
        GROUP BY p1.publisher_id
        HAVING AVG(b1.rating) > ?)
GROUP BY p.publisher_id
HAVING COUNT(1) >= 2
ORDER BY p.publisher_id;

10.


11.

Update book set rating = rating + 1
where rating<=4 and book_name like '%keyword%';

Select sum(b.rating) from book b;


12.
delete from publisher 
where not exists (Select 1 from book where book.publisher_id = publisher.publisher_id);

select count(*) from publisher;


13.

SELECT count(1)
FROM information_schema.TABLES
WHERE (TABLE_SCHEMA = 'db1949304');

drop table IF EXISTS phw1;
drop table IF EXISTS author_of;
drop table IF EXISTS book;
drop table IF EXISTS publisher;
drop table IF EXISTS author;





















