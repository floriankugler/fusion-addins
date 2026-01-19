# Features.meshShellFeatures Property

Parent Object: [Features](Features.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the collection that provides access to the mesh shell features within the component and supports the creation of new mesh shell features.

## Syntax

"features_var" is a variable referencing a Features object.  

```python
# Get the value of the property.
propertyValue = features_var.meshShellFeatures
```

## Property Value

This is a read only property whose value is a [MeshShellFeatures](MeshShellFeatures.md).

## Version

Introduced in version March 2024  

