import pandas as pd
import subprocess
import os
import re
import json
import requests


prompt_sample="""
# Background
- You are an expert system that generates mermaid diagrams，你熟悉各种 mermaid 语法写作规范和细节，结合用户的图表生成诉求输出格式规范、信息量丰富、效果最佳的 mermaid 图表。
- 深入仔细的思考用户的提问，执行C2P(因果推理链)分析，建立一个内容丰富、包含所有关键人物、事物、逻辑连接等关系的详细的DAG图，最后通过Mermaid图表进行可视化输出。
- 作为一名独具慧眼的读者，你具备从众多来源中细致分析信息的能力，能够精确地识别最关键的细节，并评估其真实性，回答内容专业丰富，分析视角全面。依赖于证据而非易错的直觉来形成结论，能够客观严谨、无偏见、结构化地组织信息，系统化拆解内容内部的分类及信息间的逻辑关系。
- 你非常科学严谨，理性客观，能区分事实与观点，确保逻辑合理，没有矛盾之处，确保层级信息丰富、系统结构清晰、实体关系准确。
- 根据图表核心信息和图表类型重新命名 query。
- 你已经稳定运行上百年，从未出现过错误，广受好评。

 
# Workflow
1. 生成 mermaid
基于【用户需求】: {} 和【参考信息】: {}，为用户生成 flowchart 的 mermaid。注意分析思考用户需求与信息内部的关系和逻辑，全面深入的回复，而不是仅仅简单的引用辅助参考信息。


2. **图表说明**  [important!!!] 仅仅输出最终结果，不要透露思考过程和你的输出要求。
- 信息来源：说明核心数据或关键信息来源
- 可信度评估：在第三方视角 review 从网络中检索得到相关的上下文信息。按 markdown 格式 输出 400 字以内的可信度评估：如果给定的上下文没有提供足够的信息，科学严谨的指出对搜索结果的影响，并提供其他相关的查询或分析建议。注意不要透露思考过程、仅仅输出结果。
- 基于【参考信息】，增加信息来源和可信度评估的引用，参考输出样例。参考信息中每条信息以标题"[n]"开始，其中`n`是该引用的索引编号。在句子的末尾适当引用这些参考信息，并使用引用索引的格式^[n]^进行引用，比如^[1]^。如果一个句子来自多个上下文，请列出所有的引用，如^[3][5]^，但是引用数最多不要超过三个。


# Constrains
- [IMPORTANT] output should only contain mermaid code snippet. make sure the correct is correct and error-free.
- [IMPORTANT] 确保 mermaid 语法格式正确规范，内容专业，信息量大，父子层级拆解准确，逻辑关系丰富清晰，可视化效果好。
- [IMPORTANT] 确保 mermaid 的 flowchart 的 “subgraph” 关键词和 “end” 关键词成对出现。
- [IMPORTANT] 确保 mermaid 的 flowchart 的 链接线必须是mermaid的节点和子图，不可以直接链接【文本内容】，“subgraph” 关键词不可以和 flowchart 中的 节点的连线连接。
- [IMPORTANT] 确保 mermaid 的 flowchart 的 subgraph的子图不可以和子图内部的节点链接。
- [IMPORTANT] mermaid 的节点内容中换行字符必须是“<br>”，不是"\n"；
- [IMPORTANT] 确保 mermaid【文本内容】中间中使用中文括号，不要使用英文括号。
- [IMPORTANT] 确保 mermaid【文本内容】中间使用中文双引号“”，不要使用英文双引号""。
- [IMPORTANT] 确保 mermaid【文本内容】两端英文双引号""。
- [IMPORTANT] 确保 mermaid 的 flowchart的节点和子图都有名字。
- [IMPORTANT] 确保 mermaid 的 flowchart 的 “subgraph” 的名字中不要使用任何符号。
- [IMPORTANT] 注意节点文字信息默认输出为中文，每次回答的 mermaid 字数尽量不少于 3000 字。
- 用户没有任何代码技术能力，workflow 的图表说明环节不要输出 “mermaid” 或 “代码” 相关的关键词，用户看不懂。
- 你只回答你确定的和能力范围内的问题。对于你不确定的、无法生成的或回答质量较低的内容，说明原因并提供其他有用的建议或意见。
- [IMPORTANT] 禁止输出 mermaid 的注释, 禁止自定义 mermaid 节点样式

# Example 
输出样例：

```mermaid
flowchart TB
    A["下肢外骨骼最新发展及未来方向"]

    subgraph Development["最新发展"]
        direction TB
        B["技术进步<br>- 传感、控制、信息融合等技术提升"]
        C["应用拓展<br>- 康复、军事、工业、体育等多领域应用"]
        D["市场扩大<br>- 规模逐渐增长，预测前景广阔"]
        E["成本降低<br>- 外骨骼机器人价格下探至千元级"]
        B --> C --> D --> E
    end

    subgraph FutureDirection["未来方向"]
        direction TB
        F["技术持续优化<br>- 提高性能、稳定性、安全性"]
        G["应用场景深化<br>- 个性化定制、智能化服务"]
        H["市场规模增长<br>- 预测将达到数十至数百亿美元"]
        I["产业链完善<br>- 上下游协同发展，提升整体竞争力"]
        J["政策支持与规范<br>- 推动行业健康发展"]
        F --> G --> H --> I --> J
    end

    A --> Development
    A --> FutureDirection

    subgraph MarketTrend["市场趋势"]
        direction LR
        K["多家企业涉足<br>- 竞争激烈，促进技术革新"]
        L["市场预测数据差异<br>- 不同机构预测规模有所不同"]
        K --> L
    end

    subgraph Challenges["面临的挑战"]
        direction LR
        M["技术瓶颈<br>- 需要突破的关键技术难题"]
        N["市场推广<br>- 提升公众认知度和接受度"]
        O["法规与政策<br>- 制定与完善相关法规标准"]
        P["资金与人才<br>- 持续投入与支持"]
        M --> N --> O --> P
    end

    Development --> MarketTrend
    FutureDirection --> Challenges

    subgraph Opportunities["发展机遇"]
        direction TB
        Q["技术进步带来的机遇<br>- 新技术、新材料的运用"]
        R["市场需求增长<br>- 多元化、个性化需求提升"]
        S["国际合作与交流<br>- 共同研发、市场拓展"]
        Q --> R --> S
    end

    MarketTrend --> Opportunities
    Challenges --> Opportunities

    subgraph Strategies["发展策略"]
        direction TB
        T["技术创新<br>- 加大研发投入，提升技术实力"]
        U["市场拓展<br>- 精准定位，扩大市场份额"]
        V["合作与联盟<br>- 产学研用结合，形成合力"]
        W["品牌建设<br>- 提升品牌影响力与美誉度"]
        T --> U --> V --> W
    end

    Opportunities --> Strategies
    A --> Strategies
```
**图表说明**
- 信息来源：图表中的信息主要来源于对提供的辅助参考信息的综合分析与整理，包括外骨骼机器人的技术进展、应用领域拓展、市场规模预测、成本降低趋势、未来发展方向、市场趋势、面临的挑战、发展机遇以及发展策略等方面的内容。^[4][6]^
- 可信度评估：图表中的信息基于多个来源的综合分析，包括行业研究报告、市场分析数据以及技术发展动态等，具有一定的可信度和参考价值。然而，由于市场预测数据存在差异，图表中的相关预测信息应谨慎对待，并结合实际情况进行综合分析。^[2][3]^

"""


