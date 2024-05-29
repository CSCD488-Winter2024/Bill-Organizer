import asyncio
import sys
import datetime
import xml.etree.ElementTree as ET
from asyncio import sleep
from typing import Coroutine

import requests

import cfg
import handler
from cfg import Cursor

name = 'wa_leg'

base_url = 'http://WSLWebServices.leg.wa.gov/'
namespace = f'{{{base_url}}}'

def res(node: ET.Element, key: str) -> str or None:
    """
    Returns the text value of a child node. Automatically prepends the namespace.
    :param node: The node to search for key in.
    :param key: The key to search for in node.
    :return: A string containing the text of the child node. None if key is not found or node is None.
    """
    if node is None: return None
    result = node.find(f'{namespace}{key}')
    return result.text if result is not None else None


async def get_node(endpoint: str, params: dict) -> ET.Element:
    """
    Makes an HTTP GET request and parses the response as xml. Handles rate limiting.
    :param endpoint: The URL endpoint to query. do not add a leading slash.
    :param params: A dictionary of query parameters.
    :return: An XML node containing the xml tree of the returned document.
    """
    # Default wait time in seconds if rate-limited and no retry_after
    wait_time = 5
    while True:
        page = requests.get(f'{base_url}{endpoint}', params=params, headers={'User-Agent': cfg.program_name})
        # If we are being rate limited:
        if page.status_code == 429:
            # If the api provided a retry_after, use that
            if 'Retry-After' in page.headers:
                wait_time = int(page.headers['Retry-After'])
            print(f'encountered a rate limit, waiting {wait_time} seconds')
            await sleep(wait_time)
            # If no Retry-After and we are still rate limited, double wait time until success
            wait_time *= 2
            continue
        # Error out if we hit a http error (other than 429)
        page.raise_for_status()
        return ET.fromstring(page.text)


async def get_sponsors(biennium: str) -> None:
    """
    Updates the sponsors table with new and updated sponsor data.
    :param biennium: The biennium to update.
    :return None: None
    """
    cfg.hlog(f'getting sponsors for biennium {biennium}', name)

    root = get_node('SponsorService.asmx/GetSponsors', {'biennium': biennium})

    sponsors: list[tuple] = []

    for sponsor in await root:
        sponsors.append((
            biennium,
            res(sponsor, 'Id'),
            res(sponsor, 'LongName'),
            res(sponsor, 'Agency'),
            res(sponsor, 'Acronym'),
            res(sponsor, 'Party'),
            res(sponsor, 'District'),
            res(sponsor, 'Phone'),
            res(sponsor, 'Email'),
            res(sponsor, 'FirstName'),
            res(sponsor, 'LastName')
        ))

    cfg.hlog(f'Gathered {str(len(sponsors))} sponsors for biennium {biennium}', name)

    with Cursor() as cur:
        cur.executemany(r"""
        insert ignore into sponsors
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, default)
            on duplicate key update 
                biennium     = value(biennium),
                id           = value(id),
                long_name    = value(long_name),
                agency       = value(agency),
                acronym      = value(acronym),
                party        = value(party),
                district     = value(district),
                phone        = value(phone),
                email        = value(email),
                first_name   = value(first_name),
                last_name    = value(last_name),
                last_updated = default
        """, sponsors)

    cfg.hlog(f'Finished writing sponsors for biennium {biennium}', name)


async def get_bills(date: str) -> None:
    """
    Fetches all bills created after a date and inserts them into the database. Also updates all sponsors for the
    years that the bills were created.
    :param date: The date to start the import from.
    :return None: None
    """

    cfg.hlog(f'getting all bills since {date}', name)

    root = get_node('LegislationService.asmx/GetLegislationIntroducedSince', {'sinceDate': date})

    bills: list[tuple] = []
    bienniums: dict[str, Coroutine] = {}

    for bill in await root:
        biennium = res(bill, 'Biennium')
        companion = bill.find(f'{namespace}Companions').find(f'{namespace}Companion')

        # If we haven't yet started gathering sponsors for a given biennium, do so.
        if biennium not in bienniums:
            bienniums[biennium] = get_sponsors(biennium)

        bills.append((
            biennium,
            res(bill, 'BillId'),
            res(bill, 'BillNumber'),
            res(bill, 'SubstituteVersion'),
            res(bill, 'EngrossedVersion'),
            res(bill, 'OriginalAgency'),
            res(bill, 'Active'),
            str(tuple(i for i in ['State', 'Local'] if res(bill, f'{i}FiscalNote') == 'true')),
            res(bill, 'Appropriations'),
            str(tuple(i for i in ['Governor', 'BudgetCommittee', 'Department', 'Other'] if res(bill, f'RequestedBy{i}') == 'true')),
            res(bill, 'ShortDescription'),
            res(bill, 'Request'),
            res(bill, 'IntroducedDate').replace('T', ' '),
            res(bill, 'PrimeSponsorID'),
            res(bill, 'LongDescription'),
            res(bill, 'LegalTitle'),
            res(companion, 'BillId') if companion is not None else None,
        ))

    # Wait for any sponsor gatherings to finish up before we process the actual bills
    for i in bienniums.values():
        await i

    cfg.hlog(f'Gathered {str(len(bills))} bills', name)

    with Cursor() as cur:
        cur.executemany(r"""
            insert ignore into bills 
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, default)
                on duplicate key update
                    bill_number        = value(bill_number),
                    substitute_version = value(substitute_version),
                    engrossed_version  = value(engrossed_version),
                    original_agency    = value(original_agency),
                    active             = value(active),
                    fiscal_notes       = value(fiscal_notes),
                    appropriations     = value(appropriations),
                    requested_by       = value(requested_by),
                    short_description  = value(short_description),
                    request            = value(request),
                    introduced_date    = value(introduced_date),
                    sponsor_id         = value(sponsor_id),
                    long_description   = value(long_description),
                    legal_title        = value(legal_title),
                    companion_bill     = value(companion_bill),
                    last_updated       = default        
        """, bills)

    cfg.hlog('Completed writing bills to database', name)


class wa_leg:
    def run_at(self) -> datetime.datetime:
        dat = cfg.read_handler_data(name)
        if dat is None:
            dat = {}
        if 'last_check' not in dat:
            dat['last_check'] = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=365)
            cfg.write_handler_data(name, dat)

        return datetime.datetime.fromisoformat(str(dat['last_check'])) + datetime.timedelta(days=7)


    async def run(self) -> None:
        dat = cfg.read_handler_data(name)

        since = datetime.datetime.fromisoformat(str(dat['last_check']))


        await get_bills(f'{since.month}/{since.day}/{since.year}')
        dat['last_check'] = datetime.datetime.now(datetime.timezone.utc)
        cfg.write_handler_data(name, dat)


handler.handlers[wa_leg()] = None

cfg.log(f'registered handler {name}')
