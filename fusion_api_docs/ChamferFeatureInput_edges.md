# ChamferFeatureInput.edges Property

Parent Object: [ChamferFeatureInput](ChamferFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the collection of edges that will be chamfered.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"chamferFeatureInput_var" is a variable referencing a ChamferFeatureInput object.  

```python
# Get the value of the property.
propertyValue = chamferFeatureInput_var.edges

# Set the value of the property.
chamferFeatureInput_var.edges = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2014  
Retired in version December 2020  

