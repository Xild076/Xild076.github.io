from enum import Enum

class Alignment(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    START = "start"
    END = "end"
    BETWEEN = "between"
    AROUND = "around"
    EVENLY = "evenly"

class Spacing(Enum):
    NONE = "none"
    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"
    AUTO = "auto"
    DEFAULT = "default"

class ButtonType(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"
    LINK = "link"
    OUTLINE_PRIMARY = "outline-primary"
    OUTLINE_SECONDARY = "outline-secondary"
    OUTLINE_SUCCESS = "outline-success"
    OUTLINE_DANGER = "outline-danger"
    OUTLINE_WARNING = "outline-warning"
    OUTLINE_INFO = "outline-info"
    OUTLINE_LIGHT = "outline-light"
    OUTLINE_DARK = "outline-dark"

class AnimationType(Enum):
    NONE = "none"
    FADE_IN = "fade-in"
    FADE_IN_UP = "fade-in-up"
    FADE_IN_DOWN = "fade-in-down"
    FADE_IN_LEFT = "fade-in-left"
    FADE_IN_RIGHT = "fade-in-right"
    SLIDE_UP = "slide-up"
    SLIDE_DOWN = "slide-down"
    SLIDE_LEFT = "slide-left"
    SLIDE_RIGHT = "slide-right"
    ZOOM_IN = "zoom-in"
    ZOOM_OUT = "zoom-out"
    PULSE = "pulse"

class ObjectFit(Enum):
    COVER = "cover"
    CONTAIN = "contain"
    FILL = "fill"
    SCALE_DOWN = "scale-down"
    NONE = "none"

class ColorTheme(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"

class InputType(Enum):
    TEXT = "text"
    EMAIL = "email"
    PASSWORD = "password"
    NUMBER = "number"
    DATE = "date"
    TEL = "tel"
    URL = "url"
    SEARCH = "search"
    FILE = "file"
    SUBMIT = "submit"
    RESET = "reset"
    BUTTON = "button"
    CHECKBOX = "checkbox"
    RADIO = "radio"

class FlexDirection(Enum):
    ROW = "row"
    ROW_REVERSE = "row-reverse"
    COLUMN = "column"
    COLUMN_REVERSE = "column-reverse"

class FlexWrap(Enum):
    NOWRAP = "nowrap"
    WRAP = "wrap"
    WRAP_REVERSE = "wrap-reverse"