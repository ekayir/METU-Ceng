/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ceng.ceng351.bookdb;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

/**
 *
 * @author Software
 */
public class BOOKDB implements IBOOKDB {

    private static String user = "1949304"; // TODO: Your userName
    private static String password = "da93d9bc"; //  TODO: Your password
    private static String host = "144.122.71.65"; // host name
    private static String database = "db1949304"; // TODO: Your database name
    private static int port = 8084; // port

    private static Connection connection = null;

    public static void connect() {

        String url = "jdbc:mysql://" + host + ":" + port + "/" + database;

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            connection = DriverManager.getConnection(url, user, password);
        } catch (SQLException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    public static void disconnect() {

        if (connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void initialize() {

    }

    @Override
    public int dropTables() {
        connect();
        String sql1 = "SELECT count(1) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'db1949304');";
        ArrayList dropQueries = new ArrayList();
        dropQueries.add("drop table IF EXISTS phw1;");
        dropQueries.add("drop table IF EXISTS author_of;");
        dropQueries.add("drop table IF EXISTS book;");
        dropQueries.add("drop table IF EXISTS publisher;");
        dropQueries.add("drop table IF EXISTS author;");
        int count = 0;

        try {
            // Execute query
            Statement st = connection.createStatement();
            ResultSet rs = st.executeQuery(sql1);

            while (rs.next()) {
                count = rs.getInt(1);
            }
            for (Object dropQuery : dropQueries) {
                st.executeUpdate(dropQuery.toString());
            }

            disconnect();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return count;
    }

    @Override
    public int createTables() {
        connect();
        int i = 0;
        ArrayList createQueries = new ArrayList();
        createQueries.add("Create table author(author_id int,author_name varchar(60),primary key(author_id));");
        createQueries.add("Create table publisher(publisher_id int,publisher_name varchar(50),primary key(publisher_id));");
        createQueries.add("Create table book(isbn char(13),book_name varchar(120),publisher_id int,first_publish_year char(4),page_count int,category varchar(25),rating float,primary key(isbn),foreign key (publisher_id) references publisher(publisher_id));");
        createQueries.add("Create table author_of(isbn char(13),author_id int,primary key(isbn,author_id),foreign key (isbn) references book(isbn),foreign key (author_id) references author(author_id));");
        createQueries.add("Create table phw1(isbn char(13),book_name varchar(120),rating float,primary key(isbn));");

        // Execute query
        for (Object createQuery : createQueries) {
            try {
                Statement st = connection.createStatement();
                st.executeUpdate(createQuery.toString());
                i++;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        disconnect();

        return i;
    }

    @Override
    public int insertAuthor(Author[] authors) {
        connect();
        int i = 0;

        for (Author author : authors) {
            try {
                PreparedStatement statement
                        = connection.prepareStatement("INSERT INTO author(author_id,author_name) VALUES(?,?);");
                statement.setInt(1, author.getAuthor_id());
                statement.setString(2, author.getAuthor_name());
                statement.executeUpdate();
                i++;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        disconnect();
        return i;
    }

    @Override
    public int insertPublisher(Publisher[] publishers) {
        connect();
        int i = 0;

        for (Publisher publisher : publishers) {
            try {

                PreparedStatement statement
                        = connection.prepareStatement("INSERT INTO publisher(publisher_id,publisher_name) "
                                + "VALUES(?,?);");
                statement.setInt(1, publisher.getPublisher_id());
                statement.setString(2, publisher.getPublisher_name());
                statement.executeUpdate();
                i++;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        disconnect();
        return i;
    }

    @Override
    public int insertBook(Book[] books) {
        connect();
        int i = 0;

        for (Book book : books) {
            try {
                PreparedStatement statement
                        = connection.prepareStatement("INSERT INTO \n"
                                + "book(isbn,book_name,publisher_id,first_publish_year,page_count,category,rating) \n"
                                + "VALUES(?,?,?,?,?,?,?);");
                statement.setString(1, book.getIsbn());
                statement.setString(2, book.getBook_name());
                statement.setInt(3, book.getPublisher_id());
                statement.setString(4, book.getFirst_publish_year());
                statement.setInt(5, book.getPage_count());
                statement.setString(6, book.getCategory());
                statement.setDouble(7, book.getRating());
                statement.executeUpdate();
                i++;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        disconnect();

        return i;
    }

    @Override
    public int insertAuthor_of(Author_of[] author_ofs) {
        connect();
        int i = 0;

        for (Author_of author_of : author_ofs) {
            try {
                PreparedStatement statement
                        = connection.prepareStatement("INSERT INTO author_of(isbn,author_id) VALUES(?,?);");
                statement.setString(1, author_of.getIsbn());
                statement.setInt(2, author_of.getAuthor_id());
                statement.executeUpdate();
                i++;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        disconnect();

        return i;
    }

    @Override
    public QueryResult.ResultQ1[] functionQ1() {
        try {
            connect();
            String sql = "SELECT DISTINCT\n"
                    + "    b.isbn, b.first_publish_year, b.page_count, p.publisher_name\n"
                    + "FROM\n"
                    + "    book b,\n"
                    + "    publisher p\n"
                    + "WHERE\n"
                    + "    b.page_count = (SELECT \n"
                    + "            MAX(b1.page_count)\n"
                    + "        FROM\n"
                    + "            book b1)\n"
                    + "        AND p.publisher_id = b.publisher_id\n"
                    + "ORDER BY b.isbn;";
            Statement st = connection.createStatement();
            ResultSet rs = st.executeQuery(sql);
            rs.last();
            int recordCount = rs.getRow();
            rs.beforeFirst();
            QueryResult.ResultQ1[] result = new QueryResult.ResultQ1[recordCount];
            int i = 0;
            while (rs.next()) {
                String a = rs.getString(1);
                String b = rs.getString(2);
                int c = rs.getInt(3);
                String d = rs.getString(4);
                result[i] = new QueryResult.ResultQ1(a, b, c, d);
                i++;
            }
            return result;
        } catch (SQLException ex) {
            ex.printStackTrace();
            return null;
        }
    }

    @Override
    public QueryResult.ResultQ2[] functionQ2(int i, int i0) {
        try {
            connect();
            String sql = "SELECT DISTINCT\n"
                    + "    b1.publisher_id,\n"
                    + "    (SELECT \n"
                    + "            AVG(b2.page_count)\n"
                    + "        FROM\n"
                    + "            book b2\n"
                    + "        WHERE\n"
                    + "            b2.publisher_id = b1.publisher_id) avgPageCount\n"
                    + "FROM\n"
                    + "    author_of a1,\n"
                    + "    book b1\n"
                    + "WHERE\n"
                    + "    a1.author_id = ?\n"
                    + "        AND EXISTS( SELECT \n"
                    + "            1\n"
                    + "        FROM\n"
                    + "            author_of a2\n"
                    + "        WHERE\n"
                    + "            a2.author_id = ? AND a2.isbn = a1.isbn)\n"
                    + "        AND b1.isbn = a1.isbn\n"
                    + "		ORDER BY b1.publisher_id;";
            PreparedStatement statement
                    = connection.prepareStatement(sql);
            statement.setInt(1, i);
            statement.setInt(2, i0);
            ResultSet rs = statement.executeQuery();
            rs.last();
            int recordCount = rs.getRow();
            rs.beforeFirst();
            QueryResult.ResultQ2[] result = new QueryResult.ResultQ2[recordCount];
            int j = 0;
            while (rs.next()) {
                int a = rs.getInt(1);
                Double b = rs.getDouble(2);
                result[j] = new QueryResult.ResultQ2(a, b);
                j++;
            }
            return result;
        } catch (SQLException ex) {
            ex.printStackTrace();
            return null;
        }
    }

    @Override
    public QueryResult.ResultQ3[] functionQ3(String sue_Donaldson) {
        try {
            connect();
            String sql = "SELECT DISTINCT\n" +
                            "    b1.book_name, b1.category, b1.first_publish_year\n" +
                            "FROM\n" +
                            "    book b1,author_of ao2\n" +
                            "WHERE\n" +
                            "     b1.isbn =ao2.isbn and\n" +
                            "    (b1.first_publish_year,ao2.author_id ) in (SELECT \n" +
                            "            MIN(b2.first_publish_year),a.author_id\n" +
                            "        FROM\n" +
                            "            book b2,\n" +
                            "            author a,\n" +
                            "            author_of ao\n" +
                            "        WHERE\n" +
                            "            a.author_id = ao.author_id\n" +
                            "                AND ao.isbn = b2.isbn\n" +
                            "                AND a.author_name = ?\n" +
                            "                group by a.author_id)\n" +
                            "        AND b1.isbn IN (SELECT \n" +
                            "            b3.isbn\n" +
                            "        FROM\n" +
                            "            book b3,\n" +
                            "            author a1,\n" +
                            "            author_of ao1\n" +
                            "        WHERE\n" +
                            "            a1.author_id = ao1.author_id\n" +
                            "                AND ao1.isbn = b3.isbn\n" +
                            "                AND a1.author_name = ?)                \n" +
                            "order by   b1.book_name, b1.category, b1.first_publish_year;";
            PreparedStatement statement
                    = connection.prepareStatement(sql);
            statement.setString(1, sue_Donaldson);
            statement.setString(2, sue_Donaldson);
            ResultSet rs = statement.executeQuery();
            rs.last();
            int recordCount = rs.getRow();
            rs.beforeFirst();
            QueryResult.ResultQ3[] result = new QueryResult.ResultQ3[recordCount];
            int j = 0;
            while (rs.next()) {
                String a = rs.getString(1);
                String b = rs.getString(2);
                String c = rs.getString(3);
                result[j] = new QueryResult.ResultQ3(a, b, c);
                j++;
            }
            return result;
        } catch (SQLException ex) {
            ex.printStackTrace();
            return null;
        }
    }

    @Override
    public QueryResult.ResultQ4[] functionQ4() {
        try {
            connect();
            String sql = "SELECT DISTINCT\n"
                    + "    bb.publisher_id, bb.category\n"
                    + "FROM\n"
                    + "    book bb\n"
                    + "WHERE\n"
                    + "    bb.publisher_id IN (SELECT \n"
                    + "            p.publisher_id\n"
                    + "        FROM\n"
                    + "            publisher p,\n"
                    + "            book b\n"
                    + "        WHERE\n"
                    + "            ((LENGTH(p.publisher_name)) - LENGTH(REPLACE(p.publisher_name, ' ', '')) + 1) > 2\n"
                    + "                AND p.publisher_id = b.publisher_id\n"
                    + "        GROUP BY p.publisher_id\n"
                    + "        HAVING COUNT(1) >= 3 AND AVG(b.rating) > 3)\n"
                    + "ORDER BY bb.publisher_id , bb.category;";
            PreparedStatement statement
                    = connection.prepareStatement(sql);
            ResultSet rs = statement.executeQuery();
            rs.last();
            int recordCount = rs.getRow();
            rs.beforeFirst();
            QueryResult.ResultQ4[] result = new QueryResult.ResultQ4[recordCount];
            int j = 0;
            while (rs.next()) {
                int a = rs.getInt(1);
                String b = rs.getString(2);
                result[j] = new QueryResult.ResultQ4(a, b);
                j++;
            }
            return result;
        } catch (SQLException ex) {
            ex.printStackTrace();
            return null;
        }
    }

    @Override
    public QueryResult.ResultQ5[] functionQ5(int i) {
        try {
            connect();
            String sql = "SELECT DISTINCT\n"
                    + "    A.*\n"
                    + "FROM\n"
                    + "    (SELECT \n"
                    + "        a.author_id, a.author_name\n"
                    + "    FROM\n"
                    + "        author_of ao, author a, book b\n"
                    + "    WHERE\n"
                    + "        ao.author_id = a.author_id\n"
                    + "            AND ao.isbn = b.isbn\n"
                    + "            AND b.publisher_id IN (SELECT DISTINCT\n"
                    + "                b1.publisher_id\n"
                    + "            FROM\n"
                    + "                author_of ao1, book b1\n"
                    + "            WHERE\n"
                    + "                ao1.author_id = ?\n"
                    + "                    AND b1.isbn = ao1.isbn)\n"
                    + "    GROUP BY a.author_id , a.author_name\n"
                    + "    HAVING COUNT(1) = (SELECT \n"
                    + "            COUNT(DISTINCT b1.publisher_id)\n"
                    + "        FROM\n"
                    + "            author_of ao1, book b1\n"
                    + "        WHERE\n"
                    + "            ao1.author_id = ?\n"
                    + "                AND b1.isbn = ao1.isbn)) A\n"
                    + "ORDER BY A.author_id;";
            PreparedStatement statement
                    = connection.prepareStatement(sql);
            statement.setInt(1, i);
            statement.setInt(2, i);
            ResultSet rs = statement.executeQuery();
            rs.last();
            int recordCount = rs.getRow();
            rs.beforeFirst();
            QueryResult.ResultQ5[] result = new QueryResult.ResultQ5[recordCount];
            int j = 0;
            while (rs.next()) {
                int a = rs.getInt(1);
                String b = rs.getString(2);
                result[j] = new QueryResult.ResultQ5(a, b);
                j++;
            }
            return result;
        } catch (SQLException ex) {
            ex.printStackTrace();
            return null;
        }
    }

    @Override
    public QueryResult.ResultQ6[] functionQ6() {
        try {
            connect();
            String sql = "Select distinct ao1.author_id,b1.isbn from book b1,author_of ao1 where ao1.isbn=b1.isbn\n"
                    + " and ao1.author_id in(\n"
                    + " select  ao.author_id from book b, author_of ao where \n"
                    + " b.publisher_id in ( SELECT p.publisher_id from publisher p\n"
                    + " where (Select Count(distinct ao.author_id) from book b, author_of ao\n"
                    + " where b.publisher_id = p.publisher_id and b.isbn = ao.isbn)=1)\n"
                    + " and ao.isbn = b.isbn)\n"
                    + " order by 1,2;";
            PreparedStatement statement
                    = connection.prepareStatement(sql);
            ResultSet rs = statement.executeQuery();
            rs.last();
            int recordCount = rs.getRow();
            rs.beforeFirst();
            QueryResult.ResultQ6[] result = new QueryResult.ResultQ6[recordCount];
            int j = 0;
            while (rs.next()) {
                int a = rs.getInt(1);
                String b = rs.getString(2);
                result[j] = new QueryResult.ResultQ6(a, b);
                j++;
            }
            return result;
        } catch (SQLException ex) {
            ex.printStackTrace();
            return null;
        }
    }

    @Override
    public QueryResult.ResultQ7[] functionQ7(double d) {
        try {
            connect();
            String sql = "SELECT DISTINCT\n"
                    + "    p.publisher_id, p.publisher_name\n"
                    + "FROM\n"
                    + "    book b,\n"
                    + "    publisher p\n"
                    + "WHERE\n"
                    + "    b.publisher_id = p.publisher_id\n"
                    + "        AND b.category = 'Roman'\n"
                    + "        AND EXISTS( SELECT \n"
                    + "            1\n"
                    + "        FROM\n"
                    + "            book b1,\n"
                    + "            publisher p1\n"
                    + "        WHERE\n"
                    + "            b1.publisher_id = p1.publisher_id\n"
                    + "                AND p1.publisher_id = p.publisher_id\n"
                    + "        GROUP BY p1.publisher_id\n"
                    + "        HAVING AVG(b1.rating) > ?)\n"
                    + "GROUP BY p.publisher_id\n"
                    + "HAVING COUNT(1) >= 2\n"
                    + "ORDER BY p.publisher_id;";
            PreparedStatement statement
                    = connection.prepareStatement(sql);
            statement.setDouble(1, d);
            ResultSet rs = statement.executeQuery();
            rs.last();
            int recordCount = rs.getRow();
            rs.beforeFirst();
            QueryResult.ResultQ7[] result = new QueryResult.ResultQ7[recordCount];
            int j = 0;
            while (rs.next()) {
                int a = rs.getInt(1);
                String b = rs.getString(2);
                result[j] = new QueryResult.ResultQ7(a, b);
                j++;
            }
            return result;
        } catch (SQLException ex) {
            ex.printStackTrace();
            return null;
        }
    }

    @Override
    public QueryResult.ResultQ8[] functionQ8() {
        connect();
        try {
            PreparedStatement bulkInsertStatement
                    = connection.prepareStatement("INSERT INTO phw1\n"
                            + "Select b1.isbn,b1.book_name,b1.rating from book b1,( \n"
                            + "select b.book_name , min(b.rating)minRate from book b\n"
                            + "group  by b.book_name\n"
                            + "having count(1)>1)lowestTemp\n"
                            + "where b1.book_name=lowestTemp.book_name and b1.rating=lowestTemp.minRate;");
            bulkInsertStatement.executeUpdate();

            PreparedStatement statement
                    = connection.prepareStatement("select isbn,book_name,rating from phw1 order by isbn;");
            ResultSet rs = statement.executeQuery();
            rs.last();
            int recordCount = rs.getRow();
            rs.beforeFirst();
            QueryResult.ResultQ8[] result = new QueryResult.ResultQ8[recordCount];
            int j = 0;
            while (rs.next()) {
                String a = rs.getString(1);
                String b = rs.getString(2);
                Double c = rs.getDouble(3);
                result[j] = new QueryResult.ResultQ8(a, b, c);
                j++;
            }
            disconnect();
            return result;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public double functionQ9(String is) {
        connect();
        double result = 0;
        try {
            PreparedStatement statement
                    = connection.prepareStatement("Update book set rating = rating + 1\n"
                            + "where rating<=4 and book_name like ?;");
            statement.setString(1, "%" + is + "%");
            statement.executeUpdate();

            Statement st = connection.createStatement();
            ResultSet rs = st.executeQuery("Select sum(b.rating) from book b;");

            while (rs.next()) {
                result = rs.getDouble(1);
            }
            disconnect();
            return result;
        } catch (SQLException e) {
            return 0;
        }
    }

    @Override
    public int function10() {
        connect();
        int result = 0;
        try {
            PreparedStatement statement
                    = connection.prepareStatement("delete from publisher \n"
                            + "where not exists (Select 1 from book "
                            + "where book.publisher_id = publisher.publisher_id);");
            statement.executeUpdate();

            Statement st = connection.createStatement();
            ResultSet rs = st.executeQuery("select count(*) from publisher;");

            while (rs.next()) {
                result = rs.getInt(1);
            }
            disconnect();
            return result;
        } catch (SQLException e) {
            return 0;
        }
    }

}
