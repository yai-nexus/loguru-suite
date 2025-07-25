# `loguru-suite` 现代化 Monorepo 与插件化改造方案

## 1. 项目愿景

将现有的 `loguru-suite` 项目重构为一个现代化的、基于插件架构的 Python monorepo。目标是创建一个高内聚、低耦合、易于扩展和维护的日志解决方案套件。

## 2. 核心设计决策

- **Monorepo 管理**: 采用 `uv` 作为唯一的包管理和虚拟环境管理工具，利用其工作区（workspace）特性来管理 monorepo 中的多个包。
- **插件化架构**: 基于 Python 标准的 `importlib.metadata.entry_points` 机制实现插件的动态发现和加载，实现最大程度的解耦。
- **命名规范**:
  - **核心库**: `yai-loguru`
  - **插件包**: `yai-loguru-*` (例如: `yai-loguru-sentry`, `yai-loguru-file-sink`)
  - **Python 包名**: `yai_loguru`, `yai_loguru_sentry` 等。

## 3. 拟定目录结构

```
/Users/harrytang/Documents/GitHub/loguru-suite/
├── .venv/                   # Python 虚拟环境 (由 uv 创建)
├── docs/
│   └── ...                    # 正式文档
├── discuss/
│   └── monorepo-and-plugin-architecture-plan.md # 方案文档
├── examples/
│   └── simple-usage/          # 示例项目 (原 loguru-example)
│       ├── main.py
│       └── pyproject.toml
├── packages/
│   ├── yai-loguru/       # 核心库 (原 loguru-support)
│   │   ├── src/yai_loguru/
│   │   │   ├── __init__.py
│   │   │   ├── config.py      # 配置加载
│   │   │   ├── manager.py     # 插件管理器
│   │   │   └── plugin.py      # 插件基类/接口定义
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── yai-loguru-file-sink/       # 第一个插件：文件日志
│       ├── src/yai_loguru_file_sink/
│       │   └── __init__.py    # 插件实现
│       ├── pyproject.toml
│       └── README.md
├── scripts/
│   ├── install.sh             # 安装所有依赖
│   └── run-example.sh         # 运行示例
├── logs/                      # 运行时日志输出目录
├── .gitignore
├── LICENSE
├── pyproject.toml             # Monorepo 根配置文件 (uv workspace)
└── README.md                  # 项目总 README
```

## 4. 插件架构详解

1.  **插件接口 (`plugin.py`)**: 在 `yai-loguru` 中定义一个抽象基类 `LoguruPlugin`，所有插件都必须继承它，并实现如 `setup(config)` 等核心方法。

2.  **插件发现 (`manager.py`)**: `PluginManager` 将使用 `importlib.metadata.entry_points(group='yai_loguru.plugins')` 来查找所有已安装的、声明了该入口点的插件。

3.  **插件声明 (`pyproject.toml`)**: 每个插件包（如 `yai-loguru-file-sink`）都需要在其 `pyproject.toml` 中声明自己的入口点，例如：
    ```toml
    [project.entry-points."yai_loguru.plugins"]
    file_sink = "yai_loguru_file_sink:FileSinkPlugin"
    ```

4.  **配置加载 (`config.py`)**: 核心库将提供一种方式（例如，从一个 `config.toml` 文件）来加载配置，并根据配置来决定启用哪些插件，以及向它们传递什么参数。

## 5. 开发与工作流程

- **初始化**: 开发者克隆项目后，只需运行 `scripts/install.sh`。该脚本会：
  1.  `uv venv` 创建虚拟环境。
  2.  `uv pip install -e .` 在根目录执行，`uv` 会根据根 `pyproject.toml` 中的 `[tool.uv.workspace]` 配置，以可编辑模式安装 `packages/` 下的所有包。
- **运行示例**: 运行 `scripts/run-example.sh` 来启动 `examples/simple-usage/main.py`，查看实际的日志输出效果。

## 6. 实施步骤

1.  **结构搭建**: 创建新的目录结构 (`packages`, `examples`, `scripts`, `discuss`, `logs`)。
2.  **代码迁移**: 将 `old/loguru-support` 的内容移动并重构到 `packages/yai-loguru`，将 `old/loguru-example` 移动到 `examples/simple-usage`。
3.  **核心实现**: 在 `yai-loguru` 中开发插件接口、管理器和配置加载器。
4.  **插件开发**: 创建第一个插件 `yai-loguru-file-sink` 作为概念验证。
5.  **配置 `uv`**: 编写根 `pyproject.toml` 和所有子包的 `pyproject.toml` 文件。
6.  **脚本编写**: 实现 `install.sh` 和 `run-example.sh`。
7.  **清理**: 移除 `old/` 目录。

请您审阅此方案。如果同意，我将开始着手实施第一步：搭建新的目录结构。