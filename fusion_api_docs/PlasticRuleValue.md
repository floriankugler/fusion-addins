# PlasticRuleValue Object

Derived from: [Base](Base.md) Object  

## Description

Used to get and set the current value associated with a plastic rule. A value can be gotten or set using a string or a double. A string can contain equations and unit specifiers, whereas a double defines the size in centimeters. In the user interface, the user is always setting the string expression. However, when programming, it is typically more convenient to set it using an explicit value. When the value is set using a double, Fusion creates an equivalent expression.

## Methods

| Name | Description |
|----|----|
| [classType](PlasticRuleValue_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [expression](PlasticRuleValue_expression.md) | Gets and sets the expression of the plastic rule value. This can be an equation that includes the name "Thickness" and can also include length unit specifiers. For example, a valid expression is "Thickness / 2 + 1 mm". If no units are specified, the unit is implied and uses the units associated with the rule which can be mm or inch. For example an expression of "3" will be 3 inches if the rule units are inches or 3 mm if the rule units are millimeters. You can find out what units are used for a rule using the PlasticRule.units property. |
| [isValid](PlasticRuleValue_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PlasticRuleValue_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [value](PlasticRuleValue_value.md) | Gets and sets the value of the plastic rule value in centimeters. Setting this value will create a new expression that is equivalent to the new value. |

## Accessed From

[PlasticRule.clearance](PlasticRule_clearance.md), [PlasticRule.draftAngle](PlasticRule_draftAngle.md), [PlasticRule.knifeEdgeThreshold](PlasticRule_knifeEdgeThreshold.md), [PlasticRule.nominalRadius](PlasticRule_nominalRadius.md), [PlasticRule.revealHeight](PlasticRule_revealHeight.md), [PlasticRule.thickness](PlasticRule_thickness.md), [PlasticRule.thicknessVariation](PlasticRule_thicknessVariation.md)

## Version

Introduced in version January 2024  

