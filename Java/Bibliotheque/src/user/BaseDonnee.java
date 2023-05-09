package user;

import java.sql.*;

public class BaseDonnee {

    private static String name = "bibliotheque";
    private static String url = "jdbc:mysql://localhost:3307/" + name;
    private static String username = "root";
    private static String password = "Bouchama123@";

    public static void executeInsert(String query) {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            Connection con = DriverManager.getConnection(url, username, password);
            Statement stmt = con.createStatement();
            int numRowsAffected = stmt.executeUpdate(query);
            System.out.println(numRowsAffected + " row(s) affected.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String[][] executeSelect(String query) {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            Connection con = DriverManager.getConnection(url, username, password);
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            ResultSetMetaData rsmd = rs.getMetaData();
            int columnsNumber = rsmd.getColumnCount();
            String[][] result = new String[100][columnsNumber];
            int i = 0;
            while (rs.next()) {
                for (int j = 0; j < columnsNumber; j++) {
                    result[i][j] = rs.getString(j + 1);
                }
                i++;
            }
            return result;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
