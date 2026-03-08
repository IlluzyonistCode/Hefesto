from ui.colors import paint
from utils.network import GetUtilities
from utils.log_manager import LogManager


def resolver_command(domain, *args):
    
    
    log_file = LogManager.create_log_file('resolver')
    
    log_data = f'Domain: {domain}\n'
    cloudflare_domains = []

    try:
        domains, ips = GetUtilities.get_subdomains_virustotal(domain)

        if domains is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "resolver", "subdomainsNotFound"])}')
            return

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "resolver", "domain"])}\n')
        unknowns_ip, cloudflare_ips = GetUtilities.get_separate_ips(ips)
        sorted_domains = sorted(domains, key=lambda x: x[1])

        for i in sorted_domains:
            is_cloudflare_domain = False

            for cf_ip in GetUtilities.cloudflare_ips:
                if i[1].startswith(cf_ip):
                    is_cloudflare_domain = True
                    break

            if not is_cloudflare_domain:
                paint(f'{GetUtilities.get_spaces()}  &a&l• &f&l{i[0]} (&7&l{i[1]}&f&l)')
                log_data += f'{i[0]} ({i[1]})\n'

        if len(cloudflare_domains) >= 1:
            for i in cloudflare_domains:
                paint(f'{GetUtilities.get_spaces()}  &a&l• &f&l{i[0]} (&d&lCloudFlare&f&l) (&d&l{i[1]}&f&l)')
                log_data += f'{i[0]} (CloudFlare) ({i[1]})\n'

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "resolver", "ip"])}\n')

        if len(unknowns_ip) >= 1:
            for ip in unknowns_ip:
                paint(f'{GetUtilities.get_spaces()}  &a&l• &f&l{ip}')
                log_data += f'{ip}\n'

        if len(cloudflare_ips) >= 1:
            for ip in cloudflare_ips:
                paint(f'{GetUtilities.get_spaces()}  &a&l• &d&l{ip} &f&l(&d&lCloudFlare&f&l)')
                log_data += f'{ip} (CloudFlare)\n'

        log_data += '\n'
        LogManager.write_log(log_file, 'resolver', log_data)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

