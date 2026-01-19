# Sketch.isComputeDeferred Property

Parent Object: [Sketch](Sketch.md)  

## Description

This property temporarily turns off sketch computing. It is used to increase the performance as sketch geometry is created and modified. Once the sketch is drawn, this property should be set to false to allow the sketch to recompute. The file does not save this setting and is always false when a file is opened.  

There is a side-effect when using this property that can result in the creation of a bad model. This is only a problem when editing an existing sketch used by one or more features. When the sketch is edited with the isComputeDeferred property set to true, the compute of the profiles can sometimes create weird results in the dependent features. There are two easy ways to solve this problem. The first is not to defer the sketch compute. The second is to roll the timeline back to just after the sketch, make whatever changes you want to the sketch with the compute deferred, and then roll the timeline back to its original location. This process mimics the behavior you see in the user interface when you manually edit a sketch where Fusion automatically rolls the timeline back while you're editing the sketch.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.isComputeDeferred

# Set the value of the property.
sketch_var.isComputeDeferred = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

