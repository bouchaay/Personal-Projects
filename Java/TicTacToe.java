package TicTacToe;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class TicTacToe extends JFrame implements ActionListener {

    // Variables to hold the buttons of the Tic Tac Toe game
    JButton[][] buttons = new JButton[3][3];

    // Variables to hold the players' turn
    int player = 1;
    int count = 0;

    // Constructor to initialize the game
    public TicTacToe() {
        // Set up the game board
        setTitle("Tic Tac Toe Game");
        setSize(300, 300);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new GridLayout(3, 3));

        // Create the buttons for the game
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                buttons[i][j] = new JButton();
                buttons[i][j].setBackground(Color.WHITE);
                buttons[i][j].addActionListener(this);
                add(buttons[i][j]);
            }
        }
        setVisible(true);
    }

    // Method to check if the game is over
    public boolean gameOver() {
        // Check rows
        for (int i = 0; i < 3; i++) {
            if (buttons[i][0].getText().equals(buttons[i][1].getText()) && 
                buttons[i][1].getText().equals(buttons[i][2].getText()) && 
                !buttons[i][0].getText().equals("")) {
                return true;
            }
        }

        // Check columns
        for (int j = 0; j < 3; j++) {
            if (buttons[0][j].getText().equals(buttons[1][j].getText()) && 
                buttons[1][j].getText().equals(buttons[2][j].getText()) && 
                !buttons[0][j].getText().equals("")) {
                return true;
            }
        }

        // Check diagonals
        if (buttons[0][0].getText().equals(buttons[1][1].getText()) && 
            buttons[1][1].getText().equals(buttons[2][2].getText()) && 
            !buttons[0][0].getText().equals("")) {
            return true;
        }

        if (buttons[0][2].getText().equals(buttons[1][1].getText()) && 
            buttons[1][1].getText().equals(buttons[2][0].getText()) && 
            !buttons[0][2].getText().equals("")) {
            return true;
        }

        // Check if all buttons are filled
        if (count == 9) {
            JOptionPane.showMessageDialog(this, "It's a tie!");
            reset();
        }

        return false;
    }

    // Method to reset the game
    public void reset() {
        // Clear the board
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                buttons[i][j].setText("");
                buttons[i][j].setEnabled(true);
                buttons[i][j].setBackground(Color.WHITE);
            }
        }

        // Reset the players' turn
        player = 1;
        count = 0;
    }

    // Method to handle button clicks
    public void actionPerformed(ActionEvent e) {
        // Get the button that was clicked
        JButton button = (JButton) e.getSource();

        // Update the button text and disable it
        if (player == 1) {
        	button.setText("X");
        	button.setBackground(Color.RED);
        	} else {
        	button.setText("O");
        	button.setBackground(Color.BLUE);
        	}
        	button.setEnabled(false);
        	// Check if the game is over
            if (gameOver()) {
                JOptionPane.showMessageDialog(this, "Player " + player + " wins!");
                reset();
            } else {
                // Switch to the other player's turn
                player = (player == 1) ? 2 : 1;
                count++;
            }
        }

        // Main method to start the game
        public static void main(String[] args) {
            new TicTacToe();
        }
}
