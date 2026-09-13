+++
title = "9 形状"
date = 2026-09-12T12:47:47+08:00
weight = 9
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/shapes](https://developer.apple.com/documentation/swiftui/shapes)

# 9 形状

用颜色、渐变或其他图案描边并填充内置形状和自定义形状。

## 概述 {#Overview}

绘制圆形、矩形等形状，以及定义你自己设计的形状的自定义路径。把包含环境感知颜色、丰富渐变和材质效果的样式，应用到形状的前景、背景和轮廓上。

![](./images/shapes-hero@2x.png)

如果你需要立即模式绘制的效率或灵活性——例如制作粒子效果——请改用 [Canvas](https://developer.apple.com/documentation/swiftui/canvas) 视图。

## 创建矩形形状 {#Creating-rectangular-shapes}

- [Rectangle](https://developer.apple.com/documentation/swiftui/rectangle) —— 对齐在容纳它的视图边框内的矩形形状。
- [RoundedRectangle](https://developer.apple.com/documentation/swiftui/roundedrectangle) —— 对齐在容纳它的视图边框内的圆角矩形形状。
- [RoundedCornerStyle](https://developer.apple.com/documentation/swiftui/roundedcornerstyle) —— 定义圆角矩形各个角的形状。
- [RoundedRectangularShape](https://developer.apple.com/documentation/swiftui/roundedrectangularshape) —— 描述圆角矩形形状的 [InsettableShape](https://developer.apple.com/documentation/swiftui/insettableshape) 协议。
- [RoundedRectangularShapeCorners](https://developer.apple.com/documentation/swiftui/roundedrectangularshapecorners) —— 描述 [RoundedRectangularShape](https://developer.apple.com/documentation/swiftui/roundedrectangularshape) 各个角样式的类型。
- [UnevenRoundedRectangle](https://developer.apple.com/documentation/swiftui/unevenroundedrectangle) —— 对齐在容纳它的视图边框内、各个角圆角值不同的矩形形状。
- [RectangleCornerRadii](https://developer.apple.com/documentation/swiftui/rectanglecornerradii) —— 描述角半径不均匀的圆角矩形各角的半径值。
- [RectangleCornerInsets](https://developer.apple.com/documentation/swiftui/rectanglecornerinsets) —— 矩形各个角的内边距大小。
- [ConcentricRectangle](https://developer.apple.com/documentation/swiftui/concentricrectangle) —— 各个角可以逐个或统一配置为直角、圆角，或相对于容器形状的角呈同心关系的形状。

## 创建圆形形状 {#Creating-circular-shapes}

- [Circle](https://developer.apple.com/documentation/swiftui/circle) —— 以容纳它的视图边框为中心的圆。
- [Ellipse](https://developer.apple.com/documentation/swiftui/ellipse) —— 对齐在容纳它的视图边框内的椭圆。
- [Capsule](https://developer.apple.com/documentation/swiftui/capsule) —— 对齐在容纳它的视图边框内的胶囊形状。

## 绘制自定义形状 {#Drawing-custom-shapes}

- [Path](https://developer.apple.com/documentation/swiftui/path) —— 二维形状的轮廓。

## 定义形状行为 {#Defining-shape-behavior}

- [ShapeView](https://developer.apple.com/documentation/swiftui/shapeview) —— 提供一个可用于绘制操作的形状的视图。
- [Shape](https://developer.apple.com/documentation/swiftui/shape) —— 绘制视图时可以使用的二维形状。
- [AnyShape](https://developer.apple.com/documentation/swiftui/anyshape) —— 类型擦除的形状值。
- [ShapeRole](https://developer.apple.com/documentation/swiftui/shaperole) —— 为形状设置样式的方式。
- [StrokeStyle](https://developer.apple.com/documentation/swiftui/strokestyle) —— 描绘路径的描边特征。
- [StrokeShapeView](https://developer.apple.com/documentation/swiftui/strokeshapeview) —— 对其形状进行描边的形状提供者。
- [StrokeBorderShapeView](https://developer.apple.com/documentation/swiftui/strokebordershapeview) —— 对其形状的边框进行描边的形状提供者。
- [FillStyle](https://developer.apple.com/documentation/swiftui/fillstyle) —— 栅格化矢量形状的样式。
- [FillShapeView](https://developer.apple.com/documentation/swiftui/fillshapeview) —— 填充其形状的形状提供者。

## 变换形状 {#Transforming-a-shape}

- [ScaledShape](https://developer.apple.com/documentation/swiftui/scaledshape) —— 应用了缩放缓变的形状。
- [RotatedShape](https://developer.apple.com/documentation/swiftui/rotatedshape) —— 应用了旋转缓变的形状。
- [OffsetShape](https://developer.apple.com/documentation/swiftui/offsetshape) —— 应用了平移偏移缓变的形状。
- [TransformedShape](https://developer.apple.com/documentation/swiftui/transformedshape) —— 应用了仿射缓变的形状。

## 设置容器形状 {#Setting-a-container-shape}

- [containerShape(_:)](https://developer.apple.com/documentation/swiftui/view/containershape(_:)) —— 设置该视图内任何相对容器形状或同心矩形所使用的容器形状。
- [InsettableShape](https://developer.apple.com/documentation/swiftui/insettableshape) —— 能对自身设置内边距、从而产生另一个形状的形状类型。
- [ContainerRelativeShape](https://developer.apple.com/documentation/swiftui/containerrelativeshape) —— 其尺寸由系统根据当前容器形状的内缩版本计算出的形状。
