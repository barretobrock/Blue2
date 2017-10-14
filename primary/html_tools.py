"""
Tools used for makeing HTML files and the formatting and graphing within
"""


class FormatTools:
    def __init__(self):
        pass

    def number_to_text(self, text, output_type, decimals=0):
        """
        Converts a text or float to text-formatted number
        Args:
            text:
            output_type: What the number output should be
                'number' = no changes
                'percent' = decimal number should be converted to percent
            decimals:

        Returns:

        """
        if isinstance(text, str):
            num = float(text.replace(',', '.'))
        else:
            num = float(text)

        if output_type == 'number' and decimals == 0:
            result = '{:,}'.format(int(round(num, decimals))).replace(',', ' ')
        elif output_type == 'number' and decimals > 0:
            result = '{:,}'.format(round(num, decimals)).replace(',', ' ')
        elif output_type == 'to_percent':
            result = '{:,}'.format(float(round(num * 100, decimals)))
        else:
            result = ''
        return result

    def num_to_text(self, num, output_as, suffix='', decimals=0):
        """
        Converts number or number string to text-formatted string
        Args:
            num: value to convert
            output_as: what type of output
                'number': normal number
                'percent': number is converted to percent (n * 100)
                'difference': forces sign (+/-) in front of number

            suffix: any text to preceded the converted string
            decimals: decimal places to round

        Returns: Formatted text

        """
        if isinstance(num, str):
            num = float(num.replace(',', '.'))
        else:
            num = float(num)

        if output_as == 'number':
            if decimals == 0:
                result = '{:,}{}'.format(int(round(num, 0)), suffix).replace(',', ' ')
            else:
                result = '{:,}{}'.format(round(num, decimals), suffix).replace(',', ' ')
        elif output_as == 'percent':
            num *= 100
            if decimals == 0:
                result = '{:,}{}'.format(int(round(num, 0)), suffix).replace(',', ' ')
            else:
                result = '{:,}{}'.format(round(num, decimals), suffix).replace(',', ' ')
        elif output_as == 'difference':
            if decimals == 0:
                result = '{:+,}{}'.format(int(round(num, 0)), suffix).replace(',', ' ')
            else:
                result = '{:+,}{}'.format(round(num, decimals), suffix).replace(',', ' ')
        else:
            result = ''

        return result

    def text_to_number(self, num_str, digits=0):
        # handle if string is None or has characters in it
        if num_str.isalpha() or num_str is None:
            num = 0
        else:
            num = round(float(num_str.replace(',', '.')), digits)
        # do rounding if necessary
        if digits == 0:
            num = int(num)
        return num

