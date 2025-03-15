from typing import List
from google.cloud.firestore import DocumentReference
from itertools import starmap


class BaseSerializer:

    def __init__(self, doc_ref: List[DocumentReference] | DocumentReference):
        self.doc_ref = doc_ref

    @property
    def data(self):
        fields = self.Meta.fields
        
        if isinstance(self.doc_ref, list):
            docs = self.doc_ref
            to_dict = lambda doc: {"id": doc.id, **doc.to_dict()}
            datas = list(map(to_dict, docs))

            def filter_list_data(data: dict):
                filter_field = lambda field, value: (field, value) if field in fields else None
                filter_data = list(filter(None, list(starmap(filter_field, data.items()))))
                return dict(filter_data)

            filter_datas = list(map(filter_list_data, datas))
            return filter_datas

        doc = self.doc_ref
        data = {"id": doc.id, **doc.to_dict()}

        filter_field = lambda field, value: (field, value) if field in fields else None
        filter_data = list(filter(None, list(starmap(filter_field, data.items()))))
        return dict(filter_data)