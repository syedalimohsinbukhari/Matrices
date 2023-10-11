"""Created on Oct 05 23:51:07 2023"""

import pretty_errors


def config():
    pretty_errors.configure(
            separator_character='*',
            filename_display=pretty_errors.FILENAME_COMPACT,
            display_trace_locals=True,
            line_number_first=True,
            display_link=True,
            lines_before=5,
            lines_after=2,
            line_color=pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
            code_color='  ' + pretty_errors.default_config.line_color,
            truncate_code=True,
            display_locals=True
            )
