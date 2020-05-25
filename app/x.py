from starlette.responses import StreamingResponse
import asyncio


async def slow_numbers(minimum, maximum):
    count = 1
    yield('<html><body><ul>')
    for number in range(minimum, maximum + 1):
        yield '<li><progress value="%d" max="20"></progress></li>' % count
        await asyncio.sleep(0.1)
        count += 1

    yield('</ul></body></html>')

async def app(scope, receive, send):
    assert scope['type'] == 'http'
    generator = slow_numbers(1, 20)
    response = StreamingResponse(generator, media_type='text/html')
    await response(scope, receive, send)

    # <progress value="70" max="100">70 %</progress>
    # <div class="progress-bar" role="progressbar" aria-valuenow="70"
    # aria-valuemin="0" aria-valuemax="100" style="width:10%">
    #   70%
    # </div>

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info", debug=True)

