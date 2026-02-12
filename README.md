# IPv6 Address Planner (IPv6 地址规划器)

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/pyinstaller/pyinstaller)

一个便捷的IPv6网络计算和规划工具，提供直观的图形界面，帮助网络工程师快速进行IPv6子网划分、地址计算和转换操作。

## 功能特性

### 1. 基础子网信息
- 解析IPv6地址和前缀长度
- 显示网络地址、子网范围、可用地址总数
- 支持IPv6地址完整格式显示
- 自动验证输入格式

### 2. 子网划分
- 按指定数量自动划分子网
- 显示新前缀长度和可划分子网总数
- 支持导出完整子网列表（CSV/TXT格式）
- 预览前100个子网段
- 智能计算最优划分方案

### 3. 可用主机地址
- 计算子网内所有可用主机地址
- 支持RFC 6164（/127点对点链路）和RFC 4291（/128单主机）
- 灵活的导出选项：
  - 导出全部地址
  - 导出前N个地址
  - 导出后N个地址
  - 导出指定范围地址
- 实时进度显示和导出速率统计
- 超大网络导出警告和文件大小预估
- 支持中断操作

### 4. 所属子网
- 计算IPv6地址所属子网
- 显示子网范围、主机位数、子网编号
- 显示地址在子网中的序号
- 快速定位网络位置

### 5. EUI-64 转换
- MAC地址转IPv6 EUI-64接口标识符
- 自动翻转U/L位
- 生成完整IPv6地址
- 显示地址结构分解
- 支持多种MAC地址格式

### 6. 快捷键支持
- `Ctrl+C` - 复制当前结果
- `Ctrl+S` - 导出当前结果
- `Ctrl+R` - 重新计算当前标签页
- `F1` - 显示帮助信息

## 执行程序下载

#### Windows 系统
下载链接：https://wwbxd.lanzouu.com/i4keA3ibtk6d

## 源码使用说明

### 环境要求
- Python 3.7 或更高版本
- tkinter（通常随Python安装）

### 安装依赖
```bash
pip install pyinstaller
```

### 从源码运行
```bash
git clone https://gitee.com/xushuai-wk/ipv6-address-planner.git
cd ipv6-address-planner
python main.py
```

## 使用方法

### 运行程序
```bash
python main.py
```

### 打包为可执行程序

#### Windows 系统
```bash
pyinstaller --onefile --windowed --name="IPv6 Address Planner" main.py
```
打包后的可执行文件位于 `dist/IPv6 Address Planner.exe`

#### macOS 系统
```bash
pyinstaller --onefile --windowed --name="IPv6 Address Planner" main.py
```
打包后的可执行文件位于 `dist/IPv6 Address Planner` 或 `dist/IPv6 Address Planner.app`

如需创建 .app 应用包，可以使用：
```bash
pyinstaller --onefile --windowed --name="IPv6 Address Planner" --osx-bundle-identifier=com.ipv6planner.app main.py
```

#### Linux 系统
```bash
pyinstaller --onefile --windowed --name="IPv6 Address Planner" main.py
```
打包后的可执行文件位于 `dist/IPv6 Address Planner`

如需为 Linux 可执行文件添加执行权限：
```bash
chmod +x dist/IPv6\ Address\ Planner
```

#### 通用打包选项说明
- `--onefile` - 将所有依赖打包成单个可执行文件
- `--windowed` - 不显示控制台窗口（仅GUI模式）
- `--name` - 指定输出文件名
- 如需包含图标，可添加 `--icon=icon.ico`（Windows）或 `--icon=icon.icns`（macOS）

## 项目结构

```
IPv6 Address Planner/
├── main.py                    # 主程序入口
├── utils.py                   # 公共工具模块
├── basic_info_tab.py          # 基础子网信息标签页
├── subnet_division_tab.py     # 子网划分标签页
├── host_addresses_tab.py       # 可用主机地址标签页
├── subnet_membership_tab.py    # 所属子网标签页
├── eui64_conversion_tab.py    # EUI-64转换标签页
├── about_tab.py              # 关于标签页
├── README.md                 # 项目文档
└── dist/
    └── IPv6 Address Planner.exe
```

