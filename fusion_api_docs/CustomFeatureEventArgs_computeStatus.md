# CustomFeatureEventArgs.computeStatus Property

Parent Object: [CustomFeatureEventArgs](CustomFeatureEventArgs.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Provides access to the Status object associated with this compute. If the compute is successful you shouldn't do anything with this property. If the compute is not fully successful, you can use this returned Status object to define any errors or warnings that occurred during the compute. These warnings and errors will be shown to the user in the Alerts dialog.

## Syntax

"customFeatureEventArgs_var" is a variable referencing a CustomFeatureEventArgs object.  

```python
# Get the value of the property.
propertyValue = customFeatureEventArgs_var.computeStatus
```

## Property Value

This is a read only property whose value is a [Status](Status.md).

## Version

Introduced in version July 2021  

