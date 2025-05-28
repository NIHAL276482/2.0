from flask import Flask, request, Response
import aiohttp
import asyncio

app = Flask(__name__)

async def fetch_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                content = await response.read()
                return content, response.status
    except aiohttp.ClientError as e:
        return f'{{"error": "Error fetching URL: {str(e)}"}}', 400

@app.route('/')
def proxy_url():
    # Get the URL parameter from the query string
    provided_url = request.args.get('url')
    
    if not provided_url:
        return Response('{"error": "No URL provided"}', status=400, content_type='application/json')
    
    # Construct the target URL
    target_url = f"https://yt.hosters.club/?url={provided_url}"
    
    # Run async aiohttp request in Flask's synchronous context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        content, status = loop.run_until_complete(fetch_url(target_url))
        return Response(
            content,
            status=status,
            content_type='application/json'
        )
    finally:
        loop.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
