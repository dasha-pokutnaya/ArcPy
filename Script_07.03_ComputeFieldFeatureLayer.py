"""
THIS SCRIPT COMPUTES THE SUM OF ALL VALUES IN A SPECIFIED FIELD A SPECIFIED FEATURE LAYER

To create an ArcToolbox tool with which to execute this script, do the following.
1   In  ArcMap > Catalog > Toolboxes > My Toolboxes, either select an existing toolbox
    or right-click on My Toolboxes and use New > Toolbox to create (then rename) a new one.
2   Drag (or use ArcToolbox > Add Toolbox to add) this toolbox to ArcToolbox.
3   Right-click on the toolbox in ArcToolbox, and use Add > Script to open a dialog box.
4   In this Add Script dialog box, use Label to name the tool being created, and press Next.
5   In a new dialog box, browse to the .py file to be invoked by this tool, and press Next.
6   In the next dialog box, specify the following inputS (using dropdown menus wherever possible)
    before pressing OK or Finish.
        DISPLAY NAME        	DATA TYPE           PROPERTY>DIRECTION>VALUE    
        Input Feature Layer?    Table View 	    Input
        Output Feature Layer?   Feature Layer	    Output
        Input Field?        	Field               Input
        Output Field?       	Field               Input
7   To later revise any of this, right-click to the tool's name and select Properties.
"""
   
# Import necessary modules
import sys, os, string, math, arcpy, traceback

# Allow output file to overwrite any existing file of the same name
arcpy.env.overwriteOutput = True

try:
    
    # Request user input of data type = Feature Layer and direction = Input
    nameOfInputFeatureLayer = arcpy.GetParameterAsText(0)
    arcpy.AddMessage('\n' + "The input shapefile name is " + nameOfInputFeatureLayer)

    # Request user input of data type = Feature Layer and direction = Output
    nameOfOutputFeatureLayer = arcpy.GetParameterAsText(1)
    arcpy.AddMessage("The output shapefile name is " + nameOfOutputFeatureLayer)

    # Request user input of data type = String and direction = Input
    nameOfInputField = arcpy.GetParameterAsText(2)
    arcpy.AddMessage("The name of the field to be summarized is " + nameOfInputField + "\n")

    # Request user input of data type = String and direction = Input
    nameOfOutputField = arcpy.GetParameterAsText(3)
    arcpy.AddMessage("The name of the field to hold summary is " + nameOfOutputField + "\n")

    # Replicate the input feature layer and add a new field to the replica
    arcpy.CopyFeatures_management(nameOfInputFeatureLayer, nameOfOutputFeatureLayer)
    arcpy.AddField_management(nameOfOutputFeatureLayer, nameOfOutputField, "DOUBLE", 30, 5)

    # Create an enumeration of updatable records from the feature layer's attribute table
    enumerationOfRecords = arcpy.UpdateCursor(nameOfOutputFeatureLayer)

    accumulationSoFar = 0
    
    # Loop through that enumeration, calculating each record's convexity
    for nextRecord in enumerationOfRecords:
        # Retrieve a value from the next record's input field
        nextValue   = nextRecord.getValue(nameOfInputField)
        # Add that value to the current accumulation of such values
        accumulationSoFar = accumulationSoFar + nextValue
        arcpy.AddMessage("The value " + str(nextValue) + " brings the accumulation to " + str(accumulationSoFar) )

    # Loop through the enumeration again, recording the final accumulation in each record
    arcpy.AddMessage("\n")
    enumerationOfRecords = arcpy.UpdateCursor(nameOfOutputFeatureLayer)
    for nextRecord in enumerationOfRecords:
        arcpy.AddMessage("Setting the next record's " + nameOfOutputField + " value to " + str(accumulationSoFar) )
        nextRecord.setValue(nameOfOutputField,accumulationSoFar)
        enumerationOfRecords.updateRow(nextRecord)
    
    # Delete row and update cursor objects to avoid locking attribute table
    arcpy.AddMessage("\n")
    del nextRecord
    del enumerationOfRecords
    
except Exception as e:
    # If unsuccessful, end gracefully by indicating why
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    # ... and where
    exceptionreport = sys.exc_info()[2]
    fullermessage   = traceback.format_tb(exceptionreport)[0]
    arcpy.AddError("at this location: \n\n" + fullermessage + "\n")
