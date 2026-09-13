# Shapes

Trace and fill built-in and custom shapes with a color, gradient, or other pattern.

## Overview {#Overview}

Draw shapes like circles and rectangles, as well as custom paths that define shapes of your own design. Apply styles that include environment-aware colors, rich gradients, and material effects to the foreground, background, and outline of your shapes.

![](./images/shapes-hero@2x.png)

If you need the efficiency or flexibility of immediate mode drawing — for example, to create particle effects — use a [Canvas](https://developer.apple.com/documentation/swiftui/canvas) view instead.

## Creating rectangular shapes {#Creating-rectangular-shapes}

- [Rectangle](https://developer.apple.com/documentation/swiftui/rectangle) — A rectangular shape aligned inside the frame of the view containing it.
- [RoundedRectangle](https://developer.apple.com/documentation/swiftui/roundedrectangle) — A rectangular shape with rounded corners, aligned inside the frame of the view containing it.
- [RoundedCornerStyle](https://developer.apple.com/documentation/swiftui/roundedcornerstyle) — Defines the shape of a rounded rectangle’s corners.
- [RoundedRectangularShape](https://developer.apple.com/documentation/swiftui/roundedrectangularshape) — A protocol of [InsettableShape](https://developer.apple.com/documentation/swiftui/insettableshape) that describes a rounded rectangular shape.
- [RoundedRectangularShapeCorners](https://developer.apple.com/documentation/swiftui/roundedrectangularshapecorners) — A type describing the corner styles of a [RoundedRectangularShape](https://developer.apple.com/documentation/swiftui/roundedrectangularshape).
- [UnevenRoundedRectangle](https://developer.apple.com/documentation/swiftui/unevenroundedrectangle) — A rectangular shape with rounded corners with different values, aligned inside the frame of the view containing it.
- [RectangleCornerRadii](https://developer.apple.com/documentation/swiftui/rectanglecornerradii) — Describes the corner radius values of a rounded rectangle with uneven corners.
- [RectangleCornerInsets](https://developer.apple.com/documentation/swiftui/rectanglecornerinsets) — The inset sizes for the corners of a rectangle.
- [ConcentricRectangle](https://developer.apple.com/documentation/swiftui/concentricrectangle) — A shape whose corners you configure, individually or uniformly, to be squared, rounded, or concentric relative to a container shape’s corners.

## Creating circular shapes {#Creating-circular-shapes}

- [Circle](https://developer.apple.com/documentation/swiftui/circle) — A circle centered on the frame of the view containing it.
- [Ellipse](https://developer.apple.com/documentation/swiftui/ellipse) — An ellipse aligned inside the frame of the view containing it.
- [Capsule](https://developer.apple.com/documentation/swiftui/capsule) — A capsule shape aligned inside the frame of the view containing it.

## Drawing custom shapes {#Drawing-custom-shapes}

- [Path](https://developer.apple.com/documentation/swiftui/path) — The outline of a 2D shape.

## Defining shape behavior {#Defining-shape-behavior}

- [ShapeView](https://developer.apple.com/documentation/swiftui/shapeview) — A view that provides a shape that you can use for drawing operations.
- [Shape](https://developer.apple.com/documentation/swiftui/shape) — A 2D shape that you can use when drawing a view.
- [AnyShape](https://developer.apple.com/documentation/swiftui/anyshape) — A type-erased shape value.
- [ShapeRole](https://developer.apple.com/documentation/swiftui/shaperole) — Ways of styling a shape.
- [StrokeStyle](https://developer.apple.com/documentation/swiftui/strokestyle) — The characteristics of a stroke that traces a path.
- [StrokeShapeView](https://developer.apple.com/documentation/swiftui/strokeshapeview) — A shape provider that strokes its shape.
- [StrokeBorderShapeView](https://developer.apple.com/documentation/swiftui/strokebordershapeview) — A shape provider that strokes the border of its shape.
- [FillStyle](https://developer.apple.com/documentation/swiftui/fillstyle) — A style for rasterizing vector shapes.
- [FillShapeView](https://developer.apple.com/documentation/swiftui/fillshapeview) — A shape provider that fills its shape.

## Transforming a shape {#Transforming-a-shape}

- [ScaledShape](https://developer.apple.com/documentation/swiftui/scaledshape) — A shape with a scale transform applied to it.
- [RotatedShape](https://developer.apple.com/documentation/swiftui/rotatedshape) — A shape with a rotation transform applied to it.
- [OffsetShape](https://developer.apple.com/documentation/swiftui/offsetshape) — A shape with a translation offset transform applied to it.
- [TransformedShape](https://developer.apple.com/documentation/swiftui/transformedshape) — A shape with an affine transform applied to it.

## Setting a container shape {#Setting-a-container-shape}

- [containerShape(_:)](https://developer.apple.com/documentation/swiftui/view/containershape(_:)) — Sets the container shape to use for any container relative shape or concentric rectangle within this view.
- [InsettableShape](https://developer.apple.com/documentation/swiftui/insettableshape) — A shape type that is able to inset itself to produce another shape.
- [ContainerRelativeShape](https://developer.apple.com/documentation/swiftui/containerrelativeshape) — A shape whose dimensions the system calculates from an inset version of the current container shape.
