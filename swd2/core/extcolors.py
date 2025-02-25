from swd2.core.exttypes import ExtEnum


class Color(ExtEnum):
    RESET = '\x1b[0m'
    RED = "\x1b[31m"
    RED_DARK = "\x1b[38;2;255;0;0m"
    RED_WITH_BG = "\x1b[38;2;254;76;76;48;2;153;0;0m"
    GREEN = "\x1b[32m"
    GREEN_DARK = "\x1b[38;2;50;153;0m"
    BLUE = "\x1b[34m"
    GRAY = "\x1b[38;2;177;177;177m"
    GRAY_LIGHT = "\x1b[38;2;227;227;227m"
    GRAY_DARK = "\x1b[38;2;127;127;127m"
    YELLOW = "\x1b[38;2;203;204;0m"
    ORANGE = "\x1b[38;2;255;127;0m"

    def __str__(self):
        return self.value

    def format(self, text: str, returnColor=None) -> str:
        return format(text.replace(str(Color.RESET), str(self)), self, returnColor)


def format(text: str, color: Color, returnColor: Color = Color.RESET) -> str:
    if returnColor is None:
        returnColor = Color.RESET

    records = []
    for line in text.splitlines():
        records.append(f'{color}{line}{returnColor}')

    return "\n".join(records)


if __name__ == '__main__':
    print('--------------------')
    print('print defined colors')
    print('--------------------')
    for key, val in Color.values():
        print(f'color {key} = {val.format("example")}')
