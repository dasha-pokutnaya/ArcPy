"""
THIS SCRIPT JOINS THE ATTRIBUTE TABLE OF ONE FEATURE LAYER TO THAT OF ANOTHER
AND SAVES THE RESULT AS A NEW SHAPEFILE

To create an ArcToolbox tool with which to execute this script, do the following.
1   In  ArcMap > Catalog > Toolboxes > My Toolboxes, either select an existing toolbox
    or right-click on My Toolboxes and use New > Toolbox to create (then rename) a new one.
2   Drag (or use ArcToolbox > Add Toolbox to add) this toolbox to ArcToolbox.
3   Right-click on the toolbox in ArcToolbox, and use Add > Script to open a dialog box.
4   In this Add Script dialog box, use Label to name the tool being created, and press Next.
5   In a new dialog box, browse to the .py file to be invoked by this tool, and press Next.
6   In the next dialog box, specify the following inputs (using dropdown menus wherever possible)
    before pressing OK or Finish.
        DISPLAY NAME            DATA TYPE           PROPERTY>DIRECTION>VALUE    PROPERTY>OBTAINEDFROM>VALUE   
        Left Feature Layer?     Feature Layer       Input
        Right Feature Layer?    Feature Layer       Input
        Left Field?             Field               Input                       Left Feature Layer?
        Right Field?            Field               Input                       Right Feature Layer?
        Output Shapefile?       Shapefile           Output
7   To later revise any of this, right-click to the tool's name and select Properties.
"""
   
# Import necessary modules
import sys, os, string, math, arcpy, traceback

# Allow output file to overwrite any existing file of the same name
arcpy.env.overwriteOutput = True

try:
    
    # Request user inputs of data type = Feature Layer and direction = Input
    nameOfLeftLayer     = arcpy.GetParameterAsText(0)
    nameOfRightLayer    = arcpy.GetParameterAsText(1)
    # Request user inputs of data type = Field, direction = Input, and ObtaineFrom the layers above
    nameOfLeftField     = arcpy.GetParameterAsText(2)
    nameOfRightField    = arcpy.GetParameterAsText(3)
    arcpy.AddMessage('\n' + nameOfRightLayer + " is to be joined to the right of " + nameOfLeftLayer)
    arcpy.AddMessage('\nby matching its ' + nameOfRightField + " values to the values in " + nameOfLeftField)
    # Request user input of data type = Shapefile and direction = Output
    nameOfOutputShapefile = arcpy.GetParameterAsText(4)
    arcpy.AddMessage("The output shapefile name is " + nameOfOutputShapefile)    

    # Create a feature layer from the vegtype featureclass
    arcpy.MakeFeatureLayer_management (nameOfLeftLayer,"leftLayer")
    
    # Join the feature layer to a table
    arcpy.AddJoin_management("leftLayer", nameOfLeftField, nameOfRightLayer, nameOfRightField,'KEEP_COMMON')
        
    # Copy the layer to a new permanent feature class
    arcpy.CopyFeatures_management("leftLayer", nameOfOutputShapefile)

except Exception as e:
    # If unsuccessful, end gracefully by indicating why
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    # ... and where
    exceptionreport = sys.exc_info()[2]
    fullermessage   = traceback.format_tb(exceptionreport)[0]
    arcpy.AddError("at this location: \n\n" + fullermessage + "\n")
