import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.text.*;

public class TextAreaSelectLine extends JFrame implements MouseListener
{
    JTextArea textArea;
    Action selectLine;

    public TextAreaSelectLine()
    {

        textArea = new JTextArea( "one two\nthree four", 10, 30 );
        textArea.addMouseListener( this );

        JScrollPane scrollPane = new JScrollPane( textArea );
        getContentPane().add( scrollPane, BorderLayout.SOUTH );
        getContentPane().add( new JTextArea() );

        selectLine = getAction(DefaultEditorKit.selectLineAction);

    }

    private Action getAction(String name)
    {
        Action action = null;
        Action[] actions = textArea.getActions();

        for (int i = 0; i < actions.length; i++)
        {
            if (name.equals( actions[i].getValue(Action.NAME).toString() ) )
            {
                action = actions[i];
                break;
            }
        }

        return action;
    }

    public void mouseClicked(MouseEvent e)
    {

        if ( SwingUtilities.isLeftMouseButton(e)  && e.getClickCount() == 1)
        {
            selectLine.actionPerformed( null );



        }
    }

    public void mousePressed(MouseEvent e) {}
    public void mouseReleased(MouseEvent e) {}
    public void mouseEntered(MouseEvent e) {}
    public void mouseExited(MouseEvent e) {}

    public static void main(String[] args)
    {
        TextAreaSelectLine frame = new TextAreaSelectLine();
        frame.setDefaultCloseOperation( EXIT_ON_CLOSE );
        frame.pack();
        frame.setVisible(true);
    }
}