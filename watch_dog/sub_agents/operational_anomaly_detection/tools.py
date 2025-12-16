# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for the operational anomaly detection agent."""

from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig


# TODO: Replace with your project and dataset details.


# This single toolset can be used by the agent to access
# any table within the specified project and dataset.
bgConf = BigQueryToolConfig()
bgConf.compute_project_id = "ccibt-hack25ww7-730"

BIGQUERY_TOOLSET = BigQueryToolset(bigquery_tool_config=bgConf)

# See the License for the specific language governing permissions and
# limitations under the License.
