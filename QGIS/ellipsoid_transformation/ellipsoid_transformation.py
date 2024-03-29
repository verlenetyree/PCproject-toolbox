# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EllipsoidTransformation
                                 A QGIS plugin
 This plugin produce a transfaormation to an ellipsoid and vice versa
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-04-19
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
from .ellipsoid_transformation_dockwidget import EllipsoidTransformationDockWidget
import os.path


class EllipsoidTransformation:
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
            'EllipsoidTransformation_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Ellipsoid Transformation')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'EllipsoidTransformation')
        self.toolbar.setObjectName(u'EllipsoidTransformation')

        #print "** INITIALIZING EllipsoidTransformation"

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
        return QCoreApplication.translate('EllipsoidTransformation', message)


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

        icon_path = ':/plugins/ellipsoid_transformation/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Ellipsoid Transformation'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING EllipsoidTransformation"

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

        #print "** UNLOAD EllipsoidTransformation"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Ellipsoid Transformation'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING EllipsoidTransformation"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = EllipsoidTransformationDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

            def to_ellipsoid():
                import math
                from qgis.core import QgsFields, QgsField, QgsVectorFileWriter, QgsWkbTypes, \
                    QgsCoordinateReferenceSystem, \
                    QgsFeature, QgsGeometry, QgsPointXY, QgsPoint
                from PyQt5.QtCore import QVariant

                a = float(self.dockwidget.lineEdit.text())
                b = float(self.dockwidget.lineEdit_2.text())

                e = math.sqrt(1 - ((b ** 2) / (a ** 2)))

                #output = open(r'C:\Users\grita\Documents\MSU\test.txt', 'w')
                #part_file = open(r'C:\Users\grita\Documents\MSU\part_file.txt', 'w')
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

                            if y == -90 or y == 90 or y == 0:
                                continue
                            if -90 < y < 0 or 0 < y < 90:
                                y = y + ((((e ** 2) / 3) + ((31 * (e ** 4)) / 180) + (
                                            (517 * e ** 6) / 5040)) * math.sin(2 * y * math.pi / 180)) + (
                                                (((23 * e ** 4) / 360) + ((251 * e ** 6) / 3780)) * math.sin(
                                            4 * y * math.pi / 180)) + (
                                                ((761 * e ** 6) / 45360) * math.sin(6 * y * math.pi / 180))

                            #output.write("{}, {}".format(x_new, y_new) + '\n')
                            points.append(QgsPointXY(x, y))

                        polygons.append(points)
                    out_feat.setGeometry(QgsGeometry.fromMultiPolygonXY([[part for part in polygons]]))
                    #part_file.write('Part:\n' + str(out_feat.geometry()) + '\n\n')
                    count = 0
                    for part in polygons:
                        count += 1
                    print('Part Count:', count)

                out_feat.setAttributes([id, out_feat.geometry().area()])
                writer.addFeature(out_feat)
                print(out_feat.hasGeometry())
                lyr = self.iface.addVectorLayer(fn, 'ellipsoid', 'ogr')
                #output.close()
                #part_file.close()

            def to_sphere():
                import math
                from qgis.core import QgsFields, QgsField, QgsVectorFileWriter, QgsWkbTypes, \
                    QgsCoordinateReferenceSystem, \
                    QgsFeature, QgsGeometry, QgsPointXY, QgsPoint
                from PyQt5.QtCore import QVariant

                a = float(self.dockwidget.lineEdit.text())
                b = float(self.dockwidget.lineEdit_2.text())

                e = math.sqrt(1 - ((b ** 2) / (a ** 2)))

                #output = open(r'C:\Users\grita\Documents\MSU\test.txt', 'w')
                #part_file = open(r'C:\Users\grita\Documents\MSU\part_file.txt', 'w')
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

                            if y == -90 or y == 90 or y == 0:
                                continue
                            if -90 < y < 0 or 0 < y < 90:
                                q = (1 - e ** 2) * ((math.sin(y * math.pi / 180) / (
                                        1 - (e ** 2) * math.sin(y * math.pi / 180) ** 2)) - ((1 / (2 * e)) * math.log(
                                    (1 - e * math.sin(y * math.pi / 180)) / (1 + e * math.sin(y * math.pi / 180)))))
                                qp = 1 - (((1 - e ** 2) / (2 * e)) * math.log((1 - e) / (1 + e)))
                                # Rq = a * math.sqrt(qp / 2)
                                y = math.asin((q / qp)) * 180 / math.pi

                            #output.write("{}, {}".format(x_new, y_new) + '\n')
                            points.append(QgsPointXY(x, y))

                        polygons.append(points)

                    out_feat.setGeometry(QgsGeometry.fromMultiPolygonXY([[part for part in polygons]]))
                    #part_file.write('Part:\n' + str(out_feat.geometry()) + '\n\n')
                    count = 0
                    for part in polygons:
                        count += 1
                    print('Part Count:', count)

                out_feat.setAttributes([id, out_feat.geometry().area()])
                writer.addFeature(out_feat)
                print(out_feat.hasGeometry())
                lyr = self.iface.addVectorLayer(fn, 'sphere', 'ogr')
                #output.close()
                #part_file.close()

            self.dockwidget.pushButton.clicked.connect(to_ellipsoid)
            self.dockwidget.pushButton_2.clicked.connect(to_sphere)
