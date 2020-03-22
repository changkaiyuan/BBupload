
import java.awt.*;
import javax.swing.*;


public class BbWindow {

    public static void setupWindow(){
        JFrame frame = new JFrame("BBUpload"); //title

        //Creating Menus
        JMenuBar menuBar = new JMenuBar();
        JMenu menuAcc = new JMenu("Account");
        JMenu menuAbout = new JMenu("About");
        JMenuItem createAcc = new JMenuItem("New Student Profile");
        menuAcc.add(createAcc);
        menuBar.add(menuAcc);
        menuBar.add(menuAbout);
        frame.setJMenuBar(menuBar);

        Container container = frame.getContentPane();
        container.setLayout(new GridLayout(3,2));

        // panelTOP
        JPanel panelTop = new JPanel();
        JLabel nameLabel = new JLabel("Student Name");
        panelTop.add(nameLabel);//label


        JTextArea nameArea = new JTextArea();
        nameArea.setColumns(20);
        nameArea.setRows(1);
        nameArea.setLineWrap(true);
        nameArea.setWrapStyleWord(true);
        JScrollPane jsp = new JScrollPane(nameArea);
        panelTop.add(jsp);//nameArea

        JButton search_btn = new JButton("Search");
        search_btn.setContentAreaFilled(false);
        search_btn.setFocusPainted(false);
        panelTop.add(search_btn);//btn

        container.add(panelTop);


        //panelCenter
        JPanel panelCenter = new JPanel();
        //dropDown box
        String[] nameStrings= {"-- Please Select Your Name --","I am A", "I am N", "Add me plox"};
        JComboBox nameList = new JComboBox(nameStrings);
        panelCenter.add(nameList);

        JButton select_btn = new JButton("Select");
        select_btn.setContentAreaFilled(false);
        select_btn.setFocusPainted(false);
        panelCenter.add(select_btn);//btn

        container.add(panelCenter);

        //panelBot
        JPanel panelBot = new JPanel();
        panelBot.setLayout(new GridLayout(1,2));
        container.add(panelBot);


        //itemList
        String[] items = {"appleaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","pear","melons","apple","pear","apple","pear","apple","pear","apple","pear","apple","pear"};
        JList itemList= new JList(items);
        itemList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        itemList.setLayoutOrientation(JList.VERTICAL);
//        itemList.setVisibleRowCount(-1);
        JScrollPane listScroller = new JScrollPane(itemList);
        listScroller.setPreferredSize(new Dimension(100, 80));
        panelBot.add(listScroller);



        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new GridLayout(2,1));
        JButton upload = new JButton("UPLOAD FILE");
        upload.setContentAreaFilled(false);
        upload.setFocusPainted(false);
        buttonPanel.add(upload);//btn

        JButton download = new JButton("DOWNLOAD FILE");
        download.setContentAreaFilled(false);
        download.setFocusPainted(false);
        buttonPanel.add(download);//btn

        panelBot.add(buttonPanel);






//        container.add(panelTop);
//        container.add(panelCenter);
//        container.add(panelBot);
        frame.setSize(600,500);
        frame.setLocation(100,100); //windows location on the screen
        frame.setResizable(false);

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }


    public static void main(String[] args){
        setupWindow();
    }
}
