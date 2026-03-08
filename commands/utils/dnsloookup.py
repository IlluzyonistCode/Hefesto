from ui.colors import paint
from utils.network import GetUtilities
from utils.log_manager import LogManager


def dnslookup(domain, *args):
    

    try:
        dns_records = [
            'A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT',
            'CAA', 'SPF', 'NAPTR'
        ]

        log_file = LogManager.create_log_file('dnslookup')
        log_data = f'Domain: {domain}\n'
        founds = False

        for dns_record in dns_records:
            output = GetUtilities.get_dns_records(domain, dns_record)

            if output is not None and len(output) >= 1:
                for i in output:
                    if not founds:
                        paint('')

                    paint(f'{GetUtilities.get_spaces()}&4[&c{dns_record}&4] &f&l{i}')
                    log_data += f'[{dns_record}] {i}\n'
                    founds = True

                log_data += '\n'
                LogManager.write_log(log_file, 'dnslookup', log_data)

        if not founds:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "dnslookup", "withoutResults"])}')

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

