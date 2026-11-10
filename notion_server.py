import httpx
from fastmcp import FastMCP
import os 
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN=os.getenv('NOTION_TOKEN')

headers={
    'Authorization':f'Bearer {NOTION_TOKEN}',
    'Notion-Version':'2022-06-28',
    'Content-Type':'application/json'
}

mcp=FastMCP(
    "Notion Notes Server"
)

@mcp.tool
async def search_notes(query:str)->dict:
    """Search notes in the connected notion workspace"""

    async with httpx.AsyncClient() as client:
        response=await client.post(
            "https://api.notion.com/v1/search",
            headers=headers,
            json={'query':query}
        )

    response.raise_for_status()

    return response.json()


@mcp.tool
async def create_notes(title:str,content:str)->dict:
    """Create a new note inside the connected Notion Page"""

    url="https://api.notion.com/v1/pages"


    payload = {
        "parent": {
            "type": "page_id",
            "page_id": os.getenv("NOTION_PARENT_ID")
        },
        "properties": {
            "title": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response=await client.post(
            url,
            headers=headers,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        return {
            "message":"Note created Successfully",
            "page_id":data['id'],
            "url":data['url']
        }

    


    









if __name__=='__main__':
    mcp.run(transport='streamable-http')


