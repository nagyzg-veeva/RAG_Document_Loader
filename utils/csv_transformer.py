import pandas as pd
import json


class DataFrameTransformer:
    @staticmethod
    def transform(df: pd.DataFrame, content_columns=None, metadata_columns=None):
        # Handle optional parameters
        if content_columns is None:
            content_columns = []
        if metadata_columns is None:
            metadata_columns = []

        # If content_columns is empty, use all columns not in metadata_columns
        if not content_columns:
            content_columns = [col for col in df.columns if col not in metadata_columns]

        # Ensure no overlap
        content_columns = [col for col in content_columns if col not in metadata_columns]

        result = []
        for _, row in df.iterrows():
            # Concatenate content
            content_parts = [str(row[col]) for col in content_columns if col in df.columns]
            content = ' '.join(content_parts)

            # Metadata dict
            metadata = {col: row[col] for col in metadata_columns if col in df.columns}

            result.append({'content': content, 'metadata': metadata})

        return json.dumps(result)