import os
from importlib import import_module

import cfg
import handler
import asyncio
from datetime import datetime, timezone

for i in os.listdir('handlers'):
    if i.endswith('.py'):
        import_module('handlers.' + i[:-3])

recheck_timer = 10


async def cycle():
    cfg.log('main loop started')
    while True:
        for k, v in handler.handlers.items():
            cfg.log(f'processing handler {k}')
            if v is not None and not v.done():
                cfg.log('handler\'s last iteration still running, skipping')
                continue

            now = datetime.now(timezone.utc)
            target = k.run_at()
            cfg.log(f'handler wants to run at or after {str(target)} and it is {str(now)}...')
            if now >= target:
                cfg.log(f'starting handler')
                handler.handlers[k] = asyncio.create_task(k.run())
            else:
                cfg.log('skipping handler')


        await asyncio.sleep(recheck_timer)

asyncio.run(cycle())