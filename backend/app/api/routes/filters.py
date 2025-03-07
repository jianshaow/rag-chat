from typing import List

from llama_index.core.vector_stores.types import (
    FilterCondition,
    FilterOperator,
    MetadataFilter,
    MetadataFilters,
)

from app.engine import UPLOADED_DATA_DIR, setting


def generate_filters(doc_ids: List[str]):
    public_doc_filter = MetadataFilter(
        key="private",
        value="true",
        operator=FilterOperator.NE,
    )
    selected_doc_filter = MetadataFilter(
        key="doc_id",
        value=doc_ids,
        operator=FilterOperator.IN,
    )
    if len(doc_ids) > 0:
        filters = MetadataFilters(
            filters=[
                public_doc_filter,
                selected_doc_filter,
            ],
            condition=FilterCondition.OR,
        )
    else:
        filters = MetadataFilters(
            filters=[
                public_doc_filter,
            ]
        )

    return (setting.get_data_dir() if len(doc_ids) == 0 else UPLOADED_DATA_DIR), filters
