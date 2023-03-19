""" Hal response structures
"""

from typing import Dict, Callable

class HalCollection:
    def to_dict(self) -> Dict:
        return {
            "_links": { "self": {"href": "foobar" }},
            "pageSize": 0
        }


class HalItemFactory:
    def __init__(self, self_link: Callable, to_dict: Callable):
        self.self_link = self_link
        self.to_dict = to_dict
        self.links = {}
        self.embeds = {}
        self.list_embeds = {}

    def with_link(self, name: str, link: Callable):
        self.links[name] = link

    def with_embedded(self, name: str, halEncoder: 'HalItemFactory', getter: Callable): 
        self.embeds[name] = (halEncoder, getter)

    def with_embedded_list(self, name: str, halEncoder: 'HalItemFactory', getter: Callable): 
        self.list_embeds[name] = (halEncoder, getter)

    def to_hal(self, data: Dict, with_embedded = []) -> Dict:
        root_link = self.self_link(data)
        ret_val = {
            "_links": { 
                "self": {"href": root_link },
                **{ 
                   name: {"href": link(root_link)} 
                   for name, link in self.links.items() 
                }
            },
            **self.to_dict(data)
        }

        if with_embedded:
            ret_val["_embedded"] = {}
            for name, (halEncoder, getter) in self.embeds.items():
                if name not in with_embedded:
                    continue
                ret_val["_embedded"][name] = halEncoder.to_hal(getter(data))

            for name, (halEncoder, getter) in self.list_embeds.items():
                if name not in with_embedded:
                    continue
                ret_val["_embedded"][name] = [ halEncoder.to_hal(embed) for embed in getter(data)]

        return ret_val

