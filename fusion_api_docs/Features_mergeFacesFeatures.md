# Features.mergeFacesFeatures Property

Parent Object: [Features](Features.md)  

## Description

Returns the collection object that supports the ability to merge faces. Merging faces is currently limited to a Direct Modeling design or a body in a base feature. The result of merging faces is a direct B-Rep modification, and the change is not represented as a feature in the browser.

## Syntax

"features_var" is a variable referencing a Features object.  

```python
# Get the value of the property.
propertyValue = features_var.mergeFacesFeatures
```

## Property Value

This is a read only property whose value is a [MergeFacesFeatures](MergeFacesFeatures.md).

## Version

Introduced in version September 2024  

