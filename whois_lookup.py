import whois

domain = input("Enter a domain (e.g. google.com): ")

try:
    info = whois.whois(domain)
    print("\nWHOIS Information:")
    print("Domain Name:", info.domain_name)
    print("Registrar:", info.registrar)
    print("Creation Date:", info.creation_date)
    print("Expiration Date:", info.expiration_date)
    print("Name Servers:", info.name_servers)
    print("Emails:", info.emails)
except:
    print("Error: Domain not found or something went wrong.")
