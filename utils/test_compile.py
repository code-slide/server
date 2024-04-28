import pytest
from compile import json_to_html, validate_color, validate_config, validate_frame, validate_size, validate_title

def test_validate_title():
    """
    Test validate_title function
    """
    # Passed
    assert validate_title("Hello, World!") == "Hello, World!"

    # Failed
    with pytest.raises(ValueError):
        validate_title(0)

def test_validate_color():
    """
    Test validate_color function
    """
    # Passed
    assert validate_color("#ffffff") == "#ffffff"

    # Failed, not a string
    with pytest.raises(ValueError):
        validate_color(0)

    # Failed, not starting with #
    with pytest.raises(ValueError):
        validate_color("ffffff")

def test_validate_size():
    """
    Test validate_size function
    """
    # Passed
    assert validate_size([100, "200"]) == [100, 200]

    # Failed, not a list
    with pytest.raises(ValueError):
        validate_size(0)

    # Failed, not enough elements
    with pytest.raises(ValueError):
        validate_size(["100"])

def test_validate_frame():
    """
    Test validate_frame function
    """
    # Passed
    assert validate_frame([['Shape1', 'Shape2'], ['Shape1']]) == [['Shape1', 'Shape2'], ['Shape1']]

    # Failed, not a list
    with pytest.raises(ValueError):
        validate_frame(0)

    # Failed, not a list of list
    with pytest.raises(ValueError):
        validate_frame(['Shape1', 'Shape2'])

    # Failed, content not a string
    with pytest.raises(ValueError):
        validate_frame([[['Shape1'], 'Shape2']])

def test_validate_config():
    """
    Test validate_config function
    """
    # Passed
    assert validate_config('{"transition": "none", "controls": false}') == '{"transition": "none", "controls": false}'

    # Failed, not a JSON
    with pytest.raises(ValueError):
        validate_config("Hello, World!")

def test_json_to_html():
    """
    Test json_to_html function
    """
    placeholder = f"<!doctype html>\n \
    <html lang=\"en\">\n \
	<head>\n \
		<meta charset=\"utf-8\">\n \
		<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">\n \
		<title>%s - Presentation</title>\n \
        <!-- Favicon -->\n \
        <link rel='apple-touch-icon' sizes='180x180' href='dist/favicon/apple-touch-icon.png'>\n \
        <link rel='icon' type='image/png' sizes='32x32' href='dist/favicon/favicon-32x32.png'>\n \
        <link rel='icon' type='image/png' sizes='16x16' href='dist/favicon/favicon-16x16.png'>\n \
        <link rel='manifest' href='dist/favicon/site.webmanifest'>\n \
        <!-- Reveal.js theme -->\n \
		<link rel=\"stylesheet\" href=\"dist/reset.css\">\n \
		<link rel=\"stylesheet\" href=\"dist/reveal.css\">\n \
		<link rel=\"stylesheet\" href=\"dist/theme/black.css\">\n \
		<link rel=\"stylesheet\" href=\"plugin/highlight/monokai.css\">\n \
	</head>\n \
	<body>\n \
		<div class=\"reveal\">\n \
			<div class=\"slides\">\n \
                <section data-transition=\"fade\">\n \
                    <div class=\"editor\" style=\"background: %s\">\n \
					    <svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 %s %s\">\n \
%s\
</svg>\n \
                    </div>\n \
                </section>\n \
            </div>\n \
		</div>\n \
		<script src=\"dist/reveal.js\"></script>\n \
		<script> Reveal.initialize(%s); </script>\n \
	</body>\n \
    </html>"

    # Passed, empty frame
    data = {
        'title': 'Hello, World!',
        'backgroundColor': '#ffffff',
        'size': [100, 200],
        'frame': [[]],
        'config': '{"transition": "none", "controls": false}',
    }
    frames = ''

    assert json_to_html(data) == placeholder % (data['title'], data['backgroundColor'], data['size'][0], data['size'][1], frames, data['config'])

    # Passed, with one frame
    data = {
        'title': 'Hello, World!',
        'backgroundColor': '#ffffff',
        'size': [100, 200],
        'frame': [['<svg><g id="Shape1"></g></svg>']],
        'config': '{"transition": "none", "controls": false}',
    }
    frames = "<g class=\"fragment\"> %s </g>\n " % data['frame'][0][0]

    assert json_to_html(data) == placeholder % (data['title'], data['backgroundColor'], data['size'][0], data['size'][1], frames, data['config'])

    # Passed, with demo data
    data = {
        'title': 'Hello, World!',
        'backgroundColor': '#ffffff',
        'size': [100, 200],
        'frame': [['<svg><g id="Shape1"></g></svg>', '<svg><g id="Shape2"></g></svg>'], ['<svg><g id="Shape1"></g></svg>'], ['<svg><g id="Shape3"></g></svg>']],
        'config': '{"transition": "none", "controls": false}',
    }
    frames = "<g class=\"fragment fade-out\" data-fragment-index=\"%s\"> %s </g>\n \
<g class=\"fragment fade-out\" data-fragment-index=\"%s\"> %s </g>\n \
<g class=\"fragment fade-in-then-out\" data-fragment-index=\"%s\"> %s </g>\n \
<g class=\"fragment\" data-fragment-index=\"%s\"> %s </g>\n " % (1, data['frame'][0][0], 1, data['frame'][0][1], 1, data['frame'][1][0], 2, data['frame'][2][0])

    assert json_to_html(data) == placeholder % (data['title'], data['backgroundColor'], data['size'][0], data['size'][1], frames , data['config'])