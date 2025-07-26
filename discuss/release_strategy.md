# 版本发布策略讨论

本文档旨在讨论并确定 `loguru-suite` 项目的版本发布策略，以确保发布流程的清晰、高效和自动化。

## 1. 版本号规范

我们遵循 [Semantic Versioning 2.0.0](https://semver.org/) 规范。

- **正式版本 (Stable)**: `X.Y.Z` (例如: `0.5.0`, `1.0.0`)
- **预发布版本 (Prerelease)**: `X.Y.Z-alpha.N`, `X.Y.Z-beta.N`, `X.Y.Z-rc.N` (例如: `0.5.0-alpha.1`, `1.0.0-rc.2`)。PyPI 规范中通常写作 `X.Y.ZaN`, `X.Y.ZbN`, `X.Y.ZrcN` (例如: `0.5.0a1`, `1.0.0rc2`)。
- **开发版本 (Development)**: `X.Y.Z.devN` (例如: `0.2.2.dev4`)。这通常用于 `main` 分支的持续集成，不作为正式或预发布版本。

## 2. 发布流程

### 2.1 开发版本 (dev)

- **触发方式**: 每次向 `main` 分支合并代码时，由 CI 自动触发。
- **目的**: 用于内部测试和快速验证，不建议外部用户使用。
- **发布到**: TestPyPI。
- **自动化**: CI 工作流自动递增 `.devN` 版本号并发布。

### 2.2 预发布版本 (alpha, beta, rc)

- **触发方式**: 手动触发 `publish.sh` 脚本，或通过 GitHub Release 创建一个标记为 `prerelease` 的版本。
- **目的**: 提供给早期用户测试，收集反馈。
- **发布到**: TestPyPI (推荐) 或 PyPI (如果需要更广泛的测试)。
- **自动化**: 
  - `publish.sh` 脚本应能识别 `alpha/beta/rc` 版本号，并自动为 `gh release create` 命令添加 `--prerelease` 标志。
  - GitHub Actions 工作流根据 `github.event.release.prerelease == true` 来判断是否为预发布，并发布到 TestPyPI。

### 2.3 正式版本 (stable)

- **触发方式**: 手动触发 `publish.sh` 脚本，或通过 GitHub Release 创建一个未标记为 `prerelease` 的版本。
- **目的**: 正式向所有用户发布。
- **发布到**: PyPI。
- **自动化**: 
  - `publish.sh` 脚本创建正式的 GitHub Release。
  - GitHub Actions 工作流根据 `github.event.release.prerelease == false` 来判断是否为正式发布，并发布到 PyPI。

## 3. 自动化策略

### 3.1 `publish.sh` 脚本

- **职责**: 
  1. 更新 `pyproject.toml` 中的版本号。
  2. 提交并推送版本更新的 commit。
  3. 创建 GitHub Release，并根据版本号自动判断是否添加 `--prerelease` 标志。
- **建议修改**: 
  - 增加逻辑，自动从版本号中解析是否为预发布版本 (例如，包含 `alpha`, `beta`, `rc`, `a`, `b`)，并设置 `PRERELEASE` 变量。

### 3.2 GitHub Actions (`publish.yml`)

- **职责**: 
  1. 监听 `release` 事件。
  2. 根据 `github.event.release.prerelease` 的值，决定发布到 TestPyPI 还是 PyPI。
- **当前实现**: 目前的 `if` 条件已经能够正确处理这种情况，无需修改。

## 4. 分支策略

- **`main` 分支**: 作为主开发分支和稳定分支。所有新功能和修复都合并到 `main` 分支。
- **`develop` 分支**: 目前项目规模较小，`main` 分支足以应对，暂时不需要 `develop` 分支。未来如果项目复杂度增加，可以考虑引入。

## 5. 待选发布策略方案

基于以上原则，我为您设计了三种业界主流的发布策略，各有优劣，请您决策。

### 方案一：Trunk-Based 极简工作流 (当前文档描述的方案)

此方案流程最简单，自动化程度最高，适合追求快速迭代的小团队。

- **分支策略**: 只保留 `main` 一个主分支，所有开发活动都直接或通过短暂的特性分支（feature branch）汇入 `main`。
- **版本发布流程**:
    1.  开发者在本地运行 `scripts/publish.sh <version>`。
    2.  `publish.sh` 脚本**智能判断**版本号：
        - 如果版本号含 `a/b/rc/dev`，则创建 GitHub Release 时自动添加 `--prerelease` 标志。
        - 否则，创建正式版 Release。
    3.  GitHub Actions 根据 Release 的 `prerelease` 标志，自动将包发布到 **TestPyPI**（预发布版）或 **正式 PyPI**（正式版）。
- **优点**:
    - **极简高效**: 没有复杂的分支管理，学习成本低，迭代速度快。
    - **CI/CD 友好**: 单一主干非常适合持续集成和持续交付。
- **缺点**:
    - **对测试要求高**: 必须有强大的自动化测试来保证 `main` 分支的稳定性。
    - **提交必须规范**: 所有合并到 `main` 的代码都应是高质量、可发布的。

### 方案二：GitFlow 规范工作流

此方案流程最严谨，分支职责划分清晰，适合需要维护多个版本、对稳定性要求极高的项目。

- **分支策略**:
    - `main`: 永远指向最新的生产环境稳定代码，只接受来自 `release` 或 `hotfix` 分支的合并。
    - `develop`: 开发主干，所有新功能开发都汇入此分支。
    - `feature/*`: 从 `develop` 分出，用于开发新功能。
    - `release/*`: 从 `develop` 分出，用于准备发布新版本。在此分支上进行版本冻结、测试和 Bug 修复，不再添加新功能。通常在此分支上打 `rc` 标签。
    - `hotfix/*`: 从 `main` 分出，用于紧急修复生产环境的 Bug。
- **版本发布流程**:
    1.  日常开发在 `develop` 分支，可发布 `dev` 或 `alpha` 版本到 TestPyPI。
    2.  当计划发布新版时，从 `develop` 创建 `release/v0.5.0` 分支。
    3.  在 `release` 分支上，发布 `0.5.0rc1`, `0.5.0rc2` 等版本到 TestPyPI。
    4.  测试通过后，将 `release` 分支同时合并到 `main` 和 `develop`，并在 `main` 分支上打上最终的 `v0.5.0` 标签。
    5.  `main` 分支的最终标签触发工作流，发布到 **正式 PyPI**。
- **优点**:
    - **稳定可靠**: `main` 分支受到严格保护，永远是可用的稳定代码。
    - **职责清晰**: 分支各司其职，版本演进路径清晰可追溯。
- **缺点**:
    - **流程繁琐**: 分支多，合并操作频繁，增加了复杂性和管理成本，降低了发布频率。

### 方案三：GitHub Flow + Release Branch (平衡方案)

此方案是前两者的折中，既保持了主干的整洁，又为版本发布提供了缓冲期，是很多开源项目的选择。

- **分支策略**:
    - `main`: 主分支，始终保持可发布状态。
    - `feature/*`: 从 `main` 分出，完成开发、测试后合并回 `main`。
    - `release/vX.Y`: **长期存在的发布分支**。当需要为某个版本（如 `0.5.x`）进行长期维护和 Bug 修复时，从 `main` 的特定节点创建此分支。
- **版本发布流程**:
    1.  所有新功能开发在 `main` 上进行。
    2.  当 `main` 分支达到一个适合发布预发布版本的状态时（例如，完成了一组重要功能），直接在 `main` 分支上运行 `scripts/publish.sh 0.5.0a1`。
    3.  脚本和 CI/CD 流程同 **方案一**，自动发布 `alpha`, `beta`, `rc` 版本到 TestPyPI。
    4.  当一个版本（如 `0.5.0`）正式发布后，如果后续需要发布 `0.5.1` 等修复版本，可以从 `v0.5.0` 标签处创建一个新的 `release/v0.5` 分支，在此分支上进行修复和发布。
- **优点**:
    - **简洁实用**: 比 GitFlow 简单，比 Trunk-Based 多了版本维护的灵活性。
    - **持续交付**: `main` 分支可以频繁地发布预发布版本。
- **缺点**:
    - 需要团队约定何时从 `main` 发布，以及何时创建 `release` 分支。

## 6. 结论与下一步

- **当前策略问题**: `publish.sh` 脚本没有自动将 `0.5.0a1` 这样的版本识别为 `prerelease`，导致 GitHub Release 创建错误，工作流没有执行预发布流程。
- **解决方案**: 根据您最终选择的方案，修改 `publish.sh` 脚本，增加自动检测预发布版本的逻辑。

请您审阅以上方案，并告知我您的选择。一旦确定，我将立即着手调整 `scripts/publish.sh` 和 `.github/workflows/publish.yml` 以匹配所选的策略。