## 模块说明

| 模块 | 功能 | 主要类 |
|------|------|--------|
| main.py | 主程序入口，初始化UI和标签页 | IPv6SubnetCalculator |
| utils.py | 公共工具函数（输入框、按钮、提示等） | UIUtils, ToolTip |
| basic_info_tab.py | 基础子网信息计算 | BasicInfoTab |
| subnet_division_tab.py | 子网划分计算和导出 | SubnetDivisionTab |
| host_addresses_tab.py | 可用主机地址生成和导出 | HostAddressesTab |
| subnet_membership_tab.py | 所属子网计算 | SubnetMembershipTab |
| eui64_conversion_tab.py | EUI-64转换 | EUI64ConversionTab |
| about_tab.py | 关于页面 | AboutTab |

## 技术特性

- **模块化设计** - 每个功能独立成文件，易于维护和扩展
- **多线程处理** - 大量数据计算和导出使用后台线程，不阻塞UI
- **响应式布局** - 自动适配不同窗口大小
- **智能输入提示** - 输入框占位符和错误高亮
- **实时进度显示** - 导出操作显示进度条和速率统计
- **数据验证** - 完善的输入验证和错误提示
- **跨平台支持** - 支持 Windows、macOS 和 Linux 系统

## RFC标准支持

本项目遵循以下 RFC 标准：

- [RFC 4291](https://datatracker.ietf.org/doc/html/rfc4291) - IPv6 地址架构
- [RFC 6164](https://datatracker.ietf.org/doc/html/rfc6164) - 使用 /127 的点对点链路
- [RFC 4293](https://datatracker.ietf.org/doc/html/rfc4293) - IPv6 无状态地址自动配置
- [RFC 4862](https://datatracker.ietf.org/doc/html/rfc4862) - IPv6 无状态地址自动配置

## IPv6 地址前缀使用建议

| 前缀长度 | 适用场景 | 说明 |
|-----------|---------|------|
| /48 | 单个站点 | 适合大型企业或组织 |
| /56 | 中小型客户 | 适合中小型企业或ISP客户 |
| /64 | 单个 LAN | SLAAC 必须使用 /64，适合普通网络 |
| /127 | 点对点链路 | 适用于路由器之间的连接 |

## 常见问题 (FAQ)

### Q: 支持哪些操作系统？
A: 支持 Windows、macOS 和 Linux 系统。

### Q: 如何导出计算结果？
A: 使用 `Ctrl+S` 快捷键或点击导出按钮，支持 CSV 和 TXT 格式。

### Q: 为什么某些网络导出很慢？
A: 大型网络（如 /64）包含大量地址，导出需要较长时间。程序会显示实时进度和预估时间。

### Q: SLAAC 是什么？
A: SLAAC (Stateless Address Autoconfiguration) 是 IPv6 的无状态地址自动配置机制，要求子网前缀为 /64。

## 许可证

本项目基于 [MIT License](LICENSE) 开源协议发布。

```
MIT License

Copyright (c) 2026 xushuai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 版本历史

### v1.0.7 (2026-02-11)
- 优化关于页面UI布局
- 添加 IPv6 地址前缀使用建议
- 添加版权声明和 Gitee 项目链接

### v1.0.6
- 模块化重构，按功能拆分为多个文件
- 添加快捷键支持
- 优化UI交互体验
- 添加导出预览功能
- 响应式布局优化
- 优化关于页面

## 贡献

欢迎提交 Issue 和 Pull Request！

贡献指南：
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 致谢

感谢所有为本项目做出贡献的开发者和用户。

## 联系方式

- **项目主页**: [https://gitee.com/xushuai-wk](https://gitee.com/xushuai-wk)
- **问题反馈**: 请通过 [Issues](https://gitee.com/xushuai-wk/ipv6-address-planner/issues) 提交

## 免责声明

使用者应自行验证所有计算结果的准确性，对于因使用本软件而导致的任何直接或间接损失，开发者不承担任何责任。
