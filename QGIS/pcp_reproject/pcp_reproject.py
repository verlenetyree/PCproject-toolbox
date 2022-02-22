# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PCPreproject
                                 A QGIS plugin
 This plugin transform vector oblects into perspective cylindrical projections
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-04-06
        git sha              : $Format:%H$
        copyright            : (C) 2021 by MSU
        email                : grita005@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .pcp_reproject_dockwidget import PCPreprojectDockWidget
import os.path


class PCPreproject:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PCPreproject_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Perspective Cylindrical Projections')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PCPreproject')
        self.toolbar.setObjectName(u'PCPreproject')

        #print "** INITIALIZING PCPreproject"

        self.pluginIsActive = False
        self.dockwidget = None


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PCPreproject', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/pcp_reproject/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Perspective Cylindrical Projections'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING PCPreproject"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD PCPreproject"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Perspective Cylindrical Projections'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING PCPreproject"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = PCPreprojectDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

            def process_normal():
                import math
                from qgis.core import QgsFields, QgsField, QgsVectorFileWriter, QgsWkbTypes, \
                    QgsCoordinateReferenceSystem, \
                    QgsFeature, QgsGeometry, QgsPointXY, QgsPoint
                from PyQt5.QtCore import QVariant
                from datetime import datetime

                start_time = datetime.now()

                K = float(self.dockwidget.lineEdit.text())
                fik = float(self.dockwidget.lineEdit_2.text())
                lyambdam = 100

                R = 6371116
                C = K + math.cos(fik * math.pi / 180)
                alpha = R * math.cos(fik * math.pi / 180)

                output = open(r'C:\Users\grita\Documents\MSU\test.txt', 'w')
                part_file = open(r'C:\Users\grita\Documents\MSU\part_file.txt', 'w')
                fn = self.dockwidget.mQgsFileWidget.filePath()

                layerFields = QgsFields()
                layerFields.append(QgsField('ID', QVariant.Int))
                layerFields.append(QgsField('AREA', QVariant.Double))
                writer = QgsVectorFileWriter(fn, 'UTF-8', layerFields, QgsWkbTypes.MultiPolygon,
                                             QgsCoordinateReferenceSystem('EPSG:3395'), 'ESRI Shapefile')

                layer = self.dockwidget.mMapLayerComboBox.currentLayer()
                out_feat = QgsFeature()
                out_feat_geom = out_feat.geometry()
                id = 1
                polygons = []
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    for part in geom.parts():
                        points = []  # КАЖДУЮ ЧАСТЬ СОЗДАЁМ СПИСОК ЕЁ ТОЧЕК
                        for pnt in part.vertices():

                            x = pnt.x()
                            y = pnt.y()

                            x_new = alpha * x * math.pi / 180
                            if (K + math.cos(y * math.pi / 180)) == 0:
                                continue
                            y_new = C * R * (math.sin(y * math.pi / 180) / (K + math.cos(y * math.pi / 180)))

                            output.write("{}, {}".format(x_new, y_new) + '\n')
                            points.append(QgsPointXY(x_new, y_new))

                        polygons.append(points)

                    out_feat.setGeometry(QgsGeometry.fromMultiPolygonXY([[part for part in polygons]]))
                    part_file.write('Part:\n' + str(out_feat.geometry()) + '\n\n')
                    count = 0
                    for part in polygons:
                        count += 1
                    print('Part Count:', count)

                out_feat.setAttributes([id, out_feat.geometry().area()])
                writer.addFeature(out_feat)
                print(out_feat.hasGeometry())
                lyr = self.iface.addVectorLayer(fn, 'normal', 'ogr')
                print('duration: ' + str(datetime.now() - start_time))
                output.close()
                part_file.close()

            def process_oblique():
                import math
                from qgis.core import QgsFields, QgsField, QgsVectorFileWriter, QgsWkbTypes, QgsCoordinateReferenceSystem,\
                    QgsFeature, QgsGeometry, QgsPointXY, QgsPoint
                from PyQt5.QtCore import QVariant

                from datetime import datetime

                start_time = datetime.now()

                K = float(self.dockwidget.lineEdit.text())
                fik = float(self.dockwidget.lineEdit_2.text())
                fi0 = float(self.dockwidget.lineEdit_3.text())
                lyambda0 = float(self.dockwidget.lineEdit_4.text())
                lyambdam = 100

                R = 6371116
                C = K + math.cos(fik * math.pi / 180)
                alpha = R * math.cos(fik * math.pi / 180)

                output = open(r'C:\Users\grita\Documents\MSU\test.txt', 'w')
                part_file = open(r'C:\Users\grita\Documents\MSU\part_file.txt', 'w')
                fn = self.dockwidget.mQgsFileWidget.filePath()

                layerFields = QgsFields()
                layerFields.append(QgsField('ID', QVariant.Int))
                layerFields.append(QgsField('AREA', QVariant.Double))
                writer = QgsVectorFileWriter(fn, 'UTF-8', layerFields, QgsWkbTypes.MultiPolygon, QgsCoordinateReferenceSystem('EPSG:3395'), 'ESRI Shapefile')

                layer = self.dockwidget.mMapLayerComboBox.currentLayer()
                out_feat = QgsFeature()
                out_feat_geom = out_feat.geometry()
                id = 1
                polygons = []
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    for part in geom.parts():
                        points = [] #КАЖДУЮ ЧАСТЬ СОЗДАЁМ СПИСОК ЕЁ ТОЧЕК
                        for pnt in part.vertices():

                            x = pnt.x()
                            y = pnt.y()

                            la = (x - lyambda0)
                            # расчёт условной широты
                            sin_fiusl = math.sin(fi0 * math.pi / 180) * math.sin(y * math.pi / 180) + math.cos(
                                fi0 * math.pi / 180) * math.cos(y * math.pi / 180) * math.cos(la * math.pi / 180)
                            fiusl = math.asin(sin_fiusl)
                            # расчёт условной долготы
                            if math.cos(fi0 * math.pi / 180) * math.sin(y * math.pi / 180) - math.sin(
                                    fi0 * math.pi / 180) * math.cos(y * math.pi / 180) * math.cos(
                                    la * math.pi / 180) == 0:
                                continue
                            sin = math.cos(y * math.pi / 180) * math.sin(la * math.pi / 180)
                            cos = math.cos(fi0 * math.pi / 180) * math.sin(y * math.pi / 180) - \
                                  (math.sin(fi0 * math.pi / 180) * math.cos(y * math.pi / 180) * math.cos(la * math.pi / 180))
                            az = math.atan2(sin, cos)
                            lyambdausl = -az
                            # пересчёт в косую ориентировку, прямоугольные координаты
                            x_new = alpha * lyambdausl
                            y_new = C * R * (math.sin(fiusl) / (K + math.cos(fiusl)))

                            output.write("{}, {}".format(x_new, y_new)+'\n')
                            points.append(QgsPointXY(x_new, y_new))

                        polygons.append(points)

                    out_feat.setGeometry(QgsGeometry.fromMultiPolygonXY([[part for part in polygons]]))

                    part_file.write('Part:\n' + str(out_feat.geometry()) + '\n\n')
                    count = 0
                    for part in polygons:
                        count+=1
                    print ('Part Count:', count)

                out_feat.setAttributes([id, out_feat.geometry().area()])
                writer.addFeature(out_feat)
                print (out_feat.hasGeometry())
                lyr = self.iface.addVectorLayer(fn, 'oblique', 'ogr')
                print('duration: '+ str(datetime.now() - start_time))
                output.close()
                part_file.close()

            def process_reverse_normal():
                import math
                from qgis.core import QgsFields, QgsField, QgsVectorFileWriter, QgsWkbTypes, \
                    QgsCoordinateReferenceSystem, \
                    QgsFeature, QgsGeometry, QgsPointXY, QgsPoint
                from PyQt5.QtCore import QVariant

                K = float(self.dockwidget.lineEdit.text())
                fik = float(self.dockwidget.lineEdit_2.text())
                lyambdam = 100

                R = 6371116
                C = K + math.cos(fik * math.pi / 180)
                alpha = R * math.cos(fik * math.pi / 180)

                output = open(r'C:\Users\grita\Documents\MSU\test.txt', 'w')
                part_file = open(r'C:\Users\grita\Documents\MSU\part_file.txt', 'w')
                fn = self.dockwidget.mQgsFileWidget.filePath()

                layerFields = QgsFields()
                layerFields.append(QgsField('ID', QVariant.Int))
                layerFields.append(QgsField('AREA', QVariant.Double))
                writer = QgsVectorFileWriter(fn, 'UTF-8', layerFields, QgsWkbTypes.MultiPolygon,
                                             QgsCoordinateReferenceSystem('EPSG:4326'), 'ESRI Shapefile')

                layer = self.dockwidget.mMapLayerComboBox.currentLayer()
                out_feat = QgsFeature()
                out_feat_geom = out_feat.geometry()
                id = 1
                polygons = []
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    for part in geom.parts():
                        points = []  # КАЖДУЮ ЧАСТЬ СОЗДАЁМ СПИСОК ЕЁ ТОЧЕК
                        for pnt in part.vertices():

                            x = pnt.x()
                            y = pnt.y()

                            if y == 0:
                                y_new = 0
                            elif y > 0:
                                D = -(K ** 2) + ((R ** 2) * (C ** 2) / y ** 2) + 1
                                y_new = (math.asin((((K * R * C) / y) + math.sqrt(D)) / (D + (K ** 2))) * 180 / math.pi)
                            elif y < 0:
                                D = -(K ** 2) + ((R ** 2) * (C ** 2) / y ** 2) + 1
                                y_new = (math.asin((((K * R * C) / y) - math.sqrt(D)) / (D + (K ** 2))) * 180 / math.pi)

                            x_new = ((x / alpha) * 180 / math.pi)

                            output.write("{}, {}".format(x_new, y_new) + '\n')
                            points.append(QgsPointXY(x_new, y_new))

                        polygons.append(points)

                    out_feat.setGeometry(QgsGeometry.fromMultiPolygonXY([[part for part in polygons]]))
                    part_file.write('Part:\n' + str(out_feat.geometry()) + '\n\n')
                    count = 0
                    for part in polygons:
                        count += 1
                    print('Part Count:', count)

                out_feat.setAttributes([id, out_feat.geometry().area()])
                writer.addFeature(out_feat)
                print(out_feat.hasGeometry())
                lyr = self.iface.addVectorLayer(fn, 'normal', 'ogr')
                output.close()
                part_file.close()

            def process_reverse_oblique():
                import math
                from qgis.core import QgsFields, QgsField, QgsVectorFileWriter, QgsWkbTypes, QgsCoordinateReferenceSystem,\
                    QgsFeature, QgsGeometry, QgsPointXY, QgsPoint
                from PyQt5.QtCore import QVariant

                K = float(self.dockwidget.lineEdit.text())
                fik = float(self.dockwidget.lineEdit_2.text())
                fi0 = float(self.dockwidget.lineEdit_3.text())
                lyambda0 = float(self.dockwidget.lineEdit_4.text())
                lyambdam = 100

                R = 6371116
                C = K + math.cos(fik * math.pi / 180)
                alpha = R * math.cos(fik * math.pi / 180)

                output = open(r'C:\Users\grita\Documents\MSU\test.txt', 'w')
                part_file = open(r'C:\Users\grita\Documents\MSU\part_file.txt', 'w')
                fn = self.dockwidget.mQgsFileWidget.filePath()

                layerFields = QgsFields()
                layerFields.append(QgsField('ID', QVariant.Int))
                layerFields.append(QgsField('AREA', QVariant.Double))
                writer = QgsVectorFileWriter(fn, 'UTF-8', layerFields, QgsWkbTypes.MultiPolygon, QgsCoordinateReferenceSystem('EPSG:4326'), 'ESRI Shapefile')

                layer = self.dockwidget.mMapLayerComboBox.currentLayer()
                out_feat = QgsFeature()
                out_feat_geom = out_feat.geometry()
                id = 1
                polygons = []
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    for part in geom.parts():
                        points = [] #КАЖДУЮ ЧАСТЬ СОЗДАЁМ СПИСОК ЕЁ ТОЧЕК
                        for pnt in part.vertices():

                            x = pnt.x()
                            y = pnt.y()

                            # вычисление географических полярных координат (условной широты и условной долготы)
                            if y == 0:
                                y_usl = 0
                            elif y > 0:
                                D = -(K ** 2) + ((R ** 2) * (C ** 2) / y ** 2) + 1
                                y_usl = (math.asin((((K * R * C) / y) + math.sqrt(D)) / (D + (K ** 2))) * 180 / math.pi)
                            elif y < 0:
                                D = -(K ** 2) + ((R ** 2) * (C ** 2) / y ** 2) + 1
                                y_usl = (math.asin((((K * R * C) / y) - math.sqrt(D)) / (D + (K ** 2))) * 180 / math.pi)

                            x_usl = (x / alpha) * 180 / math.pi

                            # переход к нормальной ориентировке
                            if y_usl == 90:
                                y_new = fi0
                                x_new = lyambda0

                            elif y_usl == -90:
                                y_new = -fi0
                                x_new = lyambda0 + 180

                            else:
                                sinfi = math.cos(y_usl * math.pi / 180) * math.cos(-x_usl * math.pi / 180) * math.cos(
                                    fi0 * math.pi / 180) + math.sin(fi0 * math.pi / 180) * math.sin(y_usl * math.pi / 180)
                                fi = math.asin(sinfi) * 180 / math.pi
                                sin = (math.cos(y_usl * math.pi / 180) * math.sin(-x_usl * math.pi / 180)) / (
                                    math.cos(fi * math.pi / 180))
                                cos = (math.sin(y_usl * math.pi / 180) - math.sin(fi * math.pi / 180) * math.sin(
                                    fi0 * math.pi / 180)) / (
                                                  math.cos(fi0 * math.pi / 180) * (math.cos(fi * math.pi / 180)))
                                la = math.atan2(sin, cos) * 180 / math.pi
                                x_new = la
                                y_new = fi
                                if x_new > 360:
                                    x_new = x - 360

                            output.write("{}, {}".format(x_new, y_new)+'\n')
                            points.append(QgsPointXY(x_new, y_new))

                        polygons.append(points)

                    out_feat.setGeometry(QgsGeometry.fromMultiPolygonXY([[part for part in polygons]]))
                    part_file.write('Part:\n' + str(out_feat.geometry()) + '\n\n')
                    count = 0
                    for part in polygons:
                        count+=1
                    print ('Part Count:', count)

                out_feat.setAttributes([id, out_feat.geometry().area()])
                writer.addFeature(out_feat)
                print (out_feat.hasGeometry())
                lyr = self.iface.addVectorLayer(fn, 'oblique', 'ogr')
                output.close()
                part_file.close()

            def disabling():
                self.dockwidget.lineEdit_3.setEnabled(False)
                self.dockwidget.lineEdit_4.setEnabled(False)
                if self.dockwidget.radioButton.isChecked() == True:
                    global a
                    a = 0

            def enabling():
                self.dockwidget.lineEdit_3.setEnabled(True)
                self.dockwidget.lineEdit_4.setEnabled(True)
                if self.dockwidget.radioButton_2.isChecked() == True:
                    global a
                    a = 1

            def forward_check():
                if self.dockwidget.radioButton_5.isChecked() == True:
                    global b
                    b = 0

            def backward_check():
                if self.dockwidget.radioButton_6.isChecked() == True:
                    global b
                    b = 1
                    print (b)

            def process():
                if a == 0 and b == 0:
                    print('forward normal')
                    process_normal()

                if a == 1 and b == 0:
                    print('forward oblique')
                    process_oblique()

                if a == 0 and b == 1:
                    print('backward normal')
                    process_reverse_normal()

                if a == 1 and b == 1:
                    print('backward oblique')
                    process_reverse_oblique()

            self.dockwidget.radioButton.toggled.connect(disabling)
            self.dockwidget.radioButton_2.toggled.connect(enabling)

            self.dockwidget.radioButton_5.toggled.connect(forward_check)
            self.dockwidget.radioButton_6.toggled.connect(backward_check)

            self.dockwidget.pushButton.clicked.connect(process)


