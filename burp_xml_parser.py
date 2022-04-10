from os import stat
import xml.etree.ElementTree as ET
import argparse
import re
import base64

class BurpExportParser:
    def __init__(self, etree):
        self.etree = etree
    
    @staticmethod
    def from_file(f):
        return BurpExportParser(ET.parse(f))
    
    @staticmethod
    def from_xml(s):
        return BurpExportParser(ET.fromstring(s))

    def get_items(self):
        return self.etree.getroot()

    def get_item_url(self, item):
        return item.find("url").text

    def get_item_path(self, item):
        return item.find("path").text

    def get_item_request(self, item):
        return self.get_and_decode(item, "request")
    
    def get_item_request_body(self, item):
        resp = self.get_item_request(item)
        blank_line_regex = r"(?:\r?\n){2,}"
        return "\n".join(re.split(blank_line_regex, resp)[1:])

    def get_item_response(self, item):
        return self.get_and_decode(item, "response")

    def get_and_decode(self, item, elem_name):
        resp_elem = item.find(elem_name)
        resp_text = resp_elem.text
        if resp_text:
            if resp_elem.attrib['base64'] == "true":
                resp_text = base64.b64decode(resp_text).decode('utf-8','ignore')
        return resp_text
    
    def get_item_response_body(self, item):
        resp = self.get_item_response(item)
        if resp:
            blank_line_regex = r"(?:\r?\n){2,}"
            return "\n".join(re.split(blank_line_regex, resp)[1:])
        else:
            return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Filename to parse", required=True)
    args = parser.parse_args()

    bxp = BurpExportParser.from_file(args.file)

    for item in bxp.get_items():
        path = bxp.get_item_path(item)
        src = bxp.get_item_response(item)

        # ignore any parameters
        filename = path.split('/')[-1].split('?')[0]
        src_raw = bxp.get_item_response_body(item)

        # print("Source: %s" % src_raw[0:1000])
        print("Writing to file: %s script of length: %d" % (filename, len(src_raw)))

        if len(filename.strip()) > 0:
            with open(filename, "w", encoding="utf-8") as outfile:
                outfile.write(src_raw)
        
