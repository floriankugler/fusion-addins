# ModelParameter Object

Derived from: [Parameter](Parameter.md) Object  

## Description

Represents a Model Parameter.

## Methods

| Name | Description |
|----|----|
| [classType](ModelParameter_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ModelParameter_deleteMe.md) | Deletes this ModelParameter. As a general rule, model parameters cannot be deleted because features depend on them. However, there are uncommon workflows where a parameter no longer has any dependents and is not automatically deleted. You can use the isDeletable property to see if the parameter is in this state and can successfully be deleted. |

## Properties

| Name | Description |
| --- | --- |
| [attributes](ModelParameter_attributes.md) | Returns the collection of attributes associated with this face. |
| [comment](ModelParameter_comment.md) | The comment associated with this parameter |
| [component](ModelParameter_component.md) | Returns the Component containing the ModelParameter. |
| [createdBy](ModelParameter_createdBy.md) | Returns the object that created this parameter. For example, a feature, a sketch dimension, or a construction plane. |
| [dependencyParameters](ModelParameter_dependencyParameters.md) | Returns a list of parameters that this parameter is dependent on. |
| [dependentParameters](ModelParameter_dependentParameters.md) | Returns a list of parameters that are dependent on this parameter as a result of this parameter being referenced in their equation. |
| [entityToken](ModelParameter_entityToken.md) | Returns a token for the Parameter object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same parameter. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [expression](ModelParameter_expression.md) | Gets and sets the expression used to calculate the value of the parameter. This is the equivalent of the "Expression" column in the Parameters dialog. Numeric parameters can be defined by a simple expression like "6.25", which will be interpreted based on whatever the default units are for the document. For example, if the units are set to millimeters, the value will be 6.25 mm; if the units are inches, it will be 6.25 inches. The expression can also contain the units so "6.25 in" will always be evaluated as inches regardless of the document units. An expression can also contain references to other parameters and use equations. For example, the expression "Length / 2" is valid for a numeric parameter as long as there is a numeric parameter named "Length". Expressions can also be used for text parameters, such as concatenating two other text parameters. For example, if there are two existing text parameters named text1 and text2, the expression for another text parameter can be "text1 + text2". More complex equations can also be used with text parameters like "if (Length 
