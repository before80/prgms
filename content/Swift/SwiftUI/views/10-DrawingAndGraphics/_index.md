+++
title = "10 绘制与图形"
date = 2026-09-12T12:47:47+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/drawing-and-graphics](https://developer.apple.com/documentation/swiftui/drawing-and-graphics)

# 10 绘制与图形

用图形效果和自定义绘图来增强你的视图。

## 概述 {#Overview}

借助 SwiftUI 提供的内置视图和 [形状](../9-Shapes/)，你可以创建丰富而动态的用户界面。为了增强任何视图，你可以应用许多通常与图形上下文相关联的图形效果，例如设置颜色、添加蒙版以及创建合成效果。

![](./images/drawing-and-graphics-hero@2x.png)

当你需要在图形上下文中使用立即模式绘制的灵活性时，请使用 [Canvas](https://developer.apple.com/documentation/swiftui/canvas) 视图。当你想要绘制数量极其庞大的动态形状时——例如创建粒子效果——这会特别有帮助。

关于设计指导，请参阅 Human Interface Guidelines 中的 [材质](https://developer.apple.com/design/human-interface-guidelines/materials) 和 [颜色](https://developer.apple.com/design/human-interface-guidelines/color)。

## 组合图形效果 {#Composing-graphics-effects}

- [用 SwiftUI 组合高级图形效果](10.1-ComposingAdvancedGraphicsEffectsWithSwiftui/) — 通过组合各种图形效果，在应用中创造出引人入胜的视觉效果。

## 立即模式绘制 {#Immediate-mode-drawing}

- [为你的 SwiftUI 应用添加丰富的图形](10.2-AddRichGraphicsToYourSwiftuiApp/) — 通过添加背景材质、鲜艳度、自定义图形和动画，让你的应用脱颖而出。
- [Canvas](https://developer.apple.com/documentation/swiftui/canvas) — 一种支持立即模式绘制的视图类型。
- [GraphicsContext](https://developer.apple.com/documentation/swiftui/graphicscontext) — 一个立即模式绘制的目标及其当前状态。

## 设置颜色 {#Setting-a-color}

- [tint(_:)](https://developer.apple.com/documentation/swiftui/view/tint(_:)) — 设置该视图内的着色颜色。
- [Color](https://developer.apple.com/documentation/swiftui/color) — 一种随给定上下文自适应变化的颜色表示。

## 为内容设置样式 {#Styling-content}

- [border(_:width:)](https://developer.apple.com/documentation/swiftui/view/border(_:width:)) — 用指定的样式和宽度为该视图添加边框。
- [foregroundStyle(_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:)) — 设置视图的前景元素使用给定的样式。
- [foregroundStyle(_:_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:)) — 设置子视图中前景样式的主要层级与次要层级。
- [foregroundStyle(_:_:_:)](https://developer.apple.com/documentation/swiftui/view/foregroundstyle(_:_:_:)) — 设置前景样式的主要、次要和第三层级。
- [backgroundStyle(_:)](https://developer.apple.com/documentation/swiftui/view/backgroundstyle(_:)) — 把指定的样式设置为视图中背景的渲染样式。
- [backgroundStyle](https://developer.apple.com/documentation/swiftui/environmentvalues/backgroundstyle) — 一种可选样式，设置后会覆盖默认的系统背景样式。
- [ShapeStyle](https://developer.apple.com/documentation/swiftui/shapestyle) — 渲染形状时使用的颜色或图案。
- [AnyShapeStyle](https://developer.apple.com/documentation/swiftui/anyshapestyle) — 类型被抹除的 ShapeStyle 值。
- [Gradient](https://developer.apple.com/documentation/swiftui/gradient) — 以颜色停点数组表示的颜色渐变，每个停点都有一个参数化位置值。
- [MeshGradient](https://developer.apple.com/documentation/swiftui/meshgradient) — 由定位颜色的二维网格定义的二维渐变。
- [AnyGradient](https://developer.apple.com/documentation/swiftui/anygradient) — 一种颜色渐变。
- [ShadowStyle](https://developer.apple.com/documentation/swiftui/shadowstyle) — 渲染阴影时使用的样式。
- [Glass](https://developer.apple.com/documentation/swiftui/glass) — 一种结构体，定义液态玻璃材质的配置。

## 变换颜色 {#Transforming-colors}

- [brightness(_:)](https://developer.apple.com/documentation/swiftui/view/brightness(_:)) — 按指定量提亮该视图。
- [contrast(_:)](https://developer.apple.com/documentation/swiftui/view/contrast(_:)) — 设置该视图中相近颜色之间的对比度与区分度。
- [colorInvert()](https://developer.apple.com/documentation/swiftui/view/colorinvert()) — 反转该视图中的颜色。
- [colorMultiply(_:)](https://developer.apple.com/documentation/swiftui/view/colormultiply(_:)) — 为该视图添加颜色相乘效果。
- [saturation(_:)](https://developer.apple.com/documentation/swiftui/view/saturation(_:)) — 调整该视图的颜色饱和度。
- [grayscale(_:)](https://developer.apple.com/documentation/swiftui/view/grayscale(_:)) — 为该视图添加灰度效果。
- [hueRotation(_:)](https://developer.apple.com/documentation/swiftui/view/huerotation(_:)) — 为该视图应用色相旋转效果。
- [luminanceToAlpha()](https://developer.apple.com/documentation/swiftui/view/luminancetoalpha()) — 为该视图添加亮度转 Alpha 效果。
- [materialActiveAppearance(_:)](https://developer.apple.com/documentation/swiftui/view/materialactiveappearance(_:)) — 为该视图中的材质设置显式的活跃外观。
- [materialActiveAppearance](https://developer.apple.com/documentation/swiftui/environmentvalues/materialactiveappearance) — 材质在其活跃状态下应采用的行为，默认为 `automatic`。
- [MaterialActiveAppearance](https://developer.apple.com/documentation/swiftui/materialactiveappearance) — 材质呈现活跃与非活跃状态的行为方式。

## 缩放、旋转或变换视图 {#Scaling-rotating-or-transforming-a-view}

- [scaledToFill()](https://developer.apple.com/documentation/swiftui/view/scaledtofill()) — 缩放该视图以填满其父视图。
- [scaledToFit()](https://developer.apple.com/documentation/swiftui/view/scaledtofit()) — 缩放该视图以适配其父视图。
- [scaleEffect(_:anchor:)](https://developer.apple.com/documentation/swiftui/view/scaleeffect(_:anchor:)) — 相对某个锚点，按给定比例均匀缩放该视图。
- [scaleEffect(x:y:anchor:)](https://developer.apple.com/documentation/swiftui/view/scaleeffect(x:y:anchor:)) — 相对某个锚点，按给定的水平与垂直量缩放该视图的渲染输出。
- [scaleEffect(x:y:z:anchor:)](https://developer.apple.com/documentation/swiftui/view/scaleeffect(x:y:z:anchor:)) — 相对某个锚点，按给定的水平、垂直和深度因子缩放该视图。
- [aspectRatio(_:contentMode:)](https://developer.apple.com/documentation/swiftui/view/aspectratio(_:contentmode:)) — 把该视图的尺寸限制为指定的宽高比。
- [rotationEffect(_:anchor:)](https://developer.apple.com/documentation/swiftui/view/rotationeffect(_:anchor:)) — 在二维平面中围绕指定点旋转视图的渲染输出。
- [rotation3DEffect(_:axis:anchor:anchorZ:perspective:)](https://developer.apple.com/documentation/swiftui/view/rotation3deffect(_:axis:anchor:anchorz:perspective:)) — 把视图内容渲染成围绕指定轴在三维空间中旋转后的样子。
- [perspectiveRotationEffect(_:axis:anchor:anchorZ:perspective:)](https://developer.apple.com/documentation/swiftui/view/perspectiverotationeffect(_:axis:anchor:anchorz:perspective:)) — 把视图内容渲染成围绕指定轴在三维空间中旋转后的样子。
- [rotation3DEffect(_:anchor:)](https://developer.apple.com/documentation/swiftui/view/rotation3deffect(_:anchor:)) — 按指定的三维旋转值旋转视图的内容。
- [rotation3DEffect(_:axis:anchor:)](https://developer.apple.com/documentation/swiftui/view/rotation3deffect(_:axis:anchor:)) — 围绕你以元素元组指定的轴，按某个角度旋转视图的内容。
- [transformEffect(_:)](https://developer.apple.com/documentation/swiftui/view/transformeffect(_:)) — 对该视图的渲染输出应用仿射变换。
- [transform3DEffect(_:)](https://developer.apple.com/documentation/swiftui/view/transform3deffect(_:)) — 对该视图的渲染输出应用三维变换。
- [projectionEffect(_:)](https://developer.apple.com/documentation/swiftui/view/projectioneffect(_:)) — 对该视图的渲染输出应用投影变换。
- [ProjectionTransform](https://developer.apple.com/documentation/swiftui/projectiontransform)
- [ContentMode](https://developer.apple.com/documentation/swiftui/contentmode) — 这些常量定义视图内容如何填充可用空间。

## 蒙版与裁剪 {#Masking-and-clipping}

- [mask(alignment:_:)](https://developer.apple.com/documentation/swiftui/view/mask(alignment:_:)) — 使用给定视图的 Alpha 通道为该视图添加蒙版。
- [clipped(antialiased:)](https://developer.apple.com/documentation/swiftui/view/clipped(antialiased:)) — 把该视图裁剪到其边界矩形内。
- [clipShape(_:style:)](https://developer.apple.com/documentation/swiftui/view/clipshape(_:style:)) — 为该视图设置裁剪形状。

## 应用模糊与阴影 {#Applying-blur-and-shadows}

- [blur(radius:opaque:)](https://developer.apple.com/documentation/swiftui/view/blur(radius:opaque:)) — 为该视图应用高斯模糊。
- [shadow(color:radius:x:y:)](https://developer.apple.com/documentation/swiftui/view/shadow(color:radius:x:y:)) — 为该视图添加阴影。
- [ColorMatrix](https://developer.apple.com/documentation/swiftui/colormatrix) — 在 RGBA 颜色变换中使用的矩阵。

## 基于几何信息应用效果 {#Applying-effects-based-on-geometry}

- [visualEffect(_:)](https://developer.apple.com/documentation/swiftui/view/visualeffect(_:)) — 为该视图应用效果，同时通过几何代理提供对布局信息的访问。
- [visualEffect3D(_:)](https://developer.apple.com/documentation/swiftui/view/visualeffect3d(_:)) — 为该视图应用效果，同时通过三维几何代理提供对布局信息的访问。
- [VisualEffect](https://developer.apple.com/documentation/swiftui/visualeffect) — 视觉效果可以在不改变视图祖先或后代的情况下改变视图的视觉外观。
- [EmptyVisualEffect](https://developer.apple.com/documentation/swiftui/emptyvisualeffect) — 可向其上追加其他效果的基础视觉效果。

## 合成视图 {#Compositing-views}

- [blendMode(_:)](https://developer.apple.com/documentation/swiftui/view/blendmode(_:)) — 设置把该视图与重叠视图合成时的混合模式。
- [compositingGroup()](https://developer.apple.com/documentation/swiftui/view/compositinggroup()) — 把该视图包裹进一个合成组。
- [drawingGroup(opaque:colorMode:)](https://developer.apple.com/documentation/swiftui/view/drawinggroup(opaque:colormode:)) — 在最终显示之前，把该视图的内容合成到一张离屏图像中。
- [BlendMode](https://developer.apple.com/documentation/swiftui/blendmode) — 把视图与重叠内容合成的模式。
- [ColorRenderingMode](https://developer.apple.com/documentation/swiftui/colorrenderingmode) — 颜色合成操作可用的工作色彩空间集合。
- [CompositorContent](https://developer.apple.com/documentation/swiftui/compositorcontent)
- [CompositorContentBuilder](https://developer.apple.com/documentation/swiftui/compositorcontentbuilder) — 用于组合一组 [CompositorContent](https://developer.apple.com/documentation/swiftui/compositorcontent) 元素的结果构建器。
- [AnyCompositorContent](https://developer.apple.com/documentation/swiftui/anycompositorcontent) — 类型被抹除的合成器内容。

## 测量视图 {#Measuring-a-view}

- [GeometryReader](https://developer.apple.com/documentation/swiftui/geometryreader) — 一种容器视图，把其内容定义为其自身尺寸和坐标空间的函数。
- [GeometryReader3D](https://developer.apple.com/documentation/swiftui/geometryreader3d) — 一种容器视图，把其内容定义为其自身尺寸和坐标空间的函数。
- [GeometryProxy](https://developer.apple.com/documentation/swiftui/geometryproxy) — 用于访问容器视图尺寸和坐标空间（用于解析锚点）的代理。
- [GeometryProxy3D](https://developer.apple.com/documentation/swiftui/geometryproxy3d) — 用于访问容器视图尺寸和坐标空间的代理。
- [coordinateSpace(_:)](https://developer.apple.com/documentation/swiftui/view/coordinatespace(_:)) — 给视图的坐标空间命名，这样其他代码就可以基于这个命名空间操作点、尺寸等维度。
- [CoordinateSpace](https://developer.apple.com/documentation/swiftui/coordinatespace) — 由坐标空间协议创建的已解析坐标空间。
- [CoordinateSpaceProtocol](https://developer.apple.com/documentation/swiftui/coordinatespaceprotocol) — 布局系统中的参照系。
- [PhysicalMetric](https://developer.apple.com/documentation/swiftui/physicalmetric) — 提供以点为单位、与指定物理测量值相对应的值的访问方式。
- [PhysicalMetricsConverter](https://developer.apple.com/documentation/swiftui/physicalmetricsconverter) — 物理度量转换器以物理长度测量的形式，在点值与其在三维空间中的范围之间进行转换。

## 响应几何信息变化 {#Responding-to-a-geometry-change}

- [onGeometryChange(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/ongeometrychange(for:of:action:)) — 添加一个动作，当由几何代理生成的值发生变化时执行。

## 访问 Metal 着色器 {#Accessing-Metal-shaders}

- [colorEffect(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/coloreffect(_:isenabled:)) — 返回一个新视图，它把 `shader` 作为滤镜效果应用于 `self` 中每个像素的颜色。
- [distortionEffect(_:maxSampleOffset:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/distortioneffect(_:maxsampleoffset:isenabled:)) — 返回一个新视图，它把 `shader` 作为几何扭曲效果应用于 `self` 中每个像素的位置。
- [layerEffect(_:maxSampleOffset:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/layereffect(_:maxsampleoffset:isenabled:)) — 返回一个新视图，它把 `shader` 作为滤镜应用于由 `self` 创建的栅格图层。
- [Shader](https://developer.apple.com/documentation/swiftui/shader) — 对 Metal 着色器库中某个函数的引用，以及与其绑定的 uniform 参数值。
- [ShaderFunction](https://developer.apple.com/documentation/swiftui/shaderfunction) — 对 Metal 着色器库中某个函数的引用。
- [ShaderLibrary](https://developer.apple.com/documentation/swiftui/shaderlibrary) — 一个 Metal 着色器库。

## 访问几何构造 {#Accessing-geometric-constructs}

- [Axis](https://developer.apple.com/documentation/swiftui/axis) — 二维坐标系中的水平或垂直维度。
- [Angle](https://developer.apple.com/documentation/swiftui/angle) — 一种几何角度，可以用弧度或度数访问其值。
- [UnitPoint](https://developer.apple.com/documentation/swiftui/unitpoint) — 视图坐标空间中经过归一化的二维点。
- [UnitPoint3D](https://developer.apple.com/documentation/swiftui/unitpoint3d) — 视图坐标空间中经过归一化的三维点。
- [Anchor](https://developer.apple.com/documentation/swiftui/anchor) — 由锚点来源和某个特定视图派生出的不透明值。
- [DepthAlignmentID](https://developer.apple.com/documentation/swiftui/depthalignmentid)
- [Alignment3D](https://developer.apple.com/documentation/swiftui/alignment3d) — 在全部三个轴向上的对齐方式。
- [GeometryProxyCoordinateSpace3D](https://developer.apple.com/documentation/swiftui/geometryproxycoordinatespace3d) — `GeometryProxy3D` 的一种表示，可用于基于 `CoordinateSpace3D` 的转换。
