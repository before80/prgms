# Drawing and graphics

Enhance your views with graphical effects and customized drawings.

## Overview {#Overview}

You create rich, dynamic user interfaces with the built-in views and [Shapes](../9-Shapes/) that SwiftUI provides. To enhance any view, you can apply many of the graphical effects typically associated with a graphics context, like setting colors, adding masks, and creating composites.

![](./images/drawing-and-graphics-hero@2x.png)

When you need the flexibility of immediate mode drawing in a graphics context, use a [Canvas](https://developer.apple.com/documentation/swiftui/canvas) view. This can be particularly helpful when you want to draw an extremely large number of dynamic shapes — for example, to create particle effects.

For design guidance, see [Materials](https://developer.apple.com/design/human-interface-guidelines/materials) and [Color](https://developer.apple.com/design/human-interface-guidelines/color) in the Human Interface Guidelines.

## Composing graphics effects {#Composing-graphics-effects}

- [Composing advanced graphics effects with SwiftUI](10.1-ComposingAdvancedGraphicsEffectsWithSwiftui/) — Create compelling visuals in your app by combining graphical effects.

## Immediate mode drawing {#Immediate-mode-drawing}

- [Add rich graphics to your SwiftUI app](10.2-AddRichGraphicsToYourSwiftuiApp/) — Make your apps stand out by adding background materials, vibrancy, custom graphics, and animations.
- [Canvas](https://developer.apple.com/documentation/swiftui/canvas) — A view type that supports immediate mode drawing.
- [GraphicsContext](https://developer.apple.com/documentation/swiftui/graphicscontext) — An immediate mode drawing destination, and its current state.

## Setting a color {#Setting-a-color}

- [tint(_:)](https://developer.apple.com/documentation/swiftui/view/tint(_:)) — Sets the tint color within this view.
- [Color](https://developer.apple.com/documentation/swiftui/color) — A representation of a color that adapts to a given context.

## Styling content {#Styling-content}

- [border(_:width:)](https://developer.apple.com/documentation/swiftui/view/border(_:width:)) — Adds a border to this view with the specified style and width.
- [foregroundStyle(_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:)) — Sets a view’s foreground elements to use a given style.
- [foregroundStyle(_:_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:)) — Sets the primary and secondary levels of the foreground style in the child view.
- [foregroundStyle(_:_:_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:_:)) — Sets the primary, secondary, and tertiary levels of the foreground style.
- [backgroundStyle(_:)](https://developer.apple.com/documentation/swiftui/view/backgroundstyle(_:)) — Sets the specified style to render backgrounds within the view.
- [backgroundStyle](https://developer.apple.com/documentation/swiftui/environmentvalues/backgroundstyle) — An optional style that overrides the default system background style when set.
- [ShapeStyle](https://developer.apple.com/documentation/swiftui/shapestyle) — A color or pattern to use when rendering a shape.
- [AnyShapeStyle](https://developer.apple.com/documentation/swiftui/anyshapestyle) — A type-erased ShapeStyle value.
- [Gradient](https://developer.apple.com/documentation/swiftui/gradient) — A color gradient represented as an array of color stops, each having a parametric location value.
- [MeshGradient](https://developer.apple.com/documentation/swiftui/meshgradient) — A two-dimensional gradient defined by a 2D grid of positioned colors.
- [AnyGradient](https://developer.apple.com/documentation/swiftui/anygradient) — A color gradient.
- [ShadowStyle](https://developer.apple.com/documentation/swiftui/shadowstyle) — A style to use when rendering shadows.
- [Glass](https://developer.apple.com/documentation/swiftui/glass) — A structure that defines the configuration of the Liquid Glass material.

## Transforming colors {#Transforming-colors}

- [brightness(_:)](https://developer.apple.com/documentation/swiftui/view/brightness(_:)) — Brightens this view by the specified amount.
- [contrast(_:)](https://developer.apple.com/documentation/swiftui/view/contrast(_:)) — Sets the contrast and separation between similar colors in this view.
- [colorInvert()](https://developer.apple.com/documentation/swiftui/view/colorinvert()) — Inverts the colors in this view.
- [colorMultiply(_:)](https://developer.apple.com/documentation/swiftui/view/colormultiply(_:)) — Adds a color multiplication effect to this view.
- [saturation(_:)](https://developer.apple.com/documentation/swiftui/view/saturation(_:)) — Adjusts the color saturation of this view.
- [grayscale(_:)](https://developer.apple.com/documentation/swiftui/view/grayscale(_:)) — Adds a grayscale effect to this view.
- [hueRotation(_:)](https://developer.apple.com/documentation/swiftui/view/huerotation(_:)) — Applies a hue rotation effect to this view.
- [luminanceToAlpha()](https://developer.apple.com/documentation/swiftui/view/luminancetoalpha()) — Adds a luminance to alpha effect to this view.
- [materialActiveAppearance(_:)](https://developer.apple.com/documentation/swiftui/view/materialactiveappearance(_:)) — Sets an explicit active appearance for materials in this view.
- [materialActiveAppearance](https://developer.apple.com/documentation/swiftui/environmentvalues/materialactiveappearance) — The behavior materials should use for their active state, defaulting to `automatic`.
- [MaterialActiveAppearance](https://developer.apple.com/documentation/swiftui/materialactiveappearance) — The behavior for how materials appear active and inactive.

## Scaling, rotating, or transforming a view {#Scaling-rotating-or-transforming-a-view}

- [scaledToFill()](https://developer.apple.com/documentation/swiftui/view/scaledtofill()) — Scales this view to fill its parent.
- [scaledToFit()](https://developer.apple.com/documentation/swiftui/view/scaledtofit()) — Scales this view to fit its parent.
- [scaleEffect(_:anchor:)](https://developer.apple.com/documentation/swiftui/view/scaleeffect(_:anchor:)) — Scales this view uniformly by the specified factor, relative to an anchor point.
- [scaleEffect(x:y:anchor:)](https://developer.apple.com/documentation/swiftui/view/scaleeffect(x:y:anchor:)) — Scales this view’s rendered output by the given horizontal and vertical amounts, relative to an anchor point.
- [scaleEffect(x:y:z:anchor:)](https://developer.apple.com/documentation/swiftui/view/scaleeffect(x:y:z:anchor:)) — Scales this view by the specified horizontal, vertical, and depth factors, relative to an anchor point.
- [aspectRatio(_:contentMode:)](https://developer.apple.com/documentation/swiftui/view/aspectratio(_:contentmode:)) — Constrains this view’s dimensions to the specified aspect ratio.
- [rotationEffect(_:anchor:)](https://developer.apple.com/documentation/swiftui/view/rotationeffect(_:anchor:)) — Rotates a view’s rendered output in two dimensions around the specified point.
- [rotation3DEffect(_:axis:anchor:anchorZ:perspective:)](https://developer.apple.com/documentation/swiftui/view/rotation3deffect(_:axis:anchor:anchorz:perspective:)) — Renders a view’s content as if it’s rotated in three dimensions around the specified axis.
- [perspectiveRotationEffect(_:axis:anchor:anchorZ:perspective:)](https://developer.apple.com/documentation/swiftui/view/perspectiverotationeffect(_:axis:anchor:anchorz:perspective:)) — Renders a view’s content as if it’s rotated in three dimensions around the specified axis.
- [rotation3DEffect(_:anchor:)](https://developer.apple.com/documentation/swiftui/view/rotation3deffect(_:anchor:)) — Rotates the view’s content by the specified 3D rotation value.
- [rotation3DEffect(_:axis:anchor:)](https://developer.apple.com/documentation/swiftui/view/rotation3deffect(_:axis:anchor:)) — Rotates the view’s content by an angle about an axis that you specify as a tuple of elements.
- [transformEffect(_:)](https://developer.apple.com/documentation/swiftui/view/transformeffect(_:)) — Applies an affine transformation to this view’s rendered output.
- [transform3DEffect(_:)](https://developer.apple.com/documentation/swiftui/view/transform3deffect(_:)) — Applies a 3D transformation to this view’s rendered output.
- [projectionEffect(_:)](https://developer.apple.com/documentation/swiftui/view/projectioneffect(_:)) — Applies a projection transformation to this view’s rendered output.
- [ProjectionTransform](https://developer.apple.com/documentation/swiftui/projectiontransform)
- [ContentMode](https://developer.apple.com/documentation/swiftui/contentmode) — Constants that define how a view’s content fills the available space.

## Masking and clipping {#Masking-and-clipping}

- [mask(alignment:_:)](https://developer.apple.com/documentation/swiftui/view/mask(alignment:_:)) — Masks this view using the alpha channel of the given view.
- [clipped(antialiased:)](https://developer.apple.com/documentation/swiftui/view/clipped(antialiased:)) — Clips this view to its bounding rectangular frame.
- [clipShape(_:style:)](https://developer.apple.com/documentation/swiftui/view/clipshape(_:style:)) — Sets a clipping shape for this view.

## Applying blur and shadows {#Applying-blur-and-shadows}

- [blur(radius:opaque:)](https://developer.apple.com/documentation/swiftui/view/blur(radius:opaque:)) — Applies a Gaussian blur to this view.
- [shadow(color:radius:x:y:)](https://developer.apple.com/documentation/swiftui/view/shadow(color:radius:x:y:)) — Adds a shadow to this view.
- [ColorMatrix](https://developer.apple.com/documentation/swiftui/colormatrix) — A matrix to use in an RGBA color transformation.

## Applying effects based on geometry {#Applying-effects-based-on-geometry}

- [visualEffect(_:)](https://developer.apple.com/documentation/swiftui/view/visualeffect(_:)) — Applies effects to this view, while providing access to layout information through a geometry proxy.
- [visualEffect3D(_:)](https://developer.apple.com/documentation/swiftui/view/visualeffect3d(_:)) — Applies effects to this view, while providing access to layout information through a 3D geometry proxy.
- [VisualEffect](https://developer.apple.com/documentation/swiftui/visualeffect) — Visual Effects change the visual appearance of a view without changing its ancestors or descendents.
- [EmptyVisualEffect](https://developer.apple.com/documentation/swiftui/emptyvisualeffect) — The base visual effect that you apply additional effect to.

## Compositing views {#Compositing-views}

- [blendMode(_:)](https://developer.apple.com/documentation/swiftui/view/blendmode(_:)) — Sets the blend mode for compositing this view with overlapping views.
- [compositingGroup()](https://developer.apple.com/documentation/swiftui/view/compositinggroup()) — Wraps this view in a compositing group.
- [drawingGroup(opaque:colorMode:)](https://developer.apple.com/documentation/swiftui/view/drawinggroup(opaque:colormode:)) — Composites this view’s contents into an offscreen image before final display.
- [BlendMode](https://developer.apple.com/documentation/swiftui/blendmode) — Modes for compositing a view with overlapping content.
- [ColorRenderingMode](https://developer.apple.com/documentation/swiftui/colorrenderingmode) — The set of possible working color spaces for color-compositing operations.
- [CompositorContent](https://developer.apple.com/documentation/swiftui/compositorcontent)
- [CompositorContentBuilder](https://developer.apple.com/documentation/swiftui/compositorcontentbuilder) — A result builder for composing a collection of [CompositorContent](https://developer.apple.com/documentation/swiftui/compositorcontent) elements.
- [AnyCompositorContent](https://developer.apple.com/documentation/swiftui/anycompositorcontent) — Type erased compositor content.

## Measuring a view {#Measuring-a-view}

- [GeometryReader](https://developer.apple.com/documentation/swiftui/geometryreader) — A container view that defines its content as a function of its own size and coordinate space.
- [GeometryReader3D](https://developer.apple.com/documentation/swiftui/geometryreader3d) — A container view that defines its content as a function of its own size and coordinate space.
- [GeometryProxy](https://developer.apple.com/documentation/swiftui/geometryproxy) — A proxy for access to the size and coordinate space (for anchor resolution) of the container view.
- [GeometryProxy3D](https://developer.apple.com/documentation/swiftui/geometryproxy3d) — A proxy for access to the size and coordinate space of the container view.
- [coordinateSpace(_:)](https://developer.apple.com/documentation/swiftui/view/coordinatespace(_:)) — Assigns a name to the view’s coordinate space, so other code can operate on dimensions like points and sizes relative to the named space.
- [CoordinateSpace](https://developer.apple.com/documentation/swiftui/coordinatespace) — A resolved coordinate space created by the coordinate space protocol.
- [CoordinateSpaceProtocol](https://developer.apple.com/documentation/swiftui/coordinatespaceprotocol) — A frame of reference within the layout system.
- [PhysicalMetric](https://developer.apple.com/documentation/swiftui/physicalmetric) — Provides access to a value in points that corresponds to the specified physical measurement.
- [PhysicalMetricsConverter](https://developer.apple.com/documentation/swiftui/physicalmetricsconverter) — A physical metrics converter provides conversion between point values and their extent in 3D space, in the form of physical length measurements.

## Responding to a geometry change {#Responding-to-a-geometry-change}

- [onGeometryChange(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/ongeometrychange(for:of:action:)) — Adds an action to be performed when a value, created from a geometry proxy, changes.

## Accessing Metal shaders {#Accessing-Metal-shaders}

- [colorEffect(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/coloreffect(_:isenabled:)) — Returns a new view that applies `shader` to `self` as a filter effect on the color of each pixel.
- [distortionEffect(_:maxSampleOffset:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/distortioneffect(_:maxsampleoffset:isenabled:)) — Returns a new view that applies `shader` to `self` as a geometric distortion effect on the location of each pixel.
- [layerEffect(_:maxSampleOffset:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/layereffect(_:maxsampleoffset:isenabled:)) — Returns a new view that applies `shader` to `self` as a filter on the raster layer created from `self`.
- [Shader](https://developer.apple.com/documentation/swiftui/shader) — A reference to a function in a Metal shader library, along with its bound uniform argument values.
- [ShaderFunction](https://developer.apple.com/documentation/swiftui/shaderfunction) — A reference to a function in a Metal shader library.
- [ShaderLibrary](https://developer.apple.com/documentation/swiftui/shaderlibrary) — A Metal shader library.

## Accessing geometric constructs {#Accessing-geometric-constructs}

- [Axis](https://developer.apple.com/documentation/swiftui/axis) — The horizontal or vertical dimension in a 2D coordinate system.
- [Angle](https://developer.apple.com/documentation/swiftui/angle) — A geometric angle whose value you access in either radians or degrees.
- [UnitPoint](https://developer.apple.com/documentation/swiftui/unitpoint) — A normalized 2D point in a view’s coordinate space.
- [UnitPoint3D](https://developer.apple.com/documentation/swiftui/unitpoint3d) — A normalized 3D point in a view’s coordinate space.
- [Anchor](https://developer.apple.com/documentation/swiftui/anchor) — An opaque value derived from an anchor source and a particular view.
- [DepthAlignmentID](https://developer.apple.com/documentation/swiftui/depthalignmentid)
- [Alignment3D](https://developer.apple.com/documentation/swiftui/alignment3d) — An alignment in all three axes.
- [GeometryProxyCoordinateSpace3D](https://developer.apple.com/documentation/swiftui/geometryproxycoordinatespace3d) — A representation of a `GeometryProxy3D` which can be used for `CoordinateSpace3D` based conversions.
