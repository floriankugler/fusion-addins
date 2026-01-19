# WorkingModel.isModelingInAssemblyEnabled Property

Parent Object: [WorkingModel](WorkingModel.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

If this design is an assembly, this property gets and sets if the modeling functionality is enabled. If this design is a part or hybrid design, the value of this property should be ignored.

## Syntax

"workingModel_var" is a variable referencing a WorkingModel object.  

```python
# Get the value of the property.
propertyValue = workingModel_var.isModelingInAssemblyEnabled

# Set the value of the property.
workingModel_var.isModelingInAssemblyEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2026  

