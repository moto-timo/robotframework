#  Copyright 2008-2015 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
if sys.platform == 'cli':
    import System
    import clr
    clr.AddReference('System.Drawing')
    clr.AddReference('System.Windows.Forms')
    
    from System.Drawing import Point, ContentAlignment, Size, SizeF
    from System.Windows.Forms import AnchorStyles, Application, AutoScaleMode, BorderStyle, Button, ColumnStyle, DockStyle, FlowDirection, FlowLayoutPanel, Form, Label, ListBox, MessageBox, Padding, RowStyle, SizeType, TableLayoutPanel, TextBox

class _AbstractWinformsDialog(Form):
    _left_button = 'OK'
    _right_button = 'Cancel'

    def __init__(self, message, value=None, **extra):
        Form.__init__(self)
        self._initialize_dialog()
        self._create_body(message, value, **extra)
        self._create_buttons()
        self.AutoScaleDimensions = SizeF(8.0,16.0)
        self.AutoScaleMode = AutoScaleMode.Font
        self.ClientSize = Size(282,254)
        self.Controls.Add(self._panel)
        self._result = None
        self.Modal = False
        self._panel.ResumeLayout(False)
        self.ResumeLayout(False)
        self.PerformLayout()
        self.CenterToScreen()
        self.BringToFront()

    def show(self):
        Application.Run(self)
        return self._result

    def _initialize_dialog(self):
        self.Text = 'Robot Framework'
        self.MinimumSize = Size(250,250)
        self._panel = TableLayoutPanel()
        self._bodyPanel = FlowLayoutPanel()
        self._buttonPanel = FlowLayoutPanel()
        self._panel.SuspendLayout()
        self.SuspendLayout()
        self._panel.ColumnCount = 1
        self._panel.ColumnStyles.Add(ColumnStyle())
        self._panel.Controls.Add(self._bodyPanel, 0, 0)
        self._panel.Controls.Add(self._buttonPanel, 0, 1)
        self._panel.Dock = DockStyle.Fill
        self._panel.Location = Point(0,0)
        self._panel.RowCount = 2
        self._panel.RowStyles.Add(RowStyle(SizeType.Percent, 80.0))
        self._panel.RowStyles.Add(RowStyle(SizeType.Percent, 20.0))
        self._panel.Size = Size(282, 254)
        self._panel.TabIndex = 0

    def _create_body(self, message, value, **extra):
        self.label = Label()
        self._bodyPanel.Dock = DockStyle.Fill
        #self._bodyPanel.Margin = Padding(20)
        self._bodyPanel.Location = Point(3,3)
        self.Size = Size(276, 197)
        self._bodyPanel.TabIndex = 0;
        self.label.Text = message
        self.label.AutoSize = True
        self.label.TextAlign = ContentAlignment.MiddleLeft
        self.label.Margin = Padding(20)
        self.label.Location = Point(20,20)
        self.label.Size = self._bodyPanel.ClientSize
        self._bodyPanel.Controls.Add(self.label)
        selector = self._create_selector(value, **extra)
        if selector:
            self._bodyPanel.Controls.Add(selector)

    def _create_selector(self, value):
        return None

    def _create_buttons(self):
        self._buttonPanel.Dock = DockStyle.Fill
        self._buttonPanel.Location = Point(3, 206)
        self._buttonPanel.Size = Size(276,45)
        self._buttonPanel.TabIndex = 1
        self.leftButton = self._create_button(self._left_button,
                            self._left_button_clicked)
        self.rightButton = self._create_button(self._right_button,
                            self._right_button_clicked)
        if self.rightButton:
            self.leftButton.Anchor = ( AnchorStyles.Top | AnchorStyles.Left )
            self.rightButton.Anchor = ( AnchorStyles.Top | AnchorStyles.Right )
            self.leftButton.Size = Size(Point(self._buttonPanel.ClientSize.Width/2 - self.leftButton.Margin.Left - self.leftButton.Margin.Right,
                                              self._buttonPanel.ClientSize.Height - self.leftButton.Margin.Top - self.leftButton.Margin.Bottom))
            self.rightButton.Size = Size(Point(self._buttonPanel.ClientSize.Width/2 - self.rightButton.Margin.Left - self.rightButton.Margin.Right,
                                               self._buttonPanel.ClientSize.Height - self.rightButton.Margin.Top - self.rightButton.Margin.Bottom))
            self.AcceptButton = self.leftButton
            self.CancelButton = self.rightButton
            self._buttonPanel.Controls.Add(self.leftButton)
            self._buttonPanel.Controls.Add(self.rightButton)
        else:
            self.leftButton.Anchor = AnchorStyles.Left | AnchorStyles.Right
            self.leftButton.Size = Size(Point(self._buttonPanel.ClientSize.Width - self.leftButton.Margin.Left - self.leftButton.Margin.Right,
                                              self._buttonPanel.ClientSize.Height - self.leftButton.Margin.Top - self.leftButton.Margin.Bottom))
            self.AcceptButton = self.leftButton
            self._buttonPanel.Controls.Add(self.leftButton)

    def _create_button(self, label, callback):
        if label:
            button = Button()
            button.Text = label
            button.Click += callback
            return button

    def _left_button_clicked(self, sender, eventArgs):
        if self._validate_value():
            self._result = self._get_value()
            self._close()

    def _right_button_clicked(self, sender, eventArgs):
        self._result = self._get_right_button_value()
        self._close()

    def _validate_value(self):
        return True

    def _get_value(self):
        return None

    def _get_right_button_value(self):
        return None

    def _close(self):
        self.Close()

