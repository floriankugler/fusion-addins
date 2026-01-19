# OperationStrategy Object

Derived from: [Base](Base.md) Object  

## Description

The OperationStrategy contains information about a strategy such as its name, title and description.

## Methods

| Name | Description |
|----|----|
| [classType](OperationStrategy_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFromString](OperationStrategy_createFromString.md) | Create an OperationStrategy for a given name. |

## Properties

| Name | Description |
| --- | --- |
| [description](OperationStrategy_description.md) | Get the localized description of the strategy. |
| [is2DStrategy](OperationStrategy_is2DStrategy.md) | Gets whether given OperationStrategy is a 2D strategy. |
| [is3DStrategy](OperationStrategy_is3DStrategy.md) | Gets whether given OperationStrategy is a 3D strategy. |
| [isAdditiveStrategy](OperationStrategy_isAdditiveStrategy.md) | Gets whether given OperationStrategy is an additive strategy. |
| [isCuttingStrategy](OperationStrategy_isCuttingStrategy.md) | Gets whether given OperationStrategy is a cutting strategy. |
| [isDrillingStrategy](OperationStrategy_isDrillingStrategy.md) | Gets whether given OperationStrategy is a drilling strategy. |
| [isFinishingStrategy](OperationStrategy_isFinishingStrategy.md) | Gets whether given OperationStrategy is a finishing strategy. |
| [isGenerationAllowed](OperationStrategy_isGenerationAllowed.md) | Returns true if the strategy is allowed to be generated due to licensing and enabled preview features. Some strategies also require Active machining extension to be generated. Returns false otherwise. |
| [isMillingStrategy](OperationStrategy_isMillingStrategy.md) | Gets whether given OperationStrategy is a milling strategy. |
| [isRotaryStrategy](OperationStrategy_isRotaryStrategy.md) | Gets whether given OperationStrategy is a rotary strategy. |
| [isSupportStrategy](OperationStrategy_isSupportStrategy.md) | Gets whether given OperationStrategy is an additive support strategy. |
| [isTurningStrategy](OperationStrategy_isTurningStrategy.md) | Gets whether given OperationStrategy is a turning strategy. |
| [isValid](OperationStrategy_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](OperationStrategy_name.md) | Get the name of the strategy. This is equivalent to the Operation's strategy property. Use as strategy parameter when creating a OperationInput. |
| [objectType](OperationStrategy_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [title](OperationStrategy_title.md) | Get the localized title of the strategy. |

## Accessed From

[Operations.compatibleStrategies](Operations_compatibleStrategies.md), [OperationStrategy.createFromString](OperationStrategy_createFromString.md)

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

