/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ide;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.InputMap;
import javax.swing.JComponent;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.JTextPane;
import javax.swing.KeyStroke;
import javax.swing.event.CaretEvent;
import javax.swing.event.CaretListener;
import javax.swing.plaf.basic.BasicMenuBarUI;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DefaultStyledDocument;
import javax.swing.text.Document;
import javax.swing.text.Element;
import javax.swing.text.JTextComponent;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyleContext;
import javax.swing.undo.CannotRedoException;
import javax.swing.undo.CannotUndoException;
import javax.swing.undo.UndoManager;
import org.python.core.PyString;
import org.python.core.PySystemState;
import org.python.util.PythonInterpreter;
import java.nio.file.Files;
/**
 *
 * @author Usuario
 */
public class Layout extends javax.swing.JFrame {

    public String RutaActual = "";
    private CountLines lineNumber;
    private boolean isNightMode;

    /**
     * Creates new form Interfaz
     */
    public Layout() {
        initComponents();
        inicializar();
        colors();
    }

    private void inicializar() {
        setTitle("Nuevo archivo");
        lineNumber = new CountLines(this.TextAreaCodigo);
        this.jScrollPane8.setRowHeaderView(this.lineNumber);
        this.TextAreaCodigo.addCaretListener(new CaretListener() {
            // Each time the caret is moved, it will trigger the listener and its method caretUpdate.
            // It will then pass the event to the update method including the source of the event (which is our textarea control)
            @Override
            public void caretUpdate(CaretEvent e) {
                int dot = e.getDot();
                int line;
                try {
                    line = getLineOfOffset(TextAreaCodigo, dot);
                    int positionInLine = dot - getLineStartOffset(TextAreaCodigo, line);
                } catch (BadLocationException ex) {
                    Logger.getLogger(Layout.class.getName()).log(Level.SEVERE, null, ex);
                }

            }
        });
    }

    static int getLineOfOffset(JTextComponent comp, int offset) throws BadLocationException {
        Document doc = comp.getDocument();
        if (offset < 0) {
            throw new BadLocationException("Can't translate offset to line", -1);
        } else if (offset > doc.getLength()) {
            throw new BadLocationException("Can't translate offset to line", doc.getLength() + 1);
        } else {
            Element map = doc.getDefaultRootElement();
            return map.getElementIndex(offset);
        }
    }

    static int getLineStartOffset(JTextComponent comp, int line) throws BadLocationException {
        Element map = comp.getDocument().getDefaultRootElement();
        if (line < 0) {
            throw new BadLocationException("Negative line", -1);
        } else if (line >= map.getElementCount()) {
            throw new BadLocationException("No such line", comp.getDocument().getLength() + 1);
        } else {
            Element lineElem = map.getElement(line);
            return lineElem.getStartOffset();
        }
    }

