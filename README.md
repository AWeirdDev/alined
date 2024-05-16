# alined

LINE Bot SDK for Python, but enhanced and strongly-typed.

```python
from alined import Client

# Make sure to add LINE_CHANNEL_SECRET and-
# LINE_CHANNEL_ACCESS_TOKEN to the env
client = Client()

# Typed decorator of @client.event()
@client.text_message
async def on_message(ctx):
    await ctx.send("No thanks. Maybe hello world?")
```

Start the app:

```haskell
$ uvicorn main:client.app --host=0.0.0.0 --port=8080
```

...or in code:

```python
client.run(host="0.0.0.0", port=8080)
```
