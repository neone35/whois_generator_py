import string
import itertools
import file_tools


def generate(top_level_domain, length=3, chosen_ascii_chars=None):
    if chosen_ascii_chars is None:
        chosen_ascii_chars = ['lowercase']
    chars = ''
    if any('lowercase' in sublist for sublist in chosen_ascii_chars):
        chars = string.ascii_lowercase  # "abcdefghijklmnopqrstuvwxyz"
    elif any('uppercase' in sublist for sublist in chosen_ascii_chars):
        chars += string.ascii_uppercase
    elif any('digits' in sublist for sublist in chosen_ascii_chars):
        chars += string.digits

    generated_domain_list = [''.join(i) for i in itertools.product(chars, repeat=int(length))]
    full_domains = []
    for domain in generated_domain_list:
        full_domain = 'www.' + domain + top_level_domain
        full_domains.append(full_domain)

    # Write to file
    filename = 'generated_domain_list.txt'
    file_tools.write_to_txt(full_domains, filename)

    # Give some stats after work finishes
    print('\nGenerated', len(full_domains), 'domains')
    print('Results written to', filename)
