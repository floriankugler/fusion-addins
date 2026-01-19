# BRepEdge Object

Derived from: [Base](Base.md) Object  

## Description

Represents a one-dimensional topological element that can be used to bound a BRepFace A BRepEdge uses a single, connected and bounded subset of a curve for it geometry.

## Methods

| Name | Description |
|----|----|
| [classType](BRepEdge_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](BRepEdge_createForAssemblyContext.md) | Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](BRepEdge_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this BRepEdge object is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly. but is already the native object. |
| [attributes](BRepEdge_attributes.md) | Returns the collection of attributes associated with this face. |
| [body](BRepEdge_body.md) | Returns the parent body of the edge. |
| [boundingBox](BRepEdge_boundingBox.md) | Returns the bounding box of this edge. |
| [coEdges](BRepEdge_coEdges.md) | Returns the BRepCoEdges on the edge. |
| [endVertex](BRepEdge_endVertex.md) | Returns the BRepVertex that bounds its high parameter end. |
| [entityToken](BRepEdge_entityToken.md) | Returns a token for the BRepEdge object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same edge. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. This is only valid for edges that exist in the design, (the isTemporary property is false). |
| [evaluator](BRepEdge_evaluator.md) | Returns CurveEvaluator3D for evaluation. |
| [faces](BRepEdge_faces.md) | Returns the BRepFaces that are associated with this edge through its BRepCoEdges. |
| [geometry](BRepEdge_geometry.md) | Returns the underlying curve geometry of the edge. |
| [isDegenerate](BRepEdge_isDegenerate.md) | Returns if the edge's geometry is degenerate. For example, the apex of a cone is a degenerate edge. |
| [isParamReversed](BRepEdge_isParamReversed.md) | Returns if the parametric direction of this edge is reversed from the parametric direction of the underlying curve obtained from the geometry property. An edge's parametric direction is from the start vertex to the end vertex. But the underlying curve geometry may have the opposite parameterization. This property indicates if the parameterization order of the evaluator obtained from this edge is reversed from the order of the geometry curve's evaluator. |
| [isTolerant](BRepEdge_isTolerant.md) | Returns if the edge is tolerant. The tolerance used is available from the tolerance property. |
| [isValid](BRepEdge_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [length](BRepEdge_length.md) | Returns the length of the edge in centimeters. |
| [nativeObject](BRepEdge_nativeObject.md) | The NativeObject is the object outside the context of an assembly. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](BRepEdge_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [pointOnEdge](BRepEdge_pointOnEdge.md) | Returns a sample point guaranteed to lie on the edge's curve, within its boundaries, and not on a vertex (unless this is a degenerate edge). |
| [shell](BRepEdge_shell.md) | Returns the parent shell of the edge. |
| [startVertex](BRepEdge_startVertex.md) | Returns the BRepVertex that bounds its low parameter end. |
| [tangentiallyConnectedEdges](BRepEdge_tangentiallyConnectedEdges.md) | Returns a collection of edges that includes all of the edges tangentially connected to this edge. The result includes this edge. The edges are in the collection in their connected order. |
| [tempId](BRepEdge_tempId.md) | Returns the temporary ID of this edge. This ID is only good while the document remains open and as long as the owning BRepBody is not modified in any way. The findByTempId method of the BRepBody will return the entity in the body with the given ID. |
| [tolerance](BRepEdge_tolerance.md) | Returns the tolerance used by a tolerant edge. This value is only useful when isTolerant is true. |

## Accessed From

[AlongEdgeRipFeatureDefinition.ripEdge](AlongEdgeRipFeatureDefinition_ripEdge.md), [AtCenterHolePositionDefinition.centerEdge](AtCenterHolePositionDefinition_centerEdge.md), [BRepCoEdge.edge](BRepCoEdge_edge.md), [BRepEdge.createForAssemblyContext](BRepEdge_createForAssemblyContext.md), [BRepEdge.nativeObject](BRepEdge_nativeObject.md), [BRepEdges.item](BRepEdges_item.md), [CornerClosureFeatureDefinition.dominantEdge](CornerClosureFeatureDefinition_dominantEdge.md), [CornerClosureFeatureDefinition.submissiveEdge](CornerClosureFeatureDefinition_submissiveEdge.md), [CornerClosureFeatureInput.dominantEdge](CornerClosureFeatureInput_dominantEdge.md), [CornerClosureFeatureInput.submissiveEdge](CornerClosureFeatureInput_submissiveEdge.md), [DoubleHemFeatureDefinition.hemEdge](DoubleHemFeatureDefinition_hemEdge.md), [FlatHemFeatureDefinition.hemEdge](FlatHemFeatureDefinition_hemEdge.md), [HemFeatureDefinition.hemEdge](HemFeatureDefinition_hemEdge.md), [OnEdgeHolePositionDefinition.edge](OnEdgeHolePositionDefinition_edge.md), [OpenHemFeatureDefinition.hemEdge](OpenHemFeatureDefinition_hemEdge.md), [PlaneAndOffsetsHolePositionDefinition.edgeOne](PlaneAndOffsetsHolePositionDefinition_edgeOne.md), [PlaneAndOffsetsHolePositionDefinition.edgeTwo](PlaneAndOffsetsHolePositionDefinition_edgeTwo.md), [RolledHemFeatureDefinition.hemEdge](RolledHemFeatureDefinition_hemEdge.md), [RopeHemFeatureDefinition.hemEdge](RopeHemFeatureDefinition_hemEdge.md), [TeardropHemFeatureDefinition.hemEdge](TeardropHemFeatureDefinition_hemEdge.md), [ThreeBendCornerClosureFeatureDefinition.dominantEdge](ThreeBendCornerClosureFeatureDefinition_dominantEdge.md), [ThreeBendCornerClosureFeatureDefinition.submissiveEdge](ThreeBendCornerClosureFeatureDefinition_submissiveEdge.md), [TwoBendCornerClosureFeatureDefinition.dominantEdge](TwoBendCornerClosureFeatureDefinition_dominantEdge.md), [TwoBendCornerClosureFeatureDefinition.submissiveEdge](TwoBendCornerClosureFeatureDefinition_submissiveEdge.md)

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version August 2014  

