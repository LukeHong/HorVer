# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'

import os

try:
    from PyQt5.Qt import (Qt, QVBoxLayout, QLabel, QComboBox, QApplication, QSizePolicy,
                      QGroupBox, QButtonGroup, QRadioButton, QDialogButtonBox, QHBoxLayout,
                      QProgressDialog, QSize, QDialog, QCheckBox, QSpinBox, QScrollArea, QWidget)
except ImportError:
    from PyQt4.Qt import (Qt, QVBoxLayout, QLabel, QComboBox, QApplication, QSizePolicy,
                      QGroupBox, QButtonGroup, QRadioButton, QDialogButtonBox, QHBoxLayout,
                      QProgressDialog, QSize, QDialog, QCheckBox, QSpinBox, QScrollArea, QWidget)

from calibre.utils.config import config_dir

from calibre.gui2.tweak_book.widgets import Dialog
from calibre_plugins.chinese_text.__init__ import (PLUGIN_NAME, PLUGIN_SAFE_NAME)

class ConversionDialog(Dialog):
    def __init__(self, parent, force_entire_book=False):
        self.prefs = self.prefsPrep()
        self.parent = parent
        self.force_entire_book = force_entire_book
        self.criteria = None
        Dialog.__init__(self, _('Chinese Conversion'), 'chinese_conversion_dialog', parent)

    def setup_ui(self):

        # Create layout for entire dialog
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        #Create a scroll area for the top part of the dialog
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        # Create widget for all the contents of the dialog except the OK and Cancel buttons
        self.scrollContentWidget = QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollContentWidget)
        widgetLayout = QVBoxLayout(self.scrollContentWidget)

        # Add scrollArea to dialog
        layout.addWidget(self.scrollArea)

        self.other_group_box = QGroupBox(_('Other Changes'))
        widgetLayout.addWidget(self.other_group_box)
        other_group_box_layout = QVBoxLayout()
        self.other_group_box.setLayout(other_group_box_layout)

        text_dir_layout = QHBoxLayout()
        other_group_box_layout.addLayout(text_dir_layout)
        direction_label = QLabel(_('Text Direction:'))
        text_dir_layout.addWidget(direction_label)
        self.text_dir_combo = QComboBox()
        text_dir_layout.addWidget(self.text_dir_combo)
        self.text_dir_combo.addItems([_('No Conversion'), _('Horizontal'), _('Vertical')])
        self.text_dir_combo.setToolTip(_('Select the desired text orientation'))
        self.text_dir_combo.currentIndexChanged.connect(self.update_gui)


        self.optimization_group_box = QGroupBox(_('Reader Device Optimization'))
        other_group_box_layout.addWidget(self.optimization_group_box)
        optimization_group_box_layout = QVBoxLayout()
        self.optimization_group_box.setLayout(optimization_group_box_layout)
        
        punc_group=QButtonGroup(self)
        self.text_dir_punc_none_button = QRadioButton("""No presentation optimization""")
        optimization_group_box_layout.addWidget(self.text_dir_punc_none_button)
        self.text_dir_punc_button = QRadioButton("""Optimize presentation for Readium reader""")
        self.text_dir_punc_button.setToolTip(_('Use vert/horiz punctuation presentation forms for Chrome Readium Epub3 reader'))
        optimization_group_box_layout.addWidget(self.text_dir_punc_button)
        self.text_dir_punc_kindle_button = QRadioButton("""Optimize presentation for Kindle reader""")
        self.text_dir_punc_kindle_button.setToolTip(_('Use vert/horiz puncuation presentation forms for Kindle reader'))
        optimization_group_box_layout.addWidget(self.text_dir_punc_kindle_button)
        self.text_dir_punc_none_button.toggled.connect(self.update_gui)
        self.text_dir_punc_button.toggled.connect(self.update_gui)
        self.text_dir_punc_kindle_button.toggled.connect(self.update_gui)

        source_group=QButtonGroup(self)
        self.file_source_button = QRadioButton(_('Selected File Only'))
        self.book_source_button = QRadioButton(_('Entire eBook'))
        source_group.addButton(self.file_source_button)
        source_group.addButton(self.book_source_button)
        self.source_group_box = QGroupBox(_('Source'))
        if not self.force_entire_book:
            widgetLayout.addWidget(self.source_group_box)
            source_group_box_layout = QVBoxLayout()
            self.source_group_box.setLayout(source_group_box_layout)
            source_group_box_layout.addWidget(self.file_source_button)
            source_group_box_layout.addWidget(self.book_source_button)

        layout.addSpacing(10)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.button_box.accepted.connect(self._ok_clicked)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        if not self.force_entire_book:
            self.file_source_button.setChecked(self.prefs['use_html_file'])
            self.book_source_button.setChecked(self.prefs['use_entire_book'])
        else:
            self.file_source_button.setChecked(False)
            self.book_source_button.setChecked(True)

        self.text_dir_combo.setCurrentIndex(self.prefs['orientation'])
        self.text_dir_punc_none_button.setChecked(self.prefs['no_optimization'])
        self.text_dir_punc_button.setChecked(self.prefs['readium_optimization'])
        self.text_dir_punc_kindle_button.setChecked(self.prefs['kindle_optimization'])
        self.update_gui()

    def update_gui(self):

        if self.text_dir_combo.currentIndex() == 0:
            self.optimization_group_box.setEnabled(False)
            self.text_dir_punc_none_button.setEnabled(False)
            self.text_dir_punc_button.setEnabled(False)
            self.text_dir_punc_kindle_button.setEnabled(False)
        else:
            self.optimization_group_box.setEnabled(True)
            self.text_dir_punc_none_button.setEnabled(True)
            self.text_dir_punc_button.setEnabled(True)
            self.text_dir_punc_kindle_button.setEnabled(True)
            
    def _ok_clicked(self):

        optimization_mode = 0
        if self.text_dir_punc_button.isChecked():
            optimization_mode = 1    #Readium
        if self.text_dir_punc_kindle_button.isChecked():
            optimization_mode = 2    #Kindle
 
        self.criteria = (self.text_dir_combo.currentIndex(), optimization_mode)
        self.savePrefs()
        self.accept()

    def getCriteria(self):
        return self.criteria

    def prefsPrep(self):
        from calibre.utils.config import JSONConfig
        plugin_prefs = JSONConfig('plugins/{0}_ChineseConversion_settings'.format(PLUGIN_SAFE_NAME))
        plugin_prefs.defaults['use_html_file'] = True
        plugin_prefs.defaults['use_entire_book'] = True
        plugin_prefs.defaults['orientation'] = 0
        plugin_prefs.defaults['no_optimization'] = True
        plugin_prefs.defaults['readium_optimization'] = False
        plugin_prefs.defaults['kindle_optimization'] = False
        return plugin_prefs

    def savePrefs(self):
        self.prefs['use_html_file'] = self.file_source_button.isChecked()
        self.prefs['use_entire_book'] = self.book_source_button.isChecked()
        self.prefs['orientation'] = self.text_dir_combo.currentIndex()
        self.prefs['no_optimization'] = self.text_dir_punc_none_button.isChecked()
        self.prefs['readium_optimization'] = self.text_dir_punc_button.isChecked()
        self.prefs['kindle_optimization'] = self.text_dir_punc_kindle_button.isChecked()

