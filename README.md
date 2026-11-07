# ai-text-assistant

## 在线体验

https://ai-text-assistant-y5yg.onrender.com/docs

点开即可直接调用，无需安装。免费实例闲置 15 分钟休眠，首次访问需等待约 1 分钟。

## 项目简介
基于 FastAPI + DeepSeek 搭建的轻量文本分析服务，快速接入大模型能力。

## 核心功能
- 对接 DeepSeek API 实现文本问答与内容解析
- 提供标准化 HTTP 接口，支持外部系统调用

## 安装方式
1. 克隆仓库到本地
2. 安装 Python 依赖，在 .env 中配置 API 密钥

## 使用方法
启动 FastAPI 服务后，访问 /docs 路径即可查看接口文档并在线调试。

## 技术栈
后端框架 FastAPI，大模型 DeepSeek-Flash，开发语言 Python 3.x。

## 后续规划
后续将新增批量文本处理、多格式文件解析与结果持久化能力。
