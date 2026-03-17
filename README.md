# 商圈标签云（https://stadyinger.github.io/tagcloud/）

本项目是一个面向城市商圈 POI 数据分析的可视化应用，提供“地图筛选 -> 数据查看 -> 词云生成 -> 细节增强”的完整流程。
系统基于 Vue 3 + D3 + AMap 构建，支持在地图上绘制筛选区域，自动提取选区内 POI，并按商圈与类别进行标签云布局，适用于商圈研究、地理教学演示与可视分析实验。

![1773739888543-2026-3-1717:31:28.png](https://gitee.com/attacking-lei/firstprogect/raw/master/1773739888543-2026-3-1717:31:28.png)
---

## 特性总览

- 地图筛选联动：支持圆形、矩形、多边形绘制筛选，实时高亮选中 POI。
- 商圈边界可视化：加载商圈轮廓和中心标记，根据缩放级别智能显隐。
- 词云布局引擎：
  - 基础模式下使用扇区约束 + 阿基米德螺旋进行类别内排布。
  - 详细模式下使用距离场（SDF）进行缝隙二次填充，提升密度与可读性。
- 多类别配色体系：按 POI 类型生成色带图例并在词云中同步渲染。
- 数据面板协同：表格分页、条件筛选与地图筛选状态联动。
- AI 对话助手：提供商圈数据问答、关键词筛选、名称精简等辅助交互能力。
- 本地数据缓存：基于 Dexie（IndexedDB）管理商圈与 POI 数据，减少重复加载。

---

## 技术栈

- 框架与构建：Vue 3、Vite 7
- 可视化：D3.js
- 地图能力：高德地图 JS API（@amap/amap-jsapi-loader）
- 状态管理：Pinia
- 数据缓存：Dexie（IndexedDB）
- UI 组件：Element Plus
- 其他：Axios、Marked、OpenAI SDK

依赖与脚本详见 package.json。

---

## 项目结构

```text
bussiness_tagCloud/
├── public/
│   ├── grouped_pois_detail.json      # 原始商圈+POI数据
│   ├── name.json                     # 名称映射数据
│   └── *.svg / *.png                 # 界面图标资源
├── src/
│   ├── App.vue                       # 主布局（左侧控制区 + 右侧词云区）
│   ├── components/
│   │   ├── TagCloud.vue              # 词云核心渲染组件
│   │   └── AiDialog.vue              # AI 助手抽屉
│   ├── content/
│   │   ├── mapContent.vue            # 地图与选区绘制
│   │   ├── dataContent.vue           # POI 表格与筛选
│   │   ├── colorContent.vue          # 配色面板
│   │   └── fontContent.vue           # 字体面板
│   ├── stores/
│   │   └── poiStore.js               # 全局数据状态与数据处理
│   ├── utils/
│   │   ├── mapTools.js               # 地图辅助渲染工具
│   │   └── tagCloudTool.js           # 词云几何、碰撞、SDF工具
│   └── db/
│       └── dexieDB.js                # IndexedDB 数据表定义
├── vite.config.js
└── package.json
```

---

## 快速开始

### 1. 环境要求

- Node.js: ^20.19.0 或 >=22.12.0
- 推荐 npm 10+

### 2. 安装依赖

```bash
npm install
```

### 3. 启动开发环境

```bash
npm run dev
```

默认启动后访问控制台输出的本地地址（通常为 `http://localhost:5173`）。

### 4. 生产构建与预览

```bash
npm run build
npm run preview
```

### 5. 代码规范检查

```bash
npm run lint
npm run format
```

---

## 核心流程

1. 在地图面板绘制筛选区域（圆/矩形/多边形）。
2. 系统筛选选区内 POI，并同步到数据表与状态仓库。
3. 点击“绘制标签云”，按商圈聚合并进行类型分扇区布局。
4. 在“详细显示”模式下启用 SDF 距离场填充，提高局部密度。
5. 根据字体和配色面板调整视觉风格，实时反馈到词云画布。

---

## 核心模块说明

- `src/content/mapContent.vue`
  - 加载高德地图、商圈多边形、海量点图层。
  - 处理选区绘制、区域筛选、底图切换与检索定位。

- `src/stores/poiStore.js`
  - 管理 `selectedArea`、`selectedPois`、`allPoisData`、`isDetailMode` 等关键状态。
  - 提供 `getStructuredPoisData()`，将筛选结果按商圈聚合为词云输入。

- `src/components/TagCloud.vue`
  - 词云渲染主逻辑：坐标映射、碰撞检测、轮廓生成、全局商圈避让。
  - 详细模式下结合 `rasterizeSpace()` 与 `computeDistanceField()` 做二次填充。

- `src/content/dataContent.vue`
  - 提供可分页、可条件过滤的数据表，便于核查筛选结果。

- `src/components/AiDialog.vue`
  - 提供自然语言问答和指令式操作（筛选、重置、名称精简）。

---

## 数据说明

- 主数据文件：`public/grouped_pois_detail.json`
- 数据入库后分为两类：
  - `shapes`：商圈边界、中心、排名等信息
  - `pois`：POI 名称、类型、经纬度、权重、所属商圈

项目会在首次导入后写入 IndexedDB，后续优先从本地缓存读取。

---

## 配置与注意事项

- 地图 Key
  - 当前在地图组件中通过 `apiKey` 配置高德 JS API Key。
  - 部署时请将 Key 与域名白名单保持一致。

- AI 能力
  - 当前 AI 对话组件使用浏览器侧请求方式，仅适合开发与演示。
  - 生产环境建议改为后端代理转发，避免敏感密钥暴露。

- 性能建议
  - 在超大数据量下，优先关闭“详细显示”进行快速预览。
  - 详细显示模式会执行更密集的空间采样与碰撞检测，耗时更高。

---


