import arcpy
import math
import os
from datetime import datetime

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [proj_kosaya_upd, proj_reverse_kosaya]


class proj_kosaya_upd(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "proj_kosaya_upd"
        self.description = "Perspective-cylindrical projections"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

        in_layer = arcpy.Parameter(
            displayName="Input Layer",
            name="in_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        K = arcpy.Parameter(
            displayName="K",
            name="K",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        K.value = 1

        fik = arcpy.Parameter(
            displayName="fik",
            name="fik",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        fik.value = 45

        fi0 = arcpy.Parameter(
            displayName="fi0",
            name="fi0",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        fi0.value = 75

        lyambda0 = arcpy.Parameter(
            displayName="lyambda0",
            name="lyambda0",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")

        lyambda0.value = -80

        out_layer = arcpy.Parameter(
            displayName="Output Layer",
            name="out_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output")

        params = [in_layer, K, fik, fi0, lyambda0, out_layer]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        start_time = datetime.now()

        in_layer = parameters[0].valueAsText
        K = float(parameters[1].valueAsText)
        fik = float(parameters[2].valueAsText)
        fi0 = float(parameters[3].valueAsText)
        lyambda0 = float(parameters[4].valueAsText)
        out_layer = parameters[5].valueAsText

        arcpy.AddMessage('Input layer: ' + in_layer)
        arcpy.AddMessage('K: ' + str(K))
        arcpy.AddMessage('fik: ' + str(fik))
        arcpy.AddMessage('fi0: ' + str(fi0))
        arcpy.AddMessage('lyambda0: ' + str(lyambda0))

        R=6371116
        C=K+math.cos(fik*math.pi/180)
        alpha=R*math.cos(fik*math.pi/180)

        desc = arcpy.Describe(in_layer)
        shapefieldname = desc.ShapeFieldName
        rows = arcpy.UpdateCursor(in_layer, ["OID@", "SHAPE@"])
        #feature_tab_xy=open('kosaya_points_XY_upd.txt','w')
        workspace = os.path.dirname(out_layer)
        name = os.path.basename(out_layer)
        arcpy.CreateFeatureclass_management(workspace, name, "POLYGON", spatial_reference=3395)
        cursor = arcpy.da.InsertCursor(out_layer, "SHAPE@")

        for row in rows:
            feat = row.getValue(shapefieldname)
            #feature_tab_xy.write("Feature {}:".format(row)+'\n')
            arr_feat = arcpy.Array()
            partnum = 0
            for part in feat:
                arr_part = arcpy.Array()
                #feature_tab_xy.write("Part {}:".format(partnum)+'\n')
                for pnt in feat.getPart(partnum):
                    if pnt:
                        x = pnt.X
                        y = pnt.Y

                        la=(x-lyambda0)
                        #расчёт условной широты
                        sin_fiusl=math.sin(fi0*math.pi/180)*math.sin(y*math.pi/180)+math.cos(fi0*math.pi/180)*math.cos(y*math.pi/180)*math.cos(la*math.pi/180)
                        fiusl=math.asin(sin_fiusl)
                        #расчёт условной долготы
                        if math.cos(fi0*math.pi/180)*math.sin(y*math.pi/180)-math.sin(fi0*math.pi/180)*math.cos(y*math.pi/180)*math.cos(la*math.pi/180)==0:
                           continue
                        sin=math.cos(y*math.pi/180)*math.sin(la*math.pi/180)
                        cos=math.cos(fi0*math.pi/180)*math.sin(y*math.pi/180)-(math.sin(fi0*math.pi/180)*math.cos(y*math.pi/180)*math.cos(la*math.pi/180))
                        az=math.atan2(sin, cos)
                        lyambdausl=-az
                        #пересчёт в косую ориентировку, прямоугольные координаты
                        x = alpha*lyambdausl
                        y = C*R*(math.sin(fiusl)/(K+math.cos(fiusl)))
                        #feature_tab_xy.write("{}, {}".format(x, y)+'\n')
                        arr_part.add(arcpy.Point(x, y))
                    else:
                         pass
                arr_feat.add(arr_part)
                partnum += 1
            polygon = arcpy.Polygon(arr_feat)
            cursor.insertRow([polygon])
            arcpy.RecalculateFeatureClassExtent_management(out_layer)
            rows.updateRow(row)
            arcpy.AddMessage('duration: '+ str(datetime.now() - start_time))
        #feature_tab_xy.close()

        return

class proj_reverse_kosaya(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "proj_reverse_kosaya"
        self.description = "Perspective-cylindric projection"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

        in_layer = arcpy.Parameter(
            displayName="Input Layer",
            name="in_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        K = arcpy.Parameter(
            displayName="K",
            name="K",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        K.value = 1

        fik = arcpy.Parameter(
            displayName="fik",
            name="fik",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")

        fik.value = 45

        fi0 = arcpy.Parameter(
            displayName="fi0",
            name="fi0",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")

        fi0.value = 75

        lyambda0 = arcpy.Parameter(
            displayName="lyambda0",
            name="lyambda0",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")

        lyambda0.value = -80

        out_layer = arcpy.Parameter(
            displayName="Output Layer",
            name="out_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output")

        params = [in_layer, K, fik, fi0, lyambda0, out_layer]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        in_layer = parameters[0].valueAsText
        K = float(parameters[1].valueAsText)
        fik = float(parameters[2].valueAsText)
        fi0 = float(parameters[3].valueAsText)
        lyambda0 = float(parameters[4].valueAsText)
        out_layer = parameters[5].valueAsText


        arcpy.AddMessage('Input layer: ' + in_layer)
        arcpy.AddMessage('K: ' + str(K))
        arcpy.AddMessage('fik: ' + str(fik))
        arcpy.AddMessage('fi0: ' + str(fi0))
        arcpy.AddMessage('lyambda0: ' + str(lyambda0))

        R=6371116
        C=K+math.cos(fik*math.pi/180)
        alpha=R*math.cos(fik*math.pi/180)


        desc = arcpy.Describe(in_layer)
        shapefieldname = desc.ShapeFieldName
        #oidfieldname= desc.OIDFieldName


        rows = arcpy.UpdateCursor(in_layer, ["OID@", "SHAPE@"])
        #rows = arcpy.UpdateCursor(in_layer, [oidfieldname, shapefieldname])
        #rows = arcpy.UpdateCursor(in_layer, where_clause=where)

        feature_tab_xy=open('feature_points_XY_upd.txt','w')
        #end_class=r'C:\Users\grita\Documents\MSU\3lvl\shape'

        workspace = os.path.dirname(out_layer)
        name = os.path.basename(out_layer)

        arcpy.CreateFeatureclass_management(workspace, name, "POLYGON", spatial_reference=4326)

        cursor = arcpy.da.InsertCursor(out_layer, "SHAPE@")

        for row in rows:
            feat = row.getValue(shapefieldname)
            feature_tab_xy.write("Feature {}:".format(row)+'\n')
            arr_feat = arcpy.Array()
            partnum = 0
            for part in feat:
                arr_part = arcpy.Array()
                feature_tab_xy.write("Part {}:".format(partnum)+'\n')
                for pnt in feat.getPart(partnum):
                    if pnt:
                        x = pnt.X
                        y = pnt.Y

                        if y==0:
                            y=0
                        elif y>0:
                            D=-(K**2)+((R**2)*(C**2)/y**2)+1
                            y=(math.asin((((K*R*C)/y)+math.sqrt(D))/(D+(K**2)))*180/math.pi)
                        elif y<0:
                            D=-(K**2)+((R**2)*(C**2)/y**2)+1
                            y=(math.asin((((K*R*C)/y)-math.sqrt(D))/(D+(K**2)))*180/math.pi)

                        x=(x/alpha)*180/math.pi

                        if y==90:
                            y=fi0
                            x=lyambda0

                        elif y==-90:
                            y=-fi0
                            x=lyambda0+180

                        else:
                            sinfi=math.cos(y*math.pi/180)*math.cos(-x*math.pi/180)*math.cos(fi0*math.pi/180)+math.sin(fi0*math.pi/180)*math.sin(y*math.pi/180)
                            fi=math.asin(sinfi)*180/math.pi
                            sin=(math.cos(y*math.pi/180)*math.sin(-x*math.pi/180))/(math.cos(fi*math.pi/180))
                            cos=(math.sin(y*math.pi/180)-math.sin(fi*math.pi/180)*math.sin(fi0*math.pi/180))/(math.cos(fi0*math.pi/180)*(math.cos(fi*math.pi/180)))
                            la=math.atan2(sin,cos)*180/math.pi
                            x=la
                            y=fi
                            if x > 360:
                                x=x-360

                        feature_tab_xy.write("{}, {}".format(x, y)+'\n')
                        arr_part.add(arcpy.Point(x, y))
                    else:
                         pass
                arr_feat.add(arr_part)
                partnum += 1
            polygon = arcpy.Polygon(arr_feat)
            cursor.insertRow([polygon])
            arcpy.RecalculateFeatureClassExtent_management(out_layer)


            #arcpy.FeatureClassToShapefile_conversion(polygon, r'C:\Users\grita\Documents\MSU\3lvl\shape')

            #fl=arcpy.MakeFeatureLayer_management(polygon, r'C:\Users\grita\Documents\MSU\3lvl\shape')
            #u=arcpy.Union_analysis(fl, end_class)'''
            #arcpy.FeatureClassToShapefile_conversion(end_class, r'C:\Users\grita\Documents\MSU\3lvl\shape')

            #row.setValue(in_layer(["SHAPE@"]), "Polygon")
            rows.updateRow(row)

        #arcpy.FeatureClassToShapefile_conversion(out_layer, r'C:\Users\grita\Documents\MSU\3lvl\shape')
        feature_tab_xy.close()

        return
