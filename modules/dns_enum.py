import dns.resolver as res


def get_dns_records(domain):

    resolver = res.Resolver()

    resolver.nameservers = [
        "8.8.8.8",
        "1.1.1.1"
    ]

    resolver.timeout = 3
    resolver.lifetime = 5


    records = {}

    for record_type in ['A','AAAA','MX','NS','TXT','CNAME']:

        try:

            answers = resolver.resolve(
                domain,
                record_type
            )

            records[record_type] = [

                r.to_text()

                for r in answers

            ]

        except Exception as e:

            print(f"{record_type} : {e}")

            records[record_type]=[]


    return records