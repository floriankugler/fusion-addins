# ScalarGraphNodeProperty.isValid Property

Parent Object: [ScalarGraphNodeProperty](ScalarGraphNodeProperty.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference.

## Syntax

"scalarGraphNodeProperty_var" is a variable referencing a ScalarGraphNodeProperty object.  

```python
# Get the value of the property.
propertyValue = scalarGraphNodeProperty_var.isValid
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version May 2025  

