# Adams Batch Analyzer

Adams Batch Analyzer 是一个面向 Codex 的通用 ADAMS 批处理仿真插件，用来自动完成：

- 批处理求解
- `.res` 结果提取
- 指定通道导出
- 曲线图生成
- 摘要说明输出

它不是专门针对发动机模型，而是针对**通用机械系统模型**设计的。发动机只是其中一种可选使用场景。

## 适用场景

- 连杆机构批处理仿真
- 悬架/传动系统结果导出
- 发动机缸力或点火时序分析
- 关节力/驱动力矩结果整理
- 仿真结果的自动打包和复现

## 基本要求

- Windows
- 本机安装 ADAMS
- 有可用许可证
- 输入模型为可求解的 `.adm`

## 核心能力

1. 自动生成 `.acf` 批处理控制文件
2. 自动调用 ADAMS 求解器
3. 自动收集 `.res/.msg/.req/.gra`
4. 自动解析 `.res`
5. 自动导出选定通道 `csv`
6. 自动生成配置化曲线图
7. 自动输出 Markdown 摘要

## 快速使用

```powershell
python scripts\adams_batch_pipeline.py `
  --adm E:\path\to\model.adm `
  --output-dir E:\path\to\outputs `
  --config examples\generic_channels.json
```

如果 ADAMS 启动器无法自动识别，可以显式传入：

```powershell
python scripts\adams_batch_pipeline.py `
  --adm E:\path\to\model.adm `
  --output-dir E:\path\to\outputs `
  --config examples\generic_channels.json `
  --launcher E:\path\to\adams2024_1.bat
```

## 示例配置

- [examples/generic_channels.json](./examples/generic_channels.json)
  通用力/力矩/关节结果提取模板
- [examples/engine_channels.json](./examples/engine_channels.json)
  发动机类模型的主支承、关键关节、驱动扭矩模板

## 当前限制

- 主要面向非交互式 batch workflow
- 不负责 ADAMS/View 的完整 GUI 建模
- 不自动修复几何依赖缺失
- 不自动推断每一种模型的物理语义，复杂模型建议自行配置通道

## 发布准备状态

这份仓库已经具备：

- 插件 manifest
- 通用批处理脚本
- 示例配置
- 开源许可证
- 中英文文档基础

后续如果正式公开，建议继续补充：

- 示例截图
- 更多模型模板
- 常见问题
- 版本发布记录
