#coding:utf8
from xml.etree import ElementTree

from tools import logger

class XMLParser:
    def __init__(self, node_name, tag_name_list):
        self.root = None
        self.node_name = node_name
        self.tag_name_list = tag_name_list
        pass
    
    def _parse(self):
        if self.root:
            node_list = self.root.getiterator(self.node_name)
            return map(lambda x:self._parse_node(x), node_list)
        else:
            logger.critical("self.root is none")
            return None
    def parse(self,xml_file_path):
        self._fromfile(xml_file_path)
        return self._parse()
        
    def _parse_node(self, node):
        #print_node(node)
        return_dict = dict()
        for tag_name in self.tag_name_list:
            tmp = node.find(tag_name)
            if tmp is not None and tmp.text is not None:
                return_dict[tag_name] = tmp.text.strip()
            else:
                return_dict[tag_name] = None
        return return_dict

    def _fromstring(self, xml_str):
        self.root = ElementTree.fromstring(xml_str)
        pass
    
    def _fromfile(self, file_path):
        self.root = ElementTree.parse(file_path)
        pass


if __name__ == "__main__":
    xmlparser = XMLParser("item",["title","link","pubDate","description"])
    tmp = xmlparser.parse("guide.xml")
    for item in tmp:
        print item["title"]
