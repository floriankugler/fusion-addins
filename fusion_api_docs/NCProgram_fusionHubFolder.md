# NCProgram.fusionHubFolder Property

Parent Object: [NCProgram](NCProgram.md)  

## Description

Gets and sets the DataFolder to which the exported files should be uploaded to if the parameter nc_program_postToFusionTeam is set to true. When a DataFolder is set, nc_program_postToFusionTeam is automatically set to true. An exception will be thrown if the DataFolder to set is not valid or not accessible. Depending on the FusionHubExecutionBehaviors used for the export the design may be saved at this location as well.

## Syntax

"nCProgram_var" is a variable referencing a NCProgram object.  

```python
# Get the value of the property.
propertyValue = nCProgram_var.fusionHubFolder

# Set the value of the property.
nCProgram_var.fusionHubFolder = propertyValue
```

## Property Value

This is a read/write property whose value is a [DataFolder](DataFolder.md).

## Version

Introduced in version July 2024  