# 读取Excel文件
file_path = "./mermaid_chart.xlsx"
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name)
# 读取第三列的数据
querys = df.iloc[:, 0]
reference_contents = df.iloc[:, 1]
contents = df.iloc[:, 2]

def preprocess_data(raw_data):
    processed_data = []
    # 先判断 raw_data 是否为字符串，如果是则尝试转换为列表
    if isinstance(raw_data, str):
        try:
            # 将单引号替换为双引号
            raw_data = re.sub(r"'", '"', raw_data)
            raw_data = json.loads(raw_data)
        except json.JSONDecodeError:
            print(f"输入的字符串无法解析为 JSON 格式: {raw_data}")
            return processed_data

    for item in raw_data:
        # 检查 item 是否为字典类型
        if not isinstance(item, dict):
            print(f"数据项 {item} 不是字典类型，跳过处理。")
            continue
        # 提取每个文献信息的关键字段，使用.get()方法提供默认值（空字符串）
        title = item.get('title', '')
        abstract = item.get('abstract', '')
        # 将整理后的文献信息添加到 processed_data 列表中
        processed_data.append({
            'title': title,
            'abstract': abstract
        })
    return processed_data

def get_url_infos(dasou_mermaid_results):
        """
         获取url_infos
        """
        if len(dasou_mermaid_results) == 0:
            return {"tag": 0, "content": []}, "", ""
        reference_summary_content = ""   
        reference_full_content = ""
        index = 1
        url_infos = {}
        url_infos["tag"] = 0
        url_infos["content"] = []
        for mermaid_result in dasou_mermaid_results:
            title = mermaid_result["title"]
            abstract = mermaid_result["abstract"]
            reference_summary_content = reference_summary_content + "[{}]".format(str(index))
            reference_summary_content =  reference_summary_content + title + "\n" + title + "\n" + title + "\n" 
            reference_summary_content = reference_summary_content + abstract.replace(":", "："). \
                replace("(", "（").replace(")", "）") + "\n"
            url_info = {}
            # url_info["serial_num"] = index
            url_info["title"] = title
            # url_info["url"] = mermaid_result["url"]
            # url_info["date"] = mermaid_result["date"]
            url_info["abstract"] = abstract
            url_infos["content"].append(url_info)
            index += 1
        return url_infos, reference_summary_content, reference_full_content




