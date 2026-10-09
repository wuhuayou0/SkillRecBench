# 材料收集优先级 (Collection Priority)

评估前按以下优先级收集目标技能的材料。按顺序收集，上下文窗口不足时截断低优先级项。

## Priority 1: 必须收集（缺一不可）

1. **SKILL.md** 全文
   如不存在，取 README.md。如 README 也不存在，取目录下最大的 .md 文件。
   提取: name, description, 正文全部内容。

2. **接口/参数信息**
   来源顺位: SKILL.md 中的 parameters 节 > .claude/settings.json 中的 parameters >
   CLI --help 输出 > 源码中的 argparse/click 定义 > 函数签名。
   提取: 参数名、类型、必填性、默认值、描述。

## Priority 2: 强烈推荐（显著提高 IC/OR/DF 准确度）

3. **依赖声明文件**
   requirements.txt / package.json / pyproject.toml / Dockerfile / environment.yml
   提取: 依赖包名和版本、是否需要 GPU、是否需要特殊编译。

4. **配置文件**
   config.yaml / config.json / .env.example / settings.py
   提取: 配置参数、环境依赖、硬编码路径。

5. **Pipeline/编排文件**（如有）
   run_pipeline.py / Makefile / docker-compose.yml / workflow 配置
   提取: 多步骤编排证据、与其他技能的串联方式。

## Priority 3: 推荐（可提高 C/OR 准确度）

6. **关键源代码**（前 200 行或涉及以下操作的部分）
   - 文件读写 (open/write, to_json, to_csv, save_pretrained)
   - 网络调用 (requests, urllib, httpx)
   - 数据库/外部系统操作
   - 随机种子设置 (random.seed, np.random.seed)
   - GPU/缓存清理 (torch.cuda.empty_cache, gc.collect)
   - 错误处理 (try/except, raise, return None)

7. **测试文件**
   test_*.py / *_test.py / tests/ 目录。
   提取: 覆盖率和测试结构（不读全部测试代码，只统计文件数和断言数）。

## Priority 4: 可选

8. **项目元数据文件**
   LICENSE / .gitignore / .vscode/settings.json / CLAUDE.md / PROMPTS.md
   提取: 许可证类型、项目结构、额外用途说明。

## 收集策略

- 总材料控制在 8000 字符以内（约 2000 tokens 的 prompt 空间）。
- 超出时从 Priority 4 开始反向截断。
- 单个文件最大 3000 字符（论文标准），但 SKILL.md 全文保留。