class MessageDialog(_AbstractWinformsDialog):
    _right_button = None

class InputDialog(_AbstractWinformsDialog):

    def __init__(self, message, default='', hidden=False):
        _AbstractWinformsDialog.__init__(self, message, default, hidden=hidden)
        self._bodyPanel.FlowDirection = FlowDirection.TopDown
        self.label.Margin = Padding(20,20,3,20)

    def _create_selector(self, default, hidden):
        self._entry = TextBox()
        self._entry.UseSystemPasswordChar = hidden
        self.Anchor = AnchorStyles.Right
        self.Dock = DockStyle.Fill
        self.AutoSize = True
        self._entry.Margin = Padding(20, 3, 20, 20)
        self._entry.Location = Point(self.label.Bounds.Right + self._entry.Margin.Left,self.label.Top)
        self._entry.Text = default if default else ''
        return self._entry

    def _get_value(self):
        return self._entry.Text


class SelectionDialog(_AbstractWinformsDialog):

    def __init__(self, message, values):
        _AbstractWinformsDialog.__init__(self, message, values)
        self._bodyPanel.FlowDirection = FlowDirection.TopDown
        self.label.Margin = Padding(20,20,20,3)
        self.label.Width = self._bodyPanel.ClientSize.Width - self.label.Margin.Left - self.label.Margin.Right

    def _create_selector(self, values):
        self._listbox = ListBox()
        self._listbox.AutoSize = True
        self._listbox.Margin = Padding(20,3,20,3)
        self._listbox.Anchor = AnchorStyles.Left
        self._listbox.Width = self._bodyPanel.ClientSize.Width - self._listbox.Margin.Left - self._listbox.Margin.Right
        for item in values:
            self._listbox.Items.Add(item)
        self._listbox.Dock = DockStyle.Fill
        return self._listbox

    def _validate_value(self):
        return bool(self._listbox.SelectedItem)

    def _get_value(self):
        return self._listbox.SelectedItem


class PassFailDialog(_AbstractWinformsDialog):
    _left_button = 'PASS'
    _right_button = 'FAIL'

    def _get_value(self):
        return True

    def _get_right_button_value(self):
        return False

def main():
    Application.EnableVisualStyles()
    Application.SetCompatibleTextRenderingDefault(False)

    #_form = _AbstractWinformsDialog(message = 'hello')
    #_form = MessageDialog(message = 'hello')
    #_form = InputDialog('name', 'Joe')
    _form = SelectionDialog('flower', ['Rose','Violet','Daisy','Iris','Geranium'])
    #_form = PassFailDialog('The sun came up today')
    _form.show()

if __name__ == '__main__':
    main()