    //METODO PARA PINTAS LAS PALABRAS 
    private void colors() {

        final StyleContext cont = StyleContext.getDefaultStyleContext();

        //COLORES 
       
        final AttributeSet attora = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(255, 153, 51));
        //main
        final AttributeSet attpurple = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(204, 0, 204));
        //delcaraciones tipos de variables
        final AttributeSet attyellow = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(204, 204, 0));
        //true false
        final AttributeSet attblue = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(0, 0, 204));
        
        final AttributeSet attblack = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(0, 0, 0));
        //comentarios
        final AttributeSet attgreen = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(51, 255, 153));
        
        final AttributeSet attOperadores = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, new Color(0, 57, 128));
        
        final AttributeSet attwhite = cont.addAttribute(cont.getEmptySet(), StyleConstants.Foreground, Color.WHITE);
        //STYLO 
        DefaultStyledDocument doc = new DefaultStyledDocument() {
            @Override
            public void postRemoveUpdate(DefaultDocumentEvent chng) {
                try {
                    super.postRemoveUpdate(chng);
                    String text = getText(0, getLength());
                    //reset text
                    if (isNightMode) {
                        setCharacterAttributes(0, getLength(), attwhite, true);
                    } else {
                        setCharacterAttributes(0, getLength(), attblack, true);
                    }
                    //match palabras reservaadas
                    Pattern palabrasReservadas = Pattern.compile("\\b(main|if|IF|else|ELSE|end|END|do|DO|while|WHILE|then|THEN|repeat|REPEAT|until|UNTIL|cin|cout)\\b");
                    Matcher matcher = palabrasReservadas.matcher(text);
                    while (matcher.find()) {
                        setCharacterAttributes(matcher.start(),
                                matcher.end() - matcher.start(), attyellow, true);
                    }
                    //match NUMEROS
                    Pattern numerosPattern = Pattern.compile("\\b(-?\\d+(\\.\\d+)?)\\b");
                    matcher = numerosPattern.matcher(text);
                    while (matcher.find()) {
                        setCharacterAttributes(matcher.start(),
                                matcher.end() - matcher.start(), attora, true);
                    }
                    //match tipo de datos
                    Pattern tipoDeDatos = Pattern.compile("\\b(int|INT|real|REAL|boolean|BOOLEAN)\\b");
                    matcher = tipoDeDatos.matcher(text);
                    while (matcher.find()) {
                        setCharacterAttributes(matcher.start(),
                                matcher.end() - matcher.start(), attpurple, true);
                    }
                    //MATCH VALORES BOOLEANOS
                    Pattern booleanPattern = Pattern.compile("\\b(true|TRUE|false|FALSE)\\b");
                    matcher = booleanPattern.matcher(text);
                    while (matcher.find()) {
                        setCharacterAttributes(matcher.start(),
                                matcher.end() - matcher.start(), attblue, true);
                    }
                    //MATCH OPERADORES
                    Pattern operatorsPattern = Pattern.compile("[-+*/=<>!]");
                    matcher = operatorsPattern.matcher(text);
                    while (matcher.find()) {
                        setCharacterAttributes(matcher.start(),
                                matcher.end() - matcher.start(), attOperadores, true);
                    }
                    //DETECTAR COMETARIOS
                    Pattern singleLinecommentsPattern = Pattern.compile("\\/\\/.*");
                    matcher = singleLinecommentsPattern.matcher(text);
                    while (matcher.find()) {
                        setCharacterAttributes(matcher.start(),
                                matcher.end() - matcher.start(), attgreen, false);
                    }

                    Pattern multipleLinecommentsPattern = Pattern.compile("\\/\\*.*?\\*\\/",
                            Pattern.DOTALL);
                    matcher = multipleLinecommentsPattern.matcher(text);
                    while (matcher.find()) {
                        setCharacterAttributes(matcher.start(),
                                matcher.end() - matcher.start(), attgreen, false);

                    }
                } catch (BadLocationException ex) {
                    Logger.getLogger(Layout.class
                            .getName()).log(Level.SEVERE, null, ex);
                }

            }

            @Override
            public void insertString(int offset, String str, AttributeSet a) throws BadLocationException {
                super.insertString(offset, str, a);

                String text = getText(0, getLength());
                //reset text
                if (isNightMode) {
                    setCharacterAttributes(0, getLength(), attwhite, true);
                } else {
                    setCharacterAttributes(0, getLength(), attblack, true);
                }
                //match palabras reservaadas
                Pattern palabrasReservadas = Pattern.compile("\\b(main|if|IF|else|ELSE|end|END|do|DO|while|then|THEN|WHILE|repeat|REPEAT|until|UNTIL|cin|cout)\\b");
                Matcher matcher = palabrasReservadas.matcher(text);
                while (matcher.find()) {
                    setCharacterAttributes(matcher.start(),
                            matcher.end() - matcher.start(), attyellow, true);
                }
                //match NUMEROS
                Pattern numerosPattern = Pattern.compile("\\b(-?\\d+(\\.\\d+)?)\\b");
                matcher = numerosPattern.matcher(text);
                while (matcher.find()) {
                    setCharacterAttributes(matcher.start(),
                            matcher.end() - matcher.start(), attora, true);
                }
                //match tipo de datos
                Pattern tipoDeDatos = Pattern.compile("\\b(int|INT|float|FLOAT|boolean|BOOLEAN)\\b");
                matcher = tipoDeDatos.matcher(text);
                while (matcher.find()) {
                    setCharacterAttributes(matcher.start(),
                            matcher.end() - matcher.start(), attpurple, true);
                }
                //MATCH VALORES BOOLEANOS
                Pattern booleanPattern = Pattern.compile("\\b(true|TRUE|false|FALSE)\\b");
                matcher = booleanPattern.matcher(text);
                while (matcher.find()) {
                    setCharacterAttributes(matcher.start(),
                            matcher.end() - matcher.start(), attblue, true);
                }
                //MATCH OPERADORES
                Pattern operatorsPattern = Pattern.compile("[-+*/=<>!]");
                matcher = operatorsPattern.matcher(text);
                while (matcher.find()) {
                    setCharacterAttributes(matcher.start(),
                            matcher.end() - matcher.start(), attOperadores, true);
                }
                //DETECTAR COMETARIOS
                Pattern singleLinecommentsPattern = Pattern.compile("\\/\\/.*");
                matcher = singleLinecommentsPattern.matcher(text);
                while (matcher.find()) {
                    setCharacterAttributes(matcher.start(),
                            matcher.end() - matcher.start(), attgreen, false);
                }

                Pattern multipleLinecommentsPattern = Pattern.compile("\\/\\*.*?\\*\\/",
                        Pattern.DOTALL);
                matcher = multipleLinecommentsPattern.matcher(text);

                while (matcher.find()) {
                    setCharacterAttributes(matcher.start(),
                            matcher.end() - matcher.start(), attgreen, false);
                }
            }

        };

        JTextPane txt = new JTextPane(doc);
        String temp = this.TextAreaCodigo.getText();
        this.TextAreaCodigo.setStyledDocument(txt.getStyledDocument());
        this.TextAreaCodigo.setText(temp);

    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {
        java.awt.GridBagConstraints gridBagConstraints;

        jPanel1 = new javax.swing.JPanel();
        jTabbedPane1 = new javax.swing.JTabbedPane();
        jPanel2 = new javax.swing.JPanel();
        jScrollPane2 = new javax.swing.JScrollPane();
        jTextAreaResultados = new javax.swing.JTextArea();
        jTabbedPane2 = new javax.swing.JTabbedPane();
        jTabbedPane7 = new javax.swing.JTabbedPane();
        jPanel4 = new javax.swing.JPanel();
        jScrollPane4 = new javax.swing.JScrollPane();
        jTextAreaLexico = new javax.swing.JTextArea();
        jPanel5 = new javax.swing.JPanel();
        jScrollPane5 = new javax.swing.JScrollPane();
        jTextAreaSintacticp = new javax.swing.JTextArea();
        jPanel3 = new javax.swing.JPanel();
        jScrollPane1 = new javax.swing.JScrollPane();
        jTextAreaSemantico = new javax.swing.JTextArea();
        jScrollPane3 = new javax.swing.JScrollPane();
        jTextAreaseman = new javax.swing.JTextArea();
        jScrollPane8 = new javax.swing.JScrollPane();
        TextAreaCodigo = new javax.swing.JTextPane();
        jMenuBar1 = new javax.swing.JMenuBar();
        jMenu1 = new javax.swing.JMenu();
        jMenuItem1 = new javax.swing.JMenuItem();
        jMenuItem2 = new javax.swing.JMenuItem();
        jMenuItem4 = new javax.swing.JMenuItem();
        jMenu2 = new javax.swing.JMenu();
        jMenu4 = new javax.swing.JMenu();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        jPanel1.setBackground(new java.awt.Color(255, 255, 255));
        jPanel1.setLayout(new java.awt.GridBagLayout());

        jPanel2.setBackground(new java.awt.Color(255, 255, 255));

        jTextAreaResultados.setEditable(false);
        jTextAreaResultados.setBackground(new java.awt.Color(255, 204, 153));
        jTextAreaResultados.setColumns(20);
        jTextAreaResultados.setFont(new java.awt.Font("Monospaced", 0, 12)); // NOI18N
        jTextAreaResultados.setRows(5);
        jTextAreaResultados.setBorder(javax.swing.BorderFactory.createMatteBorder(1, 1, 1, 1, new java.awt.Color(0, 255, 204)));
        jScrollPane2.setViewportView(jTextAreaResultados);

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 1620, Short.MAX_VALUE)
            .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(jPanel2Layout.createSequentialGroup()
                    .addContainerGap()
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 1608, Short.MAX_VALUE)
                    .addContainerGap()))
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 101, Short.MAX_VALUE)
            .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
                    .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
        );

        jTabbedPane1.addTab("OUTPUT", jPanel2);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 1;
        gridBagConstraints.gridwidth = 2;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.ipadx = 1202;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.NORTHWEST;
        gridBagConstraints.insets = new java.awt.Insets(7, 12, 13, 12);
        jPanel1.add(jTabbedPane1, gridBagConstraints);
        jPanel1.add(jTabbedPane2, new java.awt.GridBagConstraints());

        jPanel4.setBackground(new java.awt.Color(255, 204, 204));

        jTextAreaLexico.setEditable(false);
        jTextAreaLexico.setBackground(new java.awt.Color(204, 255, 204));
        jTextAreaLexico.setColumns(20);
        jTextAreaLexico.setFont(new java.awt.Font("Dubai Light", 0, 14)); // NOI18N
        jTextAreaLexico.setRows(5);
        jTextAreaLexico.setBorder(javax.swing.BorderFactory.createMatteBorder(1, 1, 1, 1, new java.awt.Color(0, 0, 255)));
        jTextAreaLexico.setCaretColor(new java.awt.Color(51, 51, 255));
        jTextAreaLexico.setSelectedTextColor(new java.awt.Color(0, 0, 0));
        jScrollPane4.setViewportView(jTextAreaLexico);

        javax.swing.GroupLayout jPanel4Layout = new javax.swing.GroupLayout(jPanel4);
        jPanel4.setLayout(jPanel4Layout);
        jPanel4Layout.setHorizontalGroup(
            jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 493, Short.MAX_VALUE)
            .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel4Layout.createSequentialGroup()
                    .addComponent(jScrollPane4, javax.swing.GroupLayout.DEFAULT_SIZE, 487, Short.MAX_VALUE)
                    .addContainerGap()))
        );
        jPanel4Layout.setVerticalGroup(
            jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 591, Short.MAX_VALUE)
            .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel4Layout.createSequentialGroup()
                    .addComponent(jScrollPane4, javax.swing.GroupLayout.DEFAULT_SIZE, 585, Short.MAX_VALUE)
                    .addContainerGap()))
        );

        jTabbedPane7.addTab("Lexico", jPanel4);

        jPanel5.setBackground(new java.awt.Color(153, 153, 153));

        jTextAreaSintacticp.setEditable(false);
        jTextAreaSintacticp.setBackground(new java.awt.Color(255, 204, 204));
        jTextAreaSintacticp.setColumns(20);
        jTextAreaSintacticp.setFont(new java.awt.Font("Algerian", 0, 14)); // NOI18N
        jTextAreaSintacticp.setRows(5);
        jTextAreaSintacticp.setBorder(javax.swing.BorderFactory.createMatteBorder(1, 1, 1, 1, new java.awt.Color(204, 153, 255)));
        jScrollPane5.setViewportView(jTextAreaSintacticp);

        javax.swing.GroupLayout jPanel5Layout = new javax.swing.GroupLayout(jPanel5);
        jPanel5.setLayout(jPanel5Layout);
        jPanel5Layout.setHorizontalGroup(
            jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 493, Short.MAX_VALUE)
            .addGroup(jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addComponent(jScrollPane5, javax.swing.GroupLayout.DEFAULT_SIZE, 493, Short.MAX_VALUE))
        );
        jPanel5Layout.setVerticalGroup(
            jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 591, Short.MAX_VALUE)
            .addGroup(jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addComponent(jScrollPane5, javax.swing.GroupLayout.DEFAULT_SIZE, 591, Short.MAX_VALUE))
        );

        jTabbedPane7.addTab("Sintactico", jPanel5);

        jPanel3.setBackground(new java.awt.Color(255, 255, 255));

        jTextAreaSemantico.setEditable(false);
        jTextAreaSemantico.setBackground(new java.awt.Color(153, 153, 255));
        jTextAreaSemantico.setColumns(20);
        jTextAreaSemantico.setFont(new java.awt.Font("Times New Roman", 0, 12)); // NOI18N
        jTextAreaSemantico.setRows(5);
        jScrollPane1.setViewportView(jTextAreaSemantico);

        javax.swing.GroupLayout jPanel3Layout = new javax.swing.GroupLayout(jPanel3);
        jPanel3.setLayout(jPanel3Layout);
        jPanel3Layout.setHorizontalGroup(
            jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 493, Short.MAX_VALUE)
        );
        jPanel3Layout.setVerticalGroup(
            jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 591, Short.MAX_VALUE)
        );

        jTabbedPane7.addTab("Arbol", jPanel3);

        jTextAreaseman.setEditable(false);
        jTextAreaseman.setBackground(new java.awt.Color(255, 204, 153));
        jTextAreaseman.setColumns(10);
        jTextAreaseman.setFont(new java.awt.Font("Nirmala UI Semilight", 0, 12)); // NOI18N
        jTextAreaseman.setLineWrap(true);
        jTextAreaseman.setRows(10);
        jTextAreaseman.setTabSize(5);
        jScrollPane3.setViewportView(jTextAreaseman);

        jTabbedPane7.addTab("Tabla", jScrollPane3);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 1;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.ipadx = 417;
        gridBagConstraints.ipady = 416;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.NORTHEAST;
        gridBagConstraints.insets = new java.awt.Insets(13, 12, 0, 12);
        jPanel1.add(jTabbedPane7, gridBagConstraints);

        TextAreaCodigo.setBackground(new java.awt.Color(204, 255, 255));
        TextAreaCodigo.setBorder(javax.swing.BorderFactory.createMatteBorder(1, 1, 1, 1, new java.awt.Color(204, 51, 255)));
        TextAreaCodigo.setFont(new java.awt.Font("Berlin Sans FB", 0, 20)); // NOI18N
        TextAreaCodigo.setCursor(new java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR));
        TextAreaCodigo.setMinimumSize(new java.awt.Dimension(255, 255));
        TextAreaCodigo.setPreferredSize(new java.awt.Dimension(286, 116));
        TextAreaCodigo.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent evt) {
                TextAreaCodigoKeyPressed(evt);
            }
            public void keyReleased(java.awt.event.KeyEvent evt) {
                TextAreaCodigoKeyReleased(evt);
            }
            public void keyTyped(java.awt.event.KeyEvent evt) {
                TextAreaCodigoKeyTyped(evt);
            }
        });
        jScrollPane8.setViewportView(TextAreaCodigo);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.ipadx = 699;
        gridBagConstraints.ipady = 508;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.NORTHWEST;
        gridBagConstraints.weightx = 1.0;
        gridBagConstraints.weighty = 1.0;
        gridBagConstraints.insets = new java.awt.Insets(13, 12, 0, 0);
        jPanel1.add(jScrollPane8, gridBagConstraints);

        jMenuBar1.setBackground(new java.awt.Color(255, 255, 204));
        jMenuBar1.setPreferredSize(new java.awt.Dimension(291, 35));

        jMenu1.setIcon(new javax.swing.ImageIcon(getClass().getResource("/ide/icons8_opened_folder_48px.png"))); // NOI18N
        jMenu1.setText("Archivo");
        jMenu1.setPreferredSize(new java.awt.Dimension(55, 55));

        jMenuItem1.setText("Abrir");
        jMenuItem1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem1ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem1);

        jMenuItem2.setText("Guardar");
        jMenuItem2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem2ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem2);

        jMenuItem4.setText("Cerrar");
        jMenuItem4.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem4ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem4);

        jMenuBar1.add(jMenu1);

        jMenu2.setIcon(new javax.swing.ImageIcon(getClass().getResource("/ide/icons8_save_as_48px.png"))); // NOI18N
        jMenu2.setText("Editar");
        jMenu2.setPreferredSize(new java.awt.Dimension(55, 55));
        jMenuBar1.add(jMenu2);

        jMenu4.setIcon(new javax.swing.ImageIcon(getClass().getResource("/ide/icons8_code_48px.png"))); // NOI18N
        jMenu4.setText("Compilar");
        jMenu4.setPreferredSize(new java.awt.Dimension(55, 55));
        jMenu4.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                jMenu4MouseClicked(evt);
            }
        });
        jMenu4.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenu4ActionPerformed(evt);
            }
        });
        jMenuBar1.add(jMenu4);

        setJMenuBar(jMenuBar1);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, 1644, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, 795, Short.MAX_VALUE)
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    public void AbrirTxt(String Ruta) {
        File archivo = null;
        FileReader fr = null;
        BufferedReader br = null;
        RutaActual = Ruta;
        try {
            // Apertura del fichero y creacion de BufferedReader para poder
            // hacer una lectura comoda (disponer del metodo readLine()).
            archivo = new File(Ruta);

            TextAreaCodigo.setText(getTextFile(archivo));
            setTitle(archivo.getName());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void jMenuItem2ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem2ActionPerformed
        saveFile();
    }//GEN-LAST:event_jMenuItem2ActionPerformed

    private void saveFile() {
        if (RutaActual != "") {
            try {
                String ruta = RutaActual;

                File file = new File(ruta);
                // Si el archivo no existe es creado
                if (!file.exists()) {
                    file.createNewFile();
                }
                FileWriter fw = new FileWriter(file);
                BufferedWriter bw = new BufferedWriter(fw);
                bw.write(TextAreaCodigo.getText());
                setTitle(file.getName());
                bw.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            JFileChooser guardar = new JFileChooser();
            guardar.showSaveDialog(null);
            guardar.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
            File archivo = guardar.getSelectedFile();
            System.out.println(guardar.getSelectedFile().getPath());
            guardarFichero(TextAreaCodigo.getText(), archivo);
            RutaActual = guardar.getSelectedFile().getPath();
        }
    }

    public String getTextFile(File file) {
        String text = "";
        try {

            BufferedReader entrada = new BufferedReader(new InputStreamReader(new FileInputStream(file), "UTF8"));
            while (true) {
                int b = entrada.read();
                if (b != -1) {
                    text += (char) b;
                } else {
                    break;
                }
            }
        } catch (FileNotFoundException ex) {
            System.out.println("El archivo no pudo ser encontrado... " + ex.getMessage());
            return null;
        } catch (IOException ex) {
            System.out.println("Error al leer el archivo... " + ex.getMessage());
            return null;
        }
        return text;
    }


    private void jMenuItem4ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem4ActionPerformed
        TextAreaCodigo.setText("");
        RutaActual = "";
        setTitle("Nuevo archivo");
        jTextAreaLexico.setText("");
        jTextAreaLexico.setText("");
    }//GEN-LAST:event_jMenuItem4ActionPerformed

    private void TextAreaCodigoKeyReleased(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_TextAreaCodigoKeyReleased
        this.tecla(evt);
    }//GEN-LAST:event_TextAreaCodigoKeyReleased

    private void TextAreaCodigoKeyTyped(java.awt.event.KeyEvent evt) {

    }

    private void TextAreaCodigoKeyPressed(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_TextAreaCodigoKeyPressed
    }//GEN-LAST:event_TextAreaCodigoKeyPressed

       

    
    private void jMenu4ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenu4ActionPerformed
        saveFile();
        executeLexico();
   
    }//GEN-LAST:event_jMenu4ActionPerformed

    private void jMenu4MouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_jMenu4MouseClicked
        saveFile();
        executeLexico();
    }//GEN-LAST:event_jMenu4MouseClicked

    private void jMenuItem1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem1ActionPerformed
        JFileChooser selectorArchivos = new JFileChooser();
        selectorArchivos.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
        selectorArchivos.showOpenDialog(this);
        AbrirTxt(selectorArchivos.getSelectedFile().getPath());
    }//GEN-LAST:event_jMenuItem1ActionPerformed

    private void executeLexico() {
        PySystemState state = new PySystemState();
        state.argv.append(new PyString("-f"));
        state.argv.append(new PyString(RutaActual));
        PythonInterpreter interpreter = new PythonInterpreter(null, state);

        interpreter.execfile("AnalizadorLexico.py");

        //abrir archivo lexemas
        jTextAreaLexico.setText("");
        BufferedReader in = null;
        try {
            in = new BufferedReader(new FileReader("lexico.txt"));
            String str;
            while ((str = in.readLine()) != null) {
                jTextAreaLexico.append(str + '\n');
            }
        } catch (IOException e) {
        } finally {
            try {
                in.close();
            } catch (Exception ex) {
            }
        }
        //abrir archivo de errores lexemas
        jTextAreaLexico.setText("");
        try {
            in = new BufferedReader(new FileReader("lexico.txt"));
            String str;
            while ((str = in.readLine()) != null) {
                jTextAreaLexico.append(str + '\n');
            }
        } catch (IOException e) {
        } finally {
            try {
                in.close();
            } catch (Exception ex) {
            }
        }
            this.Sintactico();
            this.Semantico();
            this.Semantico2();
            this.Errores();
    }

    public void Sintactico(){
        String rutaActual = System.getProperty("user.dir");
        System.out.println("Ruta actual: " + rutaActual);
        Path rutaNueva = Paths.get(rutaActual);
        System.out.println("Ruta nueva: " + rutaNueva.toString());
        //Path ruta = Paths.get(rutaNueva.toString(),"AnalizadorLexico");
        //System.out.println(ruta);
        Path rutaScript = Paths.get(rutaNueva.toString()).resolve("analizadorsintactico.py");
        
        try {
            String salidaPython = CodeAnalyzer.ejecutarScriptPython(rutaScript.toString());
            this.jTextAreaSintacticp.setText(salidaPython);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public void Semantico(){
        String rutaActual = System.getProperty("user.dir");
        //System.out.println("Ruta actual: " + rutaActual);
        Path rutaNueva = Paths.get(rutaActual);
       // System.out.println("Ruta nueva: " + rutaNueva.toString());
        //Path ruta = Paths.get(rutaNueva.toString(),"AnalizadorLexico");
        //System.out.println(ruta);
        Path rutaScript = Paths.get(rutaNueva.toString()).resolve("parse.py");
        
        //this.jTextAreaSemantico.setText("");
        System.out.println("aaa "+ rutaScript.toString());
        
        try {
            String salidaPython = CodeAnalyzer.ejecutarScriptPython(rutaScript.toString());
            this.jTextAreaSemantico.setText(salidaPython);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void Semantico2(){
        String rutaActual = System.getProperty("user.dir");
        Path rutaScript = Paths.get(rutaActual).resolve("Archivo_TabSym.txt"); // Asume que el archivo se llama "archivo_ErrorSem.txt"
    try {
        // Leer el contenido del archivo
        String contenido = new String(Files.readAllBytes(rutaScript));
        
        // Mostrar el contenido en el JTextArea
        System.out.println(contenido);
        jTextAreaseman.setText(contenido);
    } catch (IOException e) {
        e.printStackTrace();
        this.jTextAreaseman.setText("Error al leer el archivo: " + e.getMessage());
    }
        }
    
    private void tecla(java.awt.event.KeyEvent evt) {
        int keyCode = evt.getKeyCode();
        if ((keyCode >= 65 && keyCode <= 90) || (keyCode >= 48 && keyCode <= 57)
                || (keyCode >= 97 && keyCode <= 122) || (keyCode != 27 && !(keyCode >= 37
                && keyCode <= 40) && !(keyCode >= 16
                && keyCode <= 18) && keyCode != 524
                && keyCode != 20)) {

            if (!getTitle().contains("*")) {
                setTitle(getTitle() + "*");
            }
        }

    }
    
    public void Errores() {
    String rutaActual = System.getProperty("user.dir");
    Path rutaScript = Paths.get(rutaActual).resolve("Archivo_ErrorSem.txt"); // Asume que el archivo se llama "archivo_ErrorSem.txt"

    try {
        // Leer el contenido del archivo
        String contenido = new String(Files.readAllBytes(rutaScript));
        
        // Mostrar el contenido en el JTextArea
        jTextAreaResultados.setText(contenido);
    } catch (IOException e) {
        e.printStackTrace();
        jTextAreaResultados.setText("Error al leer el archivo: " + e.getMessage());
    }
}


    /**
     * @param args the command line arguments
     */
    public void guardarFichero(String cadena, File archivo) {

        FileWriter escribir;
        try {

            escribir = new FileWriter(archivo, true);
            escribir.write(cadena);
            escribir.close();
            setTitle(archivo.getName());
        } catch (FileNotFoundException ex) {
            JOptionPane.showMessageDialog(null, "Error al guardar, ponga nombre al archivo");
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(null, "Error al guardar, en la salida");
        }
    }

    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;

                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(Layout.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(Layout.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(Layout.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(Layout.class
                    .getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new Layout().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JTextPane TextAreaCodigo;
    private javax.swing.JMenu jMenu1;
    private javax.swing.JMenu jMenu2;
    private javax.swing.JMenu jMenu4;
    private javax.swing.JMenuBar jMenuBar1;
    private javax.swing.JMenuItem jMenuItem1;
    private javax.swing.JMenuItem jMenuItem2;
    private javax.swing.JMenuItem jMenuItem4;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPanel jPanel3;
    private javax.swing.JPanel jPanel4;
    private javax.swing.JPanel jPanel5;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JScrollPane jScrollPane3;
    private javax.swing.JScrollPane jScrollPane4;
    private javax.swing.JScrollPane jScrollPane5;
    private javax.swing.JScrollPane jScrollPane8;
    private javax.swing.JTabbedPane jTabbedPane1;
    private javax.swing.JTabbedPane jTabbedPane2;
    private javax.swing.JTabbedPane jTabbedPane7;
    private javax.swing.JTextArea jTextAreaLexico;
    private javax.swing.JTextArea jTextAreaResultados;
    private javax.swing.JTextArea jTextAreaSemantico;
    private javax.swing.JTextArea jTextAreaSintacticp;
    private javax.swing.JTextArea jTextAreaseman;
    // End of variables declaration//GEN-END:variables
}
