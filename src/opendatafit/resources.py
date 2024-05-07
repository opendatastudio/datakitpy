"""Object definitions for loading and using data from Frictionless Resources"""


from copy import deepcopy
import pandas as pd


class TabularDataResource:
    data: pd.DataFrame  # Resource data as pandas DataFrame
    _resource: dict  # Resource metadata in Frictionless JSON format

    def __init__(self, resource: dict) -> None:
        """Load tabular data resource from JSON dict"""

        # Load data into pandas DataFrame
        data = resource.pop("data")
        self.data = pd.DataFrame.from_dict(data)

        # Reorder columns by schema field order
        cols = [field["name"] for field in resource["schema"]["fields"]]
        self.data = self.data[cols]

        # Set index to primary key column
        self.data.set_index(resource["schema"]["primaryKey"], inplace=True)

        self._resource = resource

    def __bool__(self):
        """False if data table is empty, True if not"""
        return not self.data.empty

    def to_dict(self):
        resource_dict = deepcopy(self._resource)

        # Convert data from DataFrame to JSON record row format
        # Workaround for index=True not working with "records" orient
        data_copy = self.data.copy(deep=True)
        data_copy.reset_index()
        data = data_copy.to_dict(orient="records", index=True)
        for row, index_row in zip(data, self.data.index):
            print(row, index_row)

        resource_dict["data"] = data
        return resource_dict
