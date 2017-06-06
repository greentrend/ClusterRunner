from genty import genty, genty_dataset
import os

from app.common.console_output_segment import ConsoleOutputSegment
from app.common.cluster_service import ClusterService
from app.util.exceptions import BadRequestError, ItemNotFoundError
from test.framework.base_unit_test_case import BaseUnitTestCase


@genty
class TestClusterService(BaseUnitTestCase):
    def test_get_console_output_happy_path_returns_return_values(self):
        segment = ConsoleOutputSegment(offset_line=0, num_lines=1, total_num_lines=2, content='The content\n')
        self.patch('app.common.cluster_service.BuildArtifact').get_console_output.return_value = segment
        service = ClusterService()

        response = service.get_console_output(1, 2, 3, os.path.abspath('~'))

        self.assertDictEqual(
            response,
            {
                'offset_line': 0,
                'num_lines': 1,
                'total_num_lines': 2,
                'content': 'The content\n',
            },
            'The response dictionary did not contain the expected contents.'
        )

    @genty_dataset(
        zero_max_lines=(0, None),
        negative_max_lines=(-1, None),
        negative_offset_line=(1, -1),
    )
    def test_get_console_output_raises_bad_request_error_with_invalid_arguments(self, max_lines, offset_line):
        service = ClusterService()

        with self.assertRaises(BadRequestError):
            service.get_console_output(1, 2, 3, os.path.abspath('~'), max_lines=max_lines, offset_line=offset_line)

    def test_get_console_output_raises_item_not_found_error_if_console_output_file_doesnt_exist(self):
        self.patch('app.common.cluster_service.BuildArtifact').get_console_output.return_value = None
        service = ClusterService()

        with self.assertRaises(ItemNotFoundError):
            service.get_console_output(1, 2, 3, os.path.abspath('~'))
