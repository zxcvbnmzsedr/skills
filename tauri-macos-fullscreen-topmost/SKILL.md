---
name: tauri-macos-fullscreen-topmost
description: 处理 Tauri macOS 悬浮窗/置顶窗口在其他应用原生全屏空间不可见的问题。用于 alwaysOnTop/visibleOnAllWorkspaces 无效、需要设置 NSWindow collectionBehavior/level 或尝试 NSPanel 行为与运行时类切换的场景。
---

# Tauri macOS 全屏置顶

## 概要
修复 Tauri v2 悬浮窗在 macOS 原生全屏下不可见的问题，从前端配置到 Rust/ObjC 原生窗口行为逐级加固。

## 工作流

### 1) 前端窗口配置
- 对“已存在窗口”调用 `setAlwaysOnTop(true)` + `setVisibleOnAllWorkspaces(true)`，再 `show()`/`setFocus()`。
- 对“新建窗口”先 `visible: false` 创建，等待 `tauri://created` 后再设置置顶与跨空间，再 `show()`。
- 确保权限：`core:window:allow-set-always-on-top`、`core:window:allow-set-visible-on-all-workspaces`、`core:window:allow-show`、`core:window:allow-set-focus`。

### 2) macOS 原生窗口行为（Rust）
在 `set_window_fullscreen_auxiliary` 里设置：
- `NSWindowCollectionBehavior::CanJoinAllSpaces`
- `NSWindowCollectionBehavior::CanJoinAllApplications`
- `NSWindowCollectionBehavior::FullScreenAuxiliary`
- `NSWindowCollectionBehavior::Auxiliary`
- `setHidesOnDeactivate(false)`
- 高层级 `setLevel(NSScreenSaverWindowLevel)`
- `orderFrontRegardless()` 强制前置

### 3) 仍不可见时：尝试 NSPanel
在同一处尝试将 `NSWindow` 运行时切换为 `NSPanel`：
- 仅在类大小一致时切换（避免崩溃）
- 若切换成功，调用：`setFloatingPanel(true)`、`setBecomesKeyOnlyIfNeeded(true)`、`setWorksWhenModal(true)`
- 若失败，记录日志并回退

建议实现：
- 仅允许 `NSPanel` / `NSWindow` 两种类名
- 使用 `CStr` 获取 `AnyClass::get`
- `AnyObject::set_class` 作为关联函数调用

### 4) 调试与回退
- 必须完全退出应用再启动，旧窗口不会继承新样式。
- 查看日志中是否出现“升级为 NSPanel 失败 / 类大小不匹配”。
- 若 NSPanel 失败仍不可见，需考虑原生 helper（Swift/Obj-C）创建独立 NSPanel，并通过 IPC 控制。

## 关键代码要点（简版）
- JS：先 `alwaysOnTop + visibleOnAllWorkspaces`，再启用辅助全屏行为
- Rust：按顺序设置 style/behavior/level，再 `orderFrontRegardless`
- NSPanel：仅在安全条件下切换类
