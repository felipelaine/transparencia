from flask import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.attributes import QueryableAttribute


class Serializable(object):
    __exclude__ = ('id',)
    __include__ = ()
    __write_only__ = ()

    @classmethod
    def from_json(cls, json, selfObj=None):
        if selfObj is None:
            self = cls()
        else:
            self = selfObj
        exclude = (cls.__exclude__ or ()) + Serializable.__exclude__
        include = cls.__include__ or ()
        if json:
            for prop, value in json.iteritems():
                # ignore all non user data, e.g. only
                if (not (prop in exclude) | (prop in include)) and isinstance(
                        getattr(cls, prop, None), QueryableAttribute):
                    setattr(self, prop, value)
        return self

    def deserialize(self, json):
        if not json:
            return None
        return self.__class__.from_json(json, selfObj=self)

    @classmethod
    def serialize_list(cls, object_list=[]):
        output = []
        for li in object_list:
            if isinstance(li, Serializable):
                output.append(li.serialize())
            else:
                output.append(li)
        return output

    def serialize(self, **kwargs):

        # init write only props
        if len(getattr(self.__class__, '__write_only__', ())) == 0:
            self.__class__.__write_only__ = ()
        dictionary = {}
        expand = kwargs.get('expand', ()) or ()
        prop = 'props'
        if expand:
            # expand all the fields
            for key in expand:
                getattr(self, key)
        iterable = self.__dict__.items()
        is_custom_property_set = False
        # include only properties passed as parameter
        if (prop in kwargs) and (kwargs.get(prop, None) is not None):
            is_custom_property_set = True
            iterable = kwargs.get(prop, None)
        # loop trough all accessible properties
        for key in iterable:
            accessor = key
            if isinstance(key, tuple):
                accessor = key[0]
            if not (accessor in self.__class__.__write_only__) and not accessor.startswith('_'):
                # force select from db to be able get relationships
                if is_custom_property_set:
                    getattr(self, accessor, None)
                if isinstance(self.__dict__.get(accessor), list):
                    dictionary[accessor] = self.__class__.serialize_list(object_list=self.__dict__.get(accessor))
                # check if those properties are read only
                elif isinstance(self.__dict__.get(accessor), Serializable):
                    dictionary[accessor] = self.__dict__.get(accessor).serialize()
                else:
                    dictionary[accessor] = self.__dict__.get(accessor)
        return dictionary

class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            data = {}
            fields = o.__json__() if hasattr(o, '__json__') else dir(o)
            for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
                value = o.__getattribute__(field)
                try:
                    json.dumps(value)
                    data[field] = value
                except TypeError:
                    data[field] = None
                return data

        return json.JSONEncoder.default(self, o)