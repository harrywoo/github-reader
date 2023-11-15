from fastapi import FastAPI, HTTPException
import requests
import json

app = FastAPI()

# 假设这是您提供的解析JSON的函数
def parse_json(json_data):
    # 首先检查是否存在所需的路径
    if  'data' in json_data and 'info' in json_data['data']:
        info_list = json_data['data']['info']
        # 确保info_list是一个列表并且有至少三个元素
        if isinstance(info_list, list) and len(info_list) >= 3:
            results = ["下面是搜索结果"]
            # 遍历前三个元素
            for index, item in enumerate(info_list[:5]):
                # 检查所需的字段是否存在
                if 'content' in item and 'title' in item:
                    # 拼接title和content
                    result = "【" + str(index + 1) +"】"+ "title:" + item['title'] + "content: " + item['content']
                    results.append(result)
            # 将拼接的结果作为字符串返回
            return "\n".join(results)
        else:
            return "Info list is not valid or does not have enough elements."
    else:
        return "JSON structure does not match expected format."


# 假设这是您提供的解析JSON的函数
def parse_json2(json_data):
    # 首先检查是否存在所需的路径
    if  'data' in json_data and 'info' in json_data['data']:
        info_list = json_data['data']['info']
        # 确保info_list是一个列表并且有至少三个元素
        if isinstance(info_list, list) and len(info_list) >= 3:
            results = []
            # 遍历前三个元素
            for index, item in enumerate(info_list[:5]):
                # 检查所需的字段是否存在
                if 'content' in item and 'title' in item and 'url' in item:
                    # 拼接title和content
                    # result = "【" + str(index + 1) +"】"+ "title:" + item['title'] + "content: " + item['content']
                    result = dict()
                    result['title'] = item['title']
                    result['content'] = item['content']
                    result['url'] = item['url']
                    results.append(result)
            # 将拼接的结果作为字符串返回
            return json.dumps(results, ensure_ascii=False)
        else:
            return "Info list is not valid or does not have enough elements."
    else:
        return "JSON structure does not match expected format."


@app.get("/")
async def get_main():
    return {"message": "Welcome to Code Reader!"}


@app.get("/search/")
async def search(query: str):
    url = "https://t.aliyun.com/abs/search/searchHelpDocv?queryWord={}&limit=20&pageNo=1&from=pc&categoryId=&loc=search_helpdoc_item".format(query)
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        json_data = response.json()
        result = parse_json2(json_data)
        return result
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


# @app.get("/searchDetail/")
# async def search(query: str):
#     url = "https://t.aliyun.com/abs/search/searchHelpDocv?queryWord={}&limit=20&pageNo=1&from=pc&categoryId=&loc=search_helpdoc_item".format(query)
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # 确保请求成功
#         json_data = response.json()
#         result = parse_json(json_data)
#         return result
#     except requests.RequestException as e:
#         raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80)
