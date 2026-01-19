# WorkingModel.designIntent Property

Parent Object: [WorkingModel](WorkingModel.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the use intent of this design. Changing the design intent from one type to another is not supported in all cases. For example, if an assembly contains any external or internal components it cannot be converted to a part.

## Syntax

"workingModel_var" is a variable referencing a WorkingModel object.  

```python
# Get the value of the property.
propertyValue = workingModel_var.designIntent

# Set the value of the property.
workingModel_var.designIntent = propertyValue
```

## Property Value

This is a read/write property whose value is a [DesignIntentTypes](DesignIntentTypes.md).

## Version

Introduced in version January 2026  

