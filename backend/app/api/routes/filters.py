from typing import List

from llama_index.core.vector_stores.types import (
    FilterCondition,
    FilterOperator,
    MetadataFilter,
    MetadataFilters,
)

from app.engine import UPLOADED_DATA_DIR, setting


def generate_filters(doc_files: List[str] | None = None, doc_ids: List[str] | None = None):
    public_doc_filter = MetadataFilter(
        key="private",
        value="true",
        operator=FilterOperator.NE,
    )

    or_filters = []
    if doc_files and len(doc_files) > 0:
        file_filter = MetadataFilter(
            key="file_name",
            value=doc_files,
            operator=FilterOperator.IN,
        )
        or_filters.append(file_filter)
    if doc_ids and len(doc_ids) > 0:
        doc_id_filter = MetadataFilter(
            key="doc_id",
            value=doc_ids,
            operator=FilterOperator.IN,
        )
        or_filters.append(doc_id_filter)

    if len(or_filters) == 0:
        filters = MetadataFilters(filters=[public_doc_filter])
    else:
        filters = MetadataFilters(
            filters=[*or_filters, public_doc_filter],
            condition=FilterCondition.OR,
        )

    return (
        setting.get_data_dir() if len(or_filters) == 0 else UPLOADED_DATA_DIR
    ), filters
