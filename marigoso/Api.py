def get_request(self, route):
    response = self.session.get("".join([self.host, route]))
    if response.status_code is not self.codes.ok:
        print("[Error] Unexpected status code: {}".format(response.status_code))
        return False
    else:
        return response.json()


def check_fields(self, fields, dictionary):
    failed = None
    for field in fields:
        if field not in dictionary:
            print("[Failed] {} field is missing.".format(field))
            failed = True
    if failed:
        self.pp.pprint(dictionary)