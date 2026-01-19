# ConstructionPlaneInput.creationOccurrence Property

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the ConstructionPlane is created based on geometry (e.g. a planarEntity) in another component AND (the ConstructionPlane) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"constructionPlaneInput_var" is a variable referencing a ConstructionPlaneInput object.  

```python
# Get the value of the property.
propertyValue = constructionPlaneInput_var.creationOccurrence

# Set the value of the property.
constructionPlaneInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version August 2014  

