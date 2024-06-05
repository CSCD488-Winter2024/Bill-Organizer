import os
from importlib import import_module

import cfg
import handler
import asyncio
from datetime import datetime, timezone
from cfg import log

for i in os.listdir('handlers'):
    if i.endswith('.py'):
        import_module('handlers.' + i[:-3])


async def cycle():
    log.info('main loop started')
    while True:
        for k, v in handler.handlers.items():
            log.info(f'processing handler {k}')
            if v is not None and not v.done():
                log.info('handler\'s last iteration still running, skipping')
                continue

            now = datetime.now(timezone.utc)
            target = k.run_at()
            log.info(f'handler wants to run at or after {str(target)} and it is {str(now)}...')
            if now >= target:
                log.info(f'starting handler')
                handler.handlers[k] = asyncio.create_task(k.run())
            else:
                log.info('skipping handler')


        await asyncio.sleep(cfg.recheck_delay)

#asyncio.run(cycle())