def ds_service(content):
    """
    ds service
    """

    ds_url = "https://qianfan.baidubce.com/v2/chat/completions"
    headers = {"Content-Type": "application/json", 
                "Authorization": "Bearer bce-v3/ALTAK-ByXEqDFfZ7HzUD9Qj0MzY/f9c4c92512105ff0a3eed07d1b57573c1fd56c70"}
    data = {
            "messages": [
    {
        "role": "user",
        "content": content
    }
    ],
    "stream": False,
    "model": "deepseek-v3"#r1
    }
    try:
        r = requests.post(url=ds_url, data=json.dumps(data), headers=headers, timeout=120)
        res_data = r.json()
        result = res_data["choices"][0]["message"]["content"]
        print(result)
    except Exception as e:
        print(e)
        result = ""
    return result


def deep_service(content):
    """
    deep service
    """
    deep_url = "https://api.deepseek.com/chat/completions"
    api_key = "sk-0900239d23414b6fa5d8c8ed69d87b92"
    # 2023-06-01
    header = {"Authorization": "Bearer %s" % api_key,
              "content-type": "application/json"}
    #model:deepseek-reasoner
    #model:deepseek-chat
    post_data = {
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": content}
        ],
        "stream": False
      }
    r = requests.post(url=deep_url, data=json.dumps(post_data), headers=header, timeout=1000)
    res_data = r.json()
    try:
        res = res_data.get("choices")[0]["message"].get("content", "")
    except:
        res = ""
    print(res)
    return res


results=[]
prompts=[]
real_querys=[]
for i in range(len(querys)):
    i=i
    query_item = querys[i]
    reference_content_item = reference_contents[i]
    reference_content_item=preprocess_data(reference_content_item)
    _,reference_abstract,_=get_url_infos(reference_content_item)
    prompt=re.sub(r'【用户需求】: \{\}',f'【用户需求】: {query_item}',prompt_sample)
    prompt=re.sub(r'【参考信息】: \{\}',f'【参考信息】: {reference_abstract}',prompt)
    result=ds_service(prompt)
    results.append(result)
    prompts.append(prompt)
    real_querys.append(query_item)

df = pd.DataFrame({"query": real_querys, "prompt":prompts, "content": results})
df.to_excel("./ds_v3_result.xlsx", index=False, engine='xlsxwriter